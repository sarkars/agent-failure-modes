# Fabricated Content

## Issue: Fabricated Content Not Grounded in Input

**Frequency**: Common

**Symptoms**
- Extracted fields contain text not present in document
- Model "completes" partial information with invented data
- Addresses, names, or codes appear that don't exist in source

**Root Cause**
When visual input is ambiguous or incomplete, VLMs draw on training data patterns to generate plausible completions rather than admitting uncertainty.

**Example**
```
Input: Partially obscured address "123 Main St, San ___"
Expected: Extract only visible text or flag incomplete
Actual: "123 Main St, San Francisco, CA 94102" (ZIP fabricated)

Result: Package shipped to wrong address
```

**Mitigation Strategies**
1. **Grounding checks**: Verify every extracted token appears in source
2. **Character-level alignment**: Map outputs back to image regions
3. **Refusal training**: Fine-tune model to say "unclear" rather than guess
4. **OCR fallback**: Use traditional OCR as cross-check

## References

- [Mitigating OCR Hallucinations in MLLMs](https://arxiv.org/html/2506.20168v2) - Fabrication under ambiguity
- [Hallucination of Multimodal LLMs Survey](https://arxiv.org/html/2404.18930v2) - Content not grounded in input
- [Why OCR Alone Fails](https://dev.to/jakemiller/why-ocr-alone-fails-in-real-world-documents-5f86) - Grounding verification
