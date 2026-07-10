# Skew and Rotation

## Issue: Skew, Rotation, and Perspective Distortion

**Frequency**: Common

**Symptoms**
- Line breaks appear in middle of words
- Characters from different lines merged
- Entire document text scrambled

**Root Cause**
Mobile phone photos, misaligned scans, and documents photographed at angles create geometric distortions that break line detection.

**Example**
```
Input: Phone photo of document at 15-degree angle
Line 1: "Invoice Number: 12345"
Line 2: "Date: 2024-01-15"

Extracted: "Invoice Number: 1234Date: 2024-01-15" (lines merged)
```

## Mitigation Strategies

### Prevention
1. **Automated deskew preprocessing**: Detect the dominant text-line angle (via Hough transform or projection profile analysis) and rotate the image to horizontal before OCR runs, directly addressing the geometric distortion that causes line detection to merge adjacent lines like "Invoice Number: 1234Date: 2024-01-15". Trade-off: deskew angle estimation can fail on sparse-text or table-heavy pages, requiring a fallback detection method.
2. **Perspective/homography correction**: For mobile phone photos taken at an angle (not just simple rotation), detect the document's four corners and apply a homography transform to rectify perspective distortion before line detection, since angle alone doesn't correct trapezoidal skew. Trade-off: corner detection is unreliable against cluttered backgrounds or partially-visible documents.
3. **Capture-time alignment guidance**: Provide real-time feedback in the mobile capture UI (alignment guides, angle/quality indicators, auto-capture when flat) to prevent skewed photos from being captured in the first place, since it's cheaper to avoid the distortion than to correct it computationally after the fact. Trade-off: only helps for in-app capture flows; scanned/uploaded documents from other sources get no benefit.

### Detection & Response
1. **Line-merge pattern detection**: Monitor extracted field lengths and structure for signatures of merged lines (e.g., a field unexpectedly containing content that belongs to two logical fields, like an invoice number field containing a date), and flag for reprocessing with stronger deskew.
2. **Rotation-angle threshold flagging**: Measure detected rotation angle for every document at intake and flag anything above a threshold (e.g., 5 degrees) for mandatory deskew before OCR, rather than only correcting when initial extraction quality is poor.
3. **Orientation metadata cross-check**: Where available, compare EXIF/orientation metadata against the visually-detected skew angle; a mismatch indicates either a capture pipeline bug or a rotation that wasn't corrected, and should trigger a reprocessing pass.

### Architecture Patterns
1. **Deskew-then-detect-then-OCR pipeline**: Architect the pipeline so geometric correction (deskew, perspective) always runs as a distinct stage before line/layout detection, rather than expecting the OCR/layout model to be robust to raw skewed input.
2. **Confidence-gated human-in-the-loop review queue**: Route documents where post-deskew rotation confidence remains low, or where line-merge signatures persist after correction, to human review rather than accepting scrambled text downstream.
3. **Capture-quality gate at ingestion**: For mobile-capture workflows, reject or prompt re-capture for photos whose detected angle/perspective distortion exceeds a threshold before they ever enter the OCR pipeline.

### Metrics
1. **documents_requiring_deskew_rate**: Target: monitored baseline per channel; Alert threshold: sudden increase > 25% week-over-week
2. **line_merge_signature_rate**: Target: < 2% of processed documents; Alert threshold: > 6%
3. **post_deskew_rotation_residual**: Target: < 1 degree average residual angle; Alert threshold: > 3 degrees
4. **mobile_capture_recapture_rate**: Target: < 15% of captures prompt re-capture; Alert threshold: > 35% (indicates UI guidance isn't working)

### Alerts
1. **Line Merge Spike** (P2): Condition - line-merge signature rate exceeds 6% for a document source/channel. Action: Sample documents, verify deskew/perspective correction is running and effective for that channel.
2. **Residual Skew After Correction** (P2): Condition - post-deskew residual angle exceeds 3 degrees on average for a batch. Action: Investigate deskew algorithm failure mode (e.g., sparse text, table-dominant pages) and add fallback correction method.
3. **Capture Guidance Ineffective** (P3): Condition - mobile re-capture prompt rate exceeds 35%, indicating users aren't achieving flat/aligned captures. Action: Review and improve capture UI guidance and thresholds.

## References

- [Why OCR Alone Fails](https://dev.to/jakemiller/why-ocr-alone-fails-in-real-world-documents-5f86) - Geometric distortion
- [Why AI OCR Fails](https://parseur.com/blog/why-ai-ocr-fail) - Image preprocessing
