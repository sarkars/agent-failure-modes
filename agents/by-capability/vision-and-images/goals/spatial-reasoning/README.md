# What Are the Most Common Spatial-Reasoning Failures in Vision AI Models?

**Vision models get spatial relationships wrong because 2D image projection is fundamentally lossy for 3D properties — depth, scale, occlusion, and viewing angle all collapse into ambiguous pixel patterns that a model must resolve using learned statistical priors rather than genuine geometric reasoning, and those priors fail whenever a scene departs from the "typical" arrangements seen in training.** Spatial reasoning is the largest goal in vision-and-images (14 patterns) because spatial reasoning fails at every stage of the pipeline: localizing an object precisely, inferring its depth or 3D shape, reasoning about what's hidden behind another object, correcting for viewing angle, judging its absolute size, and staying consistent when several images or a video sequence are involved.

## Key Takeaways

- 14 failure patterns span four mechanism clusters — localization/attention, depth/3D reconstruction, occlusion, and viewpoint/scale/relational reasoning — making spatial reasoning the largest single goal in the vision-and-images category.
- Confidence does not track accuracy anywhere in spatial reasoning: models express 85-95% confidence on hallucinated depth, size, and occluded-structure estimates that are wrong by 2x-10x or more.
- Complexity compounds error multiplicatively: simple frontal, unoccluded scenes show <10% spatial-reasoning error, but complex scenes combining occlusion, non-frontal angles, and multiple objects show 40-60%+ error rates.
- Absolute measurement (depth in meters, size in cm, volume) is far less reliable than relative measurement (is A closer than B, is A bigger than B) — relative depth judgments run ~70% accurate versus 40-60% for absolute depth, and size estimates without a visible reference object are off by 2x-10x.

## Scope

- **Localization & Attention** — [bounding-box-errors](failures/bounding-box-errors.md), [spatial-attention-bias](failures/spatial-attention-bias.md). Errors in precisely where an object is within a single frame — box regression accuracy is orthogonal to classification accuracy, and models have an implicit positional bias toward the image center inherited from architecture and photographer-biased training data.
- **Depth & 3D Reconstruction** — [depth-estimation-failure](failures/depth-estimation-failure.md), [depth-estimation-hallucination-monocular-vision](failures/depth-estimation-hallucination-monocular-vision.md), [3d-reasoning-collapse](failures/3d-reasoning-collapse.md), [spatial-reasoning-failures-in-3d-environments](failures/spatial-reasoning-failures-in-3d-environments.md). Failures in inferring 3D structure — depth, volume, containment, above/below — from 2D input, where monocular depth cues (shadows, perspective lines, texture gradients) are inherently ambiguous and the model fills gaps with learned priors rather than admitting uncertainty.
- **Occlusion** — [occlusion-mishandling](failures/occlusion-mishandling.md), [occlusion-reasoning-failures](failures/occlusion-reasoning-failures.md). Failures specifically triggered by partially hidden objects: detection accuracy collapses below 40% once occlusion exceeds 50%, and models confidently hallucinate the hidden portion's structure, color, or even miscount separate fragments as one object or one object as several.
- **Viewpoint, Scale & Relational Position** — [perspective-blindness](failures/perspective-blindness.md), [perspective-distortion-misunderstanding](failures/perspective-distortion-misunderstanding.md), [scale-confusion](failures/scale-confusion.md), [size-scale-miscalibration](failures/size-scale-miscalibration.md), [relative-position-confusion](failures/relative-position-confusion.md), [multi-image-spatial-inconsistencies](failures/multi-image-spatial-inconsistencies.md). The largest cluster: errors in recognizing objects from unusual angles, mistaking perspective projection for actual object deformation, misjudging absolute or relative object size, confusing left/right or containment relationships, and — across multiple images or camera angles of the same scene — producing 3D reconstructions that contradict each other.

## When Spatial Reasoning Matters

- A robotic or physical system must grasp, navigate around, or manipulate objects based on vision-derived position, depth, or size estimates — grasp failures, collisions, and misjudged clearances trace directly back to spatial-reasoning patterns
- A task depends on correctly handling partial visibility — cluttered bins, shelved inventory, crowded scenes, or any domain where the object of interest is not fully unoccluded and frontal
- Multiple images, camera angles, or video frames of the same scene must be reconciled into one consistent 3D understanding — multi-camera perception, photogrammetry/3D reconstruction, or sequential medical imaging

## Cross-Pattern Insight

The unifying theme across all 14 patterns is that 2D-to-3D inference is an underdetermined inverse problem, and every vision model attempting 2D-to-3D inference resolves that underdetermination with a learned prior instead of flagging the ambiguity. A flat, shadowless CT slice "must" have depth because the training distribution taught the model that structure implies variation; a small object without a reference "must" be an average size because the training distribution is dominated by average-sized objects; a partially hidden motor "must" have an ordinary interior because visible fragments statistically continue in the most probable way. The mitigation strategies converge accordingly, regardless of which of the 14 patterns is in play: don't trust a single monocular/single-view estimate for anything safety-critical (add stereo, multi-view, active sensing, or domain-specific geometric constraints), and separate confidence for the visible-evidence portion of an estimate from the extrapolated/hallucinated portion, since collapsing both confidence types into one score is exactly what makes spatial-reasoning errors invisible until the errors cause a failure downstream.

## Frequently Asked Questions

