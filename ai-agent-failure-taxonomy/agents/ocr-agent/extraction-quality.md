# Extraction Quality

Text extraction accuracy is the foundation of any OCR agent. Even small errors can cascade into significant problems in downstream processing.

---

## Character Confusion

### Issue: Visually Similar Character Substitution

**Frequency**: Very Common

**Symptoms**
- Numbers appear in text fields, letters appear in numeric fields
- Validation fails on extracted data that "looks correct"
- Downstream calculations produce unexpected results

**Root Cause**
Many characters are visually similar, especially in certain fonts or at low resolutions. The model cannot distinguish between them without additional context.

**Commonly Confused Characters**

| Characters | Context Where Confusion Occurs |
|------------|-------------------------------|
| `0` / `O` / `o` | Alphanumeric codes, serial numbers |
| `1` / `l` / `I` / `|` | IDs, license plates, codes |
| `5` / `S` | Codes, amounts |
| `8` / `B` | Alphanumeric sequences |
| `2` / `Z` | Handwritten forms, fax copies |
| `6` / `G` | Low-resolution scans |
| `rn` / `m` | Narrow fonts, small text |
| `cl` / `d` | Serif fonts |
| `vv` / `w` | Stylized fonts |

**Example**
```
Input Image: Invoice #INV-2024-O1523
Expected: INV-2024-O1523 (letter O)
Actual: INV-2024-01523 (digit 0)

Result: Invoice lookup fails because ID doesn't exist
```

**Mitigation Strategies**
1. **Field-type validation**: If a field should be numeric-only, flag alphabetic characters
2. **Regex patterns**: Define expected formats (e.g., `INV-\d{4}-[A-Z]\d{4}`)
3. **Checksum validation**: Use check digits for critical IDs
4. **Confidence thresholding**: Flag characters with low confidence for review
5. **Context-aware post-processing**: Use domain dictionary to correct likely errors

**Detection**
- Monitor field validation failure rates by field type
- Track "manual correction" rates in human review queues
- A/B test extraction against ground truth samples

---

### Issue: Punctuation and Special Character Errors

**Frequency**: Common

**Symptoms**
- Decimal points become commas (or vice versa) breaking numeric parsing
- Currency symbols misread or dropped
- Hyphens, dashes, and minus signs interchanged

**Root Cause**
Small punctuation marks are often damaged in scans or rendered differently across fonts. Regional formatting differences (`.` vs `,` for decimals) add ambiguity.

**Example**
```
Input Image: Total: $1,234.56
Expected: 1234.56
Actual: 1.23456 (comma interpreted as decimal)

Result: Invoice processed for wrong amount
```

**Mitigation Strategies**
1. **Locale-aware parsing**: Detect document locale and apply appropriate numeric formatting rules
2. **Sanity bounds**: Reject values outside expected ranges (e.g., invoice line item > $1M)
3. **Multiple extraction passes**: Extract raw string AND parsed numeric, compare
4. **Currency symbol detection**: Identify currency before parsing to infer format

**Detection**
- Unusual value distributions (many values < $1 when expecting larger amounts)
- Parsing exceptions in downstream systems
- Currency mismatch alerts

---

## Font and Style Handling

### Issue: Decorative and Stylized Font Failures

**Frequency**: Occasional

**Symptoms**
- High error rates on specific document sources
- Certain company's documents consistently fail extraction
- Brand names and logos text extracted incorrectly

**Root Cause**
Decorative fonts, stylized text, and brand-specific typography differ significantly from standard fonts in training data.

**Example**
```
Input: Company logo with stylized "ACME CORP"
Expected: ACME CORP
Actual: RCME CORF (stylized A looks like R, P like F)
```

**Mitigation Strategies**
1. **Template matching**: For known document sources, define fixed regions to skip or use template-specific extraction
2. **Logo detection**: Identify and exclude logo regions from text extraction
3. **Source-specific fine-tuning**: Train on documents from frequent sources
4. **Fallback to business rules**: Use sender metadata instead of extracted company name

---

### Issue: Handwritten Text Extraction Failures

**Frequency**: Common (in forms with handwritten sections)

