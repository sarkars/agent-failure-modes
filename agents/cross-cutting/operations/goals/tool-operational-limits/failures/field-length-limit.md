# Field Length Limit

## Issue
Text fields in most APIs have a maximum length — a ticket description capped at 4,000 characters, a product title capped at 200, a commit message capped at 72 characters for the summary line. When an agent generates the content for such a field with an LLM (a summary, a composed message, a generated description), the output length is not guaranteed to respect the target field's limit, since the generation step and the submission step are typically decoupled. The tool either rejects the write outright or, more insidiously, silently truncates the string mid-word or mid-sentence, producing corrupted or nonsensical stored content that the agent has no way of detecting from a success response alone.

**Frequency**: Very Common

**Symptoms**
- Stored records with content that ends abruptly mid-sentence, missing a closing tag, or truncated mid-word
- `400`/`422` validation errors citing max length on fields the agent treats as free-text with no size awareness
- LLM-generated summaries or descriptions that vary in length run-to-run, causing intermittent rather than consistent failures
- Downstream systems (search indexes, notification templates) breaking on malformed truncated content that passed the write step silently
- User-facing garbled text (e.g., a truncated JSON blob stored in a "notes" field, cut off before its closing brace)

## Root Cause
LLM-generated text has no built-in awareness of an arbitrary downstream field's character or byte limit — the model produces content sized to the semantic task ("summarize this in a paragraph"), not to a specific API's schema constraint. Agents that pass generated text directly into a tool call without a length-validation step assume either that the tool will reject cleanly (which not all do) or that the content will "usually" fit (true for typical cases, false at the tail). Silent truncation is especially damaging because it's a common server-side behavior for legacy or defensively-coded APIs that prefer accepting a shortened write over rejecting the request outright, and the agent's response-status check alone cannot distinguish a full write from a truncated one.

## Example
```
An agent auto-generates release notes for a deployment and submits them
to a changelog API's `description` field, documented max length 2,000
characters. The LLM-generated summary, including a bulleted list of six
changes, runs to 2,340 characters. The changelog API silently truncates
any description over 2,000 characters and returns 201 Created. The stored
record ends mid-bullet: "- Fixed a regression in the checkout flow where
users with saved payment methods could see stale pricing when the cart
contained more than". The agent logs success and moves on. The truncated,
grammatically broken changelog entry is published to the public-facing
release page and stays there until a customer flags it as "the weirdest
changelog I've ever read."
```

## Statistics
| Finding | Context |
|---------|---------|
| Text fields with documented max lengths between 255 and 4,000 characters are common across CRM, ticketing, and content-management APIs | Observed pattern across common SaaS API schemas |
| Silent truncation (vs. hard rejection) is a frequent behavior for legacy string fields, particularly ones backed by fixed-width database columns | Common in APIs with database-column-length-derived limits |
| LLM-generated text length variance for "summarize in N sentences"-style prompts is commonly wide enough to cross a fixed character boundary a non-trivial fraction of the time, even when the target length is roughly known | Based on typical output-length variance in unconstrained generation |

## Mitigations
1. **Enforce length limits at generation time, not just submission time**: Pass the target field's max length into the generation prompt or a post-generation truncation/summarization step, and validate the final string length before submission.
2. **Prefer semantic truncation over hard cutoff**: When content must be shortened to fit, truncate at a sentence or word boundary (or re-summarize to a shorter target) rather than hard-cutting at the character limit, which produces broken output.
3. **Detect silent truncation by comparing lengths**: After a write, if the tool's read-back or response echoes the stored value, compare its length to the submitted length; a mismatch indicates undetected truncation occurred.
4. **Maintain a field-length registry per tool/field**: Similar to array and batch limits, keep a lookup of known max lengths per field so validation doesn't rely on rediscovering limits via failed or corrupted writes.
5. **Fail loudly on oversized content rather than trusting the API to reject cleanly**: Since not all APIs hard-reject, validate client-side and refuse to submit content known to exceed the limit, converting a possible silent corruption into a visible, actionable error.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `field_write.length_vs_limit_ratio` | Submitted content length divided by the field's known max length | Alert when ratio > 0.95 |
| `field_write.truncation_detected_count` | Count of writes where read-back length is shorter than submitted length | Alert if > 0 |
| `llm_generation.output_length_variance` | Standard deviation of generated content length for a given field/prompt template | Track to tune prompts toward tighter length control |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Truncated content detected post-write | Read-back content shorter than submitted content for a text field | High | Flag record for manual review/correction, add pre-submission length gate |
| Oversized generation before submission | LLM output exceeds target field's max length prior to write attempt | Medium | Re-summarize or truncate at boundary before retrying submission |

## Related Patterns
- [Array Element Limit](./array-element-limit.md) - the same silent-truncation risk pattern applied to array cardinality instead of string length
- [Request Payload Size Limit](./request-payload-size-limit.md) - a whole-request analogue of a single field's length limit
- [Response Payload Size Limit](./response-payload-size-limit.md) - truncation can also happen on the read side, compounding detection difficulty when both request and response are silently shortened
