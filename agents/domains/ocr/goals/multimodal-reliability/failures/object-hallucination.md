# Object Hallucination

## Issue: Object Hallucination

**Frequency**: Occasional

**Symptoms**
- Model describes elements not present in document
- Phantom tables, signatures, or stamps extracted
- Non-existent fields populated with values

**Root Cause**
The model's language prior about "what invoices usually contain" overrides what this specific document actually contains.

**Example**
```
Input: Simple invoice without purchase order reference
Model output: "PO Number: PO-2024-0892"

Result: Fake PO number causes ERP lookup failure or worse, matches wrong PO
```

**Mitigation Strategies**
1. **Schema constraints**: Only extract fields visually confirmed
2. **Bounding box validation**: Require spatial coordinates for each extraction
3. **Negative sampling**: Train on documents missing common fields

## References

- [Hallucination of Multimodal LLMs Survey](https://arxiv.org/html/2404.18930v2) - Object hallucination taxonomy
- [Mitigating OCR Hallucinations in MLLMs](https://arxiv.org/html/2506.20168v2) - Phantom element detection
- [Evaluating Multimodal LLMs for Production](https://galileo.ai/blog/multimodal-llm-guide-evaluation) - Grounding validation
