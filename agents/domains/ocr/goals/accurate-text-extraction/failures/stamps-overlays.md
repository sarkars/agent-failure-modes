# Stamps and Overlays

## Issue: Stamps, Annotations, and Overlays

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

## References

- [IDP Challenges 2026](https://idp-software.com/guides/idp-challenges-2026/) - Overlay handling
- [Why OCR Alone Fails](https://dev.to/jakemiller/why-ocr-alone-fails-in-real-world-documents-5f86) - Annotation interference
