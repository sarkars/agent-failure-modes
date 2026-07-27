# What Are the Most Common Failure Modes in AI Agents That Process or Generate Images?

**AI agents that see or generate images fail in five distinct ways: they hallucinate content that isn't there, they misjudge spatial relationships like depth, scale, and occlusion, they lose consistency when reasoning across multiple images or video frames, they degrade in quality across iterative image generation, and they break down under adversarial, compressed, or out-of-distribution input.** Unlike document-processing failures — which are largely about misreading known text — vision-and-images failures are about a vision model's confident prior overriding weak or ambiguous visual evidence, whether that model is interpreting a photo, tracking objects across frames, or generating new pixels.

## Key Takeaways

- The category spans 5 goals and 43 failure patterns, ranging from single-image hallucination to multi-image consistency to generative-model degradation to robustness against corrupted or adversarial input.
- Confidence is an unreliable failure signal throughout the category: vision models are typically miscalibrated by 20-40 percentage points, and high-confidence wrong answers appear in every one of the five goals — hallucinated objects, hallucinated depth, hallucinated occluded structure, and adversarially-flipped classifications alike.
- Spatial Reasoning is the largest goal by far (14 of 43 patterns), reflecting that 2D-to-3D inference is the single hardest and most failure-prone capability a vision model attempts — depth, scale, occlusion, and viewpoint each introduce their own ambiguity that statistical priors resolve incorrectly.
- Architectural limits (patch tokenization boundaries) and statistical limits (rare-class imbalance, salience shortcuts, training-data memorization) are mechanistically distinct root causes that happen to produce the same symptom — a confidently wrong output — so the fix differs by pattern even when the symptom looks identical.

## Vision & Images Goals

| Goal | Covers | Patterns |
|------|--------|----------|
| [Visual Hallucination](goals/visual-hallucination/) | False objects, attributes, or scenes detected that aren't in the image; confidence miscalibration; patch-tokenization blind spots | 10 |
| [Spatial Reasoning](goals/spatial-reasoning/) | Depth, 3D structure, occlusion, scale, viewpoint, bounding-box localization, and relational position errors | 14 |
| [Multi-Image Understanding](goals/multi-image-understanding/) | Contradiction detection, identity/tracking across frames, and evidence fusion across multiple images | 6 |
| [Generation Artifacts](goals/generation-artifacts/) | Quality drift, semantic drift, identity/consistency loss, model collapse, and safety-filter bypass in generated images | 7 |
| [Adversarial Robustness](goals/adversarial-robustness/) | Adversarial perturbations, compression, lighting shift, low resolution, rotation, and out-of-distribution blindness | 6 |

**Total: 43 patterns**

## How the Goals Relate

The five vision-and-images goals address different points in a vision pipeline rather than a strict sequential pipeline. Adversarial Robustness governs whether the input image itself is trustworthy before any interpretation happens — compressed, poorly lit, adversarially perturbed, or genuinely novel inputs corrupt every downstream goal if unaddressed. Visual Hallucination and Spatial Reasoning both operate on a single image (or single frame) and are frequently intertwined — several Spatial Reasoning patterns (occlusion, depth hallucination) explicitly cross-link to the confident-fabrication mechanism documented in Visual Hallucination. Multi-Image Understanding sits one layer up, assuming single-image interpretation is basically sound and asking whether that interpretation stays consistent across several images or frames. Generation Artifacts is the mirror-image concern for models that produce pixels rather than interpret images, but shares failure shape with the other four (Consistency Failure is generation's version of Multi-Image Understanding's identity-tracking problem; Safety Filter Bypass shares its adversarial-prompt mechanism with Adversarial Robustness).

To localize an incident by symptom: a detected object/attribute/scene that isn't real → **Visual Hallucination**; a real object at the wrong depth, size, position, or behind an occluder → **Spatial Reasoning**; the same object described inconsistently across photos or video frames → **Multi-Image Understanding**; a generated image that degrades, drifts from its prompt, or loses subject identity across iterations → **Generation Artifacts**; accuracy that collapses under compression, unusual lighting, low resolution, rotation, or unfamiliar objects — with confidence that doesn't drop to match → **Adversarial Robustness**.

## Frequently Asked Questions

### What's the difference between visual hallucination and spatial reasoning failures?
Visual Hallucination is about content that doesn't exist at all — a fabricated object, attribute, or scene. Spatial Reasoning is about real content whose position, depth, scale, or occlusion state is misjudged. The two overlap where a model hallucinates hidden structure behind an occluder (a Spatial Reasoning pattern that explicitly borrows the confident-fabrication mechanism from Visual Hallucination) — see [Spatial Reasoning](goals/spatial-reasoning/) and [Visual Hallucination](goals/visual-hallucination/).

### What makes Spatial Reasoning have more than twice as many patterns as any other goal?
Because 2D-to-3D inference is underdetermined at every stage — precise localization, depth, 3D shape, occlusion, viewpoint correction, absolute/relative scale, and multi-view consistency are each separately failure-prone, and each requires a distinct mitigation (stereo confirmation, occlusion-aware confidence, perspective correction, reference-object scale cues). See [Spatial Reasoning](goals/spatial-reasoning/) for the full 14-pattern breakdown into four mechanism clusters.

### Can a single model fix all 43 patterns in vision-and-images?
No. The patterns split between input-robustness problems (Adversarial Robustness) that require augmentation and detection layers around the model, and reasoning-accuracy problems (the other four goals) that require architectural changes — multi-view fusion, confidence-per-claim tracking, and explicit consistency constraints — none of which are solved simply by scaling up or fine-tuning a single vision-language model.

### Which goal should a developer check first when a vision-based agent misbehaves?
Match the symptom to the goal using the routing list above. If the failure only appears on certain input conditions (low light, low resolution, compressed video, an unfamiliar object class), start with [Adversarial Robustness](goals/adversarial-robustness/) before assuming the model's reasoning itself is broken — many Spatial Reasoning and Visual Hallucination symptoms are actually downstream consequences of degraded input the model was never trained to handle.

## Related Categories

- [Document Processing](../document-processing/) — the most relevant sibling category: shares the same hallucination and confidence-miscalibration mechanisms, but scoped to text extraction and structured-document fields rather than open-world photos and scenes
- [Multi-Agent Systems](../multi-agent-systems/) — several patterns here (multimodal hallucination cascades, multi-camera spatial inconsistency) explicitly cross-link to multi-agent communication and handoff-reliability failures when vision output feeds a downstream agent chain
- [Cross-Cutting: Accuracy](../../cross-cutting/accuracy/) — the canonical, domain-general hallucination and confidence-miscalibration patterns that several goals in vision-and-images (Visual Hallucination in particular) implement as vision-specific variants
