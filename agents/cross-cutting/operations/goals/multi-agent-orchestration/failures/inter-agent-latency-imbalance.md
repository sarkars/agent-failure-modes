# Inter-Agent Latency Imbalance

## Issue
When two or more agents collaborate on a shared task but have persistently different response latencies — one calls a fast local model, another calls a slower remote API, or one has a heavier context to process — the faster agent either sits idle waiting on the slower one, or worse, proceeds to act on the slower agent's most recently available (and now stale) output rather than waiting for its current, in-flight result. Both outcomes degrade the collaboration: idle waiting wastes throughput, and acting on stale data produces decisions based on outdated information.

**Frequency**: Common

**Symptoms**
- One agent in a pair or group consistently finishing far ahead of its counterpart across many tasks
- The faster agent's decisions occasionally based on the slower agent's previous-turn output rather than its current one
- Overall pipeline throughput bottlenecked to the slowest agent's pace even when other agents have spare capacity
- Intermittent inconsistencies traced to the fast agent having "moved on" before the slow agent's relevant update arrived
- Utilization metrics showing the fast agent idle a large fraction of the time while the slow agent is consistently saturated

## Root Cause
Multi-agent designs frequently assume roughly symmetric latency between collaborating agents, using simple synchronous request/response or round-based coordination without accounting for structural latency differences — different underlying models, different network hops, different amounts of context to process, or different downstream tool dependencies. When the assumption breaks, the coordination protocol has no way to distinguish "the slow agent hasn't answered yet" from "the slow agent has nothing new to say," so a naive implementation either blocks (killing throughput) or reads whatever value is currently in the slow agent's output slot, even if it's from a previous round and now stale relative to the fast agent's current state.

## Example
```
A trading-signal system pairs a Fast Sentiment Agent (a lightweight model
scanning news headlines, ~150ms per cycle) with a Slow Fundamentals Agent
(a heavier model cross-referencing financial filings via a third-party
API, ~4-6s per cycle) in a shared decision loop that runs every 200ms.

Cycle 1 (t=0ms): Both agents start fresh. Fast Sentiment Agent finishes at
                 150ms with "neutral". Slow Fundamentals Agent is still
                 processing.
Cycle 2 (t=200ms): The combiner logic needs both signals to act. Since
                    Slow Fundamentals Agent hasn't produced cycle-1's
                    output yet, the combiner reads its last known value
                    from three cycles ago: "bullish" (based on filings
                    data that is now over 15 seconds stale, from before
                    a negative earnings revision was published).
Cycle 2 result: The combiner issues a "buy" signal based on fresh
                sentiment but 15-second-stale fundamentals, moments
                before the earnings revision causes a 3% price drop --
                a decision that would have been "hold" or "sell" had it
                waited another 2 seconds for the current fundamentals
                result.
```

## Statistics
| Finding | Context |
|---------|---------|
| Latency imbalances of 10x or more between collaborating agents are common when mixing lightweight and heavyweight models or tools in the same pipeline | Typical range observed in mixed-model agent architectures |
| Systems that read stale values from a slower peer rather than waiting are estimated to base a meaningful share of decisions on data more than one full cycle old under sustained imbalance | Estimated from instrumented multi-agent coordination logs |
| Introducing staleness-aware combiners (explicitly tracking and bounding how old each input is) reduces stale-data-driven errors by a majority in reported deployments | Reported range across teams that added staleness tracking to fan-in combiners |

## Mitigations
1. **Staleness-aware fan-in**: Attach a timestamp or version to every agent's output and have the combining logic explicitly check and bound how old each input is before using it, rather than silently reading whatever's most recently available.
2. **Asymmetric cycle rates**: Let each agent run at its own natural cadence and have the combiner wait for or interpolate between the slower agent's actual update cycles, rather than forcing all agents into a single shared tick rate.
3. **Speculative execution with reconciliation**: Allow the fast agent to act speculatively on its best current guess of the slow agent's output, but reconcile and correct the decision once the slow agent's actual result arrives, if the action is reversible.
4. **Latency-matched agent pairing**: Where the task allows, pair agents with comparable latency profiles, or add a caching/precomputation layer to the slower agent to bring its typical latency closer to its counterpart's.
5. **Explicit "no fresh data" handling**: Give the combiner logic a defined behavior for the case where a required input hasn't arrived in time (skip the cycle, fall back to a conservative default) rather than defaulting to the last stale value with no signal that it's stale.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| inter_agent_latency_ratio | Ratio of the slowest to fastest agent's response time in a collaborating group | Alert if > 5x sustained |
| combiner_input_staleness | Age of each input at the moment a fan-in decision is made | Alert if any input exceeds 2x its expected cycle time |
| fast_agent_idle_ratio | Fraction of time the faster agent spends waiting on the slower one | Alert if > 50% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Decision made on stale input | A combined decision used an input older than the defined staleness bound | High | Flag decision for review, check slow agent's health |
| Persistent latency imbalance | inter_agent_latency_ratio exceeds threshold for a sustained period | Medium | Investigate slow agent's dependencies, consider caching or re-pairing |

## Related Patterns
- [Agent Timeout Cascade](./agent-timeout-cascade.md) - sustained latency imbalance is a common precursor to timeout cascades once one agent's slowness exceeds a caller's patience
- [Agent Resource Contention](./agent-resource-contention.md) - contention on a shared resource is a frequent cause of the latency imbalance between agents in the first place
- [Agent State Divergence](./agent-state-divergence.md) - acting on a slower peer's stale output is a specific mechanism by which state divergence occurs
