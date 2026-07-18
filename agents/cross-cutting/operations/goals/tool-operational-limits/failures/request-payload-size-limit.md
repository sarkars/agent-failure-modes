# Request Payload Size Limit

## Issue
Tools commonly cap the total byte size of a single request — a common ceiling is 1MB, 6MB, or 10MB depending on the platform — independent of any per-field or per-item limits. An agent that builds a request body from accumulated context (conversation history, retrieved documents, concatenated tool outputs, embedded file attachments) can exceed this ceiling even when every individual field is reasonable in isolation, because the agent's context-accumulation logic tracks relevance and completeness, not cumulative serialized byte size against the specific tool being called next.

**Frequency**: Very Common

**Symptoms**
- `413 Payload Too Large` or equivalent errors on requests that were assembled from multiple accumulated pieces of context, none individually large
- Failures correlated with how much upstream context the agent has gathered in a session (later calls in a long session fail more often than early ones)
- Requests that include embedded binary or base64-encoded content (images, files) inflating payload size well beyond what the visible text content would suggest
- Retries of an oversized request that fail identically because nothing was trimmed between attempts
- Payload-size failures that don't reproduce in isolated testing, since test cases rarely accumulate the same volume of context as a long-running production session

## Root Cause
Request-size limits are enforced by the receiving server, a load balancer, or an API gateway in front of it, primarily to bound memory allocation and prevent resource-exhaustion attacks. Agents assembling a request body from a growing pool of context (RAG retrieval results, conversation history, prior tool outputs passed forward) typically optimize for completeness and relevance of that context rather than for its serialized size against a specific downstream tool's limit, especially when the same context-assembly code path is reused across many tools with different size ceilings. Base64-encoded binary content is a particularly common driver of unexpected size blowup, since it inflates the underlying bytes by roughly a third and agents often reason about "attaching a file" without accounting for that encoding overhead against a text-oriented size budget.

## Example
```
An agent handling a customer support escalation accumulates context
across a session: the full conversation transcript (40 messages), three
retrieved knowledge-base articles, and a screenshot the customer attached
(a 2.4MB PNG). When it calls a `POST /tickets` endpoint to create a
detailed escalation ticket, it includes the full transcript and articles
in the description field and embeds the screenshot as a base64 data URI
in an `attachments` field. The base64-encoded image alone is ~3.2MB; combined
with the transcript and articles, the total request body is 4.1MB. The
ticketing API enforces a 4MB request size limit and rejects the call with
`413 Request Entity Too Large`. The agent's retry logic retries the
identical payload twice more, failing identically, before falling back to
creating a ticket with a generic "see chat log" placeholder and silently
dropping the screenshot the customer had specifically pointed to as
evidence of the bug.
```

## Statistics
| Finding | Context |
|---------|---------|
| Common request-body size ceilings across web APIs and gateways range from 1MB to 10MB, with many defaulting near 4-6MB | Typical of API gateway and web-framework defaults |
| Base64 encoding inflates binary payload size by approximately 33%, a frequent unaccounted-for contributor to payload-size failures involving file/image attachments | Standard property of base64 encoding |
| Payload-size failures correlate strongly with session length/context accumulation in long-running agent sessions, rarely appearing in short test interactions | Based on typical context-growth patterns in multi-turn agent sessions |

## Mitigations
1. **Track cumulative serialized payload size before submission**: Compute the actual byte size of the fully assembled request body (including base64-encoded attachments) against the target tool's known limit before sending, not after a rejection.
2. **Use reference/upload-then-link patterns for large binary content**: Where the tool supports it, upload attachments via a separate file-upload endpoint and reference them by ID/URL in the main request, rather than embedding base64 data inline.
3. **Trim or summarize accumulated context to fit the budget**: When context (transcripts, retrieved documents) would push a request over the limit, apply a summarization or truncation step targeted at the specific field, prioritizing the most relevant content rather than truncating arbitrarily.
4. **Maintain a per-tool payload-size budget in context-assembly logic**: Since the same context-accumulation code often feeds multiple tools with different limits, parameterize the assembly step by the target tool's specific limit rather than using one shared assumption.
5. **Fail with actionable diagnostics rather than blind retry**: On a 413, log which components of the payload (transcript length, attachment size, article count) contributed most to the total, so remediation (what to trim) is immediately clear instead of requiring manual investigation.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `request.serialized_size_bytes` | Actual byte size of the fully assembled request body before submission | Alert when > 90% of the tool's known size limit |
| `request.payload_rejection_413_count` | Count of requests rejected specifically for exceeding size limit | Alert if > 0 |
| `request.attachment_size_contribution_pct` | Share of total payload size attributable to embedded binary/base64 content | Track to prioritize upload-then-link migration |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Payload size limit exceeded | 413 or equivalent size-limit error received | High | Halt job, trim/offload content per known contributors, resubmit |
| Repeated identical oversized retry | Same payload resubmitted unchanged 2+ times after a 413 | Critical | Disable naive retry, route through size-aware trimming logic |

## Related Patterns
- [Response Payload Size Limit](./response-payload-size-limit.md) - the same size-ceiling concern on the response side rather than the request side
- [Field Length Limit](./field-length-limit.md) - a per-field size constraint that compounds with the overall request-size ceiling
- [Batch Size Limit](./batch-size-limit.md) - a count-based batch cap that often correlates with, but is distinct from, a byte-based payload-size cap
