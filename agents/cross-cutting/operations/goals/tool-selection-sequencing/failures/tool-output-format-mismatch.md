# Tool Output Format Mismatch

## Issue
An agent chains the output of one tool directly into the input of another, but the two tools disagree on format — one returns a date as `MM/DD/YYYY` while the next expects ISO-8601, one returns a list under a `results` key while the next expects `items`, one returns plain text while the next expects structured JSON. The agent either passes the mismatched data through unchanged (producing a downstream error or silent misinterpretation) or the LLM performs an ad hoc, occasionally-wrong reformatting step in between.

**Frequency**: Very Common

**Symptoms**
- A downstream tool call fails with a parsing or validation error immediately after consuming another tool's output
- Fields silently arrive empty or null at the downstream tool because the field name or nesting didn't match what it expected
- Numeric or date values are misinterpreted (day/month swapped, string "042" read as octal, currency amount off by a factor of 100 from cents-vs-dollars mismatch) without any error being raised
- The same tool pairing works when a human manually reformats the data between calls but fails when the agent chains them directly
- Errors cluster specifically at hand-off points between tools built by different teams or sourced from different integration vendors

## Root Cause
Tools are typically built and documented independently, each choosing its own reasonable-in-isolation conventions for dates, units, key names, and nesting structure, with no shared schema authority forcing agreement between a tool that produces data and a tool that consumes similar-looking data. An agent chaining tool calls either passes the raw output of tool A directly as an argument to tool B (assuming compatibility that was never verified) or relies on the LLM to eyeball the output and manually construct tool B's arguments, which works when the mismatch is obvious from context but fails silently when both formats are superficially plausible (an amount that could be either cents or dollars, a date that could be either format for ambiguous values like "03/04/2025").

## Example
```
A logistics agent calls get_shipment_status(tracking_id="1Z999AA1")
which returns:
  {"delivery_date": "03/04/2025", "weight": 2.5, "weight_unit": "kg"}

It then calls file_customs_declaration(), which expects:
  {"delivery_date": "2025-04-03", "weight_grams": <int>}

The agent's tool-chaining logic passes delivery_date through with a
naive reformat, but interprets "03/04/2025" as March 4th (US
convention) when the source system that produced it uses day/month
order (European convention), so the true date was April 3rd. It also
converts weight by multiplying 2.5 kg by 1000 correctly to get 2500
grams, but a separate declaration for a different shipment in the same
batch had weight already reported in grams by a different carrier
integration, and the agent applied the same *1000 conversion again,
declaring 2,500,000 grams (2.5 metric tons) for a package that
actually weighs 2.5 kg.

The customs declaration is filed with both an incorrect date and a
grossly incorrect weight, triggering a customs hold and a compliance
review three days later when the physical package's manifested weight
doesn't match the filed declaration.
```

## Statistics
| Finding | Context |
|---------|---------|
| 20-35% of multi-tool chaining failures in production agent workflows are traceable to a format/unit/schema mismatch between adjacent tool calls | Typical range observed in production agent telemetry |
| Silent misinterpretation (wrong value accepted without error) is estimated to be 2-4x more common than a hard parsing failure at format-mismatch points | Estimated from incident review of chained-tool workflows |
| Adding explicit schema adapters between tool pairs reduces chaining-related errors by an estimated 60-85% | Reported range across teams that added dedicated adapter/normalization layers |

## Mitigations
1. **Explicit schema adapters between tools**: Insert a dedicated, tested normalization/adapter step between tool pairs that are commonly chained, rather than relying on the LLM to ad hoc reformat data inline in a single pass.
2. **Canonical internal formats**: Standardize on one date format, one unit system, and one key-naming convention for any data that flows between tools within the agent's own pipeline, converting to/from that canonical form only at the true external boundary of each tool.
3. **Explicit unit/format tagging in tool outputs**: Require tools to self-describe ambiguous fields (e.g. return `{"weight": 2.5, "weight_unit": "kg"}` rather than a bare number, or `{"date": "2025-04-03", "format": "ISO-8601"}`), so downstream consumers don't have to guess.
4. **Schema validation at the hand-off point**: Validate a downstream tool's input against its declared schema before calling it, rejecting and flagging clearly malformed or out-of-range values (a 2.5-million-gram package) rather than passing them through.
5. **Round-trip sanity checks for high-risk chains**: For chains with compliance or financial consequences, add automated plausibility checks (declared weight within an expected range of the shipment's known category) that catch format-mismatch-driven outliers before they're submitted downstream.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| downstream_validation_failure_rate | Rate of downstream tool calls rejected due to malformed/out-of-schema input from an upstream tool | Alert if > 1% |
| chained_call_error_rate_by_pair | Error rate specifically at hand-off points between specific tool pairs | Alert if any pair exceeds 2x the average pair error rate |
| plausibility_outlier_count | Count of values passed downstream that fail a basic sanity/range check | Alert if > 0 for compliance-relevant fields |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Compliance-relevant field fails plausibility check | A chained value (weight, date, currency amount) submitted to a downstream tool falls wildly outside expected range | High | Page on-call, halt the downstream submission, add or fix the schema adapter for that tool pair |
| Elevated chaining error rate for a tool pair | chained_call_error_rate_by_pair exceeds threshold for a specific pair of tools | Medium | Review the two tools' documented schemas for divergence, add an explicit adapter |

## Related Patterns
- [Tool State Dependency Violation](./tool-state-dependency-violation.md) - both are hand-off failures between chained tool calls, one on data format and one on state existence
- [Tool Composition Complexity Explosion](./tool-composition-complexity-explosion.md) - format-mismatch risk compounds as more tool pairs are chained across a larger toolkit
- [Tool Selection Non-Determinism](./tool-selection-non-determinism.md) - inconsistent tool selection across runs can also mean inconsistent output formats feeding the next step
