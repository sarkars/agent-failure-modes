# Handwritten Text

## Issue: Handwritten Text Extraction Failures

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

## References

- [Why OCR Alone Fails](https://dev.to/jakemiller/why-ocr-alone-fails-in-real-world-documents-5f86) - Handwriting challenges
- [IDP Challenges 2026](https://idp-software.com/guides/idp-challenges-2026/) - Handwritten form issues
