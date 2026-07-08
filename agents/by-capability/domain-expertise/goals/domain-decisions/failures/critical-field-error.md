# Critical Field Error

## Issue: Agent extracts wrong amount, date, name, address, account number, or ID.

**Frequency**: Rare but Catastrophic

**Symptoms**
- Field mismatch against source image/database.
- [Add more specific symptoms]

**Root Cause**
Agent extracts wrong amount, date, name, address, account number, or ID.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- [List factors that make this failure more likely]

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| [Test name] | [Input] | [Expected output] | [What indicates failure] |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |

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
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Critical |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
