# What Are the Most Common Production Reliability Problems in Document-Processing AI Agents?

**Production reliability fails when a document-processing pipeline that worked in testing degrades, silently or operationally, once it runs continuously at real-world scale.** A pipeline that scored 97% accuracy in evaluation can drop to 91% after a model update with no automated detection, a vendor can reorder invoice columns without notice and swap every value silently, and a well-formed but structurally wrong extraction can propagate into payment, ERP, and tax systems before anyone notices. Production reliability failures matter precisely because they are not caught by the availability and throughput monitoring most pipelines already have — 88% of businesses still report errors in their data pipelines, with teams spending six or more hours per week fixing "automated" data that looked fine when it shipped.

## Key Takeaways

- 10 patterns cover production reliability, grouped into four mechanisms: silent/undetected accuracy failures, downstream propagation, operational scale bottlenecks, and input-diversity/context gaps.
- Silent failures dominate production reliability: silent-data-errors and format-diversity are both rated Very Common, and the defining trait across accuracy-regression, silent-data-errors, and template-drift is that the pipeline reports success while the output is wrong.
- Legacy OCR pipelines plateau around 60-70% automation because of layout-signal-loss, and up to 30% of invoice requests fail on first iteration due to template incompatibilities — both are documented, quantified ceilings, not anecdotes.
- More than half of AP department work is manual data entry and classification driven by format diversity alone, showing that input heterogeneity — not model capability — is often the largest lever on production automation rate.

## Scope

- **Silent/undetected accuracy failures** — [accuracy-regression](failures/accuracy-regression.md), [silent-data-errors](failures/silent-data-errors.md), [template-drift](failures/template-drift.md). All three describe a pipeline that completes successfully, logs no errors, and produces plausible output while the underlying accuracy or structural correctness has actually degraded — discovered weeks later via audits, business-metric drift, or customer complaints.
- **Downstream propagation** — [erp-integration](failures/erp-integration.md), [cascading-errors](failures/cascading-errors.md). Both describe a single extraction or mapping error trusted uniformly across every downstream system it touches (AP, tax reporting, spend analytics), so a small error at the source becomes a large, multi-system cleanup problem before it's caught.
- **Operational scale bottlenecks** — [review-queue-overflow](failures/review-queue-overflow.md), [batch-timing](failures/batch-timing.md). Both are throughput/ordering problems specific to running at production volume: a review queue that grows faster than reviewer capacity, and batch documents that arrive or process out of logical order (an amendment processed before its original).
- **Input-diversity / context gaps** — [format-diversity](failures/format-diversity.md), [missing-metadata](failures/missing-metadata.md), [layout-signal-loss](failures/layout-signal-loss.md). All three trace accuracy loss back to what the pipeline receives rather than the model itself: heterogeneous vendor formats overwhelming rule-based handling, missing sender/locale context needed to disambiguate genuinely ambiguous fields, and preprocessing that strips structural/layout signal before extraction ever runs.

## When Production Reliability Matters

- A pipeline has passed evaluation/staging benchmarks and is being deployed to run continuously against live, growing document volume from many vendors
- Extracted values feed multiple downstream systems (ERP, AP, tax, analytics) where a single bad value can propagate and require multi-system cleanup once discovered
- Automation rate has plateaued below target (e.g., in the 60-70% band) or a review queue is trending toward SLA violations, both of which are documented signatures of specific, addressable root causes rather than a hard model-capability ceiling

## Cross-Pattern Insight

The dominant fix across all 10 patterns is making silent failure impossible: every mitigation either adds continuous ground-truth sampling in production (accuracy-regression, template-drift), adds a validation gate at the exact point a value would otherwise propagate unchecked (cascading-errors, erp-integration, silent-data-errors), or replaces model-size/prompt investment with context or structure investment (format-diversity, missing-metadata, layout-signal-loss). A second recurring theme is treating production monitoring as a first-class metric on par with latency and uptime — production-sampled accuracy, per-vendor accuracy spread, and queue net-growth-rate all get the same alerting rigor as availability metrics, because every documented production-reliability failure was invisible to standard availability/throughput dashboards. The shared lesson is that a pipeline passing evaluation benchmarks tells you nothing about whether it will stay correct in production without dedicated, continuous, production-specific accuracy instrumentation.

