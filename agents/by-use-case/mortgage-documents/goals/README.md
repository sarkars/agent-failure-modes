# Mortgage Documents AI Agent Failures by Goal: 53 Patterns, Causes, and Fixes

**Mortgage Documents AI agents fail in 8 distinct ways, grouped by the goal each failure breaks.** Find the goal that matches what you are seeing, open its list, and use the fix on each pattern page.

## Key Takeaways

- 53 documented patterns across 8 goals; the most documented is [Cross Document Validation](cross-document-validation/) with 10.
- Each pattern page gives the symptoms, an example, the root cause, and mitigations.

## Mortgage Documents Goals

| Goal | When it fails | Patterns |
|---|---|---|
| [AI Model Reliability](ai-model-reliability/) | AI models used in mortgage processing hallucinate values, validate their own outputs in circular loops, and deliver production accuracy far below vendor promises | 3 |
| [Compliance Validation](compliance-validation/) | AI systems fail to detect regulatory violations—TRID timing breaches, APR calculation errors, missing disclosures, fair lending red flags, QM/ATR violations | 6 |
| Cross Document Validation | When multiple sources are compared against each other. | 10 |
| [Data Extraction](data-extraction/) | AI systems fail to extract structured data from mortgage documents accurately because the documents themselves are inconsistent—income appears in multiple formats across tax returns and pay stubs | 10 |
| [Document Integrity](document-integrity/) | AI systems fail to detect document tampering and forgery because technical integrity checks—PDF modification detection, metadata timestamp validation, font-substitution analysis | 8 |
| [Document Verification](document-verification/) | AI systems fail to verify that required documents exist, are authentic, complete,… | 8 |
| [Fraud Detection](fraud-detection/) | AI systems fail to detect mortgage fraud because traditional fraud signals | 7 |
| [Quality Control](quality-control/) | AI systems fail to detect appraisal discrepancies because appraiser reports contain multiple value estimates (adjusted comparable sales, cost approach, income approach) | 1 |

**Total: 53 patterns**

## Frequently Asked Questions

### How much income variance is acceptable across W-2, tax return, and pay stubs?

W-2 Box 1 should reconcile within 5% to tax-return line 1, as the difference is usually just timing (estimated tax amendments, late-year adjustments). See Cross Document Validation.

### How should income from multiple W-2s be handled if an employee had two jobs?

Each W-2 Box 1 should be extracted and summed for total W-2 income. See Data Extraction.

### How can AI detect whether a PDF has been edited after creation?

PDF files contain modification metadata and revision streams. See Document Integrity.

## Related

- [Mortgage Documents overview](../)
- [All agent failure patterns](../../../)
