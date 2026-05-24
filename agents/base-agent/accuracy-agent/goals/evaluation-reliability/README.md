# Goal: Evaluation Reliability

Ensure agent evaluation against golden datasets and expected responses accurately reflects real-world performance. Evaluation failures create false confidence or miss real issues.

## Business Context

- Golden datasets are the ground truth for agent quality
- Evaluation metrics drive development decisions
- False positives waste resources on non-issues
- False negatives let bugs reach production
- Evaluation must match production conditions

## Failure Patterns

| Failure Pattern | Frequency | Impact |
|-----------------|-----------|--------|
| [Golden Data Staleness](failures/golden-data-staleness.md) | Common | High |
| [Evaluation Metric Mismatch](failures/evaluation-metric-mismatch.md) | Common | High |
| [Overfitting to Evaluation](failures/overfitting-to-evaluation.md) | Common | Critical |
| [Golden Data Coverage Gaps](failures/golden-data-coverage-gaps.md) | Very Common | High |
| [Label Noise and Errors](failures/label-noise-and-errors.md) | Common | High |
| [Distribution Shift](failures/distribution-shift.md) | Very Common | Critical |
| [Evaluation Data Leakage](failures/evaluation-data-leakage.md) | Occasional | Critical |
| [Semantic Equivalence Failures](failures/semantic-equivalence-failures.md) | Very Common | Medium |

## Key Statistics

| Finding | Source |
|---------|--------|
| 52% of enterprise AI responses contain fabrications despite passing evals | Enterprise Survey 2026 |
| 30-50% of golden datasets have label quality issues | Data Quality Research |
| Eval-production gap: 15-40% performance drop common | MLOps Research |
| 83% of RAG systems fail on production cases despite passing benchmarks | RAGAS Study |
| Distribution shift causes 40% of model degradation | ML Monitoring Research |

## Key Metrics

- Evaluation-to-production correlation
- Golden data freshness score
- Label quality audit rate
- Coverage vs. production query distribution
- False positive/negative rates in evaluation
