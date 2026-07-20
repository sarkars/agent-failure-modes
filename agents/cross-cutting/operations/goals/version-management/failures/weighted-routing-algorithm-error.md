# Weighted Routing Algorithm Error

## Issue
The algorithm that computes how much traffic to send to each version during a weighted or gradual rollout contains a bug in the weight-computation logic itself — an off-by-one in a percentage calculation, a stale cached weight table that doesn't reflect the latest configured split, integer rounding that silently drops a low-percentage version's share to zero, or a race condition where concurrent weight updates and live traffic routing interleave incorrectly. Unlike infrastructure that executes a correct set of weights unevenly across different paths, here the weights being executed are themselves wrong: every routing decision faithfully applies a miscalculated split, so the actual traffic distribution differs from the intended one consistently and reproducibly, not intermittently or path-dependently.

**Frequency**: Occasional

**Symptoms**
- Observed version distribution differs from the configured weights by a consistent, reproducible amount (not just noise), such as a configured 5% canary that consistently measures at 0% or at 50%
- A version configured with a small nonzero weight (e.g., 1-2%) receives exactly zero traffic, consistent with integer rounding truncating a fractional percentage down to zero
- Updating the routing configuration to a new set of weights doesn't change observed traffic distribution until an unrelated restart or cache expiry, consistent with a stale cached weight table
- Two routing decisions made in rapid succession under concurrent load are inconsistent with each other in a way that suggests the weight table was being read while also being written
- The routing configuration file/API reports one set of weights while the actual traffic split, measured independently, reports a different set — with the discrepancy stable over time rather than settling once "warmed up"

## Root Cause
Weighted routing typically works by mapping a request to a version using some form of deterministic or pseudo-random selection against a cumulative weight distribution — for example, generating a random number and checking which cumulative weight bucket it falls into, or hashing a request/session identifier into a percentage range. Bugs enter at several specific points in this computation: cumulative-weight construction that has an off-by-one at a bucket boundary (causing the boundary version to get double or zero share), integer-only percentage math that truncates a fractional weight to zero rather than using an accumulator that preserves fractional share across requests, a weight table cached at startup or on a TTL that isn't invalidated when the underlying configuration changes, or concurrent writers updating the weight table without synchronization while readers are actively using it to route live traffic, producing torn reads. Because the routing logic is applying its computed weights faithfully and consistently, the resulting misdistribution is deterministic and reproducible given the bug — which distinguishes it from failures where correctly-computed weights are applied unevenly due to infrastructure quirks, and from failures where a rollout simply never finishes progressing.

## Example
```
A deployment platform implements weighted canary routing by
converting each version's percentage weight into an integer number of
"slots" out of 100 and assigning a request to a version based on
request_id % 100 falling within that version's slot range. An
operator configures a new version at a 3% canary weight.

The slot-assignment function computes each version's slot count using
integer division: int(3 * 100 / 100) in a code path that, due to an
unrelated refactor, actually receives the weight as an already-scaled
value averaged against a rounding step elsewhere in the pipeline,
producing an effective slot count of 0 for the 3% canary after the
double-scaling and truncation. The canary version is configured,
deployed, and reports itself healthy and receiving traffic in its own
service logs (from being reachable via direct debug requests), but
the routing layer's slot table gives it zero production request
slots.

The canary dashboard shows "0 requests routed to canary" for a
version that is definitely deployed and definitely healthy, which the
on-call engineer initially misdiagnoses as a deployment failure and
spends an hour investigating the deployment pipeline before finding
the actual cause in the slot-computation code, unrelated to the
deployment itself.
```

## Statistics
| Finding | Context |
|---|---|
| Weight-computation bugs are disproportionately concentrated at low configured percentages (single digits), where integer truncation and rounding errors are most likely to collapse a nonzero intended weight to an observed zero | Typical pattern observed in production weighted-routing implementations using integer-based slot math |
| Stale cached weight tables account for a notable share of "routing configuration changed but traffic distribution didn't" incidents, distinguishable from infrastructure-asymmetry causes by the fact that all entry points show the same stale split | Estimated from incident review of weighted-rollout configuration-update failures |
| Routing implementations using floating-point or fractional-accumulator weight math report a meaningfully lower rate of small-percentage-collapses-to-zero bugs than implementations using naive integer percentage math | Typical range observed comparing floating-point vs. integer-only weight computation approaches |

## Mitigations
1. **Use fractional/accumulator-based weight math, not naive integer truncation**: Compute routing decisions using floating-point weights or a fractional accumulator that preserves a low percentage's share across many requests, rather than integer division that can truncate a small nonzero weight to zero.
2. **Explicit cache invalidation on weight-configuration change**: Ensure any cached or precomputed weight table is invalidated immediately when the underlying routing configuration changes, and add a check that compares the live routing behavior against the currently configured weights rather than assuming a config update always propagates.
3. **Synchronize weight-table reads and writes under concurrent load**: Use an atomic swap or versioned snapshot for the weight table so concurrent configuration updates and live routing decisions never interleave into a torn or partially-updated read.
4. **Continuous measured-vs-configured distribution validation**: Independently measure actual traffic distribution and compare it against the configured weights on an ongoing basis, alerting on any sustained, reproducible deviation rather than assuming the routing algorithm is correct because the configuration itself looks correct.
5. **Unit-test weight computation at boundary values**: Specifically test the weight-computation logic at edge cases (very small percentages, weights summing to slightly over/under 100 due to floating-point representation, boundary values at bucket edges) rather than only testing typical mid-range weight splits.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| configured_vs_observed_weight_delta | Difference between the configured routing weight and the actual measured traffic share for each version | Alert if delta exceeds a small tolerance (e.g., 2 percentage points) and persists beyond a brief settling window |
| routing_config_propagation_lag | Time between a routing configuration change and the observed traffic distribution reflecting it | Alert if lag exceeds the expected cache TTL/propagation time by a significant margin |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Sustained weight-distribution deviation | configured_vs_observed_weight_delta remains above tolerance for a version over a rolling window | High | Audit the weight-computation code path for rounding/truncation bugs, check for stale cache |
| Zero traffic to a nonzero-weighted version | A version configured with a nonzero weight measures 0% observed traffic share | High | Treat as a routing algorithm bug candidate before assuming a deployment or health-check issue |

## Related Patterns
- [Traffic Routing Asymmetry](./traffic-routing-asymmetry.md) - a related but distinct failure where correctly-computed weights are applied unevenly across different entry points or protocols due to infrastructure quirks, rather than the weight computation itself being wrong
- [Canary Deployment Incomplete](./canary-deployment-incomplete.md) - a related but distinct failure where a rollout stalls at an intermediate weight and never progresses, as opposed to this pattern's consistently miscalculated weight at any given point in the rollout
- [Sticky Session Loss](./sticky-session-loss.md) - a related infrastructure-level routing failure that can produce similar-looking distribution anomalies but stems from session-affinity handling rather than weight-computation bugs
