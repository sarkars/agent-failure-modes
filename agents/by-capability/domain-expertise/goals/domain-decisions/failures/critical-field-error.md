# Critical Field Error

## Issue: Agent extracts wrong amount, date, name, address, account number, or ID.

**Frequency**: Rare but Catastrophic

**Symptoms**
- Field mismatch against source image/database.
- Downstream system rejects or silently processes a transposed digit (amount, account number, or date) with no validation catch.
- Manual audit finds extraction confidence was never checked against a threshold before use.

**Root Cause**
Extraction pipelines built primarily for throughput compute a per-field confidence score but don't gate downstream use on it, so a low-quality scan that produces an ambiguous OCR read (a smudged decimal, a transposed digit) proceeds exactly as confidently as a clean one. Because there is no cross-reference against a second, independent source (an accompanying purchase order, a database record) and no format or range validation before the value is used, nothing in the pipeline is positioned to catch a plausible-looking but wrong value — the error only surfaces downstream, after the action it enabled has already occurred.

**Example**
```
Agent extracts a wire transfer amount from a scanned invoice as $15,000 when
the source document actually reads $150,000 — a decimal/comma OCR
misread. The field has no confidence threshold or cross-reference check
against the accompanying purchase order, so the transfer is initiated at the
wrong amount and only caught when the vendor calls asking for the remaining
$135,000.
```

**Contributing Factors**
- Low-quality source scans (skewed, low-resolution, handwritten) increase OCR/extraction error rate.
- No confidence score attached to extracted fields, or confidence score computed but never checked before use.
- No cross-reference against a second source (database record, accompanying document) for high-stakes fields.
- Field formats (amount, date, account number) not validated against expected pattern before downstream use.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Low-quality scan with ambiguous digit | Skewed invoice scan, "$15,000" vs "$150,000" ambiguity | Low confidence triggers manual review, field not auto-used | Agent uses field without flagging low confidence |
| Field format violation | Extracted account number fails checksum | Agent rejects field and escalates | Agent passes invalid field downstream without validation |
| Cross-reference mismatch | Extracted amount conflicts with accompanying PO/database record | Agent flags mismatch, blocks auto-processing | Agent uses extracted value despite conflicting authoritative source |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| critical_field_confidence_check_coverage_percent | 100% | % of critical field extractions where confidence score was computed and checked against threshold before use |
| critical_field_eval_extraction_error_rate_percent | < 0.1% | % of eval test cases where extracted critical field doesn't match ground truth |

---

## Mitigation Strategies

### Prevention
1. **Field-Level Verification with Confidence Scoring**: For critical fields (amount, account_number, date, name), implement verification layer that: extracts field with confidence_score, validates format (amount_format, date_format, etc.), cross-references against source document. Fields below confidence threshold flagged for manual review.
2. **Risk-Aware Field Routing**: Classify fields by risk level (critical=payment_amount, high=customer_name, medium=order_date). Route low-confidence critical fields through escalation workflow. Never use low-confidence critical fields in decisions.
3. **Field Validation Rules**: Define validation rules per field type (amounts must be positive, dates in valid range, account_numbers must match format/checksum). Enforce before using field in downstream logic.

### Detection & Response
1. **Field Mismatch Detection**: Compare extracted fields against source document (image/database). Alert on mismatches. Example: extracted_amount=$500 but source_amount=$5000. Log mismatch type, confidence score, impact.
2. **Cross-Reference Validation**: For critical fields, validate against external systems (customer database, account registry). Example: validate account_number exists in banking system. Flag unvalidatable fields.
3. **Field Extraction Accuracy Audit**: Periodically audit extracted fields (sample 100 extractions/week). Domain expert verifies correctness. Track accuracy by field type and source document type.

### Architecture Patterns
1. **Multi-Field Extraction with Confidence**: Extract all critical fields with confidence scores. Store: field_value, confidence_score, extraction_method, source_location. Use confidence scores for routing decisions.
2. **Field Validation Pipeline**: After extraction, route through validation pipeline that checks: format_validity, cross_reference_check, consistency_check (e.g., amount > 0). Fail on validation error.
3. **Source Traceability**: For each extracted field, maintain link to source location (document_id, page, position). Enable auditors to verify extraction location matches claimed source.

### Metrics
1. **critical_field_extraction_error_rate_percent**: Target: < 0.1%; Alert threshold: > 0.5%; Track: field_type, error_type
2. **field_extraction_accuracy_percent_by_type**: Target: > 99%; Measure: critical, high, medium fields separately
3. **low_confidence_field_escalation_rate_percent**: Target: 2-5%; Baseline; Alert if outside range
4. **field_validation_failure_rate_percent**: Target: < 0.1%; Format/cross-reference failures
5. **field_extraction_audit_agreement_percent**: Target: > 99%; Expert auditors agree with extraction

### Alerts
1. **Critical Field Extraction Error** (P1 - Critical): Condition - critical field mismatch detected (extracted != source). Action: Immediately flag in workflow, route to manual verification, escalate if amount error > threshold.
2. **Low Confidence Field Usage** (P2 - Warning): Condition - field with confidence < threshold used in decision. Action: Alert operator, flag decision for review, potential decision reversal.
3. **Field Validation Failure** (P1 - Critical): Condition - extracted field fails validation checks (format, range, existence). Action: Block field usage, escalate to manual review, investigate extraction quality.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| critical_field_extraction_error_rate_percent | > 0.5% |
| low_confidence_field_escalation_rate_percent | outside 2-5% baseline |
| field_validation_failure_rate_percent | > 0.1% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Critical Field Extraction Error | Critical field mismatch detected (extracted != source) | Critical |
| Low Confidence Field Usage | Field with confidence < threshold used in a decision | Warning |
| Field Validation Failure | Extracted field fails validation checks (format, range, existence) | Critical |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
