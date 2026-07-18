# Policy Temporal Violation

## Issue
A policy that is only supposed to be active during a specific time window — a temporary spending freeze, a holiday change-lockdown, a time-boxed data-access restriction — is either enforced outside that window (blocking actions after it should have lapsed) or fails to be enforced within the window (letting restricted actions through during the period they were supposed to be blocked). The root cause is almost always a timezone or scheduling bug in how the window's boundaries are evaluated.

**Frequency**: Common

**Symptoms**
- A temporary restriction still blocking actions days or weeks after its stated end date
- A restriction failing to activate at its intended start time, leaving a gap where restricted actions proceed normally
- Boundary behavior that differs depending on which timezone the evaluating system or the requester is in
- Restrictions tied to calendar concepts ("business hours," "holiday period," "end of quarter") that are hardcoded for one timezone or region but applied globally
- Off-by-one-day errors at window boundaries due to date-only (no time-of-day) comparisons combined with timezone conversion

## Root Cause
Time-windowed policies require correctly comparing the current evaluation time against start/end boundaries, but this comparison is deceptively easy to get wrong: mixing UTC and local time, using date-only comparisons that silently truncate time-of-day, hardcoding a single timezone for a globally distributed system, or failing to account for daylight saving transitions. Any of these causes the effective enforcement window to diverge from the policy's actual intended window, often by hours or a full day at the boundaries.

## Example
```
1. Finance declares a spending freeze for the last three business days of
   the fiscal quarter, intended to run from 00:00 to 23:59 in the
   company's headquarters timezone (US Eastern).
2. The policy engine stores the freeze window as calendar dates only
   ("2026-06-28" to "2026-06-30") with no timezone attached, and evaluates
   "current time" using the server's UTC clock.
3. An agent operating on behalf of a team in a UTC+8 timezone submits a
   purchase request at what is 9:00 AM local time on July 1 -- already past
   the freeze in their own calendar -- but this corresponds to 21:00 UTC on
   June 30, which the engine (comparing UTC date only) still considers
   inside the freeze window.
4. The request is blocked even though, from the requester's own timezone
   and the freeze's intended Eastern-time boundary, the freeze had already
   ended.
5. Separately, a request submitted at 11:00 PM Eastern on June 30 (still
   within the intended freeze) corresponds to a UTC date of July 1, and the
   engine -- again comparing only UTC calendar date -- treats it as outside
   the freeze and approves it, letting a restricted purchase through during
   the actual freeze period.
```

## Statistics
| Finding | Context |
|---------|---------|
| Timezone-related boundary bugs are among the most commonly cited causes of incorrect enforcement in time-windowed policy systems | Well-established pattern in distributed-systems scheduling literature |
| Policies evaluated using date-only comparisons (versus full timestamp with explicit timezone) show a materially higher rate of boundary misenforcement | Consistent with the information loss inherent in date-only representations |
| Daylight saving transition periods are disproportionately represented in temporal-policy incident reports relative to the small fraction of the year they cover | Typical pattern reflecting the extra edge-case complexity DST introduces |

## Mitigations
1. **Explicit, stored timezone for every time-windowed policy**: Define policy start/end boundaries as full timestamps with an explicit timezone (or as UTC with clear conversion rules), never as bare calendar dates, and document which timezone governs the policy's intent.
2. **Single source of truth for "current time" evaluation**: Evaluate all time-window checks against a consistently sourced, correctly-synced clock (e.g., a UTC timestamp service), avoiding client-supplied or inconsistently configured local clocks.
3. **Boundary test coverage including DST transitions**: Include explicit test cases for policy windows that span a daylight saving transition and for requesters in timezones far from the policy's reference timezone.
4. **Grace-period logging at window boundaries**: Log every enforcement decision made within a defined margin (e.g., 2 hours) of a window boundary with enough detail to audit whether the boundary was applied correctly, since these are the highest-risk cases.
5. **Automated pre/post-window verification**: Automatically verify, at the moment a time-windowed policy is scheduled to start and end, that enforcement actually activated/deactivated as intended, alerting if the observed enforcement state doesn't match the expected state.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `boundary_window_decision_rate` | Share of policy decisions made within a defined margin of a time-window boundary | Tracked continuously, reviewed for boundary-margin decisions |
| `post_window_enforcement_count` | Number of actions blocked by a time-windowed policy after its stated end timestamp has passed | > 0 (should be zero) |
| `pre_window_gap_count` | Number of restricted actions allowed through before a time-windowed policy's stated start timestamp took effect | > 0 (should be zero) |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Policy still enforcing past its end timestamp | An action is blocked by a time-windowed policy after its recorded end time has passed | Critical | Immediately verify window configuration, manually clear stale enforcement state, unblock legitimate pending actions |
| Policy failed to activate at start timestamp | Actions that should be restricted proceed normally past a time-windowed policy's start timestamp | Critical | Immediately activate enforcement, audit actions taken during the gap for retroactive review |

## Related Patterns
- [Policy Retroactive Application](./policy-retroactive-application.md) - both involve mismatches between the time a policy is intended to apply and the time it's actually evaluated
- [Policy Version Mismatch](./policy-version-mismatch.md) - both can result in enforcement against the wrong effective policy state for a given moment in time
- [Approval Timeout Expiration](./approval-timeout-expiration.md) - both involve time-boundary handling errors in approval-adjacent logic
