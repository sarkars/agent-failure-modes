# Document Processing Agents: Business Goals, Failure Patterns, and Fixes

**Document Processing Agents fail along 14 goals: Cross Document Validation, Data Extraction, Multimodal Reliability carry the most documented failures.** This page maps each goal to the failures that threaten it, so you can decide what to protect first and where the fixes are.

## Key Takeaways

- 99 documented failure patterns across 14 goals. What it does: read, classify, extract, and validate information from documents such as loan files.
- The most documented goal is [Cross Document Validation](../by-use-case/mortgage-documents/goals/cross-document-validation/) with 10 patterns.
- Frequencies below are as recorded on each pattern page. They are not measured rates.
- Business-goal definitions (metric, baseline, owner, what counts as a failure) are not written yet for this agent. Define them before choosing which patterns to prioritize.

## Goals this agent must protect

| Goal | When it fails | Patterns |
|---|---|---|
| [Cross Document Validation](../by-use-case/mortgage-documents/goals/cross-document-validation/) | When multiple sources are compared against each other | 10 |
| [Data Extraction](../by-use-case/mortgage-documents/goals/data-extraction/) | AI systems fail to extract structured data from mortgage documents accurately because the documents themselves are inconsistent—income appears in multiple formats across | 10 |
| [Multimodal Reliability](../by-capability/document-processing/goals/multimodal-reliability/) | When a vision-language model produces a fluent, confident-sounding extraction that isn't actually grounded in what the document shows | 10 |
| [Production Reliability](../by-capability/document-processing/goals/production-reliability/) | When a document-processing pipeline that worked in testing degrades | 10 |
| [Document Integrity](../by-use-case/mortgage-documents/goals/document-integrity/) | AI systems fail to detect document tampering and forgery because technical integrity checks—PDF modification detection | 8 |
| [Document Verification](../by-use-case/mortgage-documents/goals/document-verification/) | AI systems fail to verify that required documents exist, are authentic | 8 |
| [Accurate Text Extraction](../by-capability/document-processing/goals/accurate-text-extraction/) | When OCR or vision-language models misread characters, numbers, or punctuation in a document image | 8 |
| [Fraud Detection](../by-use-case/mortgage-documents/goals/fraud-detection/) | AI systems fail to detect mortgage fraud because traditional fraud signals | 7 |
| [Compliance Validation](../by-use-case/mortgage-documents/goals/compliance-validation/) | AI systems fail to detect regulatory violations—TRID timing breaches | 6 |
| [Agentic Orchestration](../by-capability/document-processing/goals/agentic-orchestration/) | When an agent's document reasoning is sound but the surrounding machinery | 6 |
| [Document Classification](../by-capability/document-processing/goals/document-classification/) | When a pipeline cannot correctly determine what a document is | 6 |
| [Layout Preservation](../by-capability/document-processing/goals/layout-preservation/) | When an agent reads every character correctly but flattens the document's two-dimensional structure into the wrong one-dimensional text stream | 6 |
| [AI Model Reliability](../by-use-case/mortgage-documents/goals/ai-model-reliability/) | AI models used in mortgage processing hallucinate values, validate their own outputs in circular loops | 3 |
| [Quality Control](../by-use-case/mortgage-documents/goals/quality-control/) | AI systems fail to detect appraisal discrepancies because appraiser reports contain multiple value estimates | 1 |

## Failures most often recorded

| Failure | What goes wrong | Recorded frequency |
|---|---|---|
| [OCR Confuses Similar-Looking Characters (0/O, 1/l/I, 5/S)](../by-capability/document-processing/goals/accurate-text-extraction/failures/character-confusion.md) | OCR swaps visually similar characters (0/O, 1/l/I, 5/S, 8/B), so extracted IDs and codes look right but are wrong | Very Common |
| [AI Document Extraction Shows High Confidence on Wrong Answers](../by-capability/document-processing/goals/multimodal-reliability/failures/confidence-miscalibration.md) | Overconfident Wrong Answers — Model Confidence Doesn't Track Accuracy | Very Common |
| [Invoice Automation Breaks on Non-Standard Vendor Formats](../by-capability/document-processing/goals/production-reliability/failures/format-diversity.md) | Document Format Diversity Overwhelms Rule-Based Extraction | Very Common |
| [AI Document Extraction Accuracy Drops in Production vs Benchmarks](../by-capability/document-processing/goals/multimodal-reliability/failures/input-quality-gap.md) | Input Quality Gap — Real Documents Are Messier Than Benchmark Documents | Very Common |
| [OCR Fails on Low-Resolution Scans and Fax Images](../by-capability/document-processing/goals/accurate-text-extraction/failures/low-resolution.md) | Low DPI scans, faxes, and compressed mobile photos produce fragmented, unreadable OCR output | Very Common |
| [AI Document Extraction Silently Returns Plausible but Wrong Values](../by-capability/document-processing/goals/multimodal-reliability/failures/plausible-wrong-outputs.md) | Plausible but Wrong Outputs — Errors That Never Trip an Alarm | Very Common |

## Before you build: define each goal

For every goal in the table, write down: the metric and how you measure its baseline today; the person who owns it; what counts as a failure and how severe it is; who is told when it happens; and when a person takes over. Then use the failures above as your test list.

## Security and governance

Every agent also needs the cross-cutting checks in [security](../cross-cutting/security/), [accuracy](../cross-cutting/accuracy/), [governance](../cross-cutting/governance/), and [operations](../cross-cutting/operations/).

## Frequently Asked Questions

### What fails most often in document processing agents?

The most documented goal is Cross Document Validation (10 patterns). The failures table above lists the ones recorded as most frequent. These are the library's records, not measured rates.

### Where should I start when building document processing agents?

Define your business goals and what counts as failure, then test against the failure patterns for each goal. The section above lists what to write down.

## Related

- [All agents by business goal](./)
