# Visual Hallucination

Detecting and preventing false objects, attributes, or entire scenes that don't exist in input images.

## Universal Patterns (See Cross-Cutting)

These patterns have **universal canonical versions** in cross-cutting/accuracy that cover the general mechanism:

| Domain Pattern | Canonical Pattern |
|---|---|
| [Confidence Miscalibration](failures/confidence-miscalibration.md) | [Hallucination: Confidence Miscalibration](../../../../cross-cutting/accuracy/goals/output-accuracy/failures/hallucination-confidence-miscalibration.md) — Why hallucinated objects have high confidence |
| [Attribute Hallucination](failures/attribute-hallucination.md) | [Hallucination: Attributes](../../../../cross-cutting/accuracy/goals/output-accuracy/failures/hallucination-attribute.md) — False properties on detected objects |
| [Object Hallucination](failures/object-hallucination.md) | [Hallucination: Objects](../../../../cross-cutting/accuracy/goals/output-accuracy/failures/hallucination-object.md) — False objects detected in images |

See the canonical patterns for universal mitigation strategies. This page provides **vision-specific examples and implementations**.

---

## Failure Patterns

| Pattern |
|---------|
| [Object Hallucination](failures/object-hallucination.md) |
| [Attribute Hallucination](failures/attribute-hallucination.md) |
| [Scene Hallucination](failures/scene-hallucination.md) |
| [Salience Bias](failures/salience-bias.md) |
| [Confidence Miscalibration](failures/confidence-miscalibration.md) |
| [Training Data Leakage](failures/training-data-leakage.md) |
| [Rare Object False Positive](failures/rare-object-false-positive.md) |

**Total: 7 patterns**
