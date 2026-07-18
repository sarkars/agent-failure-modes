# Error Response Format Inconsistency

## Issue
The same tool returns errors in inconsistent shapes depending on which layer of its stack produces the failure — a structured JSON body with an `error.code` field for application-level validation errors, a bare plain-text string for a load balancer timeout, and a full HTML error page for a gateway-level 502 or a WAF block. An agent's error parser, built to expect one shape (usually the documented JSON structure), successfully handles the cases that match it and silently mishandles or crashes on the rest, because the alternate formats don't fail loudly — they just don't match, and the fallback behavior for a non-match is often to treat the response as a generic unknown failure or, worse, to attempt to parse it as JSON and swallow the resulting exception.

**Frequency**: Very Common

**Symptoms**
- Some tool failures are correctly classified and handled while others of similar underlying severity are logged as unparseable or generic errors
- The agent's error handler occasionally crashes or throws an unhandled parsing exception when a response isn't in the expected JSON shape
- Infrastructure-layer failures (timeouts, gateway errors, WAF blocks) are handled worse than application-layer failures (validation errors) even though both come from the same tool
- Log entries show raw HTML or plain-text fragments that were clearly not meant to be parsed as structured error data
- Retry/escalation decisions differ for functionally similar failures purely because of which layer generated the error response

## Root Cause
A single logical "tool" is usually backed by several infrastructure layers — the application server, a reverse proxy or API gateway, a CDN, a WAF, a load balancer — each of which can independently generate an error response when something goes wrong at its layer, and each uses its own default error format because they're often different pieces of software with no shared contract. The agent's integration is typically built and tested against the application layer's documented JSON error format, since that's what's covered in the API reference, while gateway-level and infrastructure-level failures are edge cases that show up only under real production conditions (timeouts, outages, traffic spikes) and are rarely part of initial integration testing.

## Example
```
An agent calls "InventoryAPI" and its error handler is written to expect
the documented shape: {"error": {"code": "OUT_OF_STOCK", "message": "..."}}.

Under normal application-level failures (item not found, validation
errors), this works correctly and the agent branches on error.code as
designed.

During a traffic spike, InventoryAPI's origin server becomes slow and the
CDN in front of it starts returning its own default 504 Gateway Timeout
page: an HTML document with no error.code field at all. The agent's
parser attempts response.json() on the HTML body, which throws a JSON
decode exception. That exception is caught by a broad try/except that
logs "unknown error, skipping" and moves on — treating a temporary
infrastructure timeout as a silent skip rather than a retryable failure.

Separately, when the WAF in front of InventoryAPI blocks a request it
suspects is automated traffic, it returns a plain-text body: "Access
Denied - Request Blocked". This also fails JSON parsing and falls into
the same silent-skip path, so a WAF block (which might indicate the
agent's traffic pattern needs adjustment) is never surfaced to anyone.
```

## Statistics
| Finding | Context |
|---------|---------|
| Multi-layer infrastructure (CDN, gateway, WAF, load balancer) in front of an API commonly produces error responses in a different format than the application layer's documented API errors | Common architectural pattern for production API deployments |
| A significant share of integration test suites only exercise application-layer documented error formats, not infrastructure-layer failure modes | Common gap in integration test coverage |
| Broad exception handlers around response parsing (catch-and-log-generic) are a frequent root cause of infrastructure-layer failures going unclassified in production | Frequently observed pattern in error-handling code review |

## Mitigations
1. **Content-type-aware parsing before format-specific parsing**: Check the response's `Content-Type` header first and branch parsing logic accordingly (JSON parser for `application/json`, plain-text handling for `text/plain`, HTML-stripping/logging for `text/html`) rather than assuming JSON and catching the resulting exception.
2. **HTTP status code as the primary classification signal**: Use the HTTP status code (5xx vs 4xx, specific codes like 502/504/403) as the first-line classifier for retry/escalation decisions, since it's reliably present even when the body format varies, and treat body parsing as enrichment rather than the primary signal.
3. **Distinct handling paths per infrastructure layer**: Explicitly test against and handle the error formats produced by each layer in front of the tool (gateway timeouts, WAF blocks, CDN errors), not just the application's documented API error shape, as part of integration testing.
4. **Never silently swallow parse failures**: Replace broad catch-and-skip exception handling around response parsing with explicit handling that logs the raw response at a visible severity and defaults to a conservative, retryable classification rather than silently ignoring the failure.
5. **Error format telemetry**: Track the distribution of response content-types/shapes received from each tool over time, so a shift toward more unparseable/non-JSON responses (signaling infrastructure issues) is visible before it causes downstream data loss.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| unparseable_error_response_rate | Percentage of error responses that fail structured (JSON) parsing | Alert if > 2% of total error responses |
| silent_skip_rate | Rate of tool failures that fall into a generic catch-and-skip handling path | Alert if > 1% of total calls |
| error_format_distribution | Breakdown of error response content-types/shapes observed per tool | Alert on a new dominant format not previously seen |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Spike in unparseable errors | unparseable_error_response_rate exceeds 2% in a rolling window | High | Inspect raw response samples, add explicit handling for the new format, check for infrastructure-layer changes |
| Silent skip path triggered | Any call falls into a generic catch-and-skip error handler | Medium | Log full raw response, route to review queue instead of silent skip |

## Related Patterns
- [Error Code Semantic Drift](./error-code-semantic-drift.md) - both involve the agent's error-handling assumptions about vendor error shape/meaning silently breaking without any explicit versioned change
