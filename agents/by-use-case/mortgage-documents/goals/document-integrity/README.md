# Document Integrity

> Technical validation of document authenticity, checksums, metadata, and format compliance

## Overview

Beyond content extraction, mortgage documents must pass technical integrity checks. PDF checksums, metadata consistency, embedded font analysis, and format compliance indicate whether documents are authentic or manipulated. This goal covers failures in detecting technical document tampering.

## Integrity Check Types

| Check Type | What It Validates | Fraud It Detects |
|------------|-------------------|------------------|
| PDF Checksum | Document hasn't been modified | Post-creation editing |
| Metadata Analysis | Creation/modification timestamps | Backdating, recent forgery |
| Font Consistency | Embedded fonts match expected | Text replacement |
| Image Analysis | Embedded images authentic | Photo manipulation |
| Format Compliance | Document follows standard format | Template forgery |
| Digital Signature | Cryptographic signature valid | Signature forgery |

## Failure Patterns (8)

| Pattern | Description | Frequency |
|---------|-------------|-----------|
| [PDF Modification Detection](failures/pdf-modification-detection.md) | Missing edits made after document creation | Common |
| [Metadata Timestamp Anomalies](failures/metadata-timestamp-anomalies.md) | Document dates inconsistent with metadata | Occasional |
| [Font Substitution Detection](failures/font-substitution-detection.md) | Altered text uses different fonts than original | Occasional |
| [Image Forensics Failures](failures/image-forensics-failures.md) | Missing manipulated photos or signatures | Occasional |
| [Digital Signature Validation](failures/digital-signature-validation.md) | Invalid or missing cryptographic signatures | Occasional |
| [Barcode Data Mismatch](failures/barcode-data-mismatch.md) | Visible text doesn't match encoded barcode | Common |
| [Document Template Validation](failures/document-template-validation.md) | Document doesn't match expected institution template | Common |
| [Embedded Object Analysis](failures/embedded-object-analysis.md) | Hidden or suspicious embedded objects in PDFs | Rare |

## Document-Specific Integrity Checks

### W-2 Forms
| Check | Expected | Red Flag |
|-------|----------|----------|
| Control number | Sequential | Out of sequence |
| Employer EIN | Verifiable | Unknown/invalid |
| Font | IRS standard | Variable fonts |
| Box calculations | Mathematically consistent | Calculation errors |

### Bank Statements
| Check | Expected | Red Flag |
|-------|----------|----------|
| Institution logo | High resolution, correct placement | Low quality, misaligned |
| Account format | Institution-specific pattern | Generic format |
| Transaction IDs | Sequential within date | Random or missing |
| Balance calculations | Running balance correct | Math errors |

### Pay Stubs
| Check | Expected | Red Flag |
|-------|----------|----------|
| YTD totals | Cumulative from prior stubs | Inconsistent progression |
| Tax withholdings | Proportional to income | Incorrect percentages |
| Employer info | Matches W-2 exactly | Variations |
| Check numbers | Sequential | Gaps or duplicates |

### Tax Returns
| Check | Expected | Red Flag |
|-------|----------|----------|
| DCN/barcode | Present on e-filed | Missing on claimed e-file |
| Signature | Present or "Self-prepared" | Missing entirely |
| Schedule attachments | Referenced schedules present | Missing schedules |
| Math | IRS calculations correct | Arithmetic errors |

## Risk Scoring for Document Integrity

```python
INTEGRITY_RISK_WEIGHTS = {
    "pdf_modified_after_creation": 0.4,
    "metadata_date_mismatch": 0.3,
    "font_inconsistency": 0.35,
    "barcode_text_mismatch": 0.5,  # Critical
    "template_mismatch": 0.25,
    "calculation_error": 0.3,
    "missing_expected_elements": 0.2,
    "digital_signature_invalid": 0.45
}

def calculate_integrity_risk(findings: list) -> float:
    score = sum(INTEGRITY_RISK_WEIGHTS.get(f, 0.1) for f in findings)
    return min(score, 1.0)
```

## References

- [PDF Specification ISO 32000](https://www.iso.org/standard/75839.html)
- [Adobe PDF Security](https://www.adobe.com/security.html)
- [IRS Form Standards](https://www.irs.gov/forms-instructions)
