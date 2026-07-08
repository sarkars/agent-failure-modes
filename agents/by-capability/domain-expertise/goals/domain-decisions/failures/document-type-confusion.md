# Document-Type Confusion

## Issue: Agent misclassifies paystub, W-2, bank statement, invoice, policy, etc.

**Frequency**: Common

**Symptoms**
- Wrong extraction schema or workflow applied.
- [Add more specific symptoms]

**Root Cause**
Agent misclassifies paystub, W-2, bank statement, invoice, policy, etc.

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
1. **Document Classifier with Abstain Option**: Train multi-class classifier on document types (paystub, W-2, bank_statement, invoice, policy, etc.). Classifier outputs: predicted_type, confidence_score, top_k_alternatives. If confidence < threshold, abstain (output UNKNOWN). Route ambiguous documents to manual classification.
2. **Document Type Extraction Schema Mapping**: For each document type, maintain extraction schema (fields to extract, field types, validation rules). Classifier determines type → applies schema. Prevent wrong schema application via type mismatch check.
3. **Multi-Signal Document Classification**: Use multiple signals for classification: layout_analysis (headers, sections), OCR_text_patterns (keywords specific to type), visual_features (logos, format markers). Ensemble multiple classifiers, average confidence scores.

### Detection & Response
1. **Classification Accuracy Monitoring**: Monitor classifier accuracy on production documents. Track: correct_classifications, misclassifications, abstentions. Alert if misclassification_rate > threshold. Measure per-document-type performance.
2. **Schema Application Mismatch**: Monitor extraction pipeline. Alert if extraction schema doesn't match actual document type (e.g., W-2 schema applied to bank_statement). Log schema mismatches for investigation.
3. **Extraction Validation Failure**: After extraction using determined type's schema, validate extracted fields. If validation fails (missing required fields, type mismatches), flag as potential misclassification. Log failed extractions.

### Architecture Patterns
1. **Document Type Classification Gate**: Route all documents through classifier before processing. Classifier outputs predicted_type + confidence. Only proceed if confidence > threshold, else escalate to manual classification. Log all classifications.
2. **Document Type Confidence Scoring**: Classifier produces confidence_score for each document type. Store top_3_predictions with scores. For low-confidence predictions, require 2-step verification: classifier + human review or multi-signal ensemble.
3. **Dynamic Classification Model Retraining**: Periodically retrain classifier on recent correctly-classified documents. Measure model drift (has accuracy degraded over time?). Retrain monthly or when drift detected.

### Metrics
1. **document_classification_accuracy_percent**: Target: > 98%; Alert threshold: < 96%; Track: per-document-type accuracy
2. **document_misclassification_rate_percent**: Target: < 1%; Alert if > 2%
3. **abstention_rate_percent**: Target: 2-5%; Baseline; Too high = model lacks confidence
4. **schema_application_error_rate_percent**: Target: < 0.1%; Wrong schema never applied
5. **extraction_validation_failure_rate_percent**: Target: < 0.5%; Indicates potential misclassification

### Alerts
1. **Document Type Misclassification** (P2 - Warning): Condition - document classified with confidence < 0.70 OR wrong schema applied. Action: Flag document for manual reclassification, log for classifier retraining, regenerate extraction.
2. **Classifier Accuracy Degradation** (P2 - Warning): Condition - classification_accuracy drops > 5% month-over-month. Action: Investigate model drift, retrain classifier, audit recent misclassifications.
3. **High Abstention Rate** (P2 - Warning): Condition - abstention_rate > 8% for document type. Action: Investigate classifier confusion, add more training data, consider manual review workflow for type.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | High |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
