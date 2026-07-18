# Response Payload Size Limit

## Issue
Tools that return large result sets — search results, exports, list endpoints without server-driven pagination — often cap or silently truncate the response payload above a certain size, and critically, this truncation frequently happens without a clear error or a truncation flag in the response body. An agent that reads such a response, parses whatever JSON or text made it through, and proceeds treats a partial result as the complete answer, leading to decisions, summaries, or downstream actions based on missing data with no indication anything was cut off.

**Frequency**: Common

**Symptoms**
- Parsed responses with an unexpectedly round or suspiciously specific item count (e.g., always exactly 500 or exactly at a byte boundary) regardless of how much data actually exists upstream
- JSON parse errors on large responses where the payload was cut off mid-structure, producing invalid JSON that a lenient parser may partially recover
- Agent-generated summaries or answers that consistently miss records known to exist (e.g., a report always missing the most recent entries, since those often sort last and get truncated)
- No error or warning at the HTTP level (200 OK) despite the body being incomplete, since truncation frequently happens at a proxy or gateway layer between the origin server and the client
- Downstream aggregations (counts, sums, "top N" answers) that are subtly wrong because they were computed over a truncated dataset the agent believed was complete

## Root Cause
Response-size limits exist at multiple layers — the origin application, an API gateway, a load balancer, or even the agent's own HTTP client library — and any of these can truncate or reject an oversized response, often without coordinating a consistent, agent-visible signal across layers. Some layers truncate silently (streaming a response and simply stopping, or capping a buffer) rather than returning an error, particularly older proxies or naive gateway configurations, because truncation-without-error was historically an acceptable behavior for human-consumed content but is actively dangerous for an agent parsing the response as ground truth. Agents rarely validate structural completeness of a response beyond "did it parse as valid JSON," and a response truncated exactly at a valid JSON boundary (e.g., a list where the last complete element happens to fall right at the size limit) parses successfully while still being silently incomplete, so there is no signal at all short of comparing returned count against an expected or independently-verifiable total.

## Example
```
An agent queries a logging platform's search API for all error events in
the last 24 hours to compile an incident summary, expecting roughly
15,000 matching events. The API returns results inline (no pagination
requested) and the response is capped at 10MB by an intermediate API
gateway, which truncates the JSON body mid-stream rather than erroring.
The truncation happens to land after a complete array element, so the
truncated body (missing the closing `]}` of the JSON, which the client's
lenient parser recovers by auto-closing) still parses successfully,
yielding 9,142 of the 15,000 events with no truncation flag anywhere in
the response. The agent summarizes "9,142 errors in the last 24 hours,
dominated by service X" and posts this to an incident channel. The true
count was 15,000, and service Y — whose errors clustered later in the
unsorted result stream, past the truncation point — was actually the
larger contributor, but never appears in the agent's summary.
```

## Statistics
| Finding | Context |
|---------|---------|
| API gateways and proxies commonly impose response-size caps in the 5-25MB range, frequently configured independently of and stricter than the origin application's own limits | Common in multi-layer API gateway/proxy architectures |
| Silent truncation (200 OK with an incomplete body) rather than an explicit error is a common behavior at proxy/gateway layers not purpose-built for API traffic | Structural risk distinguishing this from request-side size limits, which more often reject cleanly |
| Truncated responses that still parse as syntactically valid JSON (due to lenient client-side auto-closing or truncation landing at a clean element boundary) are effectively undetectable without an independent count check | Based on typical streaming-truncation and lenient-parser behavior |

## Mitigations
1. **Always request and verify a total-count field independent of the returned array**: When the API exposes a `total_count` or equivalent separate from the returned items, compare it against the actual number of parsed items and treat a mismatch as an incomplete response requiring pagination, not a valid answer.
2. **Prefer paginated retrieval over unbounded single-response calls**: Explicitly request small pages with a `next_cursor`/offset pattern rather than relying on an endpoint's default (and possibly gateway-truncated) unpaginated response.
3. **Validate response structural integrity, not just parseability**: Check that the response's closing structure (e.g., no missing top-level keys expected by the schema, a terminal `"done": true` marker if the API provides one) is present, since valid-but-incomplete JSON will otherwise pass a naive parse check.
4. **Check response headers for truncation or size-limit signals**: Some gateways add a header (e.g., `X-Truncated: true` or a `Content-Length` mismatch against bytes actually received) — check for these explicitly rather than assuming a 200 status guarantees a complete body.
5. **Cross-validate high-stakes aggregate answers against an independent count query**: For summaries or decisions with real consequences (incident reports, financial rollups), issue a separate lightweight count-only query and compare it to the count of items actually processed before presenting the result as complete.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `response.returned_count_vs_total_count_delta` | Difference between an API's reported total_count and the actual number of items received | Alert if delta > 0 |
| `response.byte_size_vs_known_gateway_limit` | Response body size relative to the known/observed size cap of the tool's response path | Alert when > 90% of the known limit |
| `response.truncation_suspected_rate` | Rate of responses flagged by structural-integrity checks as possibly truncated | Alert if > 0% sustained over 1 hour |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Response truncation detected via count mismatch | returned item count < reported total_count | High | Re-fetch via pagination, flag any already-produced summary/decision for correction |
| Response near known size cap with no pagination used | Unpaginated call returns a body within 10% of the known size limit | Medium | Switch call to paginated retrieval going forward |

## Related Patterns
- [Request Payload Size Limit](./request-payload-size-limit.md) - the same size-ceiling risk on the outbound side of a call rather than the inbound response
- [Field Length Limit](./field-length-limit.md) - a narrower, single-field version of silent truncation that shares the same detection challenge
- [Array Element Limit](./array-element-limit.md) - a request-side array cap that produces an analogous silent-partial-success failure mode
