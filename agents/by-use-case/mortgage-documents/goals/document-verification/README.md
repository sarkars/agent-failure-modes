# What Are the Most Common Document Verification Failures in Mortgage Processing?

**AI systems fail to verify that required documents exist, are authentic, complete, current, and properly signed because verification requires correlating multiple documents against regulatory checklists, performing manual-review escalations, and maintaining document-type-specific rules that AI systems often treat as generic—resulting in missing disclosures, expired pay stubs, unsigned documents, and altered evidence going undetected.** Mortgage underwriting requires 50–100+ documents (application, pay stubs, W-2s, tax returns, bank statements, employment verification, appraisal, title report, homeowners insurance, etc.), and each loan type, co-borrower scenario, and borrower employment situation requires different document sets; AI systems built to extract and validate content miss the meta-problem of document completeness, recency, and authenticity.

## Key Takeaways

- 8 distinct document-verification patterns span authenticity checks (detecting forged W-2s, fake pay stubs, falsified bank statements), completeness (required documents missing by loan type), signature validation (documents missing required signatures or dated before signing), document staleness (pay stubs >60 days old, outdated employment verification), and correlation failures (document dates don't align, multi-document sets incomplete).
- Document checklists vary by loan type, co-borrower count, employment type, and state; AI systems treating all loans identically miss required-document variations. A conventional conforming loan requires different documents than an FHA loan; a self-employed borrower requires 2 years of tax returns vs. 1 month of pay stubs for W-2 employees; a co-borrower loan requires co-borrower-specific income documentation.
- Fraudulent-document detection (forged W-2s, fake pay stubs, fabricated bank statements) requires document-specific authenticity markers: W-2s have control numbers and EIN formats, bank statements have account-number formats and institution logos, pay stubs have employer-specific layouts. AI systems without document-type-specific rules treat all documents the same and miss institution-specific red flags.
- Document-verification failures discovered post-closing (8–15% of loans) result in missing-document corrections, disclosure re-issuance, and closing delays that increase investor repurchase risk and regulatory scrutiny.

## Scope

- **Authenticity and signature verification** — [document-authenticity-markers](failures/document-authenticity-markers.md), [signature-verification-failures](failures/signature-verification-failures.md), [fraudulent-document-detection](failures/fraudulent-document-detection.md). Document-type-specific authenticity checks (W-2 control numbers, bank statement logos, notarization validation), required-signature presence and dating, forged-document detection.
- **Completeness and dating** — [document-completeness-gaps](failures/document-completeness-gaps.md), [stale-document-detection](failures/stale-document-detection.md), [date-consistency-failures](failures/date-consistency-failures.md). Required-document presence by loan type and borrower scenario, document recency (pay stubs <60 days, employment verification <120 days), document date alignment with loan timeline.
- **Correlation and alteration** — [multi-document-correlation-failures](failures/multi-document-correlation.md), [altered-document-detection](failures/altered-document-detection.md), [title-document-validation](failures/title-document-validation.md), [notarization-validation](failures/notarization-validation.md), [stacking-order-validation](failures/stacking-order-validation.md). Document sets correlating (set completeness), alteration detection (physical or digital tampering), notarization validity, title-document completeness, closing-document ordering.

## When Document Verification Matters

- A lender is expanding loan-product offerings (add FHA, USDA, jumbo, reverse) and needs document-requirement checklists for each product and borrower scenario to prevent missing-document closings.
- Quality-control audits discover a pattern of missing documents or outdated documents in closed loans, and the lender is implementing verification checks to prevent similar issues in future cohorts.
- A document-management system is being upgraded to track document recency, signature status, and completeness by loan type, and verification rules need to be encoded for automated flagging.

## Cross-Pattern Insight

Across all 8 document-verification patterns, the recurring gap is conflating document extraction (did the document exist, was it readable, did we extract the content) with document verification (is the document authentic, is it complete, is it current, does it meet regulatory requirements). An extraction system may successfully extract income from a pay stub without knowing if the pay stub is recent enough (too old = income not current), authentic (forged vs. genuine), or dated correctly (dated before employment start date = invalid). A completeness check requires knowing the loan-type-specific required-document set; AI systems treating all loans identically cannot check completeness. Authenticity checks require document-type-specific rules (W-2 control numbers, notarization validation on HOA documents, signature presence on closing documents). The mitigation requires separating extraction from verification: extraction should produce structured content; verification should overlay loan-type-specific and document-type-specific rules that determine acceptability.

## Frequently Asked Questions

### What makes a W-2 or pay stub "current" for underwriting purposes?

Pay stubs must be dated within 60 days of loan application (most lenders use 60-day standard); older pay stubs indicate income may have changed. W-2s are acceptable even if dated the prior year if current-year pay stubs show continuity of employment and year-to-date income progression. Tax returns must be dated within 2 years for conventional loans, 3 years for FHA/USDA. Exceptions: borrowers on leave of absence (military deployment, medical leave, disability) may use older documents if a leave-of-absence letter explains the gap and confirms return-to-work date. Self-employed borrowers' tax returns may be dated 2+ years back if business continuity is documented.

### How should AI detect forged pay stubs versus legitimate pay stubs from small employers?

Pay stub authenticity checks require employer-specific templates (if the system has templates) and internal consistency (YTD progression, tax withholding proportionality, check number sequencing). Many small employers use generic payroll software templates, so template matching isn't reliable. Better signals: employer phone/address verification (call employer or verify address via business registration), W-2 matching (employer name and EIN must match employer on pay stub), and income progression consistency (YTD totals should increase monotonically with each pay period). Forged pay stubs often have math errors (incorrect YTD totals, incorrect tax withholding percentages), missing elements (no employer contact info, no check number), or suspicious formatting (inconsistent spacing, variable fonts).

### When is a document considered "stale" and no longer usable for underwriting?

Staleness varies by document type. Pay stubs: 60 days. Employment verification letters (VOE): 120 days. Bank statements: 60 days (must show current balances as of application date). Tax returns: 2 years for conventional, 3 years for FHA (current-year returns acceptable if year has ended; prior-year acceptable if current-year not yet filed). Appraisals: 90–120 days depending on market conditions and investor guidelines. Title reports: 30 days before closing (many states require re-title check within 30 days of closing). Credit reports: 120 days. Documents older than the staleness threshold can sometimes be updated (borrower provides more recent pay stub, employer provides updated VOE), but using stale documents without update is a compliance violation.

### What documents require signatures and what indicates a forgery?

Closing documents (promissory note, mortgage/deed of trust, truth-in-lending disclosure, closing disclosure) require borrower signature (and co-borrower if applicable). Notarization requirements vary by state and document type; mortgages typically require notarization in most states. Pay stubs and W-2s do not require borrower signature (they're employer documents). Bank statements do not require borrower signature. Tax returns require signature (or "self-prepared" notation for e-filed returns). Signature forgery is detected by: (1) signature not present on documents requiring signatures, (2) signature date before document date (e.g., signature dated before pay period end), (3) multiple signatures on same document with inconsistent handwriting or digital signatures, (4) notary signature missing or notary not licensed on document-signing date.

### How should multi-document sets be validated for completeness?

Document-set completeness requires a loan-type-specific checklist: conventional conforming requires different documents than FHA, which requires different documents than USDA, jumbo, or portfolio loans. Self-employed borrowers require 2 years of tax returns; W-2 employees require 1 month pay stubs. Co-borrower loans require co-borrower-specific income and asset documentation. The checklist should include required documents (application, pay stubs, W-2s, tax returns, bank statements, employment verification, appraisal, title, homeowners insurance quote) and state-specific documents (transfer tax forms, property disclosure forms, etc.). Gaps should be flagged for collection before underwriting approval. Document sets should be correlated: if a document references another (e.g., appraisal references title report), both should be present.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Document Authenticity Markers](failures/document-authenticity-markers.md) | Missing institutional markers (W-2 control numbers, bank logos), non-standard format layouts, outdated form versions |
| [Signature Verification Failures](failures/signature-verification-failures.md) | Missing required signatures, signature dated after document date, multiple signature inconsistencies, notarization missing |
| [Fraudulent Document Detection](failures/fraudulent-document-detection.md) | Forged W-2s, fake pay stubs, fabricated bank statements detected via format analysis and authenticity checks |
| [Date Consistency Failures](failures/date-consistency-failures.md) | Document dates inconsistent with loan timeline, document dated after closing, signature date before document date |
| [Document Completeness Gaps](failures/document-completeness-gaps.md) | Required documents missing by loan type (FHA vs. conventional), co-borrower documentation absent, state-required documents missing |
| [Stale Document Detection](failures/stale-document-detection.md) | Pay stubs >60 days old, employment verification >120 days old, appraisals >90 days old, outdated credit reports |
| [Multi-Document Correlation Failures](failures/multi-document-correlation.md) | Document sets incomplete (references missing documents), co-borrower sets separate when should be combined, prior-loan documentation absent |
| [Altered Document Detection](failures/altered-document-detection.md) | Physical or digital tampering detected, corrected-field inconsistency, amendment without proper documentation |

**Total: 8 patterns**

## Related Goals

- [Document Integrity](../document-integrity/) — technical integrity checks (PDF modification, metadata, font analysis) that detect forgery and tampering at the file level; document-verification checks authenticity and completeness at the business level.
- [Cross-Document Validation](../cross-document-validation/) — consistency checks across multiple documents (income triangulation, employment alignment); document-verification checks that documents exist and are current.
- [Data Extraction](../data-extraction/) — extraction accuracy depends on document authenticity and recency; extracting from forged or stale documents produces wrong values regardless of extraction quality.
