# Vision and Images AI Agent Failures by Goal: 43 Patterns, Causes, and Fixes

**Vision and Images AI agents fail in 5 distinct ways, grouped by the goal each failure breaks.** Find the goal that matches what you are seeing, open its list, and use the fix on each pattern page.

## Key Takeaways

- 43 documented patterns across 5 goals; the most documented is [Spatial Reasoning](spatial-reasoning/) with 14.
- Each pattern page gives the symptoms, an example, the root cause, and mitigations.

## Vision and Images Goals

| Goal | When it fails | Patterns |
|---|---|---|
| [Adversarial Robustness](adversarial-robustness/) | When input images deviate from the conditions they were trained on — whether that deviation is a deliberately crafted adversarial perturbation, ordinary JPEG compression, unfamiliar lighting | 6 |
| [Generation Artifacts](generation-artifacts/) | Generated-image quality degrades over repeated generation or regeneration because generative models sample stochastically with no built-in mechanism to preserve quality, identity | 7 |
| [Multi Image Understanding](multi-image-understanding/) | When a task requires reasoning across several images — the same object from different angles, consecutive video frames, or several imaging modalities | 6 |
| [Spatial Reasoning](spatial-reasoning/) | Vision models get spatial relationships wrong because 2D image projection is fundamentally lossy for 3D properties — depth, scale, occlusion | 14 |
| [Visual Hallucination](visual-hallucination/) | When evidence is weak, ambiguous, or architecturally unavailable (patch tokenization boundaries, rare-class underrepresentation, salient distractors) | 10 |

**Total: 43 patterns**

## Frequently Asked Questions

### How is depth estimation split across four different patterns in spatial reasoning?

Because "depth fails" breaks down into distinguishable sub-mechanisms with different mitigations: [depth-estimation-failure](spatial-reasoning/failures/depth-estimation-failure.md) covers the general monocular-ambiguity problem, [depth-estimation-hallucination-monocular-vision](spatial-reasoning/failures/depth-estimation-hallucination-monocular-vision.md) focuses specifically on hallucinating depth structure in featureless/flat regions, [3d-reasoning-collapse](spatial-reasoning/failures/3d-reasoning-collapse.md) covers volume/shape inference rather than distance, and [spatial-reasoning-failures-in-3d-environments](spatial-reasoning/failures/spatial-reasoning-failures-in-3d-environments.md) covers relational 3D claims (above/below/inside) built on top of those depth estimates. See [Spatial Reasoning](spatial-reasoning/).

### What's the difference between object hallucination and rare-object false positives?

[object-hallucination](visual-hallucination/failures/object-hallucination.md) is the general phenomenon of detecting anything not present in the image (15-25% of models in cluttered scenes); [rare-object-false-positive](visual-hallucination/failures/rare-object-false-positive.md) is a specific, measured driver of it — classes with <1% training frequency are hallucinated 40% more often than common classes, because the model learns weak, spuriously-generalized features for underrepresented classes. See [Visual Hallucination](visual-hallucination/).

### Does regenerating an image multiple times improve quality?

No — the data shows the opposite. See [Generation Artifacts](generation-artifacts/).

## Related

- [Vision and Images overview](../)
- [All agent failure patterns](../../../)
