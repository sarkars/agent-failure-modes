# What Are the Most Common Data Extraction Failures in Mortgage Processing AI?

**AI systems fail to extract structured data from mortgage documents accurately because the documents themselves are inconsistent—income appears in multiple formats across tax returns and pay stubs, property values on appraisals don't match tax assessments, names and addresses vary by document type, and debt obligations hide in footnotes and attachments—resulting in 5–15% field-level extraction errors that cascade through underwriting.** Mortgage documents span tax returns (1040, schedules with small fonts and annotations), pay stubs (varying employer formats), W-2s (multi-copy forms with OCR-resistant color), bank statements (image or PDF with variable layouts), appraisals (scanned from property inspections), and applications (handwritten or typed with inconsistent field placement); extraction failures on income, assets, employment, and property data create downstream calculation errors in debt-to-income, cash-on-hand, and property valuation.

## Key Takeaways

- 10 distinct extraction failure patterns span income calculation (W-2 Box 1 vs. tax-return line 1 reconciliation, YTD pay-stub annualization), assets (bank-statement balance extraction, account-type misclassification, gift-fund source documentation), employment (job-title extraction, employment-date parsing, gap identification), and property/debt (appraisal value extraction, lien-search reconciliation, mortgage-obligation detection).
- Document format variation (printed vs. digital PDFs, handwritten vs. OCR, different employer pay-stub templates, state-specific W-2 variations) causes systematic extraction biases: OCR misreads on low-contrast PDFs, layout-aware parsing fails on non-standard formats, field-order assumptions break on unfamiliar document types.
- Extraction errors are compounded by legitimate data inconsistencies that extraction systems treat as errors (e.g., W-2 income differs from tax-return income due to estimated-tax adjustments; appraisal value differs from purchase price due to market conditions; address varies between mailing and property address).
- The critical extraction fields (income, assets, employment, debt, property value) feed into regulatory calculations (DTI, cash-on-hand, LTV, credit-to-value); a 1–2% extraction error on income cascades to 0.5–1% DTI error, which can flip a loan approval or change pricing by 25–50 basis points.

## Scope

- **Income extraction and calculation** — [income-calculation-errors](failures/income-calculation-errors.md), [tax-return-parsing-errors](failures/tax-return-parsing-errors.md), [w2-form-extraction](failures/w2-form-extraction.md). W-2 Box 1 extraction, tax-return line 1 (for non-employees), YTD pay-stub annualization, self-employment income from Schedule C, commission averaging, and bonus averaging.
- **Asset and liability tracking** — [asset-verification-failures](failures/asset-verification-failures.md), [bank-statement-misreads](failures/bank-statement-misreads.md), [debt-obligation-detection](failures/debt-obligation-detection.md). Bank-balance extraction, account-type classification (liquid vs. non-liquid), gift-fund source documentation, and mortgage-liability detection from closing disclosures or prior lien searches.
- **Identity, employment, and property data** — [name-ssn-mismatches](failures/name-ssn-mismatches.md), [employment-history-gaps](failures/employment-history-gaps.md), [address-standardization-failures](failures/address-standardization.md), [property-value-extraction](failures/property-value-extraction.md). Name/SSN consistency checks, employment-date parsing and gap identification, address standardization and prior-address extraction, and appraised-value extraction from appraisal forms.

## When Data Extraction Matters

- A lender is implementing AI-driven document processing and needs to understand error rates by document type (which are high OCR error rates, which require human validation, which can be automated safely).
- Quality-control audits discover systematic extraction errors (income consistently underestimated by 3–5%, assets classified incorrectly, employment dates off by months) that hint at model or OCR bias rather than random failures.
- A loan-origination system is being upgraded to handle new document types (self-employment documentation, recent immigrant pay stubs in foreign formats, prior-loan histories) and extraction rules need extension.

## Cross-Pattern Insight

Across all 10 data-extraction patterns, the recurring gap is the conflation of extraction errors (OCR misreads, field misidentification, parsing failure) with data inconsistency (legitimate variance across document types). W-2 Box 1 income legitimately differs from tax-return line 1 by 1–3% due to timing differences and adjustments; extraction systems that compare the two and flag variance as an error are creating false positives. Income figures that appear in multiple places on a pay stub (YTD, current, annual projection) require different handling; annualization of YTD income requires month-of-year context that extraction systems often lack. Property values extracted from appraisals may legitimately differ from purchase price due to market variance; LTV calculation requires accurate appraisal extraction, not assumption of purchase-price equivalence. The mitigation requires separation of extraction (field reading) from validation (consistency checking). Extraction systems should be optimized for individual field accuracy and documented confidence; validation systems should know which inconsistencies are legitimate (W-2 vs. tax-return income variance) and which are not (extraction reading "8" as "3" when the OCR confidence is high).

## Frequently Asked Questions

### How should income from multiple W-2s be handled if an employee had two jobs?

