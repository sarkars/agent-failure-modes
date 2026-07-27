# What Are the Most Common Multimodal Reliability Problems in Document-Processing AI Agents?

**Multimodal reliability fails when a vision-language model produces a fluent, confident-sounding extraction that isn't actually grounded in what the document shows.** VLMs are trained to complete plausible text, not to signal visual uncertainty, so when a character is degraded, a field is genuinely absent, or a table's grid is ambiguous, the model fills the gap with a statistically likely value instead of admitting it can't tell — and reports high confidence while doing so. Multimodal reliability failures matter because the resulting errors are the hardest class of document-processing failure to catch: unlike classical OCR, which fails loudly with garbled or blank output, a plausible-wrong VLM answer passes every surface-level sanity check and is discovered only during downstream reconciliation, an audit, or a customer dispute.

## Key Takeaways

- 10 patterns cover multimodal reliability, grouped into four mechanisms: hallucination taxonomy, table-specific spatial failures, confidence/silent-failure dynamics, and input-quality-driven degradation.
- Confidence-miscalibration, plausible-wrong-outputs, table-cell-omission, and input-quality-gap are all rated Very Common — multimodal-reliability failures are not edge cases but the dominant failure mode of VLM-based document extraction.
- Databricks found frontier agents scoring below 50% accuracy on real enterprise document reasoning tasks (OfficeQA benchmark), and the input-quality-gap pattern's key finding is that the accuracy gap is not a model gap — production documents (scanned PDFs, CAD drawings, legacy exports, handwritten forms) simply differ systematically from benchmark inputs.
- Three of the ten patterns (confidence-miscalibration, attribute-hallucination, object-hallucination) have a documented universal mechanism in the cross-cutting hallucination patterns — the document-processing version is the same root cause applied to extracted fields rather than generated free text.

## Scope

- **Hallucination taxonomy** — [attribute-hallucination](failures/attribute-hallucination.md), [object-hallucination](failures/object-hallucination.md), [relational-hallucination](failures/relational-hallucination.md), [fabricated-content](failures/fabricated-content.md). Four distinct ways a language prior overrides actual document content: correcting a real value toward a common pattern, inventing an entire field that doesn't exist, swapping which value belongs to which column/row, and completing obscured or missing text with a plausible guess.
- **Table-specific spatial failures** — [complex-tables](failures/complex-tables.md), [table-cell-omission](failures/table-cell-omission.md). Both stem from VLMs processing images as patch sequences and inferring grid structure implicitly rather than reading it directly — merged cells and nested headers collapse hierarchy, and sparse tables with empty cells cause column misalignment.
- **Confidence and silent-failure dynamics** — [confidence-miscalibration](failures/confidence-miscalibration.md), [plausible-wrong-outputs](failures/plausible-wrong-outputs.md). The model's self-reported confidence doesn't correlate with actual accuracy, so a wrong extraction bypasses the review queue precisely because it looks confident and plausible rather than garbled.
- **Input-quality-driven degradation** — [input-quality-gap](failures/input-quality-gap.md), [visual-degradation](failures/visual-degradation.md). The environmental driver behind the other patterns: real enterprise documents (blur, occlusion, low contrast, non-standard formats) fall outside the clean-image distribution VLMs are evaluated on, and the model doesn't recognize when quality has degraded past reliable-extraction thresholds.

## When Multimodal Reliability Matters

- A pipeline uses a VLM to extract structured fields directly from document images rather than a deterministic OCR-plus-rules approach, especially for financial, ERP, or compliance-critical values
- Documents include optional fields that are legitimately absent on some instances (a PO number missing from a simple invoice), degraded regions (stains, low-resolution faxes, occlusions), or complex/sparse table structures
- Production accuracy is measurably worse than benchmark or demo accuracy for the same model, which the input-quality-gap pattern identifies as a signal to invest in preprocessing rather than a bigger model

## Cross-Pattern Insight

Every mitigation in multimodal reliability works by forcing the model's output to be traceable back to actual pixels rather than trusting model fluency. Grounding-required architectures (fabricated-content, object-hallucination) reject any field that can't be tied to a bounding box in the source image. Dual-path extraction (attribute-hallucination, plausible-wrong-outputs) runs a deterministic OCR pass alongside the VLM and gates on disagreement, since a hallucinated "correction" has no signal in classical OCR output. Structure-detection-before-content-extraction (complex-tables, relational-hallucination, table-cell-omission) separates "what's the grid" from "what's in each cell" so the VLM is never asked to infer spatial layout and read content in the same pass — exactly the joint task VLMs are worst at. And post-hoc calibration (confidence-miscalibration, visual-degradation) replaces the model's own confidence score with an empirically-derived accuracy-per-bucket mapping, because the central finding across all 10 multimodal-reliability patterns is that VLM confidence and VLM correctness are not the same signal.

