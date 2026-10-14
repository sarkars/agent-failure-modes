# Mortgage Documents AI Agent Failures by Goal: 53 Patterns, Causes, and Fixes

**Mortgage Documents failures in AI agents are grouped here into 8 goals, each with a catalog of named failure patterns, the symptoms you will see, the root cause, and mitigations you can copy.** Start from the symptom you are debugging, pick the matching goal below, and open its failure list.

## Key Takeaways

- This use case covers 8 goals and 53 documented failure patterns.
- The largest goal is [Cross Document Validation](cross-document-validation/) with 10 patterns.
- Each goal page explains the failure class, how to tell it apart from its neighbors, and which mitigations apply across its patterns.
- Each failure page covers the symptoms, an example, the root cause, and how to fix it.

## Mortgage Documents Goals

| Goal | What goes wrong | Patterns |
|---|---|---|
| [AI Model Reliability](ai-model-reliability/) | AI models used in mortgage processing hallucinate values, validate their own outputs in circular loops, and deliver production accuracy far below vendor promises | 3 |
| [Compliance Validation](compliance-validation/) | AI systems fail to detect regulatory violations—TRID timing breaches, APR calculation errors, missing disclosures, fair lending red flags, QM/ATR violations | 6 |
| [Cross Document Validation](cross-document-validation/) | AI systems fail to validate data consistency across 50+ mortgage documents because single-document processing misses systemic inconsistencies—name variations, SSN mismatches, income triangulation failures, employment timeline conflicts | 10 |
| [Data Extraction](data-extraction/) | AI systems fail to extract structured data from mortgage documents accurately because the documents themselves are inconsistent—income appears in multiple formats across tax returns and pay stubs | 10 |
| [Document Integrity](document-integrity/) | AI systems fail to detect document tampering and forgery because technical integrity checks—PDF modification detection, metadata timestamp validation, font-substitution analysis, barcode-data matching | 8 |
| [Document Verification](document-verification/) | AI systems fail to verify that required documents exist, are authentic, complete, current, and properly signed because verification requires correlating multiple documents against regulatory checklists | 8 |
| [Fraud Detection](fraud-detection/) | AI systems fail to detect mortgage fraud because traditional fraud signals (inconsistent document values, form-field anomalies, missing signatures) are becoming less reliable—AI now generates plausible-but-fake pay stubs, tax returns | 7 |
| [Quality Control](quality-control/) | AI systems fail to detect appraisal discrepancies because appraiser reports contain multiple value estimates (adjusted comparable sales, cost approach, income approach), each with different reconciliation methods | 1 |

**Total: 53 patterns**

## Frequently Asked Questions

### Where do I start if my mortgage documents agent is failing?

Match the symptom to a goal in the table above, then open that goal's page for how to tell its failures apart and where to look first. Each failure page ends in mitigations you can apply directly.

### How are these mortgage documents failure patterns organized?

By goal: the outcome the agent is supposed to achieve. Under each goal, a `failures` folder holds one page per pattern. For the full picture see the [Mortgage Documents overview](../).

## Related

- [Mortgage Documents overview](../)
- [All agent failure patterns](../../../)
