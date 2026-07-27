# What Are the Most Common Visual Hallucination Failures in AI Agents?

**Vision-language models hallucinate objects, attributes, and entire scenes because they optimize for confident, contextually-plausible output rather than for grounding every claim in visible pixels — when evidence is weak, ambiguous, or architecturally unavailable (patch tokenization boundaries, rare-class underrepresentation, salient distractors), the model's learned prior about "what's typically here" overrides what's actually in the frame, and it reports the prior with the same high confidence as a correct detection.** Three of the ten patterns in visual hallucination are domain-specific instances of universal cross-cutting hallucination mechanisms; the other seven document vision-specific root causes — from patch-tokenization architecture to multi-step reasoning cascades — that don't have a non-vision analogue.

## Key Takeaways

- 10 patterns span four mechanisms: what gets hallucinated (objects/attributes/scenes), why certain inputs trigger it (salience, training-data imbalance, rarity), architectural blind spots unique to patch-based vision transformers, and how a single small hallucination compounds through downstream reasoning.
- Confidence is a poor hallucination signal throughout visual hallucination: object hallucinations average 72% confidence despite being wrong, vision models are typically miscalibrated by 20-40 percentage points overall, and 5-15% of predictions are wrong despite carrying >80% confidence.
- Rare-class and salience biases are measurable and directional: objects making up <1% of training data are hallucinated as false positives 40% more often than common objects, and high-saturation/high-contrast distractors drive 25-35% of false positives in industrial QC settings.
- Patch tokenization is a hard architectural limit, not a training deficiency: objects or text spanning 2+ patch boundaries show a 30-50% detection-rate drop, and grid/count tasks on small cells show >20% error specifically at cell sizes below 24px — the grid-cell/patch-boundary mechanism is a distinct root cause from the statistical-prior hallucinations elsewhere in visual hallucination.

## Scope

- **Core hallucination types** — [object-hallucination](failures/object-hallucination.md), [attribute-hallucination](failures/attribute-hallucination.md), [scene-hallucination](failures/scene-hallucination.md). The three most common outputs of vision hallucination — a nonexistent object, a wrong property (color/size/material) on a real object, or an entire fabricated scene context — each with its own cross-cutting canonical pattern (see below) and vision-specific triggers.
- **Statistical root causes** — [salience-bias](failures/salience-bias.md), [training-data-leakage](failures/training-data-leakage.md), [rare-object-false-positive](failures/rare-object-false-positive.md). The training-data properties that make hallucination more or less likely for a given input: visually salient but semantically irrelevant features, memorized dataset-specific spurious correlations, and long-tail class imbalance.
- **Architectural blind spots** — [vision-model-grid-cell-counting-failure](failures/vision-model-grid-cell-counting-failure.md), [vision-model-patch-tokenization-boundary-failure](failures/vision-model-patch-tokenization-boundary-failure.md). Failures rooted specifically in how vision transformers tokenize images into fixed-size patches (14×14 or 16×16 pixels) — semantic content that falls across a patch boundary is genuinely lost to the model, not just statistically deprioritized, making the grid-cell-counting and patch-tokenization patterns mechanistically distinct from the prior-driven hallucinations elsewhere in visual hallucination.
- **Confidence and propagation** — [confidence-miscalibration](failures/confidence-miscalibration.md), [multimodal-hallucination-cascade-across-reasoning-chain](failures/multimodal-hallucination-cascade-across-reasoning-chain.md). Why hallucinations carry unwarranted confidence, and how a single small hallucinated detail (a misread word, a wrong color) compounds through a multi-step agentic reasoning chain into a confidently wrong final conclusion.

## When Visual Hallucination Matters

- An agent takes an autonomous physical or transactional action based on a single vision-model detection — a robot gripper attempting to pick up a hallucinated object, a sorting system routing by a hallucinated attribute, an evacuation system trusting a hallucinated occupancy scene
- A vision-language model's output feeds into further reasoning steps by other agents (diagnosis, financial recommendation, incident escalation) where an early hallucination has no natural point of correction before downstream agents build on it as fact
- The input domain has known long-tail or salience characteristics — industrial QC with visually distracting labels, wildlife/rare-object detection, or any deployment where the production data distribution diverges from the curated training distribution

## Cross-Pattern Insight

Three patterns in visual hallucination — [object-hallucination](failures/object-hallucination.md), [attribute-hallucination](failures/attribute-hallucination.md), and [confidence-miscalibration](failures/confidence-miscalibration.md) — are explicitly marked in their own files as domain-specific implementations of universal cross-cutting patterns (`hallucination-object`, `hallucination-attribute`, and `hallucination-confidence-miscalibration`, all rooted in a shared `hallucination-base-mechanism` in `cross-cutting/accuracy`), with sibling domain variants documented for document-processing and knowledge-retrieval. That shared lineage matters operationally: the same universal mitigations (confidence thresholding, ensemble cross-checks, human-in-the-loop routing for low-confidence output) apply whether the hallucination surfaces in a vision pipeline, a document-extraction pipeline, or a RAG answer. What's unique to the vision instantiation is the input-side triggers — salience, patch-boundary loss, rare-class imbalance — that don't have an equivalent in text-only domains. The [multimodal-hallucination-cascade-across-reasoning-chain](failures/multimodal-hallucination-cascade-across-reasoning-chain.md) pattern shows why catching hallucination at the vision layer specifically (rather than downstream) matters most: once a hallucinated detail enters a reasoning chain, each subsequent step tends to increase confidence in the false premise rather than questioning it, so the cheapest point to intervene is the original vision-model call, not any later step.

