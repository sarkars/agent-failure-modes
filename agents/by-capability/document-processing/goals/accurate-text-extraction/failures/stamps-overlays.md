# OCR Mixes Stamp and Annotation Text Into Document Content: Causes and Fixes

## Issue: Physical stamps and handwritten annotations overlap printed text, so OCR interleaves both into a corrupted field

**Frequency**: Occasional

**Symptoms**
- Original text corrupted where a stamp or annotation overlaps it
- Stamp text mixed directly into surrounding document text
- Dates and reference numbers from a stamp extracted incorrectly or merged into an unrelated field

**Root Cause**
Physical stamps, handwritten annotations, and stickers overlay original text, creating ambiguous regions where multiple text sources compete.

**Example**
```
Input: Invoice with "APPROVED 2024-01-20" stamp over line item
Original: "Widget A    $50.00"
Extracted: "Widget APPROVED 2024-01-20 A    $50.00"

Result: Line item description corrupted
```

## How to Fix Stamp and Annotation Interference in OCR

## Mitigation Strategies

### Prevention
1. **Color/texture layer separation**: Since stamps and annotations are typically applied in a distinct ink color or with different texture/pressure than the printed original, use color clustering or texture analysis to separate the two layers before OCR reads either, preventing the interleaving seen in "Widget APPROVED 2024-01-20 A    $50.00". Trade-off: fails when the stamp is the same color as body text (e.g., black ink stamps on black printed text) and requires a secondary separation method for that case.
2. **Annotation-region detection model**: Train a detector specifically to recognize the visual signature of stamps/handwritten annotations (irregular shape, different alignment, distinct ink) and mask or isolate those regions before running the primary text-extraction pass. Trade-off: annotations that closely mimic printed formatting (typed approval stamps) are harder to distinguish and may be missed.
3. **Multi-pass extraction with region exclusion**: Run a first extraction pass with detected annotation regions masked out (to get clean original content), then a second pass restricted to just the annotation regions (to capture stamp/annotation content as separate structured data), rather than a single pass that conflates both. Trade-off: doubles OCR invocations per affected document.

### Detection & Response
1. **Business-logic/catalog validation**: Cross-check extracted line-item descriptions and values against a product catalog or expected-value list; a corrupted description like "Widget APPROVED 2024-01-20 A" fails catalog lookup and should be flagged for correction rather than accepted as-is.
2. **Field length/format anomaly detection**: Monitor extracted field lengths and formats against expected norms for that field type; an unusually long or format-breaking line-item description is a strong signal of stamp/annotation contamination.
3. **Overlapping-layer color analysis**: Run post-hoc color/texture analysis on regions that failed validation to confirm whether an overlay caused the failure, informing whether the issue is stamp interference versus a genuine data problem.

### Architecture Patterns
1. **Confidence-gated human-in-the-loop review queue**: Route line items or fields that fail catalog/business-logic validation to human review, since these are the most reliable signal of stamp-corrupted content reaching structured output.
2. **Structured dual-output extraction**: Architect the pipeline to output "document content" and "annotation/stamp content" (e.g., approval stamp date, approver) as separate structured fields rather than a single merged text stream, preserving both pieces of information without corruption.
3. **Template-aware stamp zone registry**: For recurring document sources where stamps are applied in consistent zones (e.g., an approval stamp always in the top-right), maintain a registry of expected stamp zones to exclude from body-text extraction by default.

### Metrics
1. **catalog_lookup_failure_rate**: Target: < 1% of line items; Alert threshold: > 4%
2. **field_length_anomaly_rate**: Target: < 2%; Alert threshold: > 6%
3. **annotation_region_detection_recall**: Target: > 90% of known stamp/annotation instances detected; Alert threshold: < 75%
4. **dual_pass_review_routing_rate**: Target: 100% of failed-validation items routed; Alert threshold: < 98%

### Alerts
1. **Catalog Lookup Failure Spike** (P2): Condition - line-item catalog lookup failure rate exceeds 4% for a document source. Action: Sample documents, check for new stamp/annotation pattern at that source, add to stamp-zone registry if recurring.
2. **Annotation Detection Recall Drop** (P2): Condition - annotation detection recall falls below 75% against a labeled validation set. Action: Retrain/recalibrate the annotation detection model.
3. **Unrouted Validation Failures** (P1): Condition - fields failing catalog/business-logic validation are not appearing in the review queue. Action: Fix routing pipeline immediately; audit recently processed documents for corrupted line items that reached downstream systems.

## References

- [IDP Challenges 2026](https://idp-software.com/guides/idp-challenges-2026/) - Overlay handling
- [Why OCR Alone Fails](https://dev.to/jakemiller/why-ocr-alone-fails-in-real-world-documents-5f86) - Annotation interference
