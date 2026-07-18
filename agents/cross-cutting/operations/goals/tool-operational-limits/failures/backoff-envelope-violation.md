# Backoff Envelope Violation

## Issue
Many APIs specify an expected retry envelope for failed requests — a minimum delay before retrying (to avoid hammering a recovering service) and a maximum delay (beyond which the server considers the client "gone" and drops queued state, such as an idempotency reservation or a rate-limit grace window). An agent's retry logic, especially generic exponential-backoff code reused across many tools, frequently ignores tool-specific envelope hints (a `Retry-After` header, a documented min/max, or a jittered range) and either retries too fast — getting throttled harder or banned — or waits too long — missing a narrow retry window and losing queued work or an idempotency token.

**Frequency**: Common

**Symptoms**
- Retry attempts logged at intervals shorter than the server's advertised `Retry-After`, followed by escalating `429`/`503` responses instead of recovery
- A retry that arrives after the server's idempotency-key TTL has expired, causing a duplicate side effect instead of a safe replay
- Rate-limit penalties that compound over a session because each too-fast retry resets or extends the throttle window
- Agents using a fixed or capped backoff ceiling (e.g., max 30s) against an API that expects retries no sooner than 2 minutes
- Support tickets or API-provider warnings citing "abusive retry pattern" for traffic that the agent's own logs show as "graceful retry with backoff"

## Root Cause
Generic retry libraries implement a single backoff policy (e.g., exponential with jitter, capped at some default ceiling) applied uniformly across all tools, without parsing or respecting per-tool signals like `Retry-After`, `X-RateLimit-Reset`, or documented min/max retry windows. Agents built to be "resilient by default" often hardcode these defaults at the framework level, so a tool with an unusually wide or narrow envelope (e.g., a webhook provider requiring retries no sooner than 60s, or a payment gateway requiring retries within a 5-minute idempotency window) gets a backoff schedule that was never designed for it. The mismatch is invisible until the failure that the envelope was designed to prevent actually happens.

## Example
```
An agent calls a shipping-label API that returns 429 with
Retry-After: 120 (seconds) when its per-minute quota is exceeded. The
agent's retry wrapper uses a standard exponential backoff starting at 1s,
capped at 16s: it retries at 1s, 2s, 4s, 8s, 16s, 16s, 16s... All retries
land inside the still-active 120s throttle window, each one re-triggering
the rate limiter's penalty counter. After 8 retries the API's abuse
detector flags the API key for a 1-hour cooldown, far longer than the
original 120s the agent would have waited had it honored Retry-After.
The agent's error handling treats the cooldown as "transient" and keeps
retrying every 16s for the full hour, generating 225 wasted requests
before the key is manually unblocked by an engineer.
```

## Statistics
| Finding | Context |
|---------|---------|
| A large fraction of agent frameworks default to a fixed exponential-backoff ceiling regardless of tool-specific Retry-After values | Common in general-purpose HTTP client wrappers used by agents |
| Retry storms that ignore Retry-After typically extend outage/throttle duration by 3-10x compared to compliant backoff | Based on typical rate-limiter penalty-escalation designs |
| Idempotency-key TTLs on payment and messaging APIs are commonly in the 5-15 minute range; agent retry ceilings are commonly under 1 minute, so envelope violations more often manifest as duplicate side effects than as missed windows | Comparing typical provider TTL documentation to typical retry-library defaults |

## Mitigations
1. **Parse and honor server-provided retry hints**: Always read `Retry-After`, `X-RateLimit-Reset`, or equivalent headers and use them as the floor for the next retry delay, overriding any client-side default schedule.
2. **Maintain a per-tool backoff policy, not a global default**: Store the min/max retry envelope per tool (from documentation or observed headers) and route retry scheduling through that policy instead of a single shared exponential-backoff implementation.
3. **Cap total retry duration against known TTLs**: When a tool exposes an idempotency-key or reservation TTL, ensure the retry schedule's total elapsed time never exceeds it; abandon and re-plan rather than retry past expiry.
4. **Detect and back off from escalating penalties**: If successive responses show an increasing Retry-After or a harsher error class (429 -> 503 -> account-level block), stop automatic retries and escalate to a human or a slower out-of-band recovery path.
5. **Log the envelope alongside each retry decision**: Record the server-advertised envelope and the delay actually used on every retry, so envelope violations are visible in logs rather than only inferable from downstream throttling.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `retry.delay_vs_retry_after_ratio` | Actual delay used divided by server-advertised Retry-After | Alert if ratio < 1.0 (retried before permitted) |
| `retry.penalty_escalation_count` | Count of consecutive retries met with a harsher error/status than the previous attempt | Alert if >= 2 in a single retry sequence |
| `retry.idempotency_ttl_margin` | Time remaining on an idempotency/reservation TTL when a retry is sent | Alert if margin < 10% of original TTL |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Retry-After violated | Delay used < server Retry-After on any call | High | Halt automatic retries for that tool, alert on-call, review backoff config |
| Retry storm penalty escalation | 3+ consecutive retries each receiving a harsher throttle response | Critical | Kill switch on the tool's retry path, require manual re-enable |

## Related Patterns
- [Tool Max Retry Limit Enforced](./tool-max-retry-limit-enforced.md) - server-side retry ceiling that a wrong local backoff schedule will hit even sooner
- [Batch Total Operations Limit](./batch-total-operations-limit.md) - both involve rolling-window server limits that naive client-side logic doesn't track
- [Request Timeout No Graceful Handling](./request-timeout-no-graceful-handling.md) - retries triggered by timeouts are especially prone to envelope violations if the timeout itself isn't factored into backoff timing