## Frequently Asked Questions

### What's the difference between object hallucination and rare-object false positives?
[object-hallucination](failures/object-hallucination.md) is the general phenomenon of detecting anything not present in the image (15-25% of models in cluttered scenes); [rare-object-false-positive](failures/rare-object-false-positive.md) is a specific, measured driver of it — classes with <1% training frequency are hallucinated 40% more often than common classes, because the model learns weak, spuriously-generalized features for underrepresented classes.

### Is patch-tokenization boundary failure a form of hallucination or a separate problem?
Patch-tokenization boundary failure is grouped in visual hallucination because the pattern produces hallucination-like symptoms (missed or fabricated content), but the root cause is different from the other patterns here: [vision-model-patch-tokenization-boundary-failure](failures/vision-model-patch-tokenization-boundary-failure.md) is a hard information-loss limit of fixed-size patch tokenization, not a statistical-prior overreach. An object split across a 16×16 patch boundary genuinely lacks the pixel information needed for correct classification — no amount of confidence calibration fixes that; only repositioning, multi-scale processing, or overlapping crops do.

### What keeps confidence high even when a vision model is hallucinating?
Per [confidence-miscalibration](failures/confidence-miscalibration.md), models are trained to optimize for accuracy, not calibration, and softmax naturally produces high probabilities — there's no learned distinction between "correct with strong evidence" and "correct with weak evidence." The lack of that distinction is why the confidence signal alone is an unreliable filter across every visual-hallucination pattern; a 95% confidence score can mean the same thing whether the underlying detection is genuine or hallucinated.

### How does a single hallucinated detail become a costly downstream decision?
Per [multimodal-hallucination-cascade-across-reasoning-chain](failures/multimodal-hallucination-cascade-across-reasoning-chain.md), each downstream agent in a reasoning chain treats the prior step's output as ground truth rather than a claim to verify, and confidence tends to increase (not decrease) at each step even though the entire chain is grounded in one upstream misperception — the documented examples show the cascade escalating from a misread chart or screenshot to unnecessary chemotherapy, a lost $50M deal, or an unnecessary production failover.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Attribute Hallucination](failures/attribute-hallucination.md) | Model defaults to the statistically typical attribute (color/size/material) when lighting or occlusion makes the true attribute ambiguous |
| [Confidence Miscalibration](failures/confidence-miscalibration.md) | Models optimize for accuracy, not calibration, so confidence stays high (miscalibrated by 20-40 points) regardless of true detection uncertainty |
| [Multimodal Hallucination Cascade Across Reasoning Chain](failures/multimodal-hallucination-cascade-across-reasoning-chain.md) | A small initial VLM misperception is treated as fact by downstream reasoning steps, which amplify confidence in it rather than questioning it |
| [Object Hallucination](failures/object-hallucination.md) | Statistical priors about "what's typically in this context" override weak or absent visual evidence, especially in clutter or low resolution |
| [Rare Object False Positive](failures/rare-object-false-positive.md) | Long-tail training-data imbalance produces weak, spuriously-generalized features for underrepresented classes, inflating their false-positive rate |
| [Salience Bias](failures/salience-bias.md) | Model learns shortcut correlations with visually salient features (bright color, high contrast) instead of true object shape/category |
| [Scene Hallucination](failures/scene-hallucination.md) | Free-form scene captioning amplifies the model's prior about typical scene composition, fabricating plausible context (people, activity) absent from the image |
| [Training Data Leakage](failures/training-data-leakage.md) | Model memorizes spurious dataset-endemic correlations (e.g., "grass in background") and hallucinates the correlations even when production data lacks that context |
| [Vision Model Grid Cell Counting Failure](failures/vision-model-grid-cell-counting-failure.md) | Patch tokenization misaligns with small grid-cell boundaries, causing systematic miscounts especially below 24px cell size |
| [Vision Model Patch Tokenization Boundary Failure](failures/vision-model-patch-tokenization-boundary-failure.md) | Fixed-size patch tokenization genuinely loses information for objects, edges, or text spanning a patch boundary |

**Total: 10 patterns**

## Related Goals

- [Spatial Reasoning](../spatial-reasoning/) — several spatial patterns (occlusion, depth hallucination) explicitly cross-link back to visual hallucination's confident-fabrication mechanism when hallucinating hidden or ambiguous 3D structure
- [Multi-Image Understanding](../multi-image-understanding/) — context-aggregation-error is the multi-image-specific case of the same hallucinate-rather-than-admit-uncertainty mechanism covered here for single images
- [Adversarial Robustness](../adversarial-robustness/) — out-of-distribution blindness shares the same confidently-wrong-with-no-visual-basis failure shape as object/scene hallucination, but is triggered by unfamiliar input distributions rather than statistical priors on familiar ones
