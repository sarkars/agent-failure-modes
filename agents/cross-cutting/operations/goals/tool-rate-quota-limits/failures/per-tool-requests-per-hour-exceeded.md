# Per-Tool Requests-Per-Hour Exceeded

## Issue
A tool enforces an hourly request quota, and an agent whose usage is bursty within the hour — heavy activity in a 10-minute window followed by relative quiet — exceeds the hourly cap even though its average request rate across the full day is well within budget. Unlike a daily quota, the hourly window resets often enough that the failure is usually short-lived, but frequent enough (potentially every hour) to meaningfully degrade throughput if the agent's traffic pattern is inherently spiky.

**Frequency**: Very Common

**Symptoms**
- 429 or quota-exceeded errors cluster around specific times of day (e.g., top of the hour when scheduled jobs run) rather than being evenly distributed
- The tool works fine for 40-50 minutes of every hour and then fails for the remainder until the next hourly reset
- Daily quota utilization (when tracked separately) looks comfortably under budget even during hours when the hourly cap is being hit
- Batch jobs scheduled at round-number times (e.g., every hour on the hour) are disproportionately likely to trigger the failure, since they concentrate load right after a reset
- Agent logs show request volume in the triggering window is 3-5x the hourly-average rate the agent's overall usage would suggest

## Root Cause
Hourly quotas are typically fixed-window (reset at :00 each hour) rather than rolling, so all usage within that clock hour counts against the same bucket regardless of how it's distributed inside the hour. Agents whose workload is naturally bursty — scheduled batch jobs, event-driven spikes, retry storms — concentrate their calls into narrow sub-windows within the hour, and because most agent designs pace against a *daily* or *per-minute* budget without an intermediate *hourly* check, there's no mechanism catching the mismatch between "fine on average" and "over budget in this particular hour."

## Example
```
An agent uses the "NewsAggregatorAPI" (hourly limit: 500 requests) to pull updates for a portfolio of 300 tracked topics, refreshed via a scheduled job.

The scheduling logic runs the full 300-topic refresh once every hour, at the top of the hour, plus another ~150 ad-hoc lookups trickle in from user-initiated searches spread across the rest of the hour.
09:00:00-09:00:45 — The scheduled batch job fires all 300 refresh calls in under a minute.
09:15-09:59 — Ad-hoc user searches add another 150 calls, bringing the hour's total to 450 — still under the 500 cap, so no failures yet.
10:00:00 — The next scheduled batch fires another 300 calls starting at the top of the new hour, but a few residual calls from 09:59 plus the new batch's early calls land close enough to the boundary that clock skew between the agent's scheduler and the vendor's reset time causes the first ~30 calls of the new batch to still count against the prior window in the vendor's accounting.
10:00:12 — With the prior window's count nudged over 500 by those boundary-adjacent calls, NewsAggregatorAPI starts rejecting requests, stalling the batch job 12 seconds after it started even though the "new" hour's true usage is nowhere near the cap.
```

## Statistics
| Finding | Context |
|---------|---------|
| Hourly quotas are used by an estimated 25-35% of tools alongside or instead of daily/per-minute limits, often specifically to smooth batch-job bursts | Common in SaaS API tiering |
| Scheduled jobs firing on round-number boundaries (top of the hour) are disproportionately represented in hourly-quota-exceeded incidents relative to their share of total traffic | Observed scheduling pattern in production agent deployments |
| Spreading a batch job's calls evenly across the hour (rather than firing all at :00) typically reduces hourly-quota rejections to near zero for the same total volume | Typical outcome of load-smoothing remediation |

## Mitigations
1. **Spread scheduled batch calls across the window, not at its start**: Rather than firing an entire batch job's worth of calls in the first minute of the hour, distribute them evenly (or with jitter) across the full hour so usage tracks a smooth rate rather than a spike.
2. **Track hourly usage as a distinct budget from daily/per-minute**: Maintain a separate rolling counter for the current clock hour, and throttle or defer non-critical calls once hourly usage crosses a safety threshold (e.g., 85%), independent of daily quota headroom.
3. **Avoid scheduling exactly on vendor reset boundaries**: Offset scheduled jobs by a few minutes from round-number times (e.g., :07 instead of :00) to reduce the chance of clock-skew-related boundary miscounting between the agent's scheduler and the vendor's reset clock.
4. **Reserve hourly headroom for ad-hoc/user-facing traffic**: If both scheduled batch and real-time user calls share an hourly quota, cap the batch job's consumption to a fixed fraction of the hourly limit so live traffic always has room.
5. **Detect and log hourly-specific rejections separately from daily ones**: Parse the error response or headers to identify which window (hourly vs daily) triggered the rejection, so remediation efforts target the actual bottleneck instead of guessing.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `tool.hourly_quota_consumed_pct` | Percentage of the current hour's quota consumed, reset each clock hour | Alert at 85% consumed with more than 15 minutes remaining in the hour |
| `tool.hourly_burst_ratio` | Ratio of calls made in the first 5 minutes of the hour vs the hourly average | Alert if ratio exceeds 3x, indicating a scheduling concentration problem |
| `tool.hourly_429_count` | Count of 429s specifically attributable to the hourly window | Alert if greater than 0 in more than 1 hour per day |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Hourly quota exhausted mid-hour | `hourly_quota_consumed_pct` reaches 100% with time remaining in the clock hour | Warning | Investigate whether a scheduled job is front-loading calls; add spreading/jitter |
| Recurring boundary-time rejections | `hourly_429_count` > 0 for the same clock-hour slot across multiple days | Critical | Offset the responsible scheduled job's start time away from the reset boundary |

## Related Patterns
- [Per-Tool Requests Per Day Quota](./per-tool-requests-per-day-quota.md) - the longer-window sibling; agents need to track both independently since being fine on one says nothing about the other
- [Quota Reset Boundary Race](./quota-reset-boundary-race.md) - describes the clock-skew boundary miscounting mechanism referenced in this pattern's example in more detail
- [Per-Tool Requests Per Minute Exceeded](./per-tool-requests-per-minute-exceeded.md) - the shorter-window sibling, typically hit first when a batch job front-loads its calls
