# What Are the Most Common Compliance Validation Failures in AI Agents?

**AI systems fail to detect regulatory violations—TRID timing breaches, APR calculation errors, missing disclosures, fair lending red flags, QM/ATR violations, and HMDA data misreporting—because validation logic often checks fields in isolation without enforcing regulatory thresholds or cross-document timing rules.** Mortgage processing sits at the intersection of federal (Reg Z, RESPA, Fair Housing) and state requirements, where lenders must verify not only that required disclosures exist but also that timing, accuracy, and fairness rules are met; AI-driven automation without compliance guardrails creates silent violations that trigger regulatory findings.

## Key Takeaways

- 6 distinct compliance failure patterns span APR calculations (within 0.125%–0.25% tolerance), TRID timing (business-day calculation, mail-receipt rules, changed-circumstance documentation), fair lending analysis (pricing disparities, exception inconsistency, steering detection), and disclosure completeness (by loan type and state).
- Regulatory violations are not caught by data-extraction accuracy alone: a correctly extracted APR of 5.875% may still violate Reg Z if it's 0.25 percentage points outside tolerance, or a complete disclosure package may still fail if TRID 3-day waiting period is 1 business day short.
- Compliance failures discovered post-closing by regulators (8–18% for loans processed with minimal human review) result in enforcement actions, rescission risk, and investor repurchase demands that dwarf extraction-accuracy remediation costs.
- Fair lending violations require cross-file pattern analysis (pricing variance by census tract, exception consistency, product steering) that single-document validation cannot provide; AI systems analyzing one loan at a time miss systemic discrimination patterns.

## Scope

- **Regulatory timing and calculations** — [trid-timing-violations](failures/trid-timing-violations.md), [apr-calculation-errors](failures/apr-calculation-errors.md), [qm-atr-validation](failures/qm-atr-validation.md). Business-day calculation errors, tolerance violations, irregular payment handling, and points/fees test failures.
- **Disclosure and data-reporting compliance** — [disclosure-document-gaps](failures/disclosure-document-gaps.md), [hmda-data-extraction](failures/hmda-data-extraction.md). Missing required forms by loan type and state, version outdatedness, HMDA field misclassification.
- **Fair lending and discrimination detection** — [fair-lending-red-flags](failures/fair-lending-red-flags.md). Pricing disparities, underwriting inconsistency, product steering, and documentation-burden variations by protected class.

## When Compliance Validation Matters

- A lender is accelerating straight-through processing and needs to know which compliance checks can be automated versus which require human review or third-party verification (IRS transcripts, employer VOE).
- Regulatory examination findings or DOJ/CFPB investigations have exposed pricing disparities or steering patterns, and the lender is designing controls to prevent similar violations in future cohorts.
- A loan origination system is being upgraded to handle new loan types (ARM, reverse, HELOC) with their own disclosure requirements, and QA teams need test cases for all disclosure-completeness and timing scenarios.

## Cross-Pattern Insight

Across all 6 compliance-validation patterns, the recurring gap is the difference between field-level accuracy and rule-level compliance. A disclosure can be extracted perfectly (present in file, correct version, all sections populated) yet still fail compliance if it violated timing requirements or tolerance thresholds. APR can be calculated correctly and still violate Reg Z if it's 0.126 percentage points outside tolerance. HMDA fields can be extracted correctly and still misclassify the transaction (cash-out vs. rate/term refi) due to logic, not data accuracy. Fair lending concerns require cross-file pattern analysis—single-file validation cannot detect steering or pricing disparities that only appear when comparing cohorts by protected-class proxies. The mitigation across all patterns is the same: compliance rules must be encoded as assertions in the system (not just as human-readable guidelines), and violations must gate downstream decisions rather than being flagged as post-hoc audit findings.

## Frequently Asked Questions

### How do business-day calculations differ from calendar-day counts in TRID timing?

TRID defines business days as Monday through Saturday, excluding federal holidays. A document delivered Friday counts the following Monday as business day 1 (not Saturday), and if closing is scheduled for Monday, the 3-business-day requirement is NOT met—closing must move to Thursday. Mail-receipt rules add 3 calendar days to the delivery date before counting business days forward. Many systems use simple calendar-day arithmetic or don't exclude federal holidays, creating timing violations that audits discover post-closing.

### What forces fair lending analysis to compare across multiple loans when each loan is underwritten individually?

Fair lending laws prohibit patterns of discrimination, not isolated disparities. A single loan with a pricing variance of 50 basis points may be defensible (unique compensating factors); the same variance across 20 loans in minority-census-tracts vs. majority-census-tracts is disparate impact. AI systems that validate loans one at a time cannot detect patterns; they need cohort analysis. Steering detection—placing a conventional-eligible borrower into FHA—is also a pattern issue that requires comparing product offers across similar borrowers.

### Can QM safe-harbor protection be assumed if a loan has a 40% DTI?

No. QM requires DTI ≤ 43% for the general QM category, but a 40% DTI loan may still fail QM if points/fees exceed caps (3% for loans ≥$100k), if prohibited features are present (balloon, negative amortization, interest-only >10 years), or if it's an ARM and wasn't underwritten at the maximum-rate scenario. Safe-harbor depends on meeting ALL QM criteria, not one.

### How does HMDA loan-purpose classification differ between rate/term and cash-out refinancing?

HMDA distinguishes them based on loan amount: if the new loan exceeds the payoff amount (plus reasonable closing costs) by > 5%, it's coded as cash-out refi (code 32), not rate/term refi (code 31). Many systems extract the amounts correctly but don't apply the comparison logic, resulting in misclassification that triggers resubmission and fair lending risk signals.

## Patterns

| Pattern | Mechanism |
|---|---|
| [TRID Timing Violations](failures/trid-timing-violations.md) | Business-day miscalculation, holiday omission, mail-receipt rule failure, invalid changed-circumstance documentation |
| [APR Calculation Errors](failures/apr-calculation-errors.md) | Finance-charge component omission, tolerance violation (regular 0.125%, irregular 0.25%), prepaid-interest miscalculation |
| [Disclosure Document Gaps](failures/disclosure-document-gaps.md) | Missing required forms by loan type/state, outdated form versions, receipt acknowledgment absent, content incomplete |
| [Fair Lending Red Flags](failures/fair-lending-red-flags.md) | Pricing disparity, underwriting exception inconsistency, steering to higher-cost products, documentation-burden variance by protected class |
| [QM/ATR Validation](failures/qm-atr-validation.md) | DTI limit exceeded, points/fees overage, prohibited features present, ARM not underwritten at max rate, non-QM documentation gap |
| [HMDA Data Extraction](failures/hmda-data-extraction.md) | Census tract geocoding error, loan-purpose misclassification, ethnicity/race extraction failure, action-taken code error, rate-spread miscalculation |

**Total: 6 patterns**

## Related Goals

- [Data Extraction](../data-extraction/) — APR and HMDA field extraction accuracy sits upstream of compliance validation; extraction errors that compliance checks don't catch cascade to regulatory findings.
- [Document Verification](../document-verification/) — disclosure authenticity and completeness checks that verify required documents exist; compliance validation checks their regulatory correctness.
- [Fraud Detection](../fraud-detection/) — steering and discrimination detection overlap with fair lending analysis; fraud patterns often manifest as compliance violations.
