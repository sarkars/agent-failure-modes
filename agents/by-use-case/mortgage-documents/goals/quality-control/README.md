# Quality Control & Audit

> AI-powered loan quality control, GSE defect detection, and repurchase risk mitigation

## Overview

Mortgage quality control requires identifying defects before loans enter the secondary market. AI-powered QC systems must detect the same issues human auditors find—income miscalculations, appraisal defects, missing documentation—while processing hundreds of loans daily. This goal covers failures specific to automated QC and audit systems.

## Key Statistics

| Finding | Source |
|---------|--------|
| Manual mortgage processes have 10-15% defect rates | Industry Analysis |
| Lenders must audit 10% of closed loans within 90 days | GSE Requirements |
| Top defect categories: appraisal, income, liability calculations | Fannie Mae Q1 2025 |
| AI QC can check 300+ exception triggers per loan | Vendor Analysis |
| Buyback demands trace to predictable defect categories | ICE Mortgage Technology |

## Failure Patterns (6)

| Pattern | Description | Frequency |
|---------|-------------|-----------|
| [Appraisal Data Discrepancies](failures/appraisal-data-discrepancies.md) | Missing appraisal inconsistencies that trigger GSE findings | Common |
| [Income Documentation Gaps](failures/income-documentation-gaps.md) | Failing to validate W-2s, paystubs per DU requirements | Common |
| [Liability Calculation Errors](failures/liability-calculation-errors.md) | Missing DTI miscalculations or improper exclusions | Common |
| [Pre-Funding vs Post-Closing Gap](failures/pre-post-funding-gap.md) | Defects caught post-closing that should have been flagged pre-funding | Occasional |
| [Condition Satisfaction Failures](failures/condition-satisfaction-failures.md) | Incorrectly marking conditions as satisfied | Occasional |
| [Investor Guideline Mismatches](failures/investor-guideline-mismatches.md) | Missing loan characteristics that violate investor requirements | Common |

## Why This Goal Matters

Quality control failures have direct financial consequences:

1. **Repurchase Demands**: A single buyback can erase profits from multiple performing loans. For smaller lenders, repurchases can be devastating.

2. **Regulatory Penalties**: QC failures expose lenders to CFPB, state regulator, and GSE enforcement actions.

3. **Reputation Risk**: High defect rates damage investor relationships and market reputation.

4. **Proactive vs. Reactive**: The shift from reactive QC (post-closing audits) to proactive QC (pre-funding checks) requires AI systems that catch defects before they become buyback demands.

## GSE Quality Requirements

| Requirement | Details |
|-------------|---------|
| Random Sample | 10% of closed loans |
| Audit Timeline | Within 90 days of closing |
| EPD Audits | 100% of early payment default loans (FHA) |
| Defect Reporting | Significant defects require remediation |

## References

- [Fannie Mae: Top Defects Q1 2025](https://singlefamily.fanniemae.com/originating-underwriting/loan-quality/quality-insider/september-2025)
- [ICE: Containing Repurchase Risk](https://mortgagetech.ice.com/blog/containing-repurchase-risk-with-automated-file-audits)
- [Infrrd: AI-Driven Mortgage Audits](https://www.infrrd.ai/blog/ai-driven-mortgage-audits)
- [Servion: Cost of Quality in Mortgage](https://www.myservion.com/blog/coq)
