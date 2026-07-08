# Ocr Extraction Error

## Issue: Agent misreads scanned, smudged, rotated, or low-quality text.

**Frequency**: Common

**Symptoms**
- Extracted field conflicts with image/source.
- [Add more specific symptoms]

**Root Cause**
Agent misreads scanned, smudged, rotated, or low-quality text.

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
1. **Source Image Verification**: For each OCR'd document, retain original source image. Compare OCR output to image sample via manual spot-check before indexing. Flag documents with errors for re-OCR. Target: < 0.5% error rate post-verification.
2. **Confidence-Based Routing**: For each OCR'd passage, compute confidence_score. If confidence < threshold, mark document as 'OCR-extracted' with disclaimer. Don't use for critical queries without human review.
3. **Multi-OCR Fallback**: For critical documents, run multiple OCR engines (Tesseract, Google Vision, Azure) in parallel. Compare outputs. Use voting or ensemble to improve accuracy. Flag high-discrepancy results.

### Detection & Response
1. **OCR Quality Scoring**: Periodically sample OCR results (10%/week) and manually verify accuracy. Compute per-document OCR_quality_score (% words correct). Track score distribution. Alert if quality degrades.
2. **Gibberish Detection**: Apply language model to detect OCR output that's mostly gibberish (low perplexity). Flag low-quality OCR documents automatically. Quarantine for manual review.
3. **Scanned Document Quality Assessment**: Evaluate source image quality (resolution, contrast, skew angle). Flag low-quality images as OCR error risk. Route to manual processing or re-scan.

### Architecture Patterns
1. **Confidence-Aware Indexing**: For OCR'd documents, store: raw_ocr_text + confidence_scores_per_word + quality_flags. Retrieval can filter by confidence_threshold. High-confidence passages prioritized in ranking.
2. **Image Preservation**: Keep original document images in system (not just OCR text). Enable user to view original alongside OCR. Supports verification and dispute resolution.
3. **Multi-Engine OCR Pipeline**: Route documents through multiple OCR engines. Compare outputs; use voting/ensemble. High-discrepancy results flagged for manual review before indexing.

### Metrics
1. **ocr_word_accuracy_percent**: Target: > 95%; Alert threshold: < 90%
2. **ocr_quality_score_distribution_median**: Target: > 0.90; Alert if median drops < 0.85
3. **low_confidence_ocr_documents_percent**: Target: < 5%; Alert threshold: > 10%
4. **gibberish_detection_true_positive_rate_percent**: Target: > 90%; Measure model accuracy
5. **ocr_engine_agreement_rate_percent**: Target: > 95%; Engines should agree on output

### Alerts
1. **OCR Quality Degradation** (P2 - Warning): Condition - ocr_word_accuracy drops > 5% month-over-month. Action: Investigate OCR engine config, retrain if ML-based, consider re-OCR of affected documents.
2. **Low-Confidence OCR Retrieved** (P2 - Warning): Condition - > 20% of retrieved results from low-confidence OCR. Action: Add confidence-based filtering, surface disclaimer to user, consider re-OCR.
3. **Gibberish Document Detected** (P1 - Critical): Condition - document fails gibberish detection. Action: Remove from index, quarantine for manual review, investigate source document quality.

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
