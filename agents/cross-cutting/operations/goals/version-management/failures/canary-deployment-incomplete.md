# Canary Deployment Incomplete

## Issue
An agent platform starts a canary rollout of a new agent version — routing a small percentage of live sessions (e.g., 5%) to the new build while the rest continue on the stable version — but the automated or manual promotion process that should ramp the canary from 5% to 100% never completes. The rollout stalls at some intermediate weight indefinitely, sometimes for days or weeks, because the metrics that gate promotion never clearly pass or fail, or because the person/process responsible for the next promotion step loses track of the release. Production ends up permanently running two agent versions side by side, with users nondeterministically getting different behavior depending on which version their session lands on.

**Frequency**: Common

**Symptoms**
- Canary weight (e.g., 10%) stays fixed for far longer than the intended soak period with no promotion or rollback decision made
- Support tickets describe inconsistent agent behavior for "the same" request, traceable to different users landing on different versions
- Two agent versions appear simultaneously in version-distribution dashboards weeks after a release was supposedly shipped
- On-call has no record of who owns the promote/rollback decision for a given in-flight canary
- Automated promotion gate metrics sit in an ambiguous "neither clearly better nor clearly worse" zone that never triggers either an automatic promote or an automatic rollback

## Root Cause
Canary analysis typically compares the new version's metrics (error rate, task success rate, latency, tool-call failure rate) against the baseline over a soak window, then either promotes or rolls back. This works cleanly when the difference is large and obvious, but agent workloads often produce noisy, low-volume, or slow-to-materialize signals — a subtle regression in task success rate might only become statistically distinguishable from baseline after thousands of sessions, which can take days at low canary traffic. If the promotion pipeline requires an explicit human or automated "go" decision rather than defaulting to progress or rollback after a bounded time, and if no timeout or escalation exists for an indecisive result, the canary simply sits at its last weight indefinitely. Ownership diffusion compounds this: the engineer who started the rollout may be off rotation, on a different task, or have assumed CI would auto-promote, and no dashboard surfaces "stuck canaries" as a distinct, actionable category.

## Example
```
Team ships v9 of "ResearchAgent" with a new retrieval-augmented
tool-selection policy. Rollout plan: canary at 5% for 24h, promote to
25% if success rate holds, then 100%.

Day 1: canary set to 5%. Success rate on v9 (94.1%) is statistically
indistinguishable from baseline v8 (94.4%) at this traffic volume —
not clearly worse, not clearly proven safe either.

Day 2: the on-call engineer who started the rollout rotates off.
Handoff notes mention "v9 canary in progress" but no explicit owner
or next-check date is recorded.

Day 3-11: canary stays at 5%. Nobody re-evaluates. New feature work
lands on top of v8 in the main branch, now diverging further from
what's running in the 5% canary.

Day 12: a customer reports inconsistent tool-selection behavior
across two support sessions three minutes apart. Investigation finds
both v8 and v9 are live in production, 95/5 split, nine days after
the canary was supposed to be a 24-hour check.

Day 12 (later): team manually promotes to 100% after re-running the
comparison, but the 9-day delay meant an unrelated regression in v8
(unfixed because "v9 was already rolling out") shipped to 95% of
users the whole time.
```

## Statistics
| Finding | Context |
|---------|---------|
| A meaningful share of canary rollouts in agent systems stall at an intermediate weight for longer than their intended soak window | Estimated from teams tracking rollout duration against plan |
| Stuck canaries are commonly discovered via user-facing inconsistency reports rather than internal monitoring | Typical pattern reported across teams without stuck-canary alerting |
| Adding an explicit timeout-to-decision (auto-promote or auto-rollback after N hours of inconclusive metrics) substantially reduces the incidence of indefinitely stalled canaries | Reported range across teams that added rollout timeouts |

## Mitigations
1. **Bounded soak windows with default action**: Require every canary to have an explicit maximum soak duration after which the system either auto-promotes (if no regression threshold was crossed) or auto-rolls-back (if metrics are inconclusive), rather than waiting indefinitely for a clear signal.
2. **Stuck-canary dashboard and alert**: Track every in-flight canary's age and current weight, and alert when a canary has been at a non-terminal weight (not 0% or 100%) longer than its planned soak period.
3. **Explicit rollout ownership with handoff**: Require a named owner for every active canary, and make on-call handoff checklists include explicit transfer of any in-flight rollout ownership rather than letting it fall through implicitly.
4. **Freeze downstream changes during long-running canaries**: Block or flag further merges to the baseline branch while a canary has been active beyond its planned window, so the comparison doesn't keep drifting.
5. **Statistical power pre-check**: Before starting a canary, estimate whether the planned traffic percentage and soak duration will actually reach statistical significance for the metrics being watched; if not, either widen the canary percentage or extend the plan up front instead of discovering it mid-rollout.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| canary_age_hours | Time since a canary was set to its current non-terminal traffic weight | Alert if > 2x planned soak duration |
| concurrent_live_versions | Count of distinct agent versions currently receiving production traffic | Alert if > 2 sustained for more than 48 hours |
| canary_weight_stalled | Boolean/gauge indicating canary weight has not changed despite soak window expiring | Alert on any true value |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Canary exceeded soak window | canary_age_hours crosses 2x planned duration with no promote/rollback action | Medium | Notify rollout owner or on-call, force a promote/rollback decision within a fixed SLA |
| Long-running dual-version traffic | Two agent versions both receiving >1% of traffic for over 72 hours | Medium | Escalate to release owner, review whether rollout should be aborted |

## Related Patterns
- [Blue-Green Deployment Traffic Not Switched](./blue-green-deployment-traffic-not-switched.md) - a related failure where the traffic-shift mechanism itself, rather than the promotion decision, fails to progress
- [Version Rollout Coordination](./version-rollout-coordination.md) - stalled canaries compound coordination problems when downstream services expect a rollout to have finished
- [Weighted Routing Algorithm Error](./weighted-routing-algorithm-error.md) - describes a different way the traffic split itself can be wrong, independent of whether the promotion decision stalls
- [Health Check Flapping](./health-check-flapping.md) - a noisy or flapping health signal can be one root cause of an inconclusive canary metric that never triggers promotion
