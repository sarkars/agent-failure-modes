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

**Mitigation Strategies**
1. **Deskew preprocessing**: Detect and correct rotation before OCR
2. **Perspective correction**: Apply homography transformation for angled photos
3. **Line detection validation**: Verify detected lines are roughly horizontal
4. **Mobile capture guidance**: Provide real-time feedback in capture UI (alignment guides, quality checks)

**Detection**
- Track extraction patterns that suggest line merging (unusual field lengths)
- Monitor document orientation metadata
- Flag documents with detected rotation > threshold
