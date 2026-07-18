# Tool Budget Starvation

## Issue
Multiple agents or tasks share a single pooled budget for a tool (e.g. one $500/day cap on a translation API shared across all customer-facing workflows), and a high-frequency consumer — a chatty agent that calls the tool far more often than others, or a runaway loop — consumes a disproportionate share of the pool early, leaving other agents or tasks unable to make even essential calls for the rest of the period. Unlike a simple exhaustion, the problem here is specifically that the shared pool has no fairness mechanism, so one consumer's volume determines everyone else's access.

**Frequency**: Common

**Symptoms**
- Some agents/workflows sharing a tool budget pool consistently fail to get calls through while others consume the majority of the pool
- The starved agents' failure pattern correlates with a specific high-volume consumer's activity, not with overall demand exceeding the total budget
- No per-consumer quota or fair-share allocation exists within the shared pool — it's a single counter checked by everyone
- Low-frequency but high-importance tasks (e.g. an occasional compliance-check call) fail more often than high-frequency, lower-importance tasks (e.g. a chatty exploratory agent)
- Adding more total budget to the shared pool provides only temporary relief because the high-frequency consumer scales its usage to match

## Root Cause
Shared budget pools are usually implemented as a single atomic counter that any authorized caller can decrement, because that's the simplest way to enforce an aggregate cap across multiple consumers. This design has no notion of "consumer identity" or fair allocation built in — it treats all calls as fungible and doesn't reserve capacity per consumer. When consumers have very different call frequencies (by design, by bug, or by a runaway loop), the shared-nothing counter structurally favors whichever consumer calls most often and first, since there's no mechanism stopping one consumer from claiming the entire pool before others get a turn.

## Example
```
Three internal agents share one $500/day budget pool for "TranslateAPI":
a customer-support agent (moderate, steady volume), a content-localization
batch agent (runs large overnight batches), and a compliance-review agent
(low volume, but each of its calls gates a required legal review step).

One night, the content-localization agent's batch job scope is
misconfigured and re-processes an entire historical content archive
instead of just the day's new content — roughly 40,000 calls instead of
the expected 800. By 6am, it has consumed $480 of the $500 daily pool.

When the compliance-review agent tries to make its 9am calls (typically
only 15-20/day, essential for gating releases), it receives
budget-exceeded errors for the rest of the day. Three scheduled releases
are blocked because the compliance gate can't complete its required
translation check, even though the compliance agent's own typical usage
is a tiny fraction of the total pool.
```

## Statistics
| Finding | Context |
|---------|---------|
| Shared, unpartitioned budget pools across 3+ consumers show meaningfully uneven consumption, with the top consumer often accounting for the large majority of usage | Common pattern in unpartitioned shared-resource pools |
| Low-frequency, high-importance consumers of a shared budget pool are disproportionately affected by starvation incidents relative to their share of total budget usage | Frequently observed in incident postmortems involving shared quota pools |
| Simply increasing the total pool size after a starvation incident provides only short-term relief in a majority of cases where the high-frequency consumer's behavior is unbounded | Typical outcome absent per-consumer quotas |

## Mitigations
1. **Per-consumer sub-quotas**: Partition the shared pool into guaranteed minimum allocations per consumer (agent, task type, team) so no single high-frequency consumer can claim the entire pool, with an optional shared overflow pool for excess capacity.
2. **Priority-weighted allocation**: Assign priority weights to consumers (e.g. compliance-gating calls outrank exploratory batch calls) and enforce that low-priority consumers back off first when the pool nears exhaustion.
3. **Rate limiting per consumer independent of the shared cap**: Apply a per-consumer maximum call rate in addition to the shared pool cap, so a single misconfigured or runaway consumer is capped well before it can consume the whole pool.
4. **Reserved capacity for critical paths**: Carve out a portion of the pool that only critical/gating workflows can draw from, inaccessible to bulk or exploratory consumers regardless of remaining shared balance.
5. **Consumer-level usage monitoring and circuit breakers**: Track per-consumer share of pool consumption in real time and automatically throttle or halt a consumer whose usage deviates sharply from its historical baseline, before it starves others.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| consumer_pool_share | Percentage of the shared budget pool consumed by each individual consumer in a period | Alert if any single consumer exceeds 60% of pool |
| starved_consumer_failure_rate | Call failure rate for consumers other than the top consumer of a shared pool | Alert if > 5% for any consumer while pool shows other consumers under quota |
| critical_path_budget_denial | Count of budget-exceeded errors on calls tagged as critical/gating | Alert if > 0 |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Single consumer dominance | consumer_pool_share exceeds 60% for one consumer in a shared pool | High | Throttle the dominant consumer, investigate for misconfiguration or runaway loop |
| Critical-path call denied | A call tagged critical/gating is rejected due to shared pool exhaustion | High | Immediately allocate from reserved capacity, page on-call |

## Related Patterns
- [Budget Priority Misalignment](./budget-priority-misalignment.md) - starvation is the multi-consumer version of the same lack-of-priority problem within a single agent
- [Per-Tool Daily Budget Exhaustion](./per-tool-daily-budget-exhaustion.md) - starvation is one specific cause of exhaustion, driven by uneven consumption rather than aggregate demand
- [Cross-Tool Total Budget Exceeded](./cross-tool-total-budget-exceeded.md) - both involve pooled-resource accounting gaps, one across tools and one across consumers of one tool
