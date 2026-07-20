# Integration Cascading Failure

## Issue
Multiple, ostensibly unrelated integrations share underlying infrastructure — a connection pool, a shared API gateway, a common authentication service, a rate-limited egress proxy — and a failure or degradation in that shared layer, triggered by problems with just one integration, propagates outward and takes down the others. An agent that assumes its integrations fail independently (and builds isolated fallback logic per integration) is caught off guard when a single root cause degrades several integrations at once, exhausting fallback capacity faster than expected or triggering compounding retries that make the shared resource contention worse.

**Frequency**: Occasional

**Symptoms**
- Multiple, functionally unrelated integrations start failing simultaneously with no code change to any of them individually
- Root-cause investigation reveals a shared dependency (connection pool, gateway, auth token service, network egress path) common to all the affected integrations
- Retry logic in each affected integration, acting independently, amplifies load on the already-struggling shared resource, worsening the outage
- An incident that looks like "several vendors are down at once" turns out to be one internal shared component failing
- Fallback paths designed assuming only one integration fails at a time become simultaneously unavailable because they route through the same compromised shared infrastructure

## Root Cause
Shared infrastructure exists specifically to avoid duplicating cost and effort (one connection pool instead of N, one auth gateway instead of N), but that same sharing creates a hidden coupling between integrations that were designed and are reasoned about as independent. Engineers building integration A's retry and fallback logic typically don't model "what if the shared connection pool that integration A, B, and C all use becomes exhausted because of a problem in integration B" — that failure mode lives at a layer below any single integration's ownership boundary, so no one integration's resilience design accounts for it, and the interaction is only visible when it actually happens.

## Example
```
A customer-service agent has three separate integrations -- a CRM lookup
API, a knowledge-base search API, and an order-status API -- each routed
through a shared internal API gateway that handles authentication token
refresh and connection pooling to reduce the number of open connections to
downstream vendors.

The order-status API begins returning errors due to an unrelated vendor-side
incident. The agent's retry logic for the order-status integration retries
aggressively (3 retries with short backoff) on every failure, as designed
for that integration in isolation. Because all three integrations share the
same gateway's connection pool, the retry storm from the failing
order-status calls exhausts the pool's available connections.

CRM lookups and knowledge-base searches, both completely healthy on the
vendor side, start failing with "connection pool exhausted" errors as a
side effect, even though nothing is wrong with either of those services.
The agent's fallback logic for each integration was designed assuming the
other two would remain available to compensate, so when all three degrade
simultaneously, the agent has no working path to answer even basic customer
questions, turning a single vendor's incident into a full outage of the
support agent.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 20-30% of multi-integration outages involve a shared infrastructure component as the actual root cause, despite initially appearing as multiple independent vendor failures | Typical range observed in incident postmortem classification |
| Retry storms against a shared resource are a contributing factor in an estimated 30-40% of cascading integration failures | Estimated from incident analysis of shared-resource exhaustion events |
| Per-integration connection pool isolation (bulkheading) reduces the blast radius of a single integration's failure by an estimated 60-80%, measured by number of unrelated integrations affected | Reported range across teams adopting bulkhead patterns |

## Mitigations
1. **Bulkheading shared resources per integration**: Partition shared infrastructure (connection pools, rate limit budgets, thread pools) into isolated per-integration allocations, so one integration's failure or retry storm cannot exhaust capacity needed by another.
2. **Circuit breakers scoped per downstream dependency**: Implement circuit breakers that trip independently for each specific downstream integration, stopping retries against a failing one before it can consume shared capacity needed by healthy integrations.
3. **Shared infrastructure dependency mapping**: Explicitly document and monitor which integrations share which underlying infrastructure components, so incident responders can quickly identify a shared root cause instead of investigating each integration as independently broken.
4. **Coordinated, capped retry budgets**: Cap total retry volume across all integrations sharing an infrastructure layer, rather than letting each integration's retry logic operate as if it had unlimited access to shared capacity.
5. **Chaos testing shared-infrastructure failure scenarios**: Regularly test what happens when one integration is deliberately degraded, verifying that healthy integrations sharing the same infrastructure remain unaffected, rather than discovering the coupling during a real incident.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| shared_resource_utilization_by_integration | Breakdown of shared connection pool/gateway utilization attributable to each individual integration | Alert if one integration consumes a disproportionate share during a degradation |
| cross_integration_correlated_failure_rate | Correlation of simultaneous failure onset across integrations sharing infrastructure | Alert if two or more unrelated integrations degrade within the same short window |
| retry_amplification_factor | Ratio of actual downstream request volume to baseline request volume during a degradation | Alert if > 3x baseline |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Simultaneous multi-integration degradation | Two or more integrations sharing infrastructure degrade within the same short window | High | Investigate shared infrastructure layer first, not each vendor independently; apply circuit breaker to the triggering integration |
| Shared resource near exhaustion | Shared connection pool/gateway utilization approaches capacity limit | High | Trigger bulkhead isolation, shed load from lowest-priority integration |

## Related Patterns
- [Integration Rate Limit Across Systems](./integration-rate-limit-across-systems.md) - shared rate limits are one specific type of shared infrastructure whose exhaustion by one integration can cascade to others
- [Dependency Circular Reference](./dependency-circular-reference.md) - both describe failure propagating through a coupling that isn't visible in any single component's own design
- [Integration Timeout Mismatch](./integration-timeout-mismatch.md) - inconsistent timeouts across integrations sharing infrastructure affect how quickly a cascading failure spreads versus gets contained
