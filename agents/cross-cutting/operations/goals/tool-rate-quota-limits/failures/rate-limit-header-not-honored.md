# Rate Limit Header Not Honored

## Issue
A tool returns standard or vendor-specific rate-limit headers on every response (e.g., `X-RateLimit-Remaining`, `X-RateLimit-Reset`, `Retry-After`) that would let the agent pace itself proactively and avoid ever hitting a hard rejection — but the agent's HTTP client or tool wrapper doesn't parse or act on them. The agent keeps calling at its own fixed cadence until it eventually gets rejected outright, throwing away information the vendor was actively handing it for free.

**Frequency**: Very Common

**Symptoms**
- The tool's responses consistently include remaining-quota or reset-time headers, visible in raw HTTP logs, but the agent's logic never references them
- The agent hits 429s at unpredictable moments even though the immediately preceding successful response's headers would have shown "1 request remaining" and telegraphed the rejection in advance
- Retry-After values are present on 429 responses but the agent's backoff duration doesn't match them (either much shorter or completely unrelated)
- Adding a debug log of header values shows the agent "knew" it was about to run out of quota several requests before it actually failed
- The failure is entirely preventable using data the tool was already providing — no additional vendor API call or documentation lookup is needed

## Root Cause
Many HTTP client wrappers and tool SDKs used by agents are built to extract only the response body, discarding or never inspecting response headers unless a developer explicitly wires up header parsing. Rate-limit headers are, by convention, metadata rather than part of the primary payload, so unless someone specifically added handling for them, they're invisible to the rest of the agent's logic even though they arrive on literally every response. The gap isn't a lack of information from the vendor — it's a missing plumbing step between "header arrived on the wire" and "agent's pacing logic can see it."

## Example
```
An agent calls the "EmailValidateAPI" tool (limit: 100 requests/minute) to validate a list of 500 email addresses, using a generic HTTP client wrapper that returns only response.json() to calling code.

EmailValidateAPI includes X-RateLimit-Remaining and X-RateLimit-Reset headers on every single response, updated in real time as quota is consumed.
By request 95, X-RateLimit-Remaining has dropped to 5 — clearly visible in the raw response the agent received — but the agent's wrapper only ever returns the parsed validation result, discarding the headers entirely.
Requests 96-100 succeed, using the last of the budget.
Request 101 is rejected with a 429 that also includes Retry-After: 42 — again, present in the response but never read by the agent's retry logic, which instead uses its own hardcoded 5-second backoff.
The agent retries after 5 seconds, well before the actual 42-second reset, and is rejected again — repeating this mismatch several times before finally succeeding, purely because the information needed to pace correctly was discarded at the HTTP client layer rather than being unavailable.
```

## Statistics
| Finding | Context |
|---------|---------|
| Most major and mid-tier APIs (an estimated 70%+ of rate-limited third-party services) include some form of remaining-quota or reset-time header on responses | Common across REST API implementations |
| Agent tool wrappers that only surface parsed response bodies to calling code, discarding headers, are a frequent default in quickly-built integrations | Common in ad-hoc or auto-generated tool connectors |
| Wiring header parsing into an agent's tool-call layer typically eliminates the large majority of "surprise" 429s, since the agent can proactively slow down before hitting the wall instead of reactively recovering after | Typical outcome of header-aware pacing remediation |

## Mitigations
1. **Parse rate-limit headers on every response, not just errors**: Extract remaining-quota and reset-time headers from successful (2xx) responses as well as 429s, since the whole point is to see the limit approaching before it's hit.
2. **Feed header data into a proactive pacing layer**: Use the parsed remaining-quota value to slow down (add delay, reduce concurrency) as it approaches zero, rather than only reacting after a rejection occurs.
3. **Always honor Retry-After exactly when present**: Treat a Retry-After value on a 429 as authoritative and wait at least that long before the next attempt, overriding any generic fixed or exponential backoff default.
4. **Surface headers through the tool-call abstraction layer**: If the agent framework's tool wrapper currently only returns parsed body content to calling logic, extend it to also expose relevant response headers/metadata, so header-aware pacing is possible anywhere the tool is called from.
5. **Log header trends for visibility**: Emit remaining-quota values to metrics/logs on a sample of requests, so operators can see quota depletion trending toward zero well before it becomes a production incident.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `tool.rate_limit_remaining` | Parsed remaining-quota value from the most recent response header | Alert when it drops below 10% of the tool's known limit |
| `tool.header_parsing_coverage_pct` | Percentage of tool-call code paths that actually extract and use rate-limit headers | Alert if below 100% for tools known to return these headers |
| `tool.retry_after_deviation_ms` | Difference between the agent's actual retry delay and the vendor's stated Retry-After value | Alert if deviation exceeds 1 second in either direction |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Header-blind 429 | A 429 occurs and the immediately preceding successful response's headers showed remaining quota below 5 | Warning | Confirm header parsing is wired into the tool wrapper's pacing logic |
| Retry-After ignored | Agent's retry delay deviates significantly from the vendor's Retry-After value on a 429 | Warning | Fix retry logic to read and honor the header directly |

## Related Patterns
- [Adaptive Rate Limiting](./adaptive-rate-limiting.md) - headers are especially valuable (and especially likely to be ignored) when the underlying limit moves dynamically, since they're often the only real-time signal available
- [Rate Limit Grace Period Missing](./rate-limit-grace-period-missing.md) - when headers are honored, they often compensate for a missing grace period by providing an exact wait time instead
- [Token-Based Rate Limiting](./token-based-rate-limiting.md) - some vendors expose token-consumption headers analogous to request-count headers, and the same "not honored" failure applies equally to those
