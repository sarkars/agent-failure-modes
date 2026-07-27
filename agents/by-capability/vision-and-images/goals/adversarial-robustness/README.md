# What Are the Most Common Adversarial and Robustness Failures in Vision AI Models?

**Vision models lose accuracy when input images deviate from the conditions they were trained on — whether that deviation is a deliberately crafted adversarial perturbation, ordinary JPEG compression, unfamiliar lighting, low resolution, an out-of-distribution object, or an unfamiliar rotation.** The common mechanism across all six patterns is that convolutional and transformer vision architectures have no built-in invariance to compression, lighting shift, resolution loss, rotation, adversarial perturbation, or distributional novelty; robustness has to be trained in explicitly (via augmentation, adversarial training, or auxiliary detectors) or the model degrades — sometimes gracefully, sometimes as a sharp accuracy cliff, and in the adversarial and OOD cases, with unchanged or even increased confidence.

## Key Takeaways

- 6 failure patterns cover a spectrum from deliberate attack (adversarial perturbation) to ordinary deployment drift (compression, lighting, resolution, rotation) to a structural blind spot (out-of-distribution inputs).
- Adversarial perturbations imperceptible to humans (ε=8/255 L∞ budget) drop accuracy from 95%+ clean to 10-50% adversarial, and 60-80% of adversarial examples transfer across different model architectures.
- Out-of-distribution blindness is arguably the most dangerous pattern in adversarial robustness: baseline OOD detection AUROC is only 60-75%, and 80-90% of OOD examples still receive >50% model confidence — the model has no "I don't know" mechanism.
- Every adversarial-robustness pattern shares the same two-part mitigation shape: augment training data to cover the nuisance variable (compression level, lighting range, rotation angle, adversarial budget), then add a runtime detector or ensemble that flags inputs falling outside the trained-for range rather than trusting a single point prediction.

## Scope

- **Deliberate attack surface** — [adversarial-perturbation](failures/adversarial-perturbation.md). Imperceptible, intentionally crafted noise that exploits brittle decision boundaries in high-dimensional models; the only pattern in adversarial robustness driven by an adversary rather than natural deployment drift.
- **Capture/encoding drift** — [compression-sensitivity](failures/compression-sensitivity.md), [low-resolution-failure](failures/low-resolution-failure.md), [lighting-color-shift](failures/lighting-color-shift.md), [rotation-perspective-variance](failures/rotation-perspective-variance.md). Ordinary, non-adversarial ways real-world images differ from curated training sets — codec artifacts, downsampling, illumination, and viewing angle — each causing graceful-to-severe accuracy degradation rather than a sharp attack.
- **Distributional blind spot** — [ood-blindness](failures/ood-blindness.md). Not a corruption of a known class but the absence of any known class at all; the model has no mechanism to recognize "this doesn't match anything I was trained on" and defaults to a confident wrong label.

## When Adversarial Robustness Matters

- A vision model's decisions feed safety-critical or autonomous actions (traffic-sign classification, collision avoidance, robotic grasping) where a single high-confidence wrong prediction has physical consequences
- Production input quality is heterogeneous or uncontrolled relative to training data — mobile-captured images, varying lighting environments, network-compressed video streams, or camera angles the training set didn't cover
- The deployment domain can present genuinely novel object classes or scenes not represented in any training distribution, and the system needs to reject or escalate rather than force a classification

## Cross-Pattern Insight

Across all six patterns, the fix is never "use a better pretrained model" alone — it is architectural. Every mitigation section converges on the same two-stage recipe: (1) train-time augmentation that explicitly exposes the model to the nuisance range it will see in production (adversarial examples at a fixed perturbation budget, JPEG at multiple quality factors, illumination across a color-temperature range, rotations across the full circle, synthetic OOD samples), and (2) a runtime layer — confidence thresholds keyed to detected input quality, ensemble voting, or a dedicated anomaly/OOD detector — that treats a prediction outside the validated envelope as suspect rather than authoritative. Patterns that skip stage two (trusting a single softmax confidence score) are exactly the ones where confidence stays high while accuracy collapses.

## Frequently Asked Questions

### Is adversarial robustness only about deliberate attacks?
No. Only [adversarial-perturbation](failures/adversarial-perturbation.md) involves an adversary; the other five patterns in adversarial robustness — compression, low resolution, lighting shift, rotation/perspective, and OOD blindness — are ordinary consequences of deploying a vision model outside the exact conditions of its training data.

### Is out-of-distribution blindness a robustness failure or an accuracy failure?
Because the failure mode isn't "wrong answer with appropriately low confidence" — baseline models assign >50% confidence to 80-90% of OOD examples. The model isn't uncertain about an unfamiliar input; it's confidently wrong, which is what makes [ood-blindness](failures/ood-blindness.md) dangerous in ways a calibrated low-confidence error would not be.

### Do adversarial-robustness patterns compound with each other?
Yes. A compressed, poorly lit, rotated photo of a genuinely novel object combines four of adversarial robustness's six patterns at once, and the mitigations are not mutually exclusive — augmentation for compression, lighting, and rotation can be applied in the same training pipeline, while OOD and adversarial detectors can run as parallel runtime checks on the same inference call.

### Which pattern has the most transferable mitigation architecture?
Ensemble-based detection. [adversarial-perturbation](failures/adversarial-perturbation.md), [ood-blindness](failures/ood-blindness.md), and [rotation-perspective-variance](failures/rotation-perspective-variance.md) all converge independently on running multiple models or multiple transformed views of the same input and requiring agreement before accepting a prediction — the same pattern applied to three different root causes.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Adversarial Perturbation](failures/adversarial-perturbation.md) | Imperceptible crafted noise flips predictions via brittle, high-dimensional decision boundaries |
| [Compression Sensitivity](failures/compression-sensitivity.md) | JPEG/WebP artifacts differ statistically from uncompressed training images, eroding fine detail |
| [Lighting & Color Shift](failures/lighting-color-shift.md) | Illumination is learned as a feature rather than treated as a nuisance variable, so models overfit to training-set lighting |
| [Low-Resolution Failure](failures/low-resolution-failure.md) | Downsampling destroys detail the model's receptive fields depend on, causing cliffs below training resolution |
| [Out-of-Distribution Blindness](failures/ood-blindness.md) | Softmax always outputs a class distribution; there is no built-in mechanism to reject unknown inputs |
| [Rotation & Perspective Variance](failures/rotation-perspective-variance.md) | CNNs lack rotational invariance (only approximate equivariance), so canonical-view training fails to generalize to rotated or skewed views |

**Total: 6 patterns**

## Related Goals

- [Visual Hallucination](../visual-hallucination/) — confidently wrong outputs driven by training-data statistics rather than input corruption
- [Spatial Reasoning](../spatial-reasoning/) — geometric and positional reasoning errors, a distinct failure surface from the appearance-level robustness issues here
- [Generation Artifacts](../generation-artifacts/) — degradation in models that produce images rather than classify or detect within images
