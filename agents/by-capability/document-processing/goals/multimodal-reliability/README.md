# Multimodal Reliability

Correctness and reliability of VLM/MLLM outputs for document processing and multimodal understanding.

## Universal Hallucination Patterns (See Cross-Cutting)

These patterns have **universal canonical versions** in cross-cutting/accuracy that cover the general mechanism:

| Domain Pattern | Canonical Pattern |
|---|---|
| [Confidence Miscalibration](failures/confidence-miscalibration.md) | [Hallucination: Confidence Miscalibration](../../../../cross-cutting/accuracy/goals/output-accuracy/failures/hallucination-confidence-miscalibration.md) — Why VLM extractions are overconfident |
| [Attribute Hallucination](failures/attribute-hallucination.md) | [Hallucination: Attributes](../../../../cross-cutting/accuracy/goals/output-accuracy/failures/hallucination-attribute.md) — VLMs "correct" values toward common patterns |
| [Object Hallucination](failures/object-hallucination.md) | [Hallucination: Objects](../../../../cross-cutting/accuracy/goals/output-accuracy/failures/hallucination-object.md) — VLMs invent fields that don't exist |

See the canonical patterns for universal mitigation strategies. This page provides **document-processing-specific examples and implementations**.

---

## Failure Patterns

| Pattern |
|---------|
| [Attribute Hallucination](failures/attribute-hallucination.md) |
| [Complex Tables](failures/complex-tables.md) |
| [Confidence Miscalibration](failures/confidence-miscalibration.md) |
| [Fabricated Content](failures/fabricated-content.md) |
| [Input Quality Gap](failures/input-quality-gap.md) |
| [Object Hallucination](failures/object-hallucination.md) |
| [Plausible Wrong Outputs](failures/plausible-wrong-outputs.md) |
| [Relational Hallucination](failures/relational-hallucination.md) |
| [Table Cell Omission](failures/table-cell-omission.md) |
| [Visual Degradation](failures/visual-degradation.md) |

**Total: 10 patterns**
