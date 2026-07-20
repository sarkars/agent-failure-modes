# Data Lineage Loss

## Issue
As data moves through a multi-stage pipeline (ingestion, normalization, enrichment, aggregation, and into an agent's context), each stage typically emits only its output, not a record of which input rows or upstream events produced it. When the agent later needs to explain a decision, trace an anomaly back to its source, or honor a downstream correction (a customer disputes a charge derived from a specific transaction), there is no reliable path from the final artifact back to the originating record.

**Frequency**: Common

**Symptoms**
- Agent cannot answer "which source record produced this output" when asked to justify a decision
- Corrections or deletions at the source (a corrected invoice, a retracted sensor reading) never propagate to derived outputs already consumed
- Debugging a bad aggregate requires manually re-running upstream stages with logging added after the fact
- Compliance or audit requests for "show your work" cannot be satisfied because intermediate join/merge keys were dropped
- Duplicate or conflicting values in a downstream table with no way to tell which upstream feed each came from

## Root Cause
Lineage tracking is a cross-cutting concern that no single pipeline stage is individually responsible for, so it is easy for every stage to treat it as someone else's job. Each stage is usually built and owned in isolation, optimized for its own transformation, and stores or forwards only the fields it needs for its output schema. Unless an explicit lineage identifier (a source record ID, batch ID, and transformation version) is threaded through every join, aggregation, and dedup step as a first-class field, it gets dropped the moment a stage performs a many-to-one operation like a join, group-by, or merge, because there is no single "the" source row left to point to.

## Example
```
A pricing agent ingests raw vendor price feeds (feed_id, sku, price, timestamp),
normalizes units, joins against a product catalog, and produces a single
"current_price" table consumed by a customer-facing quoting agent.

The join stage merges rows from three vendor feeds per SKU, keeping only the
lowest price and its timestamp. The vendor_feed_id and raw_price fields are
dropped because the output schema only has columns for sku, price, updated_at.

Two weeks later, Vendor B reports that a batch of prices was corrupted by a
decimal-point bug and issues a correction for feed_id=B-2026-07-03. The
pipeline team wants to identify every current_price row derived even partly
from that batch so they can invalidate stale quotes.

There is no way to answer the question: the join discarded which feed(s)
contributed to each surviving row. The team resorts to re-running the entire
three-week history of joins with ad hoc logging added, taking two days, during
which the quoting agent continues serving prices that may include the
corrupted values.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 50-65% of multi-stage agent data pipelines retain no source-record identifier past the first join or aggregation stage | Typical range observed in pipeline architecture reviews |
| Tracing a single bad output value back to its source without lineage metadata typically takes 4-16x longer than with it | Estimated from incident postmortems involving ad hoc backtracing |
| Pipelines that add explicit lineage IDs report reducing root-cause investigation time by roughly 70-80% | Reported range across teams that retrofitted lineage tracking |

## Mitigations
1. **Immutable lineage ID propagation**: Assign every source record a unique ID at ingestion and require every downstream transform to carry forward the contributing ID(s) as an array field, even through joins and aggregations.
2. **Lineage-aware aggregation functions**: Replace naive group-by/merge operations with variants that emit a `contributing_source_ids` field alongside the aggregate value, so many-to-one steps don't silently collapse traceability.
3. **Schema contract requiring lineage fields**: Make lineage ID fields a mandatory part of every inter-stage schema contract, enforced by schema validation, so a stage cannot ship without forwarding them.
4. **Periodic lineage audits**: Run automated checks that sample final-stage outputs and verify a working backward path to source records exists, flagging any stage that breaks the chain.
5. **Correction propagation hooks**: Build an explicit mechanism for source corrections/retractions to look up and flag all downstream derived records via the lineage ID, rather than relying on manual re-runs.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| lineage_id_coverage_ratio | Fraction of final-stage output rows with a resolvable path back to source record IDs | Alert if < 95% |
| lineage_backtrace_latency | Time taken to resolve a source-record query for a given output row | Alert if > 5s (indicates manual/ad hoc tracing) |
| correction_propagation_lag | Time between a source correction and downstream records being flagged | Alert if > 1 hour |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Lineage chain broken | A pipeline stage ships an output schema without a required lineage ID field | High | Block deploy, require lineage field before merge |
| Unresolved source correction | A source correction/retraction has no matching downstream records after propagation window | Medium | Manually audit affected batch, notify data owner |

## Related Patterns
- [Data Pipeline Lossy Transformation](./data-pipeline-lossy-transformation.md) - lineage loss is often a side effect of the same transforms that silently drop fields
- [Data Pipeline Schema Drift](./data-pipeline-schema-drift.md) - schema changes can silently remove the lineage fields a downstream consumer depended on
- [Data Pipeline Replay Idempotency](./data-pipeline-replay-idempotency.md) - without lineage IDs, replays cannot be scoped to only the affected records