## Frequently Asked Questions

### What makes VLM hallucinations harder to catch than classical OCR errors?
Because classical OCR fails loudly — an unreadable character produces garbled output or a blank, which is visibly wrong. The plausible-wrong-outputs pattern documents that VLMs instead produce the most statistically plausible value when uncertain (e.g., misreading a damaged "$10,000" as "$3,000"), with no error flagged in the pipeline, so the error is discovered only during downstream reconciliation or a customer dispute.

### Can a higher confidence threshold fix confidence miscalibration?
No — the confidence-miscalibration pattern's core finding is that raw model-reported confidence doesn't correlate with accuracy at all, so no threshold on the raw score is reliable. The fix is post-hoc recalibration (temperature scaling, isotonic regression) against empirically measured accuracy per confidence bucket, using that calibrated score for routing instead of the model's raw output.

### What's the difference between object-hallucination and fabricated-content?
Object-hallucination is inventing an entire field that isn't in the document at all (a "PO Number" on an invoice that has none), driven by the model's prior about what documents of that type usually contain. Fabricated-content is completing a field that's partially present but obscured or ambiguous (a torn address with a missing ZIP code), driven by the model generating a plausible completion rather than admitting the visible portion is incomplete.

### Is the input-quality gap solvable by upgrading to a better VLM?
No. The input-quality-gap pattern's key finding is explicit: the gap between benchmark and production performance is an input-quality gap, not a model gap. Enterprise documents (inconsistent scans, CAD drawings, legacy exports, handwritten forms) differ systematically from clean benchmark data, so the fix is standardized preprocessing and quality-gated routing, not a stronger model.

### How does relational-hallucination differ from table-cell-omission?
Relational-hallucination is a wrong-assignment error — values are read correctly but attached to the wrong column or row (Quantity and Unit Price swapped). Table-cell-omission is a missing/collapsed-cell error — empty cells in a sparse table cause the model to skip ahead, shifting subsequent values into the wrong column entirely. Both stem from VLMs inferring grid structure implicitly rather than reading grid structure directly, but relational-hallucination swaps values while table-cell-omission drops or shifts values.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Attribute Hallucination](failures/attribute-hallucination.md) | Correct field identified but value "corrected" toward a common training-distribution pattern |
| [Complex Tables](failures/complex-tables.md) | Multi-row headers and spanning cells collapsed, losing hierarchy |
| [Confidence Miscalibration](failures/confidence-miscalibration.md) | High self-reported confidence on incorrect extractions; confidence doesn't track accuracy |
| [Fabricated Content](failures/fabricated-content.md) | Obscured or ambiguous regions completed with invented, ungrounded content |
| [Input Quality Gap](failures/input-quality-gap.md) | Real enterprise documents fall outside the clean-image distribution benchmarks measure |
| [Object Hallucination](failures/object-hallucination.md) | Language prior invents an entire field/element the document doesn't contain |
| [Plausible Wrong Outputs](failures/plausible-wrong-outputs.md) | Model silently substitutes a statistically plausible value instead of flagging uncertainty |
| [Relational Hallucination](failures/relational-hallucination.md) | Spatial/logical relationships wrong — values assigned to the wrong column or row |
| [Table Cell Omission](failures/table-cell-omission.md) | Empty cells in sparse tables cause column misalignment and dropped values |
| [Visual Degradation](failures/visual-degradation.md) | Blur, occlusion, or low contrast causes overconfident, linguistic-prior-driven guesses |

**Total: 10 patterns**

## Related Goals

- [Accurate Text Extraction](../accurate-text-extraction/) — character-level OCR misreads, a narrower and more mechanical failure than VLM hallucination
- [Layout Preservation](../layout-preservation/) — table-boundaries and merged-cells cover structure *detection* failures, versus complex-tables/relational-hallucination here which cover VLM *content-assignment* failures once structure is ambiguous
- Cross-cutting [Output Accuracy hallucination patterns](../../../../cross-cutting/accuracy/goals/output-accuracy/) — the universal mechanism behind attribute, object, and confidence-miscalibration hallucinations, applied here specifically to document field extraction
