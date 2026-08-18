# AI Document Extraction Assigns Wrong Values to Correct Fields: Causes and Fixes

## Issue: Attribute Hallucination — Model Reads the Right Field but the Wrong Value

**Frequency**: Common

**Symptoms**
- Agent identifies the correct field but assigns a subtly wrong value
- Colors, dates, or quantities come back slightly off from the source
- Model silently "corrects" an extracted value toward a more common pattern
- Commonly reported in LlamaIndex- and LangChain-style document extraction pipelines that hand raw OCR/VLM output straight to downstream systems without a validation step

**Root Cause**
Model identifies the right object but assigns properties based on training distribution rather than image content.

**Example**
```
Input: Invoice dated "2024-02-29" (leap year)
Actual: "2024-02-28" (model "corrects" to common date)

Result: Payment terms calculated from wrong date
```

**How to fix it**: validate every extracted date and numeric field against deterministic domain rules, keep the raw extraction alongside any normalized value, and cross-check against a non-generative OCR baseline before trusting the model's "corrected" answer. See the mitigations below.

## Mitigation Strategies

### Prevention
1. **Calendar/domain-rule validation on every date and numeric field**: Validate every extracted date against actual calendar rules (leap years, days-per-month) and every numeric field against domain-plausible ranges, rejecting or flagging extractions that fail validation rather than trusting the model's "corrected" value. Trade-off: requires maintaining domain-specific validation rules per field type, which grows with the number of document types supported.
2. **Raw-extraction vs. normalized-value separation**: Always retain the raw, character-level extraction (before any model-side normalization or "cleanup") alongside the normalized value used downstream, so a hallucinated correction can be caught by comparing the two and rolling back to the raw read. Trade-off: doubles the storage/plumbing needed per field but is essential for auditability.
3. **Uncommon-but-valid value stress testing**: Specifically test extraction accuracy on documents containing statistically uncommon-but-valid values (leap-year dates, round-number-adjacent amounts like $99,987 near $100,000, unusual quantities) since these are exactly the values a language-prior-driven model is most likely to "correct" toward the common pattern. Trade-off: requires curating an adversarial test set beyond typical benchmark data.

### Detection & Response
1. **OCR-baseline cross-check flagging**: Run a traditional (non-generative) OCR pass alongside the VLM extraction and flag any case where the VLM's value diverges from the OCR baseline for the same region — divergence is a strong signal of language-prior-driven "correction" rather than faithful reading.
2. **Statistical outlier-toward-common-pattern detection**: Specifically monitor for a pattern where extracted values cluster suspiciously toward "common" values (round numbers, non-leap-year dates, standard quantities) at a higher rate than the true document population would predict — this signature indicates systematic attribute hallucination rather than random error.
3. **Field-level accuracy audits on adversarial samples**: Periodically audit extraction accuracy specifically on documents containing known uncommon-but-valid values, since aggregate accuracy metrics can look fine while this specific failure mode silently corrupts a minority of documents.

### Architecture Patterns
1. **Dual-path extraction with divergence gating**: Architect extraction to run both a generative (VLM) pass and a traditional deterministic OCR pass in parallel, gating any value where the two disagree to human review rather than trusting either path alone.
2. **Raw-value ledger with normalization as a separate, reversible layer**: Store raw extracted text immutably, with normalization/parsing (date formatting, currency parsing) implemented as a separate, versioned transformation layer that can be re-run or rolled back independent of re-extracting from the source document.
3. **Domain-rule validation gateway**: Insert a deterministic validation gateway between extraction and downstream consumption that every field must pass (valid calendar date, plausible amount range, valid checksum) before the value is allowed into production systems.

### Metrics
1. **ocr_vlm_divergence_rate**: Target: < 3% of fields show VLM/OCR divergence; Alert if > 8%
2. **domain_validation_failure_rate**: Target: < 1% of extracted fields fail domain validation; Alert if > 4%
3. **common_value_clustering_ratio**: Target: track as baseline vs. expected population distribution; Alert if extracted-value distribution skews > 20% toward common/round values relative to ground truth distribution
4. **adversarial_sample_accuracy**: Target: > 95% accuracy on uncommon-but-valid value test set; Alert if < 85%

### Alerts
1. **OCR/VLM Divergence Spike** (P2): Condition - divergence rate between VLM and OCR baseline exceeds 8% for a document source. Action: Route affected documents to human review, investigate whether a specific field type or template is driving the divergence.
2. **Domain Validation Failure Spike** (P1): Condition - domain validation failure rate exceeds 4% for a field type. Action: Halt automatic acceptance for that field, route to human review, investigate root cause (template change vs. model regression).
3. **Adversarial Accuracy Regression** (P2): Condition - accuracy on the uncommon-but-valid test set drops below 85%. Action: Treat as a model/prompt regression signal even if aggregate production accuracy looks unaffected; investigate before next deployment.

## Universal Pattern Reference

This is a domain-specific implementation of the universal pattern:
**[Hallucination: Attributes (Cross-Cutting)](../../../cross-cutting/accuracy/goals/output-accuracy/failures/hallucination-attribute.md)**

The universal pattern covers why models hallucinate object attributes. This variant focuses on **document processing** where VLMs "correct" extracted field values toward common patterns (e.g., rounding numbers, normalizing dates).

### Related Domain Variants
- [Vision: Attribute Hallucination](../../../vision-and-images/goals/visual-hallucination/failures/attribute-hallucination.md) — Hallucinated colors, sizes, materials in object detection

### Related Base Pattern
- [Hallucination: Base Mechanism](../../../cross-cutting/accuracy/goals/output-accuracy/failures/hallucination-base-mechanism.md) — Universal root cause of all hallucinations

---

## References

- [Hallucination of Multimodal LLMs Survey](https://arxiv.org/html/2404.18930v2) - Attribute hallucination types
- [Why LLMs Hallucinate More on Enterprise Documents](https://www.adlibsoftware.com/news/why-llms-hallucinate-more-on-enterprise-documents) - Value correction errors
- [IDP Accuracy Reckoning 2026](https://idp-software.com/news/idp-accuracy-reckoning-2026/) - Validation strategies
