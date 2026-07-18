# Rate Limit Grace Period Missing

## Issue
Some tools enforce rate limits with zero grace period: the moment a request is rejected with a 429, the very next request — even one sent a fraction of a second later, even one that would normally be well within budget — is also immediately rejected, with no brief cooldown signal or soft-warning phase before the hard cutoff. Agents that respond to the first 429 by retrying quickly (assuming a brief backoff is enough) get rejected again immediately, and if their backoff strategy isn't tuned for a limit with no forgiveness, this produces a tight loop of rapid-fire failures instead of a clean recovery.

**Frequency**: Common

**Symptoms**
- The request immediately following a 429 also fails with a 429, even after a short delay that "should" have been enough based on typical rate-limit behavior
- No `Retry-After` header or any other signal indicating how long to actually wait is present in the 429 response
- Agents using a fixed short backoff (e.g., always wait 1 second and retry) see repeated consecutive failures rather than a clean recovery on the first retry
- The tool's actual recovery behavior only becomes reliable after a comparatively long, empirically-discovered wait (much longer than the agent initially assumed)
- Vendor documentation doesn't mention any grace period or cooldown behavior at all, leaving the agent to guess

## Root Cause
Rate-limit enforcement implemented as a hard fixed-window or leaky-bucket counter with no smoothing or soft-reject phase means the transition from "allowed" to "blocked" is a sharp edge with no intermediate signal. Many vendors don't provide a `Retry-After` header (or provide one inconsistently), so an agent's backoff strategy has no ground truth to calibrate against and defaults to a guessed value that may be far shorter than what the tool actually needs to recover. Because there's no partial-credit or gradual re-opening behavior on the vendor side, any retry sent before the full window has elapsed is rejected exactly as hard as the original — there's no "almost allowed" state for the agent to detect and adapt to.

## Example
```
An agent calls the "GeocodingAPI" tool (limit: 50 requests/10 seconds, fixed window, no Retry-After header, no documented grace period) as part of an address-validation pipeline processing 200 addresses.

Requests 1-50 succeed within the first 2 seconds (well under the 10-second window).
Request 51 is rejected with a bare "429 Too Many Requests" and no headers indicating when to retry.
The agent's default backoff (1 second, doubling) retries after 1 second — still well inside the same 10-second fixed window, since only 3 seconds have elapsed since the window started — and is rejected again.
It retries again after 2 more seconds (3 seconds elapsed since first failure, 5 seconds since window start) — still rejected, since the window doesn't reset until 10 seconds from its start, not 10 seconds from the first failure.
Only the fourth retry, at roughly 8 seconds after the first rejection (putting it past the window's true reset point), finally succeeds — the agent burned 3 wasted round-trips and roughly 7 seconds of avoidable delay because its backoff schedule wasn't calibrated to the tool's actual (undocumented) window length.
```

## Statistics
| Finding | Context |
|---------|---------|
| A meaningful share of production APIs — commonly estimated at a third or more of smaller/less mature providers — return 429s with no `Retry-After` header or any other explicit recovery-timing signal | Common gap in third-party API implementations |
| Agents using a short fixed or lightly-scaled backoff against no-grace-period tools typically need 2-4 retry attempts before succeeding, versus 1 attempt when backoff is properly calibrated to the actual window | Observed in production retry-loop analysis |
| Calibrating backoff empirically (measuring actual time-to-recovery once and using it as a floor for future backoff) reduces wasted retry attempts by roughly half to two-thirds compared to guessed fixed backoff | Typical outcome of empirical backoff calibration |

## Mitigations
1. **Never assume a short default backoff is sufficient**: For tools with no documented grace period, treat the first observed 429-after-429 as a signal to escalate backoff aggressively (e.g., jump straight to several seconds or more) rather than incrementing gradually from a low starting point.
2. **Empirically measure and cache the real recovery time**: The first time a rate limit is hit, measure how long it actually took before a retry succeeded, and use that measured value (with margin) as the backoff floor for future occurrences against the same tool, rather than re-guessing every time.
3. **Honor Retry-After whenever present, and fall back to a conservative default when absent**: Parse the header when the vendor provides it; when absent, default to a deliberately generous wait (several seconds, not one) rather than assuming the tool is forgiving.
4. **Avoid immediate retry entirely on the first 429**: Insert a mandatory minimum delay before any retry attempt after a rate-limit rejection, even if the backoff algorithm would otherwise suggest retrying sooner — a hard floor protects against a zero-grace-period tool specifically.
5. **Rate-limit proactively so grace period rarely matters**: Since a missing grace period turns any 429 into an expensive several-retry ordeal, invest more in staying under the limit in the first place (client-side pacing) than in optimizing recovery after the fact.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `tool.consecutive_429_count` | Count of back-to-back 429 responses for the same logical call before a success | Alert if median exceeds 2 |
| `tool.retry_after_header_present_pct` | Percentage of 429 responses that include a usable Retry-After or equivalent header | Track as informational; low values justify a more conservative default backoff |
| `tool.time_to_recovery_s` | Measured time between first 429 and first subsequent success | Use to calibrate and update the cached backoff floor for this tool |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Zero-grace-period pattern detected | `consecutive_429_count` median exceeds 2 for a given tool over a rolling week | Warning | Increase the backoff floor for this tool; consider proactive client-side pacing instead of reactive retry |
| Retry storm on grace-period-less tool | 3+ consecutive 429s observed for a single logical call | Warning | Escalate backoff aggressively; verify a hard minimum delay is enforced before retry |

## Related Patterns
- [Per-Tool Requests Per Minute Exceeded](./per-tool-requests-per-minute-exceeded.md) - tight retry loops against a per-minute limit are especially damaging when combined with a missing grace period
- [Rate Limit Header Not Honored](./rate-limit-header-not-honored.md) - when Retry-After is present but ignored, the effect closely resembles a missing grace period even though the vendor did provide guidance
- [Connection Timeout No Retry](./connection-timeout-no-retry.md) - both patterns hinge on whether the agent's retry/backoff strategy matches the actual recovery characteristics of the failure
