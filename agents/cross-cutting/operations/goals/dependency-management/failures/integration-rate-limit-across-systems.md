# Integration Rate Limit Across Systems

## Issue
A single logical operation an agent performs fans out into calls against several independent downstream integrations, each with its own separately-published rate limit, and the agent's throughput planning accounts for at most one of them (usually the loudest or most recently hit limit) rather than the effective ceiling set by whichever integration is most constrained. Because none of the integrated systems know about each other's limits, and the agent's own rate-limiting logic is typically tuned per-integration rather than per-workflow, a request pattern that looks safe against every individual system's published limit can still produce compounding overload: a retry triggered by one system's 429 fans back out and re-hits every other system in the same operation, multiplying load precisely on the systems that weren't the original bottleneck.

**Frequency**: Common

**Symptoms**
- One integration in a multi-system workflow starts returning 429s even though its own traffic volume, viewed in isolation, is well under its published limit — because retries triggered by a different integration's rate limit are re-driving calls to it
- The agent's per-tool rate limiter correctly paces calls to each individual API but the workflow as a whole still overwhelms a shared downstream resource that multiple of those APIs happen to sit in front of
- Rate-limit incidents cluster around a specific business operation (e.g. "checkout," "onboarding") rather than around a specific API, because the operation's fan-out pattern — not any single integration — is the actual trigger
- Backoff/retry logic on one integration is unaware that its retries are also re-triggering already-successful calls to other integrations in the same logical transaction, wasting quota on work that didn't need to be repeated
- Effective safe throughput for the overall workflow is lower than any individual integration's advertised limit would suggest, and this ceiling isn't documented anywhere because no one integration owns the aggregate view

## Root Cause
Rate limits are published and enforced per-integration, by design, because each provider only has visibility into its own traffic — but an agent's workflow-level throughput is bounded by the minimum of every rate limit in its call graph, combined with how failures in one leg of that graph trigger retries across the others. When an orchestrator's retry and backoff logic is implemented independently per tool/integration (the common pattern, since each integration's client library ships its own retry policy), a rate-limit response from Integration A causes a retry of the entire logical operation, which re-issues calls to Integrations B and C as a side effect — even though B and C succeeded the first time and didn't need to be repeated. No component in the system has visibility into the aggregate call graph, so nothing throttles the overall operation rate to the true bottleneck; each integration only ever sees and reacts to its own slice of the problem.

## Example
```
A trip-booking agent processes a single "book itinerary" operation that
internally calls three separate providers per request: a flight-search
API, a hotel-availability API, and a payment-authorization API, in that
order, all within one orchestrated workflow.

Each provider individually allows generous throughput: flights at 100
req/min, hotels at 200 req/min, payments at 50 req/min. The agent's
per-tool rate limiter correctly paces calls to each one within these
limits when considered independently.

Under a moderate traffic burst, the payment-authorization API - the
most constrained leg - starts returning 429s. The orchestrator's retry
logic, written generically to "retry the booking operation on
failure," re-runs the entire itinerary-booking sequence from the top:
flight-search and hotel-availability are called again, even though
both had already succeeded on the first pass and their results were
simply waiting on payment to complete.

This doubles (and, under sustained payment throttling, keeps
multiplying) the effective load on the flight and hotel APIs - both of
which now also start rate-limiting, despite neither ever approaching
its own published ceiling from genuinely new bookings. What looked like
independent headroom on three APIs collapses into a correlated,
system-wide throttling incident triggered entirely by the most
constrained one.
```

## Statistics
| Finding | Context |
|---|---|
| Multi-integration workflows commonly hit an effective throughput ceiling well below the least-restrictive individual API's published limit, set instead by the most-constrained leg combined with retry fan-out | Typical range observed in workflows with per-integration rather than per-workflow rate limiting |
| A meaningful share of "unexplained" rate-limit incidents on a well-provisioned integration trace back to retries originating from a different, unrelated integration in the same logical operation | Estimated from postmortems of cross-system throttling incidents |
| Retrying only the failed leg of a multi-step operation (rather than the whole operation) measurably reduces aggregate call volume during rate-limit incidents compared to whole-operation retries | Reported range across teams comparing step-level vs. operation-level retry granularity |

## Mitigations
1. **Retry only the failed leg, not the whole operation**: Structure multi-integration workflows so that a rate-limit response from one integration triggers a retry of just that step, reusing already-successful results from prior steps, instead of re-running the entire logical operation and re-hitting integrations that already succeeded.
2. **Model the workflow's effective rate ceiling as the minimum across its call graph**: Compute and enforce a workflow-level throughput cap based on the most constrained integration in the chain, rather than pacing each integration independently against only its own published limit.
3. **Centralize retry/backoff coordination across integrations in one workflow**: Route backoff decisions for a multi-step operation through a shared coordinator that is aware of all the integrations involved, so a 429 from one system informs pacing decisions for calls to the others in the same operation rather than each integration's client library reacting in isolation.
4. **Honor Retry-After semantics at the workflow level**: When any integration in the chain returns a Retry-After hint, propagate that delay to the whole operation's retry scheduling, not just to the specific call that received it.
5. **Load-test the full call graph, not each integration individually**: Include multi-integration, whole-workflow load testing in capacity planning, since per-integration load tests each passing in isolation doesn't validate the combined, correlated load pattern the real workflow produces.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| cross_integration_retry_amplification_factor | Ratio of total downstream calls issued to calls that were strictly necessary, per logical operation | Alert if ratio rises materially above 1.0 during a rate-limit incident |
| workflow_effective_throughput_ceiling | Observed maximum safe throughput for a full multi-integration operation, tracked over time | Alert if it drops below the previously established baseline |
| single_integration_429_rate_correlated_with_other_integration_load | 429 rate on Integration X correlated against retry volume originating from Integration Y's failures | Alert on statistically significant correlation |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Whole-operation retry storm detected | cross_integration_retry_amplification_factor exceeds threshold during a rate-limit incident | High | Switch to step-level retry immediately, investigate which integration is the true bottleneck |
| Unexplained 429s on a low-traffic integration | An integration well under its own published limit starts returning 429s | Medium | Check for retry fan-out originating from a different integration in the same workflow |

## Related Patterns
- [Per-Tool Burst Rate Exceeded](../../tool-rate-quota-limits/failures/per-tool-burst-rate-exceeded.md) - covers a single integration's own burst limit being exceeded by fan-out within that one tool; this pattern is the cross-system composition of several integrations' limits interacting, not any one limit alone
- [Agent Resource Contention](../../multi-agent-orchestration/failures/agent-resource-contention.md) - resource contention is multiple agents competing for one shared resource; this pattern is one workflow's calls compounding across multiple distinct downstream resources
- [Retry Storms](../../cost-efficiency/failures/retry-storms.md) - the general retry-amplification cost pattern; this pattern is the specific cross-integration variant where the amplification crosses system boundaries that don't share visibility into each other's limits
- [Integration Timeout Mismatch](./integration-timeout-mismatch.md) - both describe a multi-system workflow's timing/pacing assumptions breaking down in ways no single integration's own configuration would reveal
