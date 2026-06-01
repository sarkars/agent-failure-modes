# Cross-Document Validation

> Verifying data consistency across multiple mortgage documents and borrower profile

## Overview

Mortgage loan files contain 50+ documents with overlapping data points. Names, SSNs, addresses, income figures, and employment details must match across W-2s, tax returns, pay stubs, bank statements, and application forms. Cross-document validation catches inconsistencies that single-document processing misses.

## Key Validation Points

| Data Point | Primary Source | Cross-Reference Sources |
|------------|----------------|------------------------|
| Borrower Name | Application (1003) | W-2, Tax Returns, Bank Statements, Credit Report, Title |
| SSN | Application | W-2, Tax Transcript, Credit Report |
| Income | W-2 Box 1 | Tax Return Line 1, Pay Stubs YTD, VOE |
| Employer | VOE | W-2, Pay Stubs, Tax Return Schedule C |
| Address | Application | Bank Statements, Pay Stubs, Credit Report, Appraisal |
| Assets | Bank Statements | Application, Gift Letters, 401k Statements |

## Failure Patterns (10)

| Pattern | Description | Frequency |
|---------|-------------|-----------|
| [Name Variation Mishandling](failures/name-variation-mishandling.md) | Failing to match legitimate name variations (Jr., middle names) | Common |
| [Name Change Documentation](failures/name-change-documentation.md) | Missing or incorrect handling of legal name changes | Occasional |
| [Income Triangulation Failures](failures/income-triangulation-failures.md) | Income doesn't reconcile across W-2, tax return, pay stubs | Common |
| [SSN Cross-Reference Errors](failures/ssn-cross-reference-errors.md) | SSN mismatches or partial extraction errors across documents | Common |
| [Address History Gaps](failures/address-history-gaps.md) | Address doesn't trace through document timeline | Occasional |
| [Employment Timeline Conflicts](failures/employment-timeline-conflicts.md) | Employment dates don't align across documents | Common |
| [Co-Borrower Data Mixing](failures/co-borrower-data-mixing.md) | Confusing borrower and co-borrower data across documents | Occasional |
| [Asset Source Tracing](failures/asset-source-tracing.md) | Unable to trace assets to legitimate sources | Common |
| [Document Date Correlation](failures/document-date-correlation.md) | Document dates don't align with stated timeline | Occasional |
| [Prior Loan Reference Mismatches](failures/prior-loan-reference-mismatches.md) | Prior loan details don't match credit report | Occasional |

## Risk Scoring Framework

### Data Consistency Risk Score

```
Risk Score = Σ (Inconsistency Weight × Severity Factor)

Inconsistency Weights:
- Name mismatch: 0.3 (high fraud indicator)
- SSN mismatch: 0.5 (critical)
- Income variance >10%: 0.4
- Employment gap: 0.2
- Address mismatch: 0.2
- Date inconsistency: 0.1

Severity Factors:
- Unexplained: 1.0
- Partially explained: 0.5
- Documented exception: 0.1
```

### Risk Thresholds

| Score Range | Risk Level | Action |
|-------------|------------|--------|
| 0.0 - 0.2 | Low | Proceed |
| 0.2 - 0.5 | Medium | Enhanced review |
| 0.5 - 0.8 | High | Senior underwriter review |
| 0.8 - 1.0 | Critical | Fraud investigation |

## Why Cross-Document Validation Matters

Single-document validation misses systemic fraud patterns:
- **Altered documents**: One document changed, others authentic
- **Identity fraud**: Real documents belonging to different people
- **Income inflation**: Pay stubs altered but W-2 authentic
- **Employment fraud**: VOE fake but W-2 from different employer

## References

- [Fannie Mae: Documentation Requirements](https://selling-guide.fanniemae.com/)
- [MISMO Data Standards](https://www.mismo.org/)
- [CFPB: Verification Requirements](https://www.consumerfinance.gov/)
