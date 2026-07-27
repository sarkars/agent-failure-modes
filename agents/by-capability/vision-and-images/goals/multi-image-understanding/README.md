# What Are the Most Common Multi-Image Understanding Failures in AI Agents?

**Vision models process images independently by default, so when a task requires reasoning across several images — the same object from different angles, consecutive video frames, or several imaging modalities — the model has no native mechanism to check consistency, maintain identity, or fuse conflicting evidence, and reasoning that would be correct on any single image breaks down across the set.** Multi-image understanding is a distinct failure surface from single-image hallucination or spatial error: the model can be accurate on every individual frame and still fail the moment two or more images need to be reconciled.

## Key Takeaways

- 6 patterns cover cross-image reasoning failure from three angles: detecting contradictions between images, maintaining identity/tracking across frames, and combining multiple images into a single coherent judgment.
- Baseline contradiction detection across images is only 30-50% accurate, with a further 10-20% false-positive rate on non-contradictions — cross-image consistency checking is unreliable in both directions.
- Object tracking degrades sharply under real-world conditions: ID switches run 0.1-0.5 per person per video and fragmentation (one object splitting into multiple tracks) affects 5-15% of tracks, worsening in crowded or occlusion-heavy scenes.
- Context aggregation is highly sensitive to missing information: accuracy drops from 90% with all images available to 65% with only half, and the model hallucinates unprovided information in 10-15% of cases rather than reporting uncertainty.

## Scope

- **Consistency and contradiction detection** — [image-contradiction](failures/image-contradiction.md). The model treats each image independently and doesn't flag when object properties reported across images logically conflict (e.g., an object reported red in one frame and blue in another).
- **Identity and tracking across frames** — [temporal-inconsistency](failures/temporal-inconsistency.md), [cross-image-reference-loss](failures/cross-image-reference-loss.md), [object-tracking-failure](failures/object-tracking-failure.md). Failures in maintaining that "the object in image or frame A is the same object as the object in image or frame B" — whether across video frames, across independently captured photos, or under occlusion in crowded scenes.
- **Fusion and aggregation** — [multi-frame-fusion-failure](failures/multi-frame-fusion-failure.md), [context-aggregation-error](failures/context-aggregation-error.md). Failures in combining multiple images' evidence into one output: naive fusion (averaging/concatenation) can produce a worse result than the single best input image, and models often hallucinate rather than admit that some of the expected evidence is missing.

## When Multi-Image Understanding Matters

- A task requires comparing or verifying consistency across images of the same subject — multi-angle product inspection, document/selfie identity verification, before/after comparison
- The pipeline processes video or a frame sequence and needs stable object identity over time — surveillance tracking, crowd monitoring, motion analysis
- A decision needs to be synthesized from multiple imaging sources or views where not all sources may be available at inference time — multi-modality medical imaging, multi-camera vehicle perception, multi-photo 3D reconstruction

## Cross-Pattern Insight

Every multi-image-understanding pattern traces back to the same architectural gap: standard vision models are built and trained to process one image at a time, so any property that should hold *across* images — consistency, identity, complete evidence — has to be imposed by an explicit multi-image architecture rather than assumed to emerge from single-image competence. The recurring mitigation families are (1) joint processing instead of independent per-image inference (multi-image fusion, learned attention-weighted fusion, joint 3D reconstruction), (2) explicit matching/tracking machinery borrowed from classical computer vision (Siamese networks, Kalman filters, Hungarian matching, optical flow), and (3) uncertainty tracking that lets the model represent "I haven't seen enough" instead of defaulting to a hallucinated or overconfident answer. Pipelines that simply run a single-image model N times and concatenate the outputs will reproduce every multi-image-understanding pattern.

## Frequently Asked Questions

### Does image-contradiction detection matter if each individual image is read correctly?
Because per-image accuracy says nothing about cross-image logical consistency. A model can correctly read "red" in image 1 and correctly read "blue" in image 2 of the same object and still fail the task if it never checks whether those two correct individual readings are compatible — that check is a separate capability the model doesn't have by default, per [image-contradiction](failures/image-contradiction.md).

### What's the difference between temporal-inconsistency and object-tracking-failure?
[temporal-inconsistency](failures/temporal-inconsistency.md) describes the general failure to treat frames as a continuous sequence (jittery positions, lost objects between frames); [object-tracking-failure](failures/object-tracking-failure.md) is the more specific, better-studied failure mode of ID switches and fragmentation, particularly under occlusion in crowded multi-object scenes, measured with tracking-specific metrics like MOTA and ID switches.

### Does adding more images always improve multi-image reasoning?
No — see [multi-frame-fusion-failure](failures/multi-frame-fusion-failure.md), where naive fusion (e.g., averaging three views) produced 75% accuracy versus 85% for the single best frame alone; only learned, confidence-weighted fusion (92%) beat the best single frame. Unweighted aggregation can dilute a good signal with noisy or misaligned inputs.

### How should a system handle a multi-image task when not all expected images are available?
Per [context-aggregation-error](failures/context-aggregation-error.md), the failure mode to design against is silent hallucination — the model claiming information that was never in the provided images (10-15% baseline rate) rather than degrading gracefully or asking for the missing image. Explicit context tracking (what's been seen vs. not) and calibrated uncertainty are the documented mitigations.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Context Aggregation Error](failures/context-aggregation-error.md) | Model can't track what it has/hasn't seen across images and hallucinates rather than reporting missing evidence |
| [Cross-Image Reference Loss](failures/cross-image-reference-loss.md) | No discriminative, viewpoint-invariant embedding to match the same object's identity across separate images |
| [Image Contradiction](failures/image-contradiction.md) | Independent per-image processing means logically conflicting properties across images go unflagged |
| [Multi-Frame Fusion Failure](failures/multi-frame-fusion-failure.md) | Naive fusion (averaging/concatenation) of misaligned or conflicting views can underperform the single best view |
| [Object Tracking Failure](failures/object-tracking-failure.md) | Frame-by-frame detection without motion/appearance modeling causes ID switches and track fragmentation, worst under occlusion |
| [Temporal Inconsistency](failures/temporal-inconsistency.md) | Frames analyzed independently ignore motion continuity, so object identity and position jitter or drop between frames |

**Total: 6 patterns**

## Related Goals

- [Spatial Reasoning](../spatial-reasoning/) — the 3D-consistency-across-views subset of spatial reasoning (see `multi-image-spatial-inconsistencies`) overlaps directly with the fusion failures here
- [Visual Hallucination](../visual-hallucination/) — context-aggregation-error's hallucination-of-missing-evidence is a multi-image-specific instance of the broader hallucination patterns cataloged there
- [Generation Artifacts](../generation-artifacts/) — consistency-failure in generated image sequences is the generative-model counterpart to identity loss across real images in multi-image understanding
