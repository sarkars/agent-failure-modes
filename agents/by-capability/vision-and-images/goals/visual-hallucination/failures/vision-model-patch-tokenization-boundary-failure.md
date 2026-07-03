# Vision Model Patch Tokenization Boundary Failure

## Issue: Vision-language models misinterpret visual boundaries because patch tokenization (dividing images into 14×14 or 16×16 pixel blocks) misaligns with semantic boundaries; objects split across patches create corrupted representations

**Frequency**: Common

**Symptoms**
- Objects split across patch boundaries are misidentified or unrecognized
- Model fails to detect edges, lines, or boundaries that align with patch edges
- High-contrast boundaries (white/black) at patch edges are ignored or hallucinated
- Model detects parts of an object but not the whole (e.g., sees half a face)
- Same object detected correctly when repositioned within patches

**Root Cause**
Vision transformers tokenize images by dividing them into fixed-size patches (typically 14×14 or 16×16 pixels). Each patch is treated as a token. When visual features (edges, lines, object boundaries) fall between patches, the model has incomplete information about that feature. Subsequent transformer layers can't reconstruct the edge because information is split across tokens. This is a hard limitation of patch-based tokenization, not a model hallucination issue.

**Examples**

### Example 1: Line Detection Across Patch Boundary
```
Image: Vertical white line dividing the image (1px thick, high contrast)
Line position: Falls exactly at patch boundary between two 16×16 patches
Model asked: "Describe the main line in this image"
Model response: "I don't see a clear line. The image appears to have slight color variations"
Actual: Clear vertical line dividing the image
Root cause: Patch boundary splits line; each patch sees half the line or noise
```

### Example 2: Face Recognition Split Across Patches
```
Image: Face positioned such that eyes are in one patch, mouth in adjacent patch
Model asked: "Identify this person's emotional expression"
Model response: "Unable to clearly identify facial expression"
Actual: Clear happy expression (smiling)
Root cause: Patches misaligned with facial features; insufficient context per patch
```

### Example 3: Document Text at Patch Boundary
```
Image: OCR of document; word boundary at patch edge
Text: "IMPORTANT" (split as "IMPORT-" and "ANT" across patches)
Model asked: "What is the key word in this document?"
Model response: "I see fragments but can't make out the word clearly"
Actual: Clear word "IMPORTANT"
Impact: Document OCR fails to extract critical keywords
Root cause: Patch boundary splits word; patches have incomplete character sequences
```

### Example 4: Medical Image Lesion Detection
```
Image: CT scan with lesion straddling patch boundary
Lesion size: 28×20 pixels; positioned to split across multiple patches
Model asked: "Identify any abnormalities in this scan"
Model response: "No clear abnormalities detected"
Actual: Clear lesion visible to radiologist
Impact: Missed diagnosis; significant patient safety risk
Root cause: Lesion fragments across patches; insufficient local context to recognize
```

**Key Statistics**
| Finding | Source |
|---|---|
| Patch misalignment creates visual blind spots | arXiv:2509.15435 (ORCA) |
| Objects spanning 2+ patches show 30-50% detection rate drop | arXiv:2509.15435 |
| High-contrast edges at patch boundaries are 60% likely to be missed | arXiv:2509.15435 |
| Repositioning object within patch improves detection | arXiv:2509.15435 |

---


## Test Scenario & Reproduction

### Scenario Setup
- Vision model with standard patch tokenization
- Test images with semantic boundaries at patch edges
- Objects split across patch boundaries
- No image preprocessing

### Trigger Mechanism
```
1. Create test image: object split exactly at patch boundary
2. Ask model object detection or counting question
3. Model tokenizes with patches at misaligned boundaries
4. Model struggles to recognize split object
5. Compare to unaligned version
```

### Expected Failure State
- Object recognition fails when split at patch boundary
- Same object recognized correctly when not at boundary
- Model output shows incomplete/fragmented object
- Boundary misalignment causes systematic errors

### Mitigation Validation Protocol
**Test Checklist:**
- [ ] Reproduce: Object at boundary causes recognition failure
- [ ] Apply mitigation (overlay grid lines, upscale)
- [ ] Re-run → object recognized despite boundary
- [ ] Test with multiple object types

**Success Criteria:**
- Object recognition consistent across boundary positions
- No systematic failures at patch boundaries
- Accuracy >95% regardless of boundary alignment

## Mitigation Strategies

1. **Patch-Aware Image Composition**
   - Manually position critical visual features to fall within patch centers (not boundaries)
   - Pad images so important content is >8 pixels from patch edges
   - Requires knowledge of model's patch size (typically 14-16 pixels)

2. **Multi-Scale Processing**
   - Process image at multiple resolutions (1x, 0.5x, 2x)
   - Model patch size stays fixed, but relative feature position changes
   - Combine results: if feature detected at 2+ scales, confidence higher
   - Trade-off: 2-3x compute cost

3. **Boundary-Aware Prompting**
   - Add instruction: "Pay attention to edges and lines, especially at image boundaries"
   - Some models have internal attention mechanisms that can be directed
   - Minimal compute overhead; often improves detection by 10-20%

4. **Overlapping Crops**
   - Divide image into overlapping patches (50% overlap)
   - Run detection on each crop separately
   - Merge detections, preferring features detected in multiple crops
   - Trade-off: 4x compute for full coverage

5. **Use Vision Models with Smaller Patches**
   - Some models use 8×8 or variable patch sizes
   - Better granularity for detecting small features
   - Check model architecture; not all models support this
   - May require retraining or fine-tuning

6. **Structural Verification**
   - After vision model detection, verify with OCR (for text), edge detection (for lines), or object bounding box (for shapes)
   - Vision model gives semantics; structural analysis verifies boundaries
   - Combine signals for robust detection

### Metrics
- Detection rate for features at patch boundaries vs. patch centers
- Sensitivity to object position (should be independent of patch alignment)
- False negative rate for high-contrast boundaries
- Compute cost of mitigation (multi-scale, overlapping crops)

### Alerts
- Detection changes significantly when image is reprojected → P2 (patch sensitivity)
- Boundary features missed but center features detected → P2 (patch misalignment)
- Medical/critical domain with patch-boundary misses → P1 (safety risk)

---

## Related Patterns
- [Vision Model Grid Cell Counting Failure](./vision-model-grid-cell-counting-failure.md) — Specific instance: counting fails due to patch misalignment
- [Confident Fabrication](../../../../../cross-cutting/accuracy/goals/output-accuracy/failures/confident-fabrication.md) — Model may hallucinate entire objects to fill patch gaps
- [Semantic Similarity Retrieval Misses Structural Attributes](../../../../../by-capability/knowledge-retrieval/goals/retrieval-relevance/failures/semantic-similarity-retrieval-misses-structural-attributes.md) — Related: structural attributes lost in embeddings

---

## References

- [ORCA: An Agentic Reasoning Framework for Hallucination and Adversarial Robustness in Vision-Language Models](https://arxiv.org/abs/2509.15435) - Documents patch tokenization boundary failures
- [Steal the Patch Size: Adversarially Manipulate Vision-Language Models](https://arxiv.org/abs/2607.00174) - Adversarial exploitation of patch vulnerability
- [A Survey on Agentic Multimodal Large Language Models](https://arxiv.org/abs/2510.10991) - Comprehensive survey including patch-related failures
