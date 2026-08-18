# AI Invents Fields or Objects Not in the Document: Causes and Fixes

## Issue: Object Hallucination — Model Populates Fields the Document Never Contained

**Frequency**: Occasional

**Symptoms**
- Agent describes elements that aren't actually present in the document
- Phantom tables, signatures, or stamps get extracted from documents that don't have them
- Non-existent optional fields (like a PO number) come back populated with values
- Commonly reported in LlamaIndex- and LangChain-style extraction schemas that mark every field as expected rather than explicitly optional

**Root Cause**
The model's language prior about "what invoices usually contain" overrides what this specific document actually contains.

**Example**
```
Input: Simple invoice without purchase order reference
Model output: "PO Number: PO-2024-0892"

Result: Fake PO number causes ERP lookup failure or worse, matches wrong PO
```

**How to fix it**: require spatial grounding for every populated field (including optional ones), separate "does this field exist" from "what is its value" as distinct steps, and verify reference values against the system of record. See the mitigations below.

## Mitigation Strategies

### Prevention
1. **Mandatory bounding-box grounding for every populated field**: Require every extracted field, including optional ones like "PO Number," to carry a spatial bounding box pointing to the exact region it was read from; a field cannot be populated without one, which structurally prevents inventing a value the document doesn't contain. Trade-off: requires the extraction model/pipeline to support spatial grounding output, and adds validation overhead per field.
2. **Negative-sample training/prompting on fields commonly absent**: Explicitly fine-tune or few-shot-prompt on documents that lack commonly-expected fields (e.g., invoices without a PO number) so the model learns "absent" is a valid and expected state rather than defaulting to its training-distribution prior that "invoices usually have a PO number." Trade-off: requires curating a labeled negative-sample dataset per document type/field.
3. **Optional-field schema with explicit absence marking**: Design extraction schemas so optional fields require an explicit "present" or "absent" determination as a separate step from value extraction, rather than a single "extract this field" prompt that implicitly encourages producing *something*. Trade-off: adds an extra decision point per optional field, increasing prompt/schema complexity.

### Detection & Response
1. **Grounding-absence flagging for populated optional fields**: Flag for review any populated field — especially optional/commonly-absent ones — that lacks a valid bounding box or spatial grounding, since a value with no traceable source region is very likely hallucinated.
2. **Downstream lookup-failure correlation**: Monitor cases where an extracted reference value (PO number, order ID) fails lookup in the system of record, and specifically check whether the source document actually contained that field — an unusually high rate of "extracted-but-not-found" values on optional fields signals object hallucination.
3. **Field-presence-rate monitoring per document type**: Track what percentage of documents of a given type have a given optional field populated, and compare against the known population rate; the extraction pipeline populating an optional field far more often than the document type genuinely contains it is a systemic hallucination signal.

### Architecture Patterns
1. **Presence-detection-then-extraction two-step pipeline**: Separate "does this field exist in the document" (a binary/grounded detection task) from "what is its value" (an extraction task conditioned on presence), rather than a single end-to-end prompt that conflates the two and defaults toward assuming presence.
2. **Grounding-required schema validation gate**: Insert a validation gate between extraction and downstream consumption that rejects any populated field lacking valid spatial grounding metadata, structurally preventing ungrounded values from reaching production systems regardless of which model produced them.
3. **Reference-value verification against system of record**: For extracted values that reference external identifiers (PO numbers, order IDs), verify existence against the system of record before accepting the value as confirmed, since a hallucinated but well-formatted ID will fail this check even when it looks plausible.

### Metrics
1. **ungrounded_optional_field_rate**: Target: 0% of populated optional fields lack bounding-box grounding; Alert on any occurrence
2. **field_presence_rate_vs_known_population_rate**: Target: within 5 percentage points of known population base rate; Alert if extraction populates a field > 15 points more often than the true population rate
3. **reference_value_lookup_failure_rate**: Target: < 2% of extracted reference IDs fail system-of-record lookup; Alert if > 8%
4. **phantom_field_audit_rate**: Target: < 1% of sampled "field not in document" cases were populated by extraction; Alert if > 5%

### Alerts
1. **Ungrounded Field Reaches Production** (P1): Condition - a populated field without valid spatial grounding is found in production output. Action: Treat as a pipeline defect; halt the responsible extraction path and audit recent output from that path for other hallucinated fields.
2. **Field Presence Rate Anomaly** (P2): Condition - a document type's field-population rate for an optional field exceeds the known true population rate by more than 15 points. Action: Sample recently processed documents to confirm hallucination, tighten presence-detection step or negative-sample training.
3. **Reference Lookup Failure Spike** (P2): Condition - lookup failure rate for an extracted reference ID field exceeds 8%. Action: Sample failed lookups against source documents to check whether the field was genuinely absent and hallucinated rather than a data-quality issue in the system of record.

## Universal Pattern Reference

This is a domain-specific implementation of the universal pattern:
**[Hallucination: Objects (Cross-Cutting)](../../../cross-cutting/accuracy/goals/output-accuracy/failures/hallucination-object.md)**

The universal pattern covers why models hallucinate objects/fields. This variant focuses on **document processing** where models invent fields that don't exist (phantom PO numbers, phantom tables, phantom signatures).

### Related Domain Variants
- [Vision: Object Hallucination](../../../vision-and-images/goals/visual-hallucination/failures/object-hallucination.md) — Hallucinated objects in cluttered or empty scenes

### Related Base Pattern
- [Hallucination: Base Mechanism](../../../cross-cutting/accuracy/goals/output-accuracy/failures/hallucination-base-mechanism.md) — Universal root cause of all hallucinations

---

## References

- [Hallucination of Multimodal LLMs Survey](https://arxiv.org/html/2404.18930v2) - Object hallucination taxonomy
- [Mitigating OCR Hallucinations in MLLMs](https://arxiv.org/html/2506.20168v2) - Phantom element detection
- [Evaluating Multimodal LLMs for Production](https://galileo.ai/blog/multimodal-llm-guide-evaluation) - Grounding validation
