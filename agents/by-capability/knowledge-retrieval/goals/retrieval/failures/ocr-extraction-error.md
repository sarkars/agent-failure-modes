# Ocr Extraction Error

## Issue: Agent misreads scanned, smudged, rotated, or low-quality text.

**Frequency**: Common

**Symptoms**
- Extracted field conflicts with image/source.
- Extracted numeric field (price, date, ID) differs from what's visible in the source scan due to character confusion (e.g., "0" read as "O", "8" as "3").
- OCR output contains garbled or nonsensical text runs where the source image was rotated, skewed, or low-resolution, yet the document is indexed and retrieved anyway.
- Agent answers confidently using an OCR'd figure that is objectively wrong when checked against the original scanned image.

**Root Cause**
Agent misreads scanned, smudged, rotated, or low-quality text.

**Example**
```
A scanned invoice states the total as "$1,800.00," but poor scan quality and a stray
toner smudge cause the OCR engine to read the amount as "$1,300.00" (the '8' misread
as '3'). The document is indexed with no confidence flag. A user later asks "What was
the invoice total?" and the agent retrieves the OCR'd text and answers "$1,300.00,"
propagating the misread figure as if it were ground truth from the source document.
```

**Contributing Factors**
- Low source scan quality (low resolution, skew, smudges, faded print) increases character-level OCR error rate, especially for numerals and similar-looking glyphs.
- No per-word or per-field confidence scores retained alongside OCR output, so downstream retrieval can't distinguish high- and low-confidence extractions.
- Single OCR engine used with no cross-validation or ensemble check against a second engine.
- Original source images not retained or linked, so there's no way to verify or correct a misread field after indexing.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Numeral confusion | Scanned document with a smudged or low-resolution numeric field (e.g., invoice total) | Extracted value matches the true value on the source image | Extracted value differs from the source image due to character misread |
| Low-quality scan flagged | Rotated or low-DPI scanned page ingested through the OCR pipeline | Document is tagged low-confidence and excluded from confident-answer synthesis | Low-quality OCR text is indexed and retrieved with no confidence flag |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| ocr_word_accuracy_percent | > 95% | Weekly manual spot-check comparing sampled OCR output against source images, computing % of words correctly transcribed |

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
| ocr_word_accuracy_percent | < 90% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| OCR Accuracy Degradation | ocr_word_accuracy_percent drops more than 5% month-over-month on spot-check sample | High |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
