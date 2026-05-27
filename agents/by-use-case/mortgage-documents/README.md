# Mortgage Documents OCR

Failure patterns specific to mortgage document processing, including loan applications, income verification, property documents, and compliance requirements.

## Goals

| Goal | Patterns |
|------|----------|
| [Document Verification](goals/document-verification/) | 8 |
| [Data Extraction](goals/data-extraction/) | 10 |
| [Compliance Validation](goals/compliance-validation/) | 6 |

**Total: 24 patterns**

## Why Mortgage Documents?

Mortgage document processing has unique failure modes:

- **High-stakes accuracy**: Errors can delay closings or cause compliance violations
- **Multi-document correlation**: Income, assets, employment must align across documents
- **Regulatory requirements**: TRID, RESPA, fair lending compliance
- **Fraud detection**: Altered documents, misrepresented income
- **Document variety**: W-2s, tax returns, bank statements, appraisals, titles

## Cross-References

- [Document Processing](../../by-capability/document-processing/) - General OCR patterns
- [Knowledge Retrieval](../../by-capability/knowledge-retrieval/) - RAG for mortgage guidelines
- [Cross-Cutting Security](../../cross-cutting/security/) - PII handling in financial docs