### How is depth estimation split across four different patterns in spatial reasoning?
Because "depth fails" breaks down into distinguishable sub-mechanisms with different mitigations: [depth-estimation-failure](failures/depth-estimation-failure.md) covers the general monocular-ambiguity problem, [depth-estimation-hallucination-monocular-vision](failures/depth-estimation-hallucination-monocular-vision.md) focuses specifically on hallucinating depth structure in featureless/flat regions, [3d-reasoning-collapse](failures/3d-reasoning-collapse.md) covers volume/shape inference rather than distance, and [spatial-reasoning-failures-in-3d-environments](failures/spatial-reasoning-failures-in-3d-environments.md) covers relational 3D claims (above/below/inside) built on top of those depth estimates.

### What's the difference between perspective-blindness and perspective-distortion-misunderstanding?
[perspective-blindness](failures/perspective-blindness.md) is a recognition failure — the model can't identify the object at all from an unfamiliar angle (accuracy drops from 95% frontal to 20% upside-down). [perspective-distortion-misunderstanding](failures/perspective-distortion-misunderstanding.md) is a reasoning failure one step further — the model does recognize the object but misinterprets the perspective-induced foreshortening as actual physical deformation (calling a normal box "damaged" because it looks trapezoidal from an angle).

### Are scale-confusion and size-scale-miscalibration the same pattern?
No. [scale-confusion](failures/scale-confusion.md) covers confusing objects at different physical scales that look visually similar (a toy car mistaken for a real one, since texture/color features are scale-invariant). [size-scale-miscalibration](failures/size-scale-miscalibration.md) is specifically about estimating an object's absolute dimensions (mm/cm/meters) with no visible reference object present, which produces 2x-10x errors even for objects the model correctly identifies.

### How much does occlusion alone degrade spatial-reasoning accuracy?
Substantially and non-linearly. Per [occlusion-mishandling](failures/occlusion-mishandling.md), accuracy stays above 95% at 0-20% occlusion, drops to 60-80% at 20-50%, and falls below 40% past 50% occlusion — and per [occlusion-reasoning-failures](failures/occlusion-reasoning-failures.md), the model's confidence does not fall proportionally, producing exactly the high-confidence/low-accuracy gap that makes occlusion dangerous in safety-critical pipelines.

## Patterns

| Pattern | Mechanism |
|---|---|
| [3D Reasoning Collapse](failures/3d-reasoning-collapse.md) | Single-image models trained for classification never learn 3D volume/shape, only surface texture, so grasp-relevant volume estimates are wrong 40-60% of the time |
| [Bounding Box Errors](failures/bounding-box-errors.md) | Localization is a regression task orthogonal to classification; coarse feature maps and imprecise training annotations produce 10-15% box-size error |
| [Depth Estimation Failure](failures/depth-estimation-failure.md) | Monocular depth is inherently ambiguous without stereo/temporal cues; models fall back on size-based priors that fail on atypical scale combinations |
| [Depth Estimation Hallucination (Monocular Vision)](failures/depth-estimation-hallucination-monocular-vision.md) | When shadows, texture, and perspective cues are minimal, the model hallucinates plausible depth structure instead of reporting ambiguity |
| [Multi-Image Spatial Inconsistencies](failures/multi-image-spatial-inconsistencies.md) | Each image is reconstructed independently with no cross-view consistency constraint, so the same object's position/size contradicts across views |
| [Occlusion Mishandling](failures/occlusion-mishandling.md) | Training data underrepresents occluded objects, so detection accuracy collapses (<40%) once occlusion exceeds 50% |
| [Occlusion Reasoning Failures](failures/occlusion-reasoning-failures.md) | Models hallucinate hidden structure, color, or count from learned priors and stay confident despite having no visual basis for the hidden portion |
| [Perspective Blindness](failures/perspective-blindness.md) | Training data is biased toward frontal/canonical views, so recognition accuracy collapses for rotated, upside-down, or extreme-angle objects |
| [Perspective Distortion Misunderstanding](failures/perspective-distortion-misunderstanding.md) | Perspective-projection foreshortening is misread as physical object deformation, or converging parallel lines are misread as non-parallel geometry |
| [Relative Position Confusion](failures/relative-position-confusion.md) | Models learn statistical shortcuts about typical object arrangements instead of genuine relational reasoning, causing left/right and containment errors |
| [Scale Confusion](failures/scale-confusion.md) | Texture and color features used for recognition are scale-invariant, so models can't distinguish a miniature object from a full-size one |
| [Size/Scale Miscalibration](failures/size-scale-miscalibration.md) | Absolute size requires a distance or reference cue; without one, the model defaults to a learned "typical size" prior, causing 2x-10x errors |
| [Spatial Attention Bias](failures/spatial-attention-bias.md) | Convolutional architecture and center-composed training photos bias detection toward the image center, dropping to 20-40% accuracy at the corners |
| [Spatial Reasoning Failures in 3D Environments](failures/spatial-reasoning-failures-in-3d-environments.md) | Complex scenes with occlusion and non-frontal angles compound depth and relational errors, hitting 40-60% error versus <10% in simple frontal scenes |

**Total: 14 patterns**

## Related Goals

- [Visual Hallucination](../visual-hallucination/) — object/attribute/scene hallucination is a sibling concern; several spatial-reasoning patterns here explicitly cross-link to the cross-cutting confident-fabrication pattern shared with that goal
- [Multi-Image Understanding](../multi-image-understanding/) — multi-image-spatial-inconsistencies overlaps directly with the fusion and cross-image consistency failures cataloged there
- [Adversarial Robustness](../adversarial-robustness/) — rotation-perspective-variance covers the same viewing-angle sensitivity from a robustness/accuracy-metrics angle rather than a reasoning angle
