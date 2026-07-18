# Per-Tool Requests-Per-Minute Exceeded

## Issue
A tool enforces a per-minute rate limit, and the agent hits it during a tight retry loop: an initial call fails or is slow, the agent retries immediately without backoff, and each retry itself consumes another slot against the same per-minute budget — compounding the original problem instead of resolving it. What starts as one transient failure turns into a cascade of rate-limit rejections that persists well past whatever caused the first failure.

**Frequency**: Very Common

**Symptoms**
- A single initial error (timeout, 500, or even a first 429) is followed by a rapid burst of additional 429s within the same minute
- Retry timestamps in logs show sub-second or low-second gaps between attempts, with no increasing backoff
- The tool's per-minute quota is exhausted almost entirely by retries of the same logical request, not by distinct new requests
- The failure resolves on its own once the per-minute window rolls over, then immediately recurs if the same tight-loop retry logic triggers again
- Total distinct "useful" work attempted is much lower than the total request count sent, because most requests were retries of the same handful of failed calls

## Root Cause
Naive retry implementations (a `while not success: call()` loop, or a fixed-delay retry with no exponential backoff) treat a 429 the same as any other transient error and retry as fast as the loop allows. Because the per-minute limit counts *all* requests including failed retries, a tight retry loop against a rate-limited tool is self-defeating: each retry both consumes budget and has a high chance of also failing, generating yet another retry. Without backoff that specifically respects the rate-limit window, the agent's own retry behavior becomes the dominant driver of continued failures.

## Example
```
An agent's "PriceCheck" step calls the RetailPricingAPI connector (limit: 60 requests/minute) once per product, for a catalog of 80 products, dispatched with a naive for-loop and no rate-aware pacing.

Requests 1-60 within the current minute succeed.
Request 61 (for product #61) returns 429 "rate limit exceeded, 60/min."
The agent's retry wrapper catches the exception and immediately retries with no delay, consuming another slot in the same already-exhausted minute — also rejected.
This immediate-retry loop repeats 3 times for request 61 alone before the wrapper gives up and marks it failed, having spent 4 requests (1 original + 3 retries) to fail once.
Requests 62-80 are dispatched right behind it in the same tight loop, each independently repeating the same 4x retry-and-fail pattern.
By the time the per-minute window rolls over, the agent has sent well over 130 requests trying to complete 20 remaining product lookups, and still has 19 of them unresolved because most of its budget in the new minute is immediately consumed by yet another wave of retries from the backlog.
```

## Statistics
| Finding | Context |
|---------|---------|
| Retry loops without backoff can amplify a single rate-limit event into 3-5x the original request volume before self-correcting | Typical of naive fixed-delay or no-delay retry logic |
| Per-minute limits are the most frequently hit rate-limit tier in agent tool usage, given how easily bursty task dispatch (loops, fan-out) concentrates calls within a 60-second window | Common across API-integrated agent tools |
| Adding exponential backoff with a floor tied to the per-minute window (e.g., wait at least until the next minute boundary after 2 consecutive 429s) typically cuts total request volume for the same completed work by more than half | Typical outcome of backoff remediation |

## Mitigations
1. **Never retry a 429 immediately**: On receiving a rate-limit rejection, the very next attempt must wait — at minimum the vendor's `Retry-After` value if provided, otherwise an exponential backoff starting well above zero (e.g., 1-2 seconds, doubling on repeat 429s).
2. **Pace proactively, not just reactively**: Rather than dispatching all requests and reacting to 429s, use a client-side rate limiter (token bucket sized to the known per-minute limit) so the agent stays under the ceiling by design instead of by trial and error.
3. **Cap total retry attempts per logical request**: Set a hard ceiling (e.g., 3-4 attempts) so a persistently rate-limited call fails cleanly and is handled by the orchestrator (queued, deferred) rather than retrying indefinitely and eating into every subsequent minute's budget.
4. **Serialize backlog processing after a rate-limit event**: Once a 429 is observed, switch remaining queued calls to a tool from parallel/immediate dispatch to a paced serial dispatch until a window boundary passes cleanly with no rejections.
5. **Log retry-vs-original request ratio**: Track what fraction of total requests to a tool are retries versus original attempts, making runaway retry amplification visible in dashboards rather than hidden inside aggregate request counts.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `tool.retry_to_original_ratio` | Ratio of retry requests to original (first-attempt) requests for a given tool | Alert if ratio exceeds 1.0 (more retries than original calls) |
| `tool.per_minute_429_count` | Count of 429 responses attributed to the per-minute window | Alert if greater than 5 in any single minute |
| `tool.time_between_retries_ms` | Median gap between a failed call and its retry | Alert if under 500ms, indicating missing/ineffective backoff |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Retry amplification detected | `retry_to_original_ratio` exceeds 1.0 while `per_minute_429_count` is elevated | Warning | Confirm exponential backoff is active; check for a tight retry loop bypassing it |
| Sustained per-minute exhaustion | `per_minute_429_count` > 5 for 3+ consecutive minutes | Critical | Switch affected tool traffic to serialized/paced dispatch; page on-call if task-critical |

## Related Patterns
- [Rate Limit Grace Period Missing](./rate-limit-grace-period-missing.md) - the immediate-next-call-also-rejected scenario this pattern's retry loop is especially vulnerable to
- [Per-Tool Burst Rate Exceeded](./per-tool-burst-rate-exceeded.md) - a shorter-window variant of the same "dispatch too much too fast" root problem
- [Connection Timeout No Retry](./connection-timeout-no-retry.md) - the opposite failure (no retry at all); both stem from retry logic that isn't tuned to the specific failure type
