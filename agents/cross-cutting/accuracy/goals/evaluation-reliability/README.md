# What Are the Most Common Evaluation Reliability Failures in AI Agents?

**Agents pass evaluation on golden datasets but fail systematically in production because the test dataset doesn't represent production's actual distribution, contains stale or mislabeled data, or measures the wrong metrics — the evaluation score doesn't predict real-world performance, creating a false sense of readiness.** These failures are silent: evaluation reports look good, so decision-makers trust the agent to production, where it fails on query types the golden set didn't cover.

## Key Takeaways

- 8 distinct failure patterns affect evaluation validity, grouped into four mechanisms: coverage gaps (golden set underrepresents edge cases, minorities, or new features), distribution shift (production queries differ from test), data quality (labels wrong or outdated), and metric mismatch (evaluation measures the wrong thing).
- Evaluation failures are particularly dangerous because they're invisible to stakeholders until production incidents surface — a 96% evaluation score feels like a pass but can mask 58% actual accuracy on critical use cases that weren't in the golden set.
- The reliable fix is architectural, not model-only: analyze production query distribution before creating golden sets; validate golden-set labels against authoritative sources; track production performance disaggregated by segment (not just overall accuracy); refresh golden data regularly and replace it when production distribution shifts measurably.
- Coverage gaps concentrate in edge cases, rare conditions, minority segments, new features, and adversarial inputs — exactly the scenarios where real-world impact is highest but golden-set representation is lowest.

## Scope

- **Coverage gaps** — [golden-data-coverage-gaps](failures/golden-data-coverage-gaps.md), [golden-data-staleness](failures/golden-data-staleness.md). Test set missing critical scenarios (edge cases, rare conditions, minority segments, new features); agent passes evaluation but fails on untested query types.
- **Distribution shift** — [distribution-shift](failures/distribution-shift.md). Production query distribution diverges from golden-set distribution (seasonal, trend-driven, demographic changes); agent trained on one distribution encounters another.
- **Evaluation data quality** — [label-noise-and-errors](failures/label-noise-and-errors.md), [evaluation-data-leakage](failures/evaluation-data-leakage.md). Golden-set labels are incorrect or were influenced by training data leakage; evaluation score doesn't reflect actual accuracy.
- **Metric mismatch** — [evaluation-metric-mismatch](failures/evaluation-metric-mismatch.md), [overfitting-to-evaluation](failures/overfitting-to-evaluation.md), [semantic-equivalence-failures](failures/semantic-equivalence-failures.md). Evaluation uses the wrong metric, or agent optimizes for the metric instead of the goal; reported score misleads about production readiness.

## When Evaluation Reliability Matters

- Agent handles diverse, changing queries and a golden set created once at the start doesn't grow or update as production distribution evolves
- Golden set is created from convenience samples (most frequent queries, clean examples) rather than systematic sampling across all real-world scenarios
- Multiple user segments, languages, or geographic regions exist and the golden set skews heavily toward one (common in AI safety and fairness concerns)
- A production incident revealed a failure on a query type that should have been in evaluation — indicates evaluation coverage was too narrow

## Cross-Pattern Insight

Across all 8 patterns, the single most reliable mitigation is systematic coverage analysis: before evaluation, analyze production's actual distribution and ensure golden-set composition matches it, with explicit oversampling of high-stakes edge cases, rare conditions, and minority segments. The second universal mitigation is disaggregated performance tracking — report accuracy overall and separately for each segment (language, geography, query type, complexity level) so coverage gaps and distribution shift surface as breakdowns in specific segments rather than being masked by overall-accuracy averages. If evaluation reports only a single aggregate score, the gaps are invisible.

## Frequently Asked Questions

### How does evaluation reliability differ from verification failures?
Evaluation reliability covers testing methodology and golden-data quality — whether the test dataset accurately represents production. Verification failures cover how agents validate their own outputs at runtime. See [Verification](../verification/) for testing approaches; evaluation reliability is the upstream problem that testing approaches should catch.

### Can you fix coverage gaps with a larger dataset?
Larger golden sets help but don't eliminate coverage gaps — a 10,000-example set with poor distribution representation is worse than a 1,000-example set systematically stratified across segments. The issue is composition (coverage of important segments), not just size. A convenience sample scales the bias rather than fixing it.

### Can you fix golden-data staleness by periodically retraining the model?
Retraining helps, but the core issue is golden-set staleness — if the test data is outdated, retraining on outdated production labels propagates the stale distribution into the new model. The fix is to refresh the golden set itself, not just retrain against a stale golden set.

### How do you detect evaluation-metric mismatch?
Disaggregate production performance by the metric you care about and compare against evaluation scores for the same metric. If evaluation reports 94% accuracy but production shows 94% on common queries and 58% on edge cases, the aggregate metric was masking the gap. Watch for divergence between metrics (e.g., precision looks good but recall terrible) that the primary evaluation metric didn't capture.

## Patterns

| Pattern | Mechanism |
|---------|-----------|
| [Distribution Shift](failures/distribution-shift.md) | Production queries differ from golden-set distribution; coverage perfect for old distribution but gaps emerging for new |
| [Evaluation Data Leakage](failures/evaluation-data-leakage.md) | Test data contaminated by training data; evaluation score is optimistic because model saw test examples during training |
| [Evaluation Metric Mismatch](failures/evaluation-metric-mismatch.md) | Evaluation uses wrong metric; high score on metric doesn't predict success on actual production goal |
| [Golden Data Coverage Gaps](failures/golden-data-coverage-gaps.md) | Test set missing critical scenarios (edge cases, rare conditions, minorities); good eval score, poor production performance |
| [Golden Data Staleness](failures/golden-data-staleness.md) | Test data created months ago; production evolved (new features, trend changes, policy updates) but golden set unchanged |
| [Label Noise and Errors](failures/label-noise-and-errors.md) | Golden-set labels incorrect or inconsistently applied; evaluation score reflects label quality, not agent quality |
| [Overfitting to Evaluation](failures/overfitting-to-evaluation.md) | Agent optimizes for evaluation metric rather than production goal; high eval score masks misalignment between metric and actual value |
| [Semantic Equivalence Failures](failures/semantic-equivalence-failures.md) | Metric treats semantically different outputs as equivalent; evaluation score hides quality gaps the metric doesn't capture |

**Total: 8 patterns**

## Related Goals

- [Verification](../verification/) — test-time evaluation methodology and validation approaches that can catch evaluation-reliability gaps
- [Output Accuracy](../output-accuracy/) — hallucination and fabrication issues that evaluation should detect but often misses
- [Reasoning Quality](../reasoning-quality/) — reasoning failures that evaluation metrics may not measure
