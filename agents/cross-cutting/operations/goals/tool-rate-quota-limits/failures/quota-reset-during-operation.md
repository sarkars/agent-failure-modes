# Quota Reset During Operation

## Issue
A single logical operation — a multi-step workflow, a paginated data pull, or a batch job that makes many sequential tool calls — spans a quota reset boundary partway through. The calls made before the reset count against the old window, the calls made after count against the new one, and because the agent tracks the operation as one atomic unit but the vendor tracks quota in two disjoint windows, the two views of "how much budget is left" fall out of sync mid-operation, sometimes causing the tail of the operation to fail even though a fresh reset "should" have provided plenty of headroom.

**Frequency**: Occasional

**Symptoms**
- A long-running batch or pagination job fails partway through specifically around known reset times (e.g., top of the hour, midnight UTC), not randomly
- The failure count and success count for a single logical operation don't add up cleanly against one quota window — some of the operation's calls are attributed to yesterday's quota, some to today's
- Restarting the failed portion of the operation immediately after the reset succeeds, suggesting quota was available but the operation's own accounting didn't realize it
- Operations that happen to start well clear of a reset boundary never exhibit the issue, while operations that start close to one do, even with identical total call counts
- Progress-tracking or checkpoint logic for the operation doesn't record which quota window each call was made under, making post-hoc debugging difficult

## Root Cause
Agents typically treat a quota as a single running counter for the duration of an operation ("I have a budget of X calls for this job") without accounting for the fact that the vendor's quota window is anchored to wall-clock time, not to the operation's start time. When an operation's duration is comparable to or longer than the time remaining until the next reset, calls made before and after the boundary are silently split across two separate vendor-side buckets. If the agent's pre-flight quota check happened once at operation start (checking "is there enough quota for N calls" against the then-current window), it has no way of knowing the window will roll over mid-operation, and if it happened to start near quota exhaustion in the old window, the operation can stall right at the boundary waiting on a reset that its own tracking doesn't model.

## Example
```
A data-sync agent runs a "FullCatalogSync" job against the InventorySystem API (quota: 5,000 requests per rolling calendar day, reset at 00:00 UTC), paginating through 4,800 SKUs at roughly 1 request per SKU.

23:40 UTC — The sync job starts. A pre-flight check confirms "4,800 needed, quota shows 4,850 remaining today" — looks safe.
23:40-23:59 — The job processes about 3,600 SKUs (900 requests/minute pace), consuming quota against the pre-reset day's window.
00:00 UTC — The quota resets. The remaining 1,200 SKUs should now have a fresh 5,000-request budget available.
00:00-00:02 — Due to how the job's internal retry/pagination cursor handles an in-flight request that was issued at 23:59:58 and receives its response at 00:00:03, the job's own quota accounting (which incremented its local counter at request-send time, tied to the old window) reports "exceeded pre-reset budget" and pauses the job, waiting for a reset that, from the vendor's side, already happened — a false stall caused by the operation's internal bookkeeping not re-synchronizing with the new window.
00:05 UTC — An operator manually resumes the job after noticing it stalled despite the vendor dashboard showing ample quota, losing several minutes of unattended runtime.
```

## Statistics
| Finding | Context |
|---------|---------|
| Long-running batch operations (over 15-30 minutes) that don't explicitly account for reset boundaries have an elevated chance of hitting boundary-related stalls proportional to how close their scheduled start time is to a known reset | Common in nightly/hourly batch-sync agent workloads |
| Operations that re-check remaining quota against a live vendor-provided counter (rather than a locally-cached pre-flight number) avoid the large majority of boundary-crossing stalls | Typical outcome of live-quota-check remediation |
| Checkpointing progress with the quota window it was made under simplifies post-incident reconciliation, cutting debugging time for boundary-related failures substantially compared to operations with no window-tagged checkpoints | Typical benefit of window-aware checkpointing |

## Mitigations
1. **Re-check live quota periodically during long operations**: Instead of a single pre-flight quota check at operation start, poll the vendor's remaining-quota signal (header or endpoint) at intervals throughout a long-running operation, so the agent's view stays current across a reset.
2. **Tag checkpoints with the quota window they were made under**: When checkpointing progress in a multi-call operation, record which quota window (e.g., "2026-07-18" vs "2026-07-19") each batch of calls was attributed to, making it possible to reconcile actual vendor-side usage against the operation's own accounting after the fact.
3. **Treat a reset mid-operation as an opportunity, not an obstacle**: Design the operation's pacing logic to recognize a reset event and immediately resume at full budget rather than continuing to enforce the old window's now-irrelevant limit.
4. **Schedule long operations to avoid straddling known reset times where feasible**: If an operation's typical duration is known and a vendor's reset time is documented, prefer start times that keep the bulk of the operation comfortably within a single window, reserving cross-boundary operations for cases where it's unavoidable.
5. **Decouple local quota bookkeeping from request-send time**: Increment local quota counters based on response time/window-at-response rather than request-send time, so calls that straddle a boundary (sent in one window, responded to in the next) are attributed consistently with how the vendor actually counted them.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `operation.reset_boundary_crossings` | Count of long-running operations whose duration spanned a known quota reset | Informational; correlate with stall/failure events |
| `operation.stall_duration_near_reset_s` | Time an operation spent paused/stalled within 5 minutes of a reset boundary | Alert if greater than 60 seconds |
| `operation.quota_window_mismatch_count` | Count of checkpoints where local quota accounting diverged from vendor-reported usage for the same window | Alert if greater than 0 |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Operation stalled at reset boundary | An in-progress operation pauses within a few minutes of a known reset time | Warning | Check whether local quota tracking is stale vs the vendor's live counter; resume manually if confirmed safe |
| Recurring boundary stalls on scheduled job | Same scheduled operation stalls at reset boundary across multiple runs | Critical | Reschedule the job's start time or add live quota re-checking |

## Related Patterns
- [Quota Reset Boundary Race](./quota-reset-boundary-race.md) - a related boundary-timing issue, but caused by multiple concurrent instances racing the boundary rather than one operation spanning it
- [Quota Reset Timing Unknown](./quota-reset-timing-unknown.md) - not knowing the exact reset time makes it harder to even detect that an operation is about to straddle one
- [Per-Tool Requests Per Day Quota](./per-tool-requests-per-day-quota.md) - the daily-quota context in which this cross-boundary operation failure most commonly occurs
