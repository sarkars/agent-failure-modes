# Per-Tool Requests-Per-Day Quota

## Issue
A tool enforces a hard daily request quota (e.g., 1,000 calls/day on a free or standard tier), and the agent has no visibility into how much of that quota remains as the day progresses. Because the agent paces its usage without any remaining-quota signal, it can burn through the full day's allotment in the first few hours of heavy activity, leaving the tool completely unavailable for the remainder of the day regardless of how important later calls are.

**Frequency**: Very Common

**Symptoms**
- The tool works normally in the morning and then fails 100% of calls for the rest of the day, resuming only after a quota reset
- Errors reference "daily quota exceeded" or "daily limit reached" specifically, distinct from per-minute or per-hour rate-limit errors
- High-priority late-day tasks fail for the same reason as low-priority early-day tasks that consumed the quota — there's no reservation or prioritization
- The agent has no logged awareness of remaining quota before the failure — the first sign of trouble is the rejection itself
- Usage is front-loaded (heavy morning batch jobs, exploratory testing) without any deliberate pacing against the known daily cap

## Root Cause
Daily quotas reset on a vendor-defined schedule (often UTC midnight or account-creation-anniversary time) and are consumed on a first-come-first-served basis with no built-in prioritization. Agents typically call tools reactively, as tasks demand, without tracking cumulative daily usage or fetching a remaining-quota endpoint (when one exists), so there is no mechanism preventing early, possibly low-value calls from exhausting a budget that later, possibly high-value calls will need. The failure is entirely a pacing/visibility gap, not a vendor outage.

## Example
```
An agent uses the "CompanyEnrichAPI" connector (daily quota: 2,000 lookups) to enrich lead records as part of a sales-automation pipeline.

08:00 — A scheduled morning batch job kicks off, enriching 1,400 leads from an overnight import — well within a plausible single burst.
11:30 — Ad-hoc enrichment requests from live user sessions have added another 550 lookups, bringing the day's total to 1,950 — still technically fine, but no one is tracking this running total.
11:47 — The batch job's tail end plus a live request pushes the count to 2,001. CompanyEnrichAPI starts returning "daily quota exceeded" for every subsequent call.
14:00 — A high-value enterprise prospect fills out a contact form, triggering a real-time enrichment lookup that the sales team is actively waiting on. It fails with the same quota error as the earlier bulk batch calls.
The quota doesn't reset until 00:00 UTC, so the enrichment tool is unusable for the live sales workflow for the rest of the business day.
```

## Statistics
| Finding | Context |
|---------|---------|
| Daily quotas are the most common quota granularity on free and standard-tier third-party APIs used by agents, appearing in an estimated 40-50% of integrations | Common across SaaS API tiers |
| Agents without remaining-quota tracking exhaust their daily allotment before end-of-day in a majority of moderate-to-high-usage deployments, typically by mid-to-late afternoon | Observed in production agent usage patterns |
| Introducing priority-based quota reservation (holding back a percentage of daily quota for high-priority calls) reduces quota-exhaustion-driven failures for critical-path tasks by 70%+ | Typical outcome of quota reservation remediation |

## Mitigations
1. **Track cumulative daily usage locally**: Maintain a running counter of calls made to the tool since the last known reset, incremented on every call, so the agent always has a same-order-of-magnitude estimate of remaining quota even without a vendor-provided endpoint.
2. **Query the vendor's quota-status endpoint when available**: Many APIs expose a `/usage` or similar endpoint, or return remaining-quota headers on every response — poll or parse these as the authoritative source rather than relying solely on the local counter.
3. **Reserve quota for high-priority call classes**: Partition the daily budget (e.g., 70% for scheduled batch jobs, 30% reserved for real-time/user-facing calls) and enforce the split in the orchestrator so low-priority bulk work can't starve time-sensitive requests later in the day.
4. **Degrade gracefully near quota exhaustion**: When remaining quota drops below a threshold (e.g., 10%), switch the agent to a fallback behavior — cached data, a lower-fidelity alternate tool, or deferred processing — rather than calling until the hard rejection.
5. **Alert well before exhaustion, not after**: Surface a warning when daily usage crosses 80-90% of quota so operators can intervene (reschedule batch jobs, request a quota increase) before the tool goes fully dark for the rest of the day.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `tool.daily_quota_consumed_pct` | Percentage of the daily quota used so far, tracked against the known reset time | Alert at 80% consumed |
| `tool.daily_quota_exhausted_events` | Count of days per week the daily quota was fully exhausted before reset | Alert if 2+ in a rolling 7-day window |
| `tool.quota_denied_high_priority_count` | Count of high-priority/user-facing calls rejected due to daily quota exhaustion | Alert if greater than 0 |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Daily quota approaching exhaustion | `daily_quota_consumed_pct` crosses 80% before 60% of the day has elapsed | Warning | Throttle non-critical batch consumers; consider requesting a quota increase |
| High-priority call denied by quota | Any user-facing or critical-path call rejected with a daily-quota error | Critical | Page on-call; verify quota reservation partitioning is active and correctly sized |

## Related Patterns
- [Per-Tool Requests Per Hour Exceeded](./per-tool-requests-per-hour-exceeded.md) - a shorter-window version of the same visibility gap, often hit before the daily quota even becomes relevant
- [Quota Reset Timing Unknown](./quota-reset-timing-unknown.md) - not knowing precisely when the daily quota resets compounds the pacing problem described here
- [Rolling Window Quota Misunderstanding](./rolling-window-quota-misunderstanding.md) - agents that assume a fixed daily reset when the vendor actually uses a rolling 24-hour window will mispace their usage in a related but distinct way
