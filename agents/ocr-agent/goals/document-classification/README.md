# Goal: Document Classification

Correctly identifying document types is essential for applying the right extraction logic. Misclassification cascades into extraction failures.

## Business Context

- Invoices vs. POs need different processing workflows
- Template version determines extraction schema
- Multi-page documents must be grouped correctly

## Failure Patterns

| Failure Pattern | Frequency | Impact |
|-----------------|-----------|--------|
| [Similar Templates](failures/similar-templates.md) | Common | High |
| [Version Confusion](failures/version-confusion.md) | Occasional | High |
| [Page Grouping](failures/page-grouping.md) | Common | High |
| [Embedded Documents](failures/embedded-documents.md) | Occasional | Medium |
| [Blank Pages](failures/blank-pages.md) | Common | Low |
| [Quality Rejection](failures/quality-rejection.md) | Occasional | Medium |

## Key Metrics

- Classification accuracy
- False positive/negative rates by document type
- Multi-page grouping accuracy