Each W-2 Box 1 should be extracted and summed for total W-2 income. Tax-return line 1 represents the same total income (sum of all W-2s + self-employment + other income), so reconciliation should compare total-W-2-income to tax-return line 1, not individual W-2s. If an employee had two jobs in the same year, two W-2s will appear; both should be extracted and summed for underwriting DTI calculation. Pay-stub income should be extracted from the most recent pay stub available (or average of last 2–3 if available), not summed across time periods.

### What causes appraisal values extracted from forms to sometimes not match purchase prices?

Appraisal value and purchase price are independent. Purchase price is what the buyer agreed to pay; appraisal value is what the property is worth according to the appraiser's analysis. A purchase-price discrepancy exists when appraisal < purchase price (appraisal gap); when it exists, the lender typically adjusts the loan-to-value and may change pricing or increase down-payment requirements. Extraction should read appraisal value directly from the appraisal form (usually on the first page, in a box labeled "estimated market value" or "appraised value"), not calculate it from purchase price. LTV should then be calculated as loan-amount / appraised-value, not loan-amount / purchase-price.

### How should employment history gaps be identified and documented?

Employment history should be extracted as a list of (employer, title, start-date, end-date) tuples from employment history sections on applications and from VOE documents. Gaps are identified by comparing end-date of job N to start-date of job N+1; gaps >60 days should be flagged and documented with written explanation from the borrower. Gaps <30 days are typical between job changes and don't require explanation. The extraction process should also flag unexplained gaps (no explanation letter, no school/military documentation) for downstream review.

### Can bank-statement balances be used to determine liquid asset availability, or must they be further filtered?

Bank-statement balances should be extracted but require further filtering. Liquid assets include cash, checking, and savings accounts. Non-liquid assets include IRAs, 401(k)s, stocks, bonds (which require time to liquidate). Checking and savings balances are liquid if they're not restricted (no court order, no HOA lien, no pledge as collateral for other loans); extraction should identify the account type and note any visible restrictions. Gift-fund deposits in the bank statement must be documented with a gift letter from the donor; extraction should flag deposits near down-payment time for gift-letter verification.

### How should debt obligations be extracted from multiple sources?

Debt obligations should be extracted from three sources: (1) credit report (most authoritative; lists all credit accounts), (2) closing disclosure or prior mortgage documents (for existing loans), and (3) borrower's own disclosure on the 1003 application. Extraction should reconcile these sources; undisclosed debts on the credit report are high-risk (intentional omission vs. clerical error). Each debt should be extracted as (account-type, balance, monthly-payment, term) and validated against credit-report amounts. Paid-off accounts should be extracted as $0 balance but retained in the history for employment timeline context.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Income Calculation Errors](failures/income-calculation-errors.md) | W-2 annualization, YTD pay-stub annualization bias, self-employment income averaging, commission/bonus handling, seasonal income interpretation |
| [Asset Verification Failures](failures/asset-verification-failures.md) | Bank-balance extraction, account-type misclassification (liquid vs. retirement), gifted-down-payment source undocumented, asset value extraction from statements |
| [Employment History Gaps](failures/employment-history-gaps.md) | Gap identification >60 days, employment-date extraction (start/end), employer-name variation, gap-explanation documentation |
| [Property Value Extraction](failures/property-value-extraction.md) | Appraised-value extraction error, appraisal-date outdatedness, property-address extraction, prior-sale-price confusion |
| [Tax Return Parsing Errors](failures/tax-return-parsing-errors.md) | Form-type variation (1040, 1040-SR, 1040-NR), schedule-extraction errors (Schedule C, Schedule E), income-line misidentification, deduction-line confusion |
| [Bank Statement Misreads](failures/bank-statement-misreads.md) | Balance-extraction error, statement-date misidentification, account-number extraction, transaction-type misclassification |
| [W-2 Form Extraction Failures](failures/w2-form-extraction.md) | Box-1-income extraction OCR error, Box-2-withholding misread, employer-name extraction, state-tax discrepancy |
| [Debt Obligation Detection](failures/debt-obligation-detection.md) | Mortgage-liability not detected (omitted from credit report), lien-amount mismatch, existing-debt undisclosed, HELOC balance overlooked |
| [Name and SSN Mismatches](failures/name-ssn-mismatches.md) | SSN extraction error (digit reversal, partial read), name-variation extraction (maiden name, suffix), OCR confidence on high-risk fields |
| [Address Standardization Failures](failures/address-standardization.md) | Mailing vs. property address confusion, prior-address extraction, address-parsing error (street/city/state/zip), suffix standardization (St. vs. Street) |

**Total: 10 patterns**

## Related Goals

- [Cross-Document Validation](../cross-document-validation/) — data-extraction accuracy feeds into cross-document consistency checks; extraction errors on income, employment, or address propagate as false inconsistencies that validation systems must distinguish from real fraud signals.
- [Compliance Validation](../compliance-validation/) — extracted income and asset data feeds into DTI, LTV, and QM calculations; extraction errors cascade to regulatory compliance violations (APR miscalculation, QM violation).
- [AI Model Reliability](../ai-model-reliability/) — extraction hallucination (AI fabricating plausible values) layers on top of extraction-accuracy problems (OCR errors, format parsing failures); both contribute to downstream errors.
