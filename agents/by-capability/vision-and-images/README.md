# Vision & Image Understanding

Agents that process, generate, or reason over images face unique failure modes distinct from text-only or OCR-based agents. These patterns cover visual hallucination, spatial reasoning errors, multi-image reconciliation, generated-image quality, and adversarial robustness.

## Goals

| Goal | Description | Patterns |
|------|-------------|----------|
| [Visual Hallucination](goals/visual-hallucination/) | Detecting/preventing false objects, attributes, or scenes | In progress |
| [Spatial Reasoning](goals/spatial-reasoning/) | 3D/2D relationships, bounding boxes, relative positioning | In progress |
| [Multi-Image Understanding](goals/multi-image-understanding/) | Reconciling information across multiple images | In progress |
| [Generation Artifacts](goals/generation-artifacts/) | Quality drift, consistency, safety in generated images | In progress |
| [Adversarial Robustness](goals/adversarial-robustness/) | Defense against adversarial perturbations and edge cases | In progress |

**Status**: ~40 patterns planned

## Key Challenges

1. **Training Data Imbalance**: Vision models overfit to salient features; rare objects hallucinated
2. **Spatial Blindness**: Vision transformers struggle with spatial relationships and object localization
3. **Multi-Image Fusion**: LLMs can't reliably reconcile conflicting info across multiple images
4. **Generation Collapse**: Iterative refinement of generated images degrades quality
5. **Adversarial Vulnerability**: Small perturbations fool vision-based agent decisions

## Common Evaluation Metrics

- False positive rate (hallucinated objects per 1k images)
- Spatial error metrics (IoU, bounding box accuracy)
- Multi-image reconciliation accuracy
- Generated image quality (FID, LPIPS) over iterative loops
- Adversarial robustness (certified perturbation bounds)
