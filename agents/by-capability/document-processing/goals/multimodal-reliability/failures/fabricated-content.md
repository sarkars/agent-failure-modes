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

## Mitigation Strategies

### Prevention
1. **Character-level grounding verification**: Require every extracted token to be traceable to a specific bounding-box region in the source image, and reject any extracted value that cannot be spatially aligned back to actual visible content — this directly blocks generative "completion" of obscured or missing text. Trade-off: requires a model/pipeline capable of producing spatial grounding, not just text output, which not all VLM APIs support natively.
2. **Explicit refusal/uncertainty fine-tuning or prompting**: Fine-tune or prompt the model to explicitly output "unclear" or "partially obscured" for ambiguous regions instead of completing them with a plausible guess, making non-extraction a valid and expected output rather than a failure to route around. Trade-off: increases the rate of incomplete extractions requiring downstream handling (human review or re-scan) versus a model that always produces something.
3. **Deterministic OCR fallback for cross-verification**: Run traditional (non-generative) OCR alongside the VLM specifically on regions the VLM extracted with content, and require agreement between the two before accepting a value — a fabricated completion has no corresponding signal in classical OCR output. Trade-off: traditional OCR itself performs worse than VLMs on many document types, so disagreement isn't always a fabrication indicator.

### Detection & Response
1. **Source-coverage validation for every extracted field**: Check that the source region corresponding to an extracted value actually has visible pixel content (not blank/obscured) before accepting the extraction; a value extracted from a region with no visible content is definitionally fabricated.
2. **Never-seen-token flagging**: Flag any extracted value containing tokens (words, codes, numbers) with zero character-level correspondence to the source image region, even if the overall extraction looks plausible.
3. **Partial-obscuration incident review**: Specifically audit documents with known partial obscuration (stains, tears, redactions, cropped edges) since these are the highest-risk population for fabrication and aggregate accuracy metrics can mask a high fabrication rate within this subset.

### Architecture Patterns
1. **Grounding-required extraction architecture**: Architect the extraction pipeline so that "extracted value" and "source grounding" are a single atomic unit that cannot be separated — no value is accepted or passed downstream without its corresponding spatial grounding metadata attached.
2. **Refuse-then-escalate pipeline**: Design the pipeline to treat model refusal ("unclear") as a first-class successful outcome that routes to human transcription or re-scan, rather than as an error state to be worked around by prompting the model to "try harder" (which reintroduces the fabrication risk).
3. **Dual-extraction reconciliation gate**: Require agreement between a generative VLM pass and a deterministic OCR pass as a gate before a value from an ambiguous/degraded region is accepted, with automatic escalation to human review on disagreement.

### Metrics
1. **ungrounded_extraction_rate**: Target: 0% of accepted extractions lack source grounding; Alert on any occurrence in production
2. **fabrication_rate_on_obscured_regions**: Target: < 2% (measured via audit of documents with known obscuration); Alert if > 8%
3. **refusal_rate**: Target: track as baseline; Alert if it drops to near-0% for a document type known to have degraded/obscured content (signals the model is fabricating instead of refusing)
4. **ocr_vlm_disagreement_on_flagged_regions**: Target: < 5% net disagreement after reconciliation; Alert if > 15%

### Alerts
1. **Ungrounded Extraction Detected** (P1): Condition - any extraction reaches production without valid source grounding. Action: Treat as a pipeline defect, halt the affected code path, audit recently processed documents for fabricated values.
2. **Obscured-Region Fabrication Spike** (P1): Condition - audit shows fabrication rate on obscured-content documents exceeds 8%. Action: Tighten refusal prompting/fine-tuning, route affected document types to mandatory human review until fixed.
3. **Suspiciously Low Refusal Rate** (P2): Condition - refusal rate approaches 0% for a document source known to contain degraded scans. Action: Investigate whether refusal training/prompting has regressed, since a model that never says "unclear" on genuinely unclear input is very likely fabricating.

## References

- [Mitigating OCR Hallucinations in MLLMs](https://arxiv.org/html/2506.20168v2) - Fabrication under ambiguity
- [Hallucination of Multimodal LLMs Survey](https://arxiv.org/html/2404.18930v2) - Content not grounded in input
- [Why OCR Alone Fails](https://dev.to/jakemiller/why-ocr-alone-fails-in-real-world-documents-5f86) - Grounding verification
