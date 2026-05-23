# Goal: Production Reliability

Document processing pipelines fail in ways distinct from individual model failures. These are architecture, integration, and trust problems that occur when OCR/IDP systems operate at scale.

## Business Context

- Silent failures propagate bad data to production databases
- Template changes break extraction without alerting
- Review queues overflow when confidence calibration fails

## Failure Patterns

| Failure Pattern | Frequency | Impact |
|-----------------|-----------|--------|
| [Silent Data Errors](failures/silent-data-errors.md) | Very Common | Critical |
| [Cascading Downstream Errors](failures/cascading-errors.md) | Common | Critical |
| [Missing Document Metadata](failures/missing-metadata.md) | Common | High |
| [Layout Signal Loss](failures/layout-signal-loss.md) | Common | High |
| [Template Drift](failures/template-drift.md) | Common | High |
| [Format Diversity](failures/format-diversity.md) | Very Common | High |
| [ERP Integration Errors](failures/erp-integration.md) | Common | High |
| [Batch Timing Failures](failures/batch-timing.md) | Occasional | Medium |
| [Review Queue Overflow](failures/review-queue-overflow.md) | Common | Medium |
| [Accuracy Regression](failures/accuracy-regression.md) | Occasional | High |

## Key Statistics

| Finding | Source |
|---------|--------|
| 88% of businesses report errors in automated data pipelines | Parseur 2026 Survey |
| 30% of invoices fail first processing iteration | Accenture |
| 60-70% automation plateau for legacy OCR | Industry analysis |
| 68% of businesses see errors on >1% of invoices | IOFM |

## Key Metrics

- End-to-end accuracy rate
- Silent failure detection rate
- Mean time to detect regressions
