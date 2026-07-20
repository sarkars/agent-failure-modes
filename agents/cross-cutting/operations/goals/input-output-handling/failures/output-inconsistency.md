# Output Inconsistency

## Issue
The same logical input, processed by an agent on separate occasions, produces output with a different structure, field set, ordering, or format each time — not because the underlying data changed, but because the generation process itself is nondeterministic and nothing constrains it to produce a stable shape. A consumer that parses the first call's output shape and hardcodes assumptions from it breaks on the next call, even though nothing about the request changed.

**Frequency**: Common

**Symptoms**
- Identical or near-identical requests producing structurally different responses (different field names, different nesting, optional fields sometimes present/absent) across calls
- Downstream parsers that worked correctly in testing failing intermittently in production against the same logical request type
- A/B or regression tests flagging "differences" between two runs that a human reviewer would judge as equivalent in meaning but not in shape
- Integration code full of defensive `.get()`-with-fallback patterns because no single call's output shape can be trusted to repeat
- Support tickets describing "it worked yesterday, now it's broken" for a workflow where nothing was actually changed

## Root Cause
Generative models produce output through a probabilistic sampling process, and unless the calling code constrains that process tightly (a strict schema, a fixed low temperature, explicit formatting instructions reinforced by validation), the model has latitude to express the same underlying content in multiple structurally different ways — sometimes including a field, sometimes omitting it if it judges it "not applicable"; sometimes nesting related data under a subobject, sometimes flattening it. This is compounded when the system prompt or schema description is itself ambiguous about optionality, ordering, or nesting expectations, giving the model no strong signal about which of several valid-seeming shapes to prefer. Because each individual response is usually well-formed on its own terms, the inconsistency doesn't look like an error until it's compared against a different call's output or against a consumer's fixed parsing assumptions.

## Example
```
A customer-support agent generates structured ticket-resolution summaries
consumed by a reporting pipeline expecting:

    { "resolution": string, "category": string, "follow_up_required": bool }

For most tickets the agent returns exactly this shape. For a ticket
where no follow-up is needed, on one run it returns:

    { "resolution": "...", "category": "billing", "follow_up_required": false }

On a structurally identical ticket the following week, it instead omits
the field entirely when it judges follow-up as obviously not applicable:

    { "resolution": "...", "category": "billing" }

The reporting pipeline's aggregation query, written against the
assumption that follow_up_required is always present, treats the missing
field as a parse error for that record and drops it from the weekly
follow-up compliance report. The dashboard silently undercounts total
tickets processed by a small percentage each week, in a way that isn't
visible unless someone reconciles the report's ticket count against the
support system's own count.
```

## Statistics
| Finding | Context |
|---------|---------|
| A meaningful share of "intermittent parsing failure" tickets in agent-backed pipelines trace to output shape drift across calls rather than to a code regression | Typical range observed in pipeline incident triage |
| Enforcing a strict, validated output schema (rejecting and regenerating on any shape deviation) substantially reduces downstream shape-related failures | Reported range across teams that added strict schema enforcement |
| Structural inconsistency rates tend to concentrate on optional/conditional fields rather than uniformly across the whole schema | Common pattern observed in structured-output consistency audits |

## Mitigations
1. **Enforce strict schema conformance, including for optional fields**: Require every schema-defined field to always be present (using null rather than omission for "not applicable" cases) so the shape itself never varies, only the values within it.
2. **Fixed, low-variance generation settings for structured tasks**: Use low or zero sampling temperature and, where available, structured-output/function-calling modes that constrain the model's output space more tightly than free-form prompting.
3. **Explicit shape examples in the prompt/schema description**: Provide the model with one or more concrete examples showing the exact expected shape, including how conditional/optional cases should be represented, rather than describing the shape only in prose.
4. **Validate shape stability as part of regression testing**: Run the same logical input through the agent multiple times in CI and assert that output shape (not necessarily exact values) is stable, catching shape-drift regressions before deployment.
5. **Defensive parsing with explicit shape-mismatch logging**: Even with strict schema enforcement upstream, have downstream consumers log (not silently swallow) any unexpected shape deviation, so drift is caught quickly rather than silently degrading aggregate data quality.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| output_shape_variance_rate | Share of logically-identical or similar requests producing structurally different output shapes | Alert if > 2% |
| downstream_parse_drop_rate | Rate of records silently dropped or defaulted by downstream consumers due to shape mismatch | Alert if > 0.5% |
| optional_field_presence_rate | Presence rate of each optional/conditional field across calls, tracked for unexpected swings | Alert on sudden shift from historical baseline |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Output shape deviation detected | Agent output for a given request type deviates from its established schema shape | Medium | Route to repair/regeneration, log input/output for review |
| Downstream aggregation record drop spike | Reporting/aggregation pipeline drop rate for agent-sourced records rises sharply | High | Reconcile against source-of-truth counts, audit recent output-shape changes |

## Related Patterns
- [Output Format Not Validated](./output-format-not-validated.md) - the underlying enforcement gap that allows shape inconsistency to reach consumers unfiltered
- [Output Ordering Nondeterminism](./output-ordering-nondeterminism.md) - a specific instance of output inconsistency scoped to list/array element ordering
- [Output Hallucination in Structured Format](./output-hallucination-in-structured-format.md) - a related failure where the model fills schema gaps with fabricated content rather than varying the shape itself
