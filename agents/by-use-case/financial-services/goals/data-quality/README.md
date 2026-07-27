# What Are the Most Common Data Quality Failures in AI Agents?

**Data quality failures in financial systems occur when agents ingest, cleanse, or propagate data containing misattributed entities, stale hierarchies, fabricated values, or unresolved ambiguities—and pass that corrupted data downstream to pricing, risk, or compliance calculations without flagging the corruption.** Most data quality failures are silent: a misread field, a merged entity, or a cached value presents itself as clean data until a downstream reconciliation or a compliance audit discovers the error months later. The core failure is structural—multi-stage cleansing and consuming agents operate on fixed schemas that drop critical provenance and confidence signals at handoff boundaries, leaving downstream systems blind to data-quality warnings that upstream systems actually surfaced.

## Key Takeaways

- 5 distinct failure patterns affect data quality in financial pipelines, spanning entity resolution, hierarchy mapping, missing-data handling, handoff schema gaps, and point-in-time violations.
- Entity resolution errors via embedding similarity over identifiers (LEI, CUSIP) are documented to surface a taxonomy of retrieval errors distinct from generation errors, particularly when two genuinely distinct entities share lexically similar names.
- Multi-agent handoff drops are among the most under-detected data-quality failures: a cleansing agent's free-text confidence note or a hierarchy mismatch never reaches a downstream consuming agent because the handoff schema lacks a structured field for it.
- Point-in-time data violations (backtests using later-restated or later-released information) are one of the most common causes of backtest-to-live performance decay, yet remain among the hardest to catch in automated validation.

## Scope

- **Entity and Hierarchy Resolution** — [corporate-hierarchy-misattribution](failures/corporate-hierarchy-misattribution.md), [embedding-retrieval-merges-similarly-named-issuer-entities](failures/embedding-retrieval-merges-similarly-named-issuer-entities-in-data-cleansing-pipeline.md). Entity deduplication and parent-subsidiary mapping failures where embedding similarity or name-based matching incorrectly merges or splits distinct entities or misattributes exposure.
- **Data Imputation and Gap Handling** — [missing-data-handling](failures/missing-data-mishandling-in-financial-models.md). Naive imputation (mean, forward-fill) or deletion introducing bias, reduced volatility, or survivor bias into time series and fundamental data.
- **Multi-Agent Handoff Gaps** — [multi-agent-handoff-drops-data-quality-flag](failures/multi-agent-handoff-drops-data-quality-flag-between-cleansing-agent-and-downstream-consuming-agent.md). Cleansing agent's free-text confidence or method notes dropped at the schema boundary, leaving downstream agents blind to whether a field is source-confirmed or inferred.
- **Temporal Data Violations** — [point-in-time-data-violations](failures/point-in-time-data-violations.md). Backtests and live recommendations using data (restatements, later-released earnings, retroactive index membership) that was not actually available at decision time.

## When Data Quality Matters

- Cleansed data feeds directly into downstream pricing, risk aggregation, or compliance calculations with no independent verification step
- Data integration spans multiple heterogeneous source feeds with overlapping entity naming conventions or incomplete identifiers
- Backtests or recommendations depend on historical time series where data completeness and point-in-time accuracy materially affect the outcome

## Cross-Pattern Insight

All 5 data-quality patterns share a common root mechanism: data flows through a pipeline where intermediate agents surface findings in free text (confidence notes, discrepancy flags, imputation methods, temporal concerns) but the structured schemas passed between agents omit fields to carry those findings downstream. The fix is architectural: add structured fields for cleansing confidence, hierarchy versioning, imputation method, and point-in-time validity to every handoff schema, backed by mandatory gating that any data failing these checks is flagged for human review before use. Entity resolution via embedding similarity is fixable by indexing on unique identifiers first, then similarity only on the already-matched cohort.

## Frequently Asked Questions

### Can entity deduplication use embedding similarity safely if the embedding is trained on structured attributes instead of names?

Only if the embedding is explicitly weighted toward unique-identifier fields (LEI, CUSIP, ID) and the retrieval is constrained to a set of entities that have already been confirmed to share a common parent or identifier. Name-based embedding matching across a full population of potentially unrelated entities will continue to surface lexically similar but genuinely distinct entities. Unique-identifier matching first, similarity only within the already-matched set, is the only reliable approach.

### What is the difference between missing-data mishandling and point-in-time violations?

Missing-data mishandling is local to a single time series: how to fill a gap when no data point exists (mean imputation, forward-fill, deletion). Point-in-time violations are forward-looking: using data that exists but was not yet known at the decision timestamp (restatements, later-released earnings, retroactive index changes). Both corrupt backtests, but they require different fixes — missing-data needs domain-aware imputation; point-in-time needs temporal labeling and versioning.

### How do you detect multi-agent handoff drops before downstream calculations use corrupted data?

Require every handoff schema to include a required `data_quality_flags` field (an array of issues the upstream agent surfaces), with a mandatory post-handoff validation that any flag in that field triggers downstream review or gating rather than allowing downstream agents to proceed with unreviewed data. Log the field's contents alongside every calculation, so audit can trace missing flags back to the handoff boundary.

### What makes embedding-based entity deduplication fail for issuers with similar names across regions?

Embedding similarity is dominated by shared vocabulary (industry terms, company-name roots), and regional naming conventions (e.g., "Investment Holdings" + region name repeated across unrelated entities) produce high embedding overlap despite distinct identifiers and no corporate relationship. Embedding is a signal for topical relevance, not identity confirmation. Use embedding only after confirming identifier match or documented corporate relationship.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Corporate Hierarchy Misattribution](failures/corporate-hierarchy-misattribution.md) | Risk/exposure attributed to legal entity instead of ultimate parent; hierarchy mapping stale post-M&A |
| [Embedding Retrieval Merges Similarly-Named Issuers](failures/embedding-retrieval-merges-similarly-named-issuer-entities-in-data-cleansing-pipeline.md) | Two distinct issuers merged by name similarity without identifier confirmation; exposure concentrates incorrectly |
| [Missing Data Mishandling](failures/missing-data-mishandling-in-financial-models.md) | Mean imputation reduces volatility; forward-fill introduces lookahead bias; deletion creates survivor bias |
| [Multi-Agent Handoff Drops Data-Quality Flag](failures/multi-agent-handoff-drops-data-quality-flag-between-cleansing-agent-and-downstream-consuming-agent.md) | Cleansing confidence/method in free text not carried to downstream agent's structured input; field treated as reliable |
| [Point-in-Time Data Violations](failures/point-in-time-data-violations.md) | Backtest uses restated/later-released data unavailable at decision time; inflates backtest performance |

**Total: 5 patterns**

## Related Goals

- [Market Data Freshness](../market-data-freshness/) — real-time staleness of prices and corporate actions, distinct from the historical point-in-time accuracy covered here
- [Regulatory Compliance](../regulatory-compliance/) — data quality feeds into compliance rule application; compliance gates must verify data freshness
