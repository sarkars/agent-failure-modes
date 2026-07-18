# Per-Tool Daily Budget Exhaustion

## Issue
A tool has a fixed daily budget cap, and normal usage patterns (a morning traffic spike, a batch job front-loaded early in the day) exhaust it well before the day ends. The agent has no fallback tool, no degraded mode, and no queuing strategy for when the cap is hit — it either starts failing every task that needs the tool, or silently stops calling it and produces lower-quality output without telling anyone, for the remaining hours of the day.

**Frequency**: Very Common

**Symptoms**
- Tool call failure rate spikes at a consistent time of day, correlating with when the daily cap is typically reached
- Task quality or completeness degrades in the afternoon/evening relative to morning for tasks depending on the capped tool
- No alerting distinguishes "tool is down" from "tool budget is exhausted for the day" — both look like call failures to downstream consumers
- Users or downstream systems receive silently degraded results (agent falls back to a weaker method) with no indication the primary tool was unavailable
- Budget resets at midnight/start-of-day cause a burst of queued or retried work right after reset

## Root Cause
Daily budget caps are usually implemented as a simple hard stop — reject calls once the counter hits the ceiling — because it's the easiest control to build and reason about. This treats the budget as a binary available/unavailable resource rather than a finite resource that needs to be paced across the day or that requires an explicit fallback strategy when exhausted. Nobody designs for the exhausted state because it's treated as an edge case, even though front-loaded usage patterns make it a routine daily occurrence.

## Example
```
An agent uses "EnrichAPI" for customer lookups, capped at $30/day
(3,000 calls at $0.01 each). Usage is heavily front-loaded: 65% of the
day's customer interactions happen between 9am and 1pm.

By 12:40pm, the agent has made 2,980 calls. At 12:47pm the cap is hit.

For the remaining 8+ hours of the business day, every call to EnrichAPI
returns a budget-exceeded error. The agent has no configured fallback, so
it silently returns customer records without enrichment data (skipping
the enrichment step in a try/except that logs at debug level only).

Support agents reviewing enriched customer profiles that afternoon see
incomplete data for every ticket and assume EnrichAPI is broken; it takes
three days before someone traces the pattern to the daily budget cap
consistently resetting usage at midnight and being consumed by 1pm.
```

## Statistics
| Finding | Context |
|---------|---------|
| Usage-based tools integrated into customer-facing workflows commonly see 50-70% of daily volume concentrated in a 4-6 hour peak window | Typical range for business-hours-driven workloads |
| Silent-fallback failure handling (catching a budget error and proceeding with degraded output, without logging at a visible severity) is a common pattern in agent tool wrappers | Frequently observed in production incident postmortems |
| Time-to-detection for daily-cap exhaustion incidents is often measured in days when fallback behavior is silent, versus minutes when the failure is a hard error surfaced to monitoring | Typical range depending on fallback design |

## Mitigations
1. **Intra-day pacing**: Rate-limit the agent's own consumption of the daily budget (e.g. no more than 1/24th of the daily cap per hour, with some burst allowance) so usage is spread across the day rather than front-loaded.
2. **Explicit degraded-mode signaling**: When the budget is exhausted, have the agent return a clearly flagged degraded result (not a silent fallback) so downstream consumers and monitoring know the difference between "tool down" and "budget exhausted."
3. **Priority queuing for exhaustion windows**: When approaching the cap, shift to serving only high-priority requests and queue or defer low-priority ones to the next budget reset rather than serving all requests until the cap hits, then serving none.
4. **Fallback tool or cached-data path**: Configure a secondary, cheaper (or free) data source to use once the primary tool's daily budget is exhausted, even if lower quality, rather than no data at all.
5. **Predictive alerting before exhaustion**: Alert when projected end-of-day usage (based on current burn rate) will exceed the cap, while there's still time in the day to intervene (raise the cap, throttle, or notify stakeholders).

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| daily_budget_burn_rate | Percentage of daily cap consumed versus percentage of the day elapsed | Alert if burn rate exceeds elapsed-day ratio by 1.5x |
| budget_exhaustion_time_of_day | Clock time each day when the cap is reached | Alert if exhaustion occurs before 80% of the day has elapsed |
| degraded_mode_duration | Total time per day spent operating without the capped tool | Alert if > 2 hours/day |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Projected early exhaustion | Current burn rate implies the cap will be hit before end of business hours | High | Throttle low-priority calls, notify budget owner for possible cap increase |
| Silent degraded mode active | Tool calls are failing due to budget exhaustion and no explicit fallback signal is being emitted | High | Add explicit degraded-mode flagging, page integration owner |

## Related Patterns
- [Per-Tool Monthly Budget Overrun](./per-tool-monthly-budget-overrun.md) - the monthly-scale analog of the same fixed-cap-without-pacing problem
- [Tool Budget Starvation](./tool-budget-starvation.md) - describes what happens when the exhausted budget is shared across multiple consumers rather than one
- [Budget Priority Misalignment](./budget-priority-misalignment.md) - a priority scheme is one of the core fixes for exhaustion-window degradation
