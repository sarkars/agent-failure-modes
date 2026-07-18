# Per-Tool Burst Pricing Penalty

## Issue
A tool vendor prices calls at a low baseline rate up to a sustained throughput threshold (e.g. 10 requests/second) but charges a significant premium — sometimes 5-10x — for requests above that threshold within a billing window. An agent's retry-with-backoff logic, built purely to handle rate-limit errors or transient failures, resubmits requests in tight clusters after a failure or during a burst of user activity, pushing throughput over the baseline and triggering premium billing that the agent's cost model never anticipated because it only models the advertised baseline rate.

**Frequency**: Occasional

**Symptoms**
- Cost per call spikes during periods of high request concentration even though the per-call price sheet doesn't change
- Retry storms (many calls in a short window after an initial failure) correlate with disproportionate billing spikes
- Vendor invoices show a distinct "burst" or "overage" line item that the agent's cost tracker has no corresponding category for
- Exponential backoff intended to reduce load instead clusters retries into a burst window right at the point the rate limit resets, re-triggering the burst tier
- Cost-per-call anomalies appear specifically during traffic spikes, incident response, or backfill/batch jobs rather than steady-state operation

## Root Cause
Retry and backoff logic is designed against a purely technical model of the API (rate limits, error codes, latency) and has no awareness of the vendor's pricing tiers, which live in a separate billing schedule the engineering team building the retry logic may never have read. When many agent instances or a single agent's retries synchronize — a common effect of naive fixed or lightly-jittered backoff — they resubmit in a tight cluster that looks, from the vendor's throughput-metering perspective, like a burst, even though each individual request is "just a retry."

## Example
```
"GeoLookupAPI" bills $0.001/call up to 20 requests/second sustained, and
$0.02/call (20x) for any request that pushes the rolling 1-second rate
above that baseline.

An agent processing a batch of 5,000 address-verification calls hits a
transient 503 from GeoLookupAPI at call 1,200 and applies exponential
backoff: wait 1s, retry 50 queued calls at once, wait 2s, retry the next
100 at once. Each retry batch fires in a tight cluster because the queued
calls were all waiting on the same backoff timer, producing bursts of
80-150 requests/second — 4-7x the 20 req/s baseline.

The agent's cost model assumed $0.001 x 5,000 = $5.00 for the whole batch.
The actual invoice bills roughly 3,000 of the calls at the $0.02 burst
rate because they landed inside metered burst windows, for a real cost
of approximately $61 — more than 12x the estimate.
```

## Statistics
| Finding | Context |
|---------|---------|
| Burst/overage pricing tiers on metered APIs commonly charge 5-20x the baseline per-call rate | Typical range across usage-based API pricing schedules |
| Naive (non-jittered) exponential backoff resynchronizes concurrent retries into clusters in a large share of high-concurrency retry scenarios, a well-documented effect sometimes called retry storming | Commonly observed in distributed systems literature and production incident reviews |
| Cost overruns attributable specifically to burst-tier billing are typically discovered via invoice review, not real-time monitoring, in the majority of cases | Typical range absent dedicated throughput-cost instrumentation |

## Mitigations
1. **Jittered, rate-aware backoff**: Add randomized jitter to backoff intervals and cap the number of retries released per second to stay under the vendor's documented baseline throughput, not just under the rate-limit error threshold.
2. **Client-side request throttling to baseline**: Implement a token-bucket or leaky-bucket limiter client-side, configured to the vendor's pricing-tier baseline (not just their hard rate limit), so the agent voluntarily paces itself below the burst threshold.
3. **Burst-tier-aware cost model**: Model two cost tiers in the budget estimator — baseline and burst — and flag any batch job whose projected concurrency could exceed the baseline threshold before it runs.
4. **Queue-based dispatch with pacing**: Route bursty workloads (batch jobs, backfills, incident-driven spikes) through a queue that dispatches at a fixed sustainable rate rather than releasing all queued/retried calls simultaneously.
5. **Vendor billing schedule reconciliation**: Read and encode the vendor's actual metered-billing documentation (often separate from the API rate-limit docs) into the cost model, and revisit it whenever the vendor changes pricing tiers.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| requests_per_second_vs_baseline | Rolling request rate to a metered tool compared to its documented baseline throughput | Alert if sustained > 90% of baseline for > 30s |
| burst_tier_call_share | Percentage of calls in a billing window priced at the burst/overage rate | Alert if > 5% of calls in any hour |
| retry_cluster_density | Number of retries fired within a 1-second window following a backoff wait | Alert if > baseline throughput threshold |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Burst-tier billing triggered | burst_tier_call_share exceeds 5% in a rolling hour | High | Throttle dispatch rate, review retry/backoff jitter configuration |
| Retry storm detected | retry_cluster_density exceeds the vendor's baseline throughput for a metered tool | Medium | Add or widen jitter, route through paced queue |

## Related Patterns
- [Per-Tool Cost-Per-Operation Surprise](./per-tool-cost-per-operation-surprise.md) - both involve pricing mechanics the agent's cost estimator fails to model
- [Hidden Tool Costs Not Visible](./hidden-tool-costs-not-visible.md) - burst pricing is a form of hidden cost that only appears under specific traffic conditions
- [Per-Tool Tiered Pricing Unknown](./per-tool-tiered-pricing-unknown.md) - a related but inverse case where higher volume should reduce, not increase, per-call cost
