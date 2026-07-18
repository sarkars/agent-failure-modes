# Quota Reset Boundary Race

## Issue
Multiple instances of an agent (or multiple sub-agents sharing one API key) send requests right around a quota window's reset boundary, and because clock synchronization between the agent fleet and the vendor's rate-limit accounting is imperfect, the enforcement becomes inconsistent at exactly the moment it should be cleanest: some requests sent a few milliseconds before the reset are counted against the new window, some sent a few milliseconds after are still counted against the old (exhausted) one, and different agent instances observe different outcomes for functionally identical timing.

**Frequency**: Occasional

**Symptoms**
- Two agent instances issuing near-simultaneous requests right at a known reset time get different results — one succeeds, one gets rate-limited — despite both believing the window has reset
- Rejections cluster in a narrow window (often under 1-2 seconds) immediately before or after the documented reset boundary, then disappear
- The same agent instance, retried a few seconds later, succeeds without any code change
- Aggregate quota usage reported by the vendor for the "new" window is nonzero within the first second after reset, even though the agent fleet expected a clean slate
- The issue is hard to reproduce deterministically because it depends on the fleet's exact request timing relative to the vendor's internal clock, not on any code path the agent controls

## Root Cause
Distributed rate-limit enforcement (especially at a load-balanced API gateway backed by multiple counting nodes) rarely applies a perfectly atomic, instantaneous cutover at the reset boundary — there's a small window where different backend nodes may have slightly different views of "has this key's counter reset yet." Combine that with multiple agent instances (or sub-agents) independently timing their requests off their own local clocks, which are themselves not perfectly synchronized with the vendor's reset clock, and you get a scenario where simultaneous or near-simultaneous requests from the agent side land on both sides of a fuzzy, non-atomic boundary on the vendor side — producing outcomes that look inconsistent even though each individual decision was locally correct.

## Example
```
Three instances of a horizontally-scaled agent worker fleet all use the same ScrapingAPI key, which resets its per-minute quota (100 requests) at the top of each minute.

At 14:32:59.950, all three worker instances have exhausted the current minute's quota and are each holding one queued request, timed to fire right at 14:33:00.000 based on the reset time returned by a previous response header.
14:33:00.010 — Worker A's request lands on a gateway node whose internal clock/counter has already rolled over; it succeeds and counts against the new minute.
14:33:00.015 — Worker B's request lands on a different gateway node that hasn't yet processed the rollover for this key; it's rejected as still exceeding the old minute's 100/100 count.
14:33:00.020 — Worker C's request succeeds, landing on yet another node that already rolled over.
The fleet's shared assumption ("it's past :00, we're all clear") turns out to be false for one of three functionally identical requests, and Worker B's task fails with a rate-limit error immediately after what everyone believed was a clean reset.
```

## Statistics
| Finding | Context |
|---------|---------|
| Boundary-race inconsistencies typically affect a narrow sub-second-to-2-second window around a reset, but that window disproportionately concentrates fleet traffic that was deliberately queued to fire right at reset | Common in horizontally-scaled agent deployments sharing one API key |
| Multi-instance agent fleets racing a known reset boundary see inconsistent outcomes (some succeed, some rejected) in an estimated 5-15% of reset events, depending on gateway architecture | Observed in distributed agent worker deployments |
| Adding a small deliberate delay (200-500ms) after the nominal reset time before resuming traffic largely eliminates boundary-race rejections at the cost of a small fixed latency per reset cycle | Typical outcome of delayed-resume remediation |

## Mitigations
1. **Don't queue requests to fire exactly at the reset boundary**: Add a small buffer (a few hundred milliseconds) after the nominal reset time before resuming traffic, trading a negligible latency cost for avoiding the fuzziest part of the boundary.
2. **Stagger multi-instance resume timing**: If multiple agent instances share a key and are all waiting on the same reset, add per-instance jitter to when each resumes sending, so the fleet doesn't collectively slam the boundary in the same sub-second window.
3. **Treat boundary-adjacent rejections as retryable, not fatal**: Specifically for 429s occurring within a couple seconds of an expected reset, retry once after a short delay rather than treating it as a hard failure — it's very likely to succeed on the next attempt once the vendor's own state settles.
4. **Centralize quota tracking across instances**: Route all instances' awareness of remaining quota through a shared coordinator (e.g., a Redis-backed counter) rather than each instance independently guessing based on its own last-seen response headers, reducing the chance that multiple instances all believe they have quota available at the same instant.
5. **Log gateway/node-identifying response metadata if available**: If the vendor exposes any request-ID or node-identifying header, log it alongside boundary-race failures — it helps confirm (and report to the vendor) that the inconsistency is a backend propagation artifact rather than an agent-side bug.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `tool.boundary_race_rejection_count` | 429s occurring within 2 seconds of a known/expected quota reset time | Alert if greater than 0 across more than one reset cycle per day |
| `tool.fleet_reset_outcome_variance` | Fraction of simultaneous post-reset requests from different instances that receive different outcomes | Alert if variance exceeds 10% of reset events |
| `tool.resume_delay_ms` | Configured buffer delay after nominal reset before resuming traffic | Verify nonzero; alert if 0 (no buffer configured) |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Boundary race detected | Multiple instances get differing outcomes for near-simultaneous post-reset requests | Warning | Confirm resume-delay buffer and instance jitter are configured |
| Recurring boundary rejections | `boundary_race_rejection_count` > 0 for 3+ consecutive reset cycles | Warning | Increase resume-delay buffer; consider centralized quota coordination |

## Related Patterns
- [Quota Reset Timing Unknown](./quota-reset-timing-unknown.md) - not knowing the precise reset time in the first place makes this race harder to avoid, since the agent can't even queue accurately near the boundary
- [Quota Reset During Operation](./quota-reset-during-operation.md) - both involve inconsistent state at a reset boundary, but this pattern is about concurrent instances racing the boundary rather than one long operation spanning it
- [Per-Tool Requests Per Hour Exceeded](./per-tool-requests-per-hour-exceeded.md) - describes a related boundary-adjacent miscounting scenario at the hourly-window granularity
