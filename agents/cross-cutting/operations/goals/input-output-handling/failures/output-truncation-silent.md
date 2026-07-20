# Output Truncation Silent

## Issue
An agent's generated output — a chat completion, a streamed response, or a payload returned from a tool call — gets cut off mid-generation or mid-transmission (hitting a `max_tokens` cap, a proxy timeout, a streaming connection drop, or an intermediate buffer limit), and nothing in the pipeline detects or flags that the content is incomplete. The truncated fragment is syntactically plausible enough (a sentence that just stops, or JSON that's missing its closing braces) that it gets parsed, stored, or displayed as if it were the complete, intended output, rather than triggering a retry or an explicit incompleteness signal.

**Frequency**: Very Common

**Symptoms**
- Stored responses or logs that end mid-sentence, mid-word, or mid-JSON-object with no error recorded anywhere in the pipeline
- Downstream JSON parsers throwing on a subset of records for "unexpected end of input," traceable to generation stopping before the closing delimiter
- API responses whose `finish_reason`/`stop_reason` field says `length` or `max_tokens` rather than `stop`, but where no code path actually checks that field
- User-facing answers that trail off without a clear ending, especially for longer or more detailed requests
- A steady low background rate of "malformed output" that correlates with output length approaching the configured token or size limit, rather than being randomly distributed

## Root Cause
Generation and transmission both have hard boundaries — a token budget set on the completion request, a network buffer or proxy timeout on a streamed response, a maximum response size on a tool's HTTP call — and when the boundary is hit mid-output, the API layer typically returns whatever was produced so far along with a status field indicating the stop was involuntary, rather than raising an exception. Because a truncated string is still a valid string (and often still valid UTF-8, still displayable text), nothing forces the calling code to check the completion-status metadata before treating the content as final; only code that explicitly inspects `finish_reason`, validates JSON completeness, or checks for a closing delimiter will ever notice. Since the majority of generations complete normally, the missing check goes unexercised until a longer-than-usual output or an unlucky network hiccup produces a truncation, at which point the corrupted fragment flows downstream exactly like a complete one.

## Example
```
A support-ticket summarization agent calls the completion API with
max_tokens=500 to generate a structured JSON summary: {"category":
..., "priority": ..., "resolution_steps": [...]}. For a long, complex
ticket, the model's response is cut off partway through the
"resolution_steps" array - finish_reason comes back as "length," but
the ingestion code only checks for a non-empty response body, not the
finish_reason field.

The truncated JSON string (missing its closing "]}") gets written
to the ticket record's summary field via a lenient parser elsewhere
in the pipeline that tolerates minor syntax issues by truncating to
the last valid token, silently dropping the last partial resolution
step with no error.

Weeks later, a support-quality audit finds that a cluster of complex
tickets have summaries missing their final resolution step, with no
corresponding error in any log, because every layer treated the
truncated output as successfully generated and successfully parsed.
```

## Statistics
| Finding | Context |
|---|---|
| A small but persistent share of long-form generations hit configured token/size limits before naturally completing | Typical range observed in production for summarization and structured-extraction tasks with tight max_tokens budgets |
| Most ingestion pipelines that consume LLM output do not check finish_reason/stop_reason before persisting the result | Estimated from code review of typical agent pipelines |
| Truncation-related malformed-output rates rise sharply as requested output length approaches the configured token cap | Typical pattern observed when max_tokens is set close to expected output size rather than with headroom |

## Mitigations
1. **Check completion-status metadata before use**: Always inspect `finish_reason`/`stop_reason` (or the streaming-connection close status) before treating output as complete; treat `length`, `max_tokens`, or an abnormal stream close as a distinct code path from a normal `stop`.
2. **Structural completeness validation**: For structured output (JSON, XML, delimited formats), validate that the payload actually parses and is well-formed before accepting it, rather than using lenient parsers that silently truncate to the last valid token.
3. **Budget headroom and continuation**: Set token/size limits with meaningful headroom above the expected output size, and implement automatic continuation (re-prompting for "the rest") when a legitimate long output is cut off, rather than only detecting the failure after the fact.
4. **Fail loud on truncation**: Route detected truncation to an explicit retry or error state instead of persisting the partial content, so incomplete output never reaches storage or the end user disguised as complete.
5. **End-to-end truncation telemetry**: Emit a metric whenever a completion-status check detects an involuntary stop, broken down by task type, so truncation rate is visible and tied to specific token-budget or timeout configurations rather than discovered via downstream data-quality audits.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| involuntary_stop_rate | Share of completions where finish_reason/stop_reason indicates a non-natural stop (length, timeout, connection drop) | Alert if > 1% of completions for a given task type |
| downstream_parse_failure_rate | Rate of JSON/structured-parse failures on agent-generated output | Alert on any sustained increase correlated with output length |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Truncation rate spike | involuntary_stop_rate exceeds threshold for a task type over a rolling window | High | Increase token/size budget headroom, add continuation logic, audit recent output for corruption |
| Truncated content persisted | A record is detected in storage with a finish_reason of length/timeout that was never retried or flagged | Medium | Backfill/regenerate affected records, add a completeness gate before the persistence step |

## Related Patterns
- [Output Length Not Enforced](./output-length-not-enforced.md) - related but distinct: that pattern is about the agent never being bounded to a downstream limit at all, while this one is about detecting when a bounded generation was cut off mid-stream
- [Context Window Overflow with Silent Truncation](../../memory-safety/failures/context-window-overflow-silent-truncation.md) - the input-side counterpart, where incoming context (not generated output) is silently dropped
- [Truncation Information Loss](../../context-lifecycle/failures/truncation-information-loss.md) - similar silent-loss mechanism applied to conversation history truncation rather than a single generation being cut off
- [Output Format Not Validated](./output-format-not-validated.md) - broader pattern of unchecked output structure, of which unvalidated truncation is one specific cause