## Frequently Asked Questions

### What's the difference between accuracy-regression and template-drift?
Accuracy-regression is caused by a pipeline-side change — a new model or prompt version deployed by the team running the pipeline. Template-drift is caused by a source-side change — a vendor altering their document layout (reordering columns, renaming a label) without notifying anyone. Both produce the same symptom (silent accuracy degradation with no pipeline error), but the fix differs: regression needs pre-deployment testing and canary comparison, while drift needs template fingerprinting and per-vendor monitoring.

### How do you get past the 60-70% automation plateau common in legacy OCR pipelines?
The layout-signal-loss pattern identifies a preprocessing problem, not a model ceiling: many preprocessing pipelines strip layout information (column boundaries, row groupings, header associations) while "cleaning" a document, flattening a table into unstructured text before extraction ever sees the structure. The fix is making layout-preserving output the default preprocessing format rather than an opt-in, since layout information discarded in preprocessing cannot be recovered downstream regardless of extraction model quality.

### How is a cascading error different from a plain extraction error?
A plain extraction error is wrong at the point of extraction. A cascading error (per the cascading-errors pattern) is an extraction error that gets trusted uniformly across every downstream system it touches — a vendor name misread as "ABC Corp" instead of "ABG Corp" propagates into AP payment routing, spend analytics, and tax reporting simultaneously — so the fix requires a validation gate at every integration boundary, not just one at the extraction step.

### Can better model accuracy alone fix format diversity or missing-metadata failures?
No. The format-diversity pattern's key finding is that more than half of AP work is manual due to format diversity, and its fix is semantic field mapping plus tiered automation by format confidence — not a stronger model. Similarly, missing-metadata's core finding is that context (sender identity, locale, historical vendor conventions) determines output quality more than model size or OCR accuracy alone, since some ambiguities (like a DD/MM vs. MM/DD date) are only resolvable with metadata the document itself doesn't contain.

### What's the fastest way to tell if a review queue overflow is a calibration problem or a capacity problem?
Track queue net-growth-rate against reviewer capacity, not just current queue depth, per the review-queue-overflow pattern — a queue that's growing net-positive will overflow regardless of its current size. If automation rate is well below its calibrated target, the fix is empirically recalibrating confidence thresholds (a calibration problem); if automation rate is at target but volume still exceeds capacity, the fix is adding reviewer capacity or field-level partial automation (a capacity problem).

## Patterns

| Pattern | Mechanism |
|---|---|
| [Accuracy Regression](failures/accuracy-regression.md) | Model/pipeline update silently degrades accuracy with no automated detection |
| [Batch Timing](failures/batch-timing.md) | Documents processed out of logical order (amendment before original) |
| [Cascading Errors](failures/cascading-errors.md) | A single extraction error propagates across multiple trusted downstream systems |
| [ERP Integration](failures/erp-integration.md) | Extraction-to-ERP field mapping breaks silently as either schema changes |
| [Format Diversity](failures/format-diversity.md) | Heterogeneous vendor formats overwhelm rule-based handling; long tail stays manual |
| [Layout Signal Loss](failures/layout-signal-loss.md) | Preprocessing strips structural/layout signal before extraction runs |
| [Missing Metadata](failures/missing-metadata.md) | Absent sender/locale context leaves genuinely ambiguous fields unresolved |
| [Review Queue Overflow](failures/review-queue-overflow.md) | Miscalibrated confidence thresholds route too much volume to human review |
| [Silent Data Errors](failures/silent-data-errors.md) | Well-formed output with wrong structural relationships, no error flagged |
| [Template Drift](failures/template-drift.md) | Vendor changes document layout without notice; positional extraction silently swaps values |

**Total: 10 patterns**

## Related Goals

- [Document Classification](../document-classification/) — version-confusion covers per-document schema selection, versus template-drift's fleet-level monitoring of undetected format changes here
- [Multimodal Reliability](../multimodal-reliability/) — plausible-wrong-outputs and confidence-miscalibration cover the model-level version of the same silent-failure problem that silent-data-errors and accuracy-regression cover at the pipeline level
- [Agentic Orchestration](../agentic-orchestration/) — conflicting-information and error-recovery-errors happen within a single document's processing, versus the fleet-wide, over-time failures in production reliability