**Symptoms**
- Extremely low accuracy on handwritten portions
- Model returns garbled or nonsensical text
- High variance in accuracy across documents

**Root Cause**
Handwriting varies dramatically between individuals. Models trained primarily on printed text struggle with cursive, poor penmanship, and unconventional letterforms.

**Example**
```
Input: Handwritten signature field with printed name "Dr. Smith"
Expected: Dr. Smith
Actual: Do Smlte (or rejected entirely)
```

**Mitigation Strategies**
1. **Separate pipelines**: Use specialized handwriting recognition models
2. **Field classification**: Detect handwritten vs. printed and route accordingly
3. **Low-confidence flagging**: Automatically route low-confidence handwritten fields to human review
4. **Constrained recognition**: If field has limited valid values (e.g., Yes/No checkboxes), use classification instead of OCR
5. **Skip and supplement**: For signature fields, skip extraction and use upstream metadata

**Detection**
- Confidence score distributions by field type
- Character-level entropy (garbled text has unusual character distributions)

---

## Image Quality Issues

### Issue: Low Resolution and Compression Artifacts

**Frequency**: Very Common

**Symptoms**
- Consistent errors on documents from specific sources (fax, mobile upload)
- Small text (footnotes, fine print) fails completely
- JPEG artifacts cause character fragmentation

**Root Cause**
Low DPI scans, aggressive compression, and small original text create images where characters lack sufficient detail for recognition.

**Example**
```
Document: Faxed invoice at 100 DPI
Footer text: "Terms: Net 30 days"
Extracted: "Tenns: Nel 30 drys"

Result: Payment terms not correctly parsed
```

**Mitigation Strategies**
1. **Minimum DPI requirements**: Reject or flag documents below 200 DPI
2. **Image preprocessing**: Apply super-resolution or denoising before OCR
3. **Multi-scale extraction**: Run OCR at multiple resolutions and ensemble results
4. **Source quality feedback**: Notify upstream systems about quality issues
5. **Targeted high-res extraction**: Re-extract specific regions at higher zoom for critical fields

**Detection**
- Track accuracy by document source/channel
- Monitor image quality metrics (DPI, file size, noise levels) alongside accuracy
- Alert on sudden quality drops from specific sources

---

### Issue: Skew, Rotation, and Perspective Distortion

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

---

## Noise and Artifacts

### Issue: Background Interference

**Frequency**: Common

**Symptoms**
- Extra characters appear in extracted text
- Watermarks partially extracted as text
- Security patterns (guilloche) cause garbled output

**Root Cause**
Background elements like watermarks, security patterns, colored backgrounds, and stamps are interpreted as text characters.

**Example**
```
Input: Invoice with "PAID" watermark across page
Extracted line: "Total Due: $0P.0A0I D"

Result: Amount parsing fails
```

**Mitigation Strategies**
1. **Background removal**: Preprocess to isolate foreground text
2. **Color channel separation**: Process different color channels independently
3. **Watermark detection**: Identify and mask known watermark patterns
4. **Confidence filtering**: Watermark-derived characters typically have lower confidence

---

### Issue: Stamps, Annotations, and Overlays

**Frequency**: Occasional

**Symptoms**
- Original text corrupted where stamps/annotations overlap
- Stamp text mixed with document text
- Dates and reference numbers from stamps extracted incorrectly

**Root Cause**
Physical stamps, handwritten annotations, and stickers overlay original text, creating ambiguous regions where multiple text sources compete.

**Example**
```
Input: Invoice with "APPROVED 2024-01-20" stamp over line item
Original: "Widget A    $50.00"
Extracted: "Widget APPROVED 2024-01-20 A    $50.00"

Result: Line item description corrupted
```

**Mitigation Strategies**
1. **Layer separation**: Use color/texture analysis to separate stamp from original
2. **Annotation detection**: Train model to identify and isolate annotation regions
3. **Multi-pass extraction**: First pass for original, second for annotations
4. **Business logic validation**: Flag line items that don't match product catalog

**Detection**
- Unusual field lengths or formats
- Catalog/database lookup failures
- Color analysis detecting overlapping layers
