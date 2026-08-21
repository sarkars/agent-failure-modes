# AI Agent Misclassifies a Document Type: Causes and Fixes

## Issue: The agent misclassifies a paystub, W-2, bank statement, invoice, policy, or similar document, so the wrong extraction schema gets applied.

**Frequency**: Common

**Symptoms**
- Wrong extraction schema or workflow applied.
- Required fields for the actual document type come back empty or nonsensical because the wrong schema's field map was used.
- Downstream approval or underwriting decision is based on fields extracted from a misidentified document.

**Root Cause**
The classifier is built to assign a single label per document and has no abstain path, so when it encounters genuinely ambiguous input — a multi-page upload mixing two document types, or two types sharing near-identical layout features — it still forces out a best-guess label rather than flagging uncertainty. Downstream, no validation step checks whether the fields the assumed schema expected actually came back populated and well-formed, so a wrong classification propagates through extraction and into the workflow without anything checking that the applied schema actually matched the content it was applied to.

**Example**
```
A loan-processing agent receives a scanned combined document containing both
a bank statement and a paystub on facing pages. It classifies the whole
upload as "bank statement," applies the bank-statement extraction schema, and
never extracts the paystub's gross income field. The application proceeds
with an incomplete income picture, and the mistake surfaces only when
underwriting can't reconcile the stated income with the extracted fields.
```

**Contributing Factors**
- Documents with mixed or multi-page content confuse single-label classifiers.
- Classifier has no abstain/low-confidence path, forcing a best-guess label even when uncertain.
- Visually similar document types (invoice vs. purchase order, W-2 vs. 1099) share layout features that confuse classification.
- No post-extraction validation step to catch when required fields for the assumed type are missing or malformed.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Mixed multi-document upload | Single PDF with bank statement + paystub pages | Classifier splits/flags mixed content or abstains for manual review | Classifier assigns one label to whole document, misses second document type |
| Visually similar document pair | W-2 vs. 1099 with similar layout | Classifier distinguishes correctly using text-pattern signals, not just layout | Classifier confuses the two based on layout alone |
| Low-confidence scan | Poor-quality scan of an uncommon document type | Classifier abstains, routes to manual classification | Classifier forces a best-guess label despite low confidence |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| document_classification_accuracy_eval_percent | > 98% | % of eval documents correctly classified against ground-truth labels |
| schema_field_completeness_post_classification_percent | > 99% | % of extractions where all required fields for the assigned schema are present and valid |

---

Fixing this means giving the classifier an abstain path and validating extracted fields against the assumed schema before trusting them.

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
| document_misclassification_rate_percent | > 2% |
| abstention_rate_percent | outside 2-5% baseline |
| schema_application_error_rate_percent | > 0.1% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Document Type Misclassification | Document classified with confidence < 0.70 or wrong schema applied | Warning |
| Classifier Accuracy Degradation | Classification accuracy drops > 5% month-over-month | Warning |
| High Abstention Rate | Abstention rate > 8% for a document type | Warning |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
