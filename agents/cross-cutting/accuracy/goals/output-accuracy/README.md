# Output Accuracy

Correctness of generated outputs

## Hallucination Family (Universal Mechanism + Domain Variants)

These patterns cover hallucination — the fundamental failure where models generate plausible but false content.

**Canonical (Universal) Patterns:**
| Pattern | Covers |
|---------|--------|
| [Hallucination: Base Mechanism](failures/hallucination-base-mechanism.md) | Universal LLM/vision hallucination root cause |
| [Hallucination: Confidence Miscalibration](failures/hallucination-confidence-miscalibration.md) | Why hallucinated content has high confidence |
| [Hallucination: Attributes](failures/hallucination-attribute.md) | False properties on correct objects |
| [Hallucination: Objects](failures/hallucination-object.md) | False objects/fields not in input |

**Domain-Specific Variants** (see also by-capability sections):
- Knowledge Retrieval: [Confidence Miscalibration](../../../by-capability/knowledge-retrieval/goals/answer-synthesis/failures/confidence-miscalibration.md)
- Document Processing: [Confidence Miscalibration](../../../by-capability/document-processing/goals/multimodal-reliability/failures/confidence-miscalibration.md), [Attribute Hallucination](../../../by-capability/document-processing/goals/multimodal-reliability/failures/attribute-hallucination.md), [Object Hallucination](../../../by-capability/document-processing/goals/multimodal-reliability/failures/object-hallucination.md)
- Vision & Images: [Confidence Miscalibration](../../../by-capability/vision-and-images/goals/visual-hallucination/failures/confidence-miscalibration.md), [Attribute Hallucination](../../../by-capability/vision-and-images/goals/visual-hallucination/failures/attribute-hallucination.md), [Object Hallucination](../../../by-capability/vision-and-images/goals/visual-hallucination/failures/object-hallucination.md)

---

## Other Failure Patterns

| Pattern |
|---------|
| [Algorithmic Discrimination](failures/algorithmic-discrimination.md) |
| [Bias Amplification](failures/bias-amplification.md) |
| [Confident Fabrication](failures/confident-fabrication.md) |
| [Content Fabrication](failures/content-fabrication.md) |
| [Domain Mismatch](failures/domain-mismatch.md) |
| [Entity Confusion](failures/entity-confusion.md) |
| [Extrapolation](failures/extrapolation.md) |
| [Inherited Errors](failures/inherited-errors.md) |
| [Source Misattribution](failures/source-misattribution.md) |
| [Verification Failure](failures/verification-failure.md) |

**Total: 15 patterns (4 canonical hallucination + 11 other)**
