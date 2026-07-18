# Rolling Window Quota Misunderstanding

## Issue
The agent's pacing logic assumes a tool's quota resets at a fixed clock boundary (e.g., "resets at midnight UTC" or "resets at the top of the hour"), but the tool actually enforces a rolling/sliding window — quota consumed at any given moment doesn't free up until exactly that much time has elapsed since it was consumed, continuously, rather than all at once at a fixed reset point. Because the agent's scheduling strategy is built around a reset-and-refill mental model, it either waits far longer than necessary for capacity to return, or assumes capacity is available at a "reset time" that doesn't actually exist for a rolling window.

**Frequency**: Common

**Symptoms**
- The agent waits until an assumed fixed reset time (e.g., top of the hour) but the tool was actually already available again well before that, or still exhausted after that
- Quota "frees up" gradually in small increments over time rather than jumping back to full capacity all at once
- Two identical requests made at the same clock time on different days get different outcomes, because what matters is time-since-each-individual-past-request, not time-since-a-fixed-anchor
- Debugging reveals that the actual availability pattern tracks "N requests in the trailing X minutes" rather than "N requests since HH:00"
- Vendor documentation says "sliding window," "rolling limit," or "trailing N-minute window" — terminology the agent's fixed-reset scheduling logic doesn't account for

## Root Cause
Fixed windows and rolling windows are implemented very differently on the vendor side (a fixed window resets a single counter at a clock boundary; a rolling window tracks a timestamped log of recent requests and only "frees" capacity as old requests age out of the trailing window), and the two produce meaningfully different availability patterns. Agent developers who default to assuming fixed-window semantics — because it's the simpler mental model and the more common convention for daily/monthly quotas — build scheduling and backoff logic around waiting for a discrete reset event, which simply doesn't exist for a rolling window. There's no "reset moment" to wait for; there's only a continuously shifting boundary of trailing time, and pacing has to be modeled completely differently.

## Example
```
An agent uses the "SmsGatewayAPI" tool, documented as "100 messages per 10-minute window" — ambiguous language that could mean either a fixed 10-minute bucket (resets every :00, :10, :20, etc.) or a rolling 10-minute window (trailing from now).

The integration team assumes a fixed window and builds retry logic that, upon hitting the limit, waits until the next 10-minute clock boundary (e.g., if rate-limited at 14:23, it waits until 14:30).
In reality, SmsGatewayAPI enforces a rolling window: it tracks the timestamp of each of the last 100 requests and only allows a new one once the oldest of those 100 ages past 10 minutes.
The 100 requests that triggered the limit were sent in a tight burst between 14:18 and 14:23. Under the true rolling-window behavior, capacity should start trickling back at 14:28 (10 minutes after the earliest of the 100), well before the agent's assumed 14:30 fixed boundary.
The agent needlessly waits an extra 2 minutes doing nothing, even though the tool had capacity available starting at 14:28.
On a different occasion, the same agent hits the limit at 14:31 (just after what it assumes is a "fresh" window starting at 14:30) and, believing it just got a full reset, immediately fires 100 more requests — but because the rolling window is still counting some of the pre-14:30 burst, only a fraction of those succeed before it's rate-limited again, contradicting the agent's fixed-window assumption in the other direction.
```

## Statistics
| Finding | Context |
|---------|---------|
| Rolling/sliding window rate limiting is used by an estimated 30-40% of modern rate-limited APIs, particularly those built on token-bucket or sliding-log algorithms, and is increasingly common relative to simple fixed windows | Common in contemporary API gateway implementations |
| Agents built with fixed-window assumptions against an actually-rolling-window tool see both false waits (delaying longer than necessary) and false starts (assuming full capacity too early) in roughly equal measure | Observed in production integrations with ambiguous vendor documentation |
| Switching pacing logic to a sliding-log or leaky-bucket client-side model that mirrors the vendor's actual algorithm (once confirmed) eliminates both failure directions simultaneously | Typical outcome of correcting the window-model mismatch |

## Mitigations
1. **Confirm the window type explicitly before building pacing logic**: Don't infer fixed-vs-rolling from ambiguous documentation language ("per 10 minutes" can mean either) — test empirically by sending a burst, then probing capacity recovery at multiple points to observe whether it returns all-at-once (fixed) or gradually (rolling).
2. **Model rolling-window quota with a client-side sliding log**: For confirmed rolling-window tools, track the timestamp of every request made in the trailing window locally, and compute "can I send now" based on how many of those timestamps are still within the window — mirroring the vendor's actual algorithm instead of waiting for a nonexistent reset event.
3. **Avoid burst-then-wait-for-reset patterns against rolling windows**: Since there's no discrete reset to wait for, replace "wait until reset, then burst again" scheduling with steady-state pacing that spreads requests evenly, which works correctly under both fixed and rolling semantics.
4. **Don't assume symmetric behavior across window types when handling 429s**: Rate-limit recovery logic that works correctly for a fixed window (wait until known reset time) will systematically misbehave against a rolling window and vice versa — branch the backoff strategy on the confirmed window type rather than using one generic approach.
5. **Document the confirmed window type per tool in integration notes**: Once empirically determined, record whether each integrated tool uses fixed or rolling windows so future changes to pacing logic don't regress back to the wrong assumption.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `tool.capacity_recovery_pattern` | Observed shape of quota recovery after exhaustion (step-function vs gradual) | Flag mismatch if gradual recovery is observed but fixed-window logic is configured |
| `tool.premature_burst_rejection_count` | Count of rejections occurring shortly after an assumed fixed-window reset | Alert if greater than 0, suggesting the window is actually rolling |
| `tool.unnecessary_wait_time_s` | Time spent idle waiting for an assumed reset when capacity was actually already available | Alert if consistently over a few minutes per cycle |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Window-model mismatch suspected | Rejections occur just after an assumed fixed reset, or capacity is observed recovering gradually rather than all at once | Warning | Empirically re-verify window type; switch pacing model to sliding-log if rolling is confirmed |
| Recurring false-start rejections | 429s recur immediately after each assumed reset across multiple cycles | Warning | Treat as high-confidence rolling-window mismatch; prioritize fixing pacing logic |

## Related Patterns
- [Per-Tool Requests Per Hour Exceeded](./per-tool-requests-per-hour-exceeded.md) - the underlying limit this pattern's misdiagnosis often applies to, since hourly limits are a common place for the fixed-vs-rolling ambiguity to appear
- [Quota Reset Timing Unknown](./quota-reset-timing-unknown.md) - a broader pattern of not knowing the reset mechanism at all; this pattern is the specific case of confidently assuming the wrong mechanism
- [Token-Based Rate Limiting](./token-based-rate-limiting.md) - another case where the agent's mental model of "what's being counted and how" diverges from the vendor's actual accounting method
