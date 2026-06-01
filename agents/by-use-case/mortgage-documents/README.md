# Mortgage Documents OCR

Failure patterns specific to mortgage document processing, including loan applications, income verification, property documents, fraud detection, quality control, and AI model reliability.

## Goals

| Goal | Description | Patterns |
|------|-------------|----------|
| [Document Verification](goals/document-verification/) | Fraud detection, signatures, authenticity, completeness | 8 |
| [Data Extraction](goals/data-extraction/) | Income, assets, employment, property values | 10 |
| [Compliance Validation](goals/compliance-validation/) | TRID, APR, fair lending, QM/ATR, HMDA | 6 |
| [Fraud Detection](goals/fraud-detection/) | Synthetic identity, AI forgery, deepfakes, behavioral signals | 7 |
| [Quality Control](goals/quality-control/) | GSE defects, repurchase risk, audit failures | 6 |
| [AI Model Reliability](goals/ai-model-reliability/) | Verification collapse, hallucination, vendor accuracy | 7 |
| [Cross-Document Validation](goals/cross-document-validation/) | Name matching, income triangulation, SSN correlation, timeline consistency | 10 |
| [Document Integrity](goals/document-integrity/) | PDF forensics, barcode validation, font analysis, digital signatures | 8 |

**Total: 62 patterns across 8 goals**

## Key Statistics

| Finding | Source |
|---------|--------|
| 48% of mortgage lenders list AI as top tech priority | Industry Survey 2025 |
| FBI logged 12,000+ real estate fraud complaints, $275M losses (2025) | FBI IC3 |
| AI-assisted document forgery rose from 0% to 2% of fakes (2024-2025) | FraudFinder AI |
| Manual mortgage processes have 10-15% defect rates | Industry Analysis |
| 63% of AI-using lenders rely on AI for document classification | Industry Survey |
| Rocket Mortgage's LLM achieves 90% accuracy on extraction | AWS Case Study |

## Why Mortgage Documents?

Mortgage document processing has unique failure modes:

- **High-stakes accuracy**: Errors can delay closings or cause compliance violations
- **Multi-document correlation**: Income, assets, employment must align across documents
- **Cross-document validation**: W-2 must match tax return, pay stubs must align with VOE, names must correlate across timeline
- **Document integrity**: PDF metadata, barcode encoding, font consistency reveal tampering
- **Regulatory requirements**: TRID, RESPA, fair lending compliance
- **Fraud detection**: AI-generated forgeries, synthetic identities, deepfakes
- **Document variety**: W-2s, tax returns, bank statements, appraisals, titles
- **Verification collapse**: AI validating its own outputs without independent verification
- **GSE quality requirements**: 10% audit sampling, 90-day windows, repurchase risk

## The Verification Collapse

> "Decision engines are increasingly 'signing their own homework,' validating the same data they rely on to make decisions. This is the Verification Collapse."
> — National Mortgage Professional, 2026

As AI handles both extraction AND underwriting, the industry faces a systemic risk: speed has outpaced data integrity. [Read more](goals/ai-model-reliability/failures/verification-collapse.md)

## Cross-References

- [Document Processing](../../by-capability/document-processing/) - General OCR patterns
- [Knowledge Retrieval](../../by-capability/knowledge-retrieval/) - RAG for mortgage guidelines
- [Cross-Cutting Security](../../cross-cutting/security/) - PII handling in financial docs

## References

See [REFERENCES.md](../../../REFERENCES.md#mortgage-document-processing) for full source list.
