# Model Output Format Instability

## Issue
An agent requests a strictly-formatted response (JSON matching a schema, XML with specific tags, a fixed-width table) and the model complies most of the time, but intermittently deviates — adding prose before the JSON, using a slightly different key name, wrapping output in markdown code fences one call and not the next, or emitting a subtly malformed structure. Because the deviation is intermittent rather than constant, it passes casual testing and only surfaces as parse failures at some rate in production.

**Frequency**: Very Common

**Symptoms**
- Downstream JSON.parse (or equivalent) calls fail on a small but nonzero percentage of otherwise-successful model calls
- The same prompt template, run repeatedly, produces output wrapped in markdown code fences on some calls and raw JSON on others
- Field names or nesting occasionally shift (e.g. `"user_id"` vs `"userId"`, or a field nested one level differently) despite an unchanged schema instruction
- Format compliance rate drops when the requested output is longer, more deeply nested, or the prompt includes competing formatting cues (e.g. a code example in a different format)
- Adding few-shot examples of correctly-formatted output measurably improves but does not eliminate the failure rate

## Root Cause
The model generates output as free-form text token by token; strict format compliance is a learned behavior pattern, not an enforced constraint, unless the calling code uses a constrained-decoding or schema-enforcement feature explicitly. Small variations in prompt phrasing, in the surrounding conversation, or even in the specific tokens sampled at a formatting decision point (opening brace vs. explanatory sentence) can push the model down a slightly different completion path, and standard sampling introduces enough stochasticity that a low but persistent error rate is expected even when the model "knows" the correct format in the vast majority of cases. Longer or more deeply nested target structures compound this because there are more individual formatting decisions where a single deviation breaks the whole structure, and any competing formatting pattern earlier in the context (a markdown-fenced code example, a different schema mentioned in passing) can bias the model toward the wrong pattern for that specific call.

## Example
```
An agent extracts structured order data from customer emails using the
prompt: "Return ONLY a JSON object matching this schema: {order_id: string,
items: [{sku: string, qty: number}], total: number}. No other text."

Across 5,000 production calls:
- 4,850 calls (97%) return clean, schema-matching JSON
- 90 calls (1.8%) wrap the JSON in a ```json code fence despite the
  "no other text" instruction
- 40 calls (0.8%) prepend a sentence like "Here is the extracted order:"
  before the JSON
- 20 calls (0.4%) use "quantity" instead of "qty" in the items array

The pipeline's JSON.parse call throws on the fenced and prefixed
responses (2.6% of traffic), and the schema validator rejects the
key-mismatched ones (0.4%), producing a combined ~3% silent pipeline
failure rate that only surfaces as a spike in a dead-letter queue.
```

## Statistics
| Finding | Context |
|---------|---------|
| Format compliance for JSON output without constrained decoding typically runs in the 95-99% range for simple schemas, dropping to 85-95% for deeply nested or long schemas | Typical range observed across agent pipelines relying on prompt-only formatting instructions |
| Enabling provider-level structured output / constrained decoding features reduces format parse failures by an estimated 90%+ relative to prompt-only instructions | Estimated from comparisons of constrained vs. unconstrained generation modes |
| Few-shot formatting examples reduce but do not eliminate deviation rate, typically improving compliance by 3-8 percentage points over zero-shot instructions alone | Typical range observed in prompt-engineering evaluations |

## Mitigations
1. **Constrained decoding / structured output APIs**: Use the model provider's schema-enforced output mode where available, rather than relying on natural-language formatting instructions alone.
2. **Defensive parsing with fallback extraction**: Strip common wrapper patterns (code fences, leading prose) before parsing, and log/retry rather than hard-failing on the first parse error.
3. **Schema validation with typed error handling**: Validate parsed output against the full schema (not just "is it valid JSON") and route validation failures to an automatic single retry with the error fed back to the model.
4. **Format-stability monitoring**: Track parse/validation failure rate per prompt template in production and treat any upward drift as a signal to revisit the prompt or add constrained decoding.
5. **Minimize competing format cues in context**: Avoid including differently-formatted examples (unrelated code blocks, other schemas) in the same prompt as the target schema, since these measurably increase deviation rate.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| format_parse_failure_rate | Share of model responses that fail JSON/XML parsing or schema validation | Alert if > 1% |
| format_deviation_type_distribution | Breakdown of failure types (fencing, prefix text, key mismatch) | Alert on any new deviation type appearing at > 0.1% |
| retry_success_rate_after_format_failure | Share of format failures resolved by a single automatic retry | Alert if < 90% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Format failure rate spike | format_parse_failure_rate exceeds threshold in a rolling window | Medium | Check for prompt/model version changes, consider enabling constrained decoding |
| Persistent unrecoverable failures | retry_success_rate_after_format_failure drops significantly | High | Escalate to pipeline owner, review prompt template and schema complexity |

## Related Patterns
- [Model Reasoning Inconsistency](./model-reasoning-inconsistency.md) - both describe nondeterministic output variation across logically identical calls, one in structure and one in content
- [Model Instruction Following Decay](./model-instruction-following-decay.md) - format instructions are a specific case of instructions whose adherence can degrade under competing contextual pressure
- [Model Capacity Limits](./model-capacity-limits.md) - deeper/longer target schemas raise the same per-call complexity that drives capacity-related quality drops
