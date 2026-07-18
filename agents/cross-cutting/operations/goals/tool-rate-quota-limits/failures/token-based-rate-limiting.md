# Token-Based Rate Limiting

## Issue
Some tools — especially LLM inference APIs and other usage-metered services — rate-limit by consumed tokens or compute units rather than by raw request count (e.g., "200,000 tokens per minute" instead of "500 requests per minute"). An agent whose rate-limiting logic only tracks how many requests it has sent has no visibility into token consumption, so it can stay well under any request-count budget while still blowing through the token-based limit, especially when individual calls vary wildly in size (a short classification prompt vs. a long document-summarization prompt).

**Frequency**: Common

**Symptoms**
- The agent hits 429s despite sending far fewer requests than any documented request-count limit would suggest is safe
- Failures correlate with the *size* of recent requests (long prompts, large payloads, high max-output-token settings), not their *count*
- A batch of 5 large requests fails while a batch of 50 small requests of the same tool succeeds, even though the small batch sent 10x more requests
- The agent's internal rate-limiter dashboard (if it tracks request count only) shows plenty of headroom at the exact moment the vendor rejects a call for exceeding a token-based limit
- Error messages explicitly reference "tokens per minute" or "compute units exceeded" rather than "requests per minute"

## Root Cause
Token-based rate limiting exists because, for services like LLM inference, the actual backend cost of a call scales with input/output size, not with the number of HTTP requests — so vendors protect their infrastructure by metering the resource that actually matters to them. Agent-side rate-limiting middleware, however, is very often built generically (a simple request counter or token-bucket keyed on call count) because that's the simpler and more broadly applicable implementation, and it's easy to overlook that a specific tool's true constraint is denominated in a completely different unit. Unless someone explicitly wires token/unit accounting into the agent's local rate limiter for that specific tool, the agent has no way to see the constraint that's actually binding.

## Example
```
An agent uses the "LLM-Summarize" tool (limit: 150,000 tokens/minute, no explicit request-count limit) to summarize a queue of documents ranging from 200-word memos to 40-page reports.

The agent's generic rate limiter tracks "requests per minute" and is configured with a conservative cap of 30 requests/minute, well below any request-count limit LLM-Summarize might plausibly have.
For the first hour, the queue consists mostly of short memos (roughly 500 input tokens + 200 output tokens each = ~700 tokens/request). At 30 requests/minute, that's ~21,000 tokens/minute — comfortably under the 150,000 token limit. No failures.
The queue then shifts to a batch of 40-page reports (roughly 25,000 input tokens + 4,000 output tokens each = ~29,000 tokens/request). The agent's request-count limiter still allows up to 30 requests/minute.
At just 6 of these large requests in a minute (well under the 30-request cap), token consumption reaches 174,000 tokens/minute — over the 150,000 token limit — and the 7th request in that window is rejected with a token-based rate-limit error.
The agent's monitoring shows "6/30 requests used this minute" — apparently enormous headroom — while the actual binding constraint (tokens) was already exceeded, producing a confusing failure that looks inconsistent with the agent's own utilization dashboard.
```

## Statistics
| Finding | Context |
|---------|---------|
| Token/unit-based rate limiting is the dominant model for LLM inference APIs and is increasingly used by other usage-metered services (embeddings, transcription-by-duration, image generation-by-resolution) | Common across modern AI-adjacent APIs |
| Agents with request-count-only rate limiters against a token-metered tool see a materially higher 429 rate on workloads with variable-sized payloads compared to workloads with uniform small payloads, even at identical average request counts | Observed in production LLM-integrated agent systems |
| Adding token-aware pacing (estimating token cost per call before sending, tracked against a token-based budget) largely closes the gap between the two workload types' failure rates | Typical outcome of token-aware rate limiter remediation |

## Mitigations
1. **Track consumption in the unit the vendor actually limits**: For any tool that documents a token/unit-based limit, build (or extend) the local rate limiter to accumulate estimated token/unit cost per call, not just call count, and pace against that.
2. **Estimate token cost before sending when possible**: Use a tokenizer or the vendor's own estimation utility to approximate input token count pre-flight, and factor in expected output tokens (via `max_tokens` settings) so the local budget accounts for the full cost of a call before it's made, not just after the fact.
3. **Read actual token usage from response metadata**: Most token-metered APIs return exact consumed-token counts in the response body/headers — use the real reported value to true up the local running total after each call, rather than relying solely on pre-flight estimates which can be off for variable-length outputs.
4. **Don't conflate request-count budgets and token budgets in dashboards**: Surface both metrics separately in monitoring so operators can see which constraint is actually binding at any given moment, instead of a single "requests used" number that hides the real bottleneck.
5. **Batch or truncate variable-size payloads deliberately**: For workloads with highly variable request sizes, consider chunking large inputs or capping max-output-tokens per call so token consumption per request stays more predictable, making the token-based budget easier to pace against.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `tool.tokens_consumed_per_minute` | Running total of tokens/units consumed against the tool's token-based limit | Alert at 85% of the documented per-minute token limit |
| `tool.request_count_vs_token_utilization_gap` | Difference between request-count-based headroom and token-based headroom | Alert if the gap is large (e.g., request utilization under 50% while token utilization is over 90%), signaling the wrong metric is being used for pacing |
| `tool.avg_tokens_per_request` | Rolling average tokens consumed per call | Track trend; a rising average without a corresponding drop in request-rate cap increases 429 risk |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Token limit hit despite low request count | 429 with a token-based error message while request-count utilization is under 50% | Warning | Confirm token-aware pacing is implemented for this tool; add if missing |
| Sustained token budget pressure | `tokens_consumed_per_minute` stays above 85% of limit for 10+ minutes | Warning | Throttle large-payload requests or spread them across a longer window |

## Related Patterns
- [Rate Limit Header Not Honored](./rate-limit-header-not-honored.md) - token-metered APIs often expose token-usage headers that are just as easy to overlook as request-count headers
- [Rolling Window Quota Misunderstanding](./rolling-window-quota-misunderstanding.md) - token-based limits are frequently also rolling-window based, compounding both misunderstandings at once
- [Per-Tool Requests Per Minute Exceeded](./per-tool-requests-per-minute-exceeded.md) - the request-count analog of this pattern; agents need both forms of pacing for tools that meter by token but also cap raw request count
