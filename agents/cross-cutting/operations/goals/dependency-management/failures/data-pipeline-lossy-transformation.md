# Data Pipeline Lossy Transformation

## Issue
An intermediate stage in a data pipeline — a normalization step, a schema-mapping step, a "clean up the data" step written before the agent's needs were fully known — silently drops or truncates fields, coerces types in ways that lose precision, or collapses distinct source values into the same output value. The pipeline continues to run without errors because the transformation is syntactically valid; it is only semantically incomplete, and the agent downstream never learns that information it needed was discarded before it ever saw the data.

**Frequency**: Common

**Symptoms**
- Fields the agent expects to reason over are consistently null, empty, or a default value, even though the source system has real data for them
- Numeric values lose precision (currency amounts rounded to whole units, timestamps truncated to date-only) causing downstream calculation errors
- Two semantically distinct source values map to the same output value after transformation, and the agent cannot distinguish cases it should treat differently
- No transformation-stage errors or warnings are logged, because the code path considers a dropped field a successful, valid transformation
- The gap is only discovered when someone manually compares a source record to its final-stage counterpart

## Root Cause
A transformation stage is written against the schema and use case known at the time, mapping only the fields the original consumer needed and discarding the rest as "noise" to keep the output schema clean and small. Because the transformation succeeds (it produces valid, well-typed output for every input), there is no error signal when a later consumer — often a different team's agent, added months afterward — needs a field that was never carried through. The lossiness is invisible by construction: nothing compares the transform's output information content against its input, so a silent narrowing of the data is indistinguishable from a correct, intentional mapping unless someone inspects both sides.

## Example
```
An order-processing pipeline has a normalization stage that maps raw
checkout events (which include: item_id, unit_price, currency,
discount_code, discount_amount, tax_jurisdiction, tax_amount) into a
simplified "order_summary" schema used by the original consumer, a monthly
reporting dashboard: (item_id, total_price).

total_price is computed as unit_price - discount_amount + tax_amount, and
discount_code, currency, and tax_jurisdiction are dropped because the
dashboard only ever displayed a single blended total per item.

A year later, a customer-support agent is built on top of order_summary to
answer "why was I charged this amount." The agent can see total_price=47.32
but has no discount_code, no tax_jurisdiction, and no breakdown of how the
figure was composed. When a customer disputes a charge, the agent cannot
explain whether the total reflects a promo code, what tax rate applied, or
what currency the original transaction was in -- the transformation stage
discarded exactly the fields the new consumer needs, and there is no
indication in the schema that anything was ever removed.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 40-55% of "missing data" tickets for agents built on existing pipelines trace back to fields dropped by an upstream transform, not absent at the source | Typical range observed in data-quality incident reviews |
| Reconstructing dropped fields after the fact (re-deriving from raw source logs) takes an estimated 5-10x longer than if the transform had preserved them | Estimated from remediation effort tracking |
| Pipelines with schema-diff checks between transform input and output catch an estimated 60-75% of lossy transformations before a new consumer is affected | Reported range across teams using automated schema comparison |

## Mitigations
1. **Preserve-by-default transforms**: Default new transformation stages to passing through all source fields unless explicitly and documentedly excluded, rather than allow-listing only the fields the current consumer needs.
2. **Schema diff auditing**: Automatically compare the field set and value cardinality of a transform's input against its output, flagging any field that is dropped or any many-to-one value collapse for human review.
3. **Raw-event retention**: Retain raw, untransformed source events for a defined retention window alongside the transformed output, so lossy transforms can be corrected retroactively without re-ingesting from the original source system.
4. **Consumer-declared field requirements**: Require new consumers of a shared pipeline stage to declare which fields they need, and validate that declaration against the actual output schema at build/deploy time, not at runtime.
5. **Precision-preserving type mapping**: Use explicit, reviewed type-mapping rules for numeric and temporal fields (fixed-point currency types, full timestamps) rather than default coercions that silently round or truncate.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| transform_field_retention_ratio | Fraction of input fields present (non-null, non-default) in transform output | Alert if < 90% for a newly reviewed transform |
| output_value_cardinality_drop | Ratio of distinct output values to distinct input values for a mapped field | Alert if drop exceeds expected collapse ratio for that field |
| null_default_rate_by_field | Rate at which a downstream-consumed field is null/default in final-stage output | Alert if > 20% for a field a live consumer reads |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| New consumer needs dropped field | A newly deployed consumer declares a dependency on a field absent from an existing transform's output | High | Block deploy, require transform update or raw-source fallback |
| Precision loss detected | Numeric/temporal field shows rounding or truncation beyond declared tolerance | Medium | Review type mapping, backfill affected records if feasible |

## Related Patterns
- [Data Lineage Loss](./data-lineage-loss.md) - lossy transformations often destroy the same fields that would otherwise carry lineage information
- [Data Pipeline Schema Drift](./data-pipeline-schema-drift.md) - schema drift is an unplanned version of the same field-loss risk, driven by upstream change rather than an intentional narrow mapping
- [Integration Impedance Mismatch](./integration-impedance-mismatch.md) - lossy transformation is the pipeline-internal analog of impedance mismatch between two integrated systems' data models
