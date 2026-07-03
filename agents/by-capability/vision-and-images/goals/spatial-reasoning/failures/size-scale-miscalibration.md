# Size/Scale Miscalibration: Absolute Dimensions Failure

## Issue: Vision models correctly identify objects but estimate their absolute size (mm, cm, meters) incorrectly; errors range 2x-10x when no reference object is visible; relative sizing also fails when all objects are unfamiliar

**Frequency**: Common

**Symptoms**
- Model estimates object size with high confidence but 3-5x error
- Errors increase when no reference object is visible (no scale cue)
- Errors increase for unfamiliar objects (model can't use memorized sizes)
- Same object size depends on image context (presence/absence of reference objects)
- Errors concentrated in images without explicit scale markers (rulers, coins, people)
- Frontal-view, distance-known images show <10% error; contextless images show 50%+ error

**Root Cause**
Estimating absolute size from 2D image requires knowing viewing distance (or having reference objects). Model trained on diverse images with implicit size distributions. Model learns: "This object looks like X; objects that look like X are typically Y size". But without distance cue or reference, true size is ambiguous from image alone. Model defaults to learned priors (average object size). Model confident because its reasoning is sound ("object A looks like a human-hand-sized object → 5cm"); actual error comes from wrong prior or missing distance information.

**Examples**

### Example 1: Geological Survey - Rock Size Estimation
```
Scene: Geological survey photo; isolated rock, no scale reference
Model task: "Estimate rock diameter for geological classification"
Model estimate: "Rock is 15cm diameter" (confidence 85%)
Actual: Rock is 2.5 meters diameter (boulders don't fit in typical photo frame context)
Impact: Rock misclassified; geological survey data wrong; expensive remediation
Root cause: Model assumed "medium rock" size (learned prior); no distance cue to correct it
```

### Example 2: Autonomous Drone Obstacle Detection
```
Scene: Drone aerial view; objects on ground without scale reference
Object: Power line post ahead
Model size estimate: "Post diameter ~5cm" (height estimate: 4 meters)
Actual: Post diameter 30cm (height 10 meters)
Model decision: "Object is thin; safe to pass at 2 meters altitude"
Impact: Drone hits post; crash; mission failure
Root cause: Aerial view lacks scale; model underestimated post size by 6x
```

### Example 3: Medical Imaging - Lesion Size
```
Scene: CT scan of lung with lesion, no visual scale marker
Model measurement: "Lesion is 3mm across"
Model diagnosis: "Small benign lesion; recommend observation"
Actual: Lesion is 25mm across (serious malignancy)
Impact: Serious cancer missed; patient diagnosis delayed months
Root cause: No scale reference in image; model defaulted to small-lesion prior
```

### Example 4: Retail Inventory - Package Dimension
```
Scene: Product photo; isolated box, no reference object
Model size estimate: "Box dimensions 30cm × 20cm × 15cm"
Actual: Box dimensions 3cm × 2cm × 1.5cm (miniature collectible, not full-size product)
Impact: Shipping container wrong size; product damaged; customer return
Root cause: Model assumed standard product size; no visual scale to correct estimate
```

**Key Statistics**
| Finding | Source |
|---|---|
| Size estimation error without reference: 2x-10x deviation | arXiv:2108.04930 |
| Accuracy improves dramatically with scale reference (coin, ruler, person) | arXiv:2108.04930 |
| Unfamiliar objects: 40-60% error; familiar objects: <10% error | arXiv:2108.04930 |
| Model confidence unchanged despite size error | arXiv:2108.04930 |

---


## Test Scenario & Reproduction

### Scenario Setup
- Vision model for object size/scale estimation
- Test images with size reference ambiguity
- Multiple possible interpretations of scale
- No explicit size context provided

### Trigger Mechanism
```
1. Provide image: small object in foreground, large in background
2. Ask model object size estimation
3. Model estimates dramatically wrong size
4. Ambiguity in scale makes multiple answers plausible
5. Model picks implausible interpretation
```

### Expected Failure State
- Object size vastly over/underestimated
- Size estimates inconsistent with image context
- Model expresses high confidence in wrong size
- Multiple valid interpretations but model chooses worst

### Mitigation Validation Protocol
**Test Checklist:**
- [ ] Reproduce: Size estimation off by 10x+
- [ ] Apply mitigation (depth + size relation, reference objects)
- [ ] Re-run → size estimates more plausible
- [ ] Provide explicit scale references

**Success Criteria:**
- Size estimates consistent with spatial context
- Errors reduced to <2x in magnitude
- Multi-scale consistency achieved

## Mitigation Strategies

1. **Explicit Scale References**
   - Include scale marker in image (ruler, coin, reference object of known size)
   - Model measures relative size; computes absolute size from reference
   - Most reliable method when scale marker available
   - Trade-off: Requires deliberate inclusion of reference; may not be available

2. **Camera Intrinsic Parameters + Distance Estimation**
   - Use camera intrinsic parameters (focal length, sensor size)
   - Estimate viewing distance from object size + image position
   - Compute absolute size from geometry: size = f × object_height / distance
   - Trade-off: Requires accurate distance estimation; can propagate errors

3. **Contextual Size Priors**
   - If other objects are visible, use them as implicit scale references
   - Example: If person is visible, estimate their height (1.7m), use as scale
   - Refine object size estimate based on spatial relationships
   - Trade-off: Requires recognizing reference objects; may not always be present

4. **Uncertainty Quantification for Scale**
   - Output size estimate + uncertainty range
   - High uncertainty (large range) indicates scale ambiguity
   - Don't use high-uncertainty size estimates for critical decisions
   - Example: "Object is 5cm ± 15cm" → uncertainty too high; requires verification

5. **Stereo/Multi-View Size Verification**
   - Capture stereo pair or multiple views from different distances
   - Triangulate actual object size from multiple viewpoints
   - Trade-off: Requires multiple images; provides definitive size

6. **Domain-Specific Size Constraints**
   - For known objects, encode typical size ranges
   - Example: "Coins are typically 15-30mm"; "Human heads are 15-20cm"
   - Reject size estimates outside known ranges; flag as errors
   - Trade-off: Only works for objects with known size distributions

### Metrics
- Absolute size error: |estimated_size - actual_size| / actual_size
- Error by context: Separate accuracy for images with vs without scale references
- Familiar vs unfamiliar: Track separately for known vs novel objects
- Confidence calibration: % of high-confidence size estimates that are wrong
- Scale ambiguity: Uncertainty range of size estimates

### Alerts
- Size estimate without scale reference → P2 (verify size)
- High-confidence size estimate differs by >50% from reference → P1 (critical error)
- Contextless image with critical size requirement → P1 (manual measurement needed)
- Unfamiliar object + size estimate → P2 (low confidence inherent)

---

## Related Patterns
- [Depth Estimation Hallucination](./depth-estimation-hallucination-monocular-vision.md) — Related: size requires depth knowledge
- [Confident Fabrication](../../../../../cross-cutting/accuracy/goals/output-accuracy/failures/confident-fabrication.md) — High confidence + size error
- [Attribute Recognition Under Lighting Variation](../../../../../by-capability/vision-and-images/goals/visual-attribute-detection/failures/attribute-recognition-under-lighting-variation.md) — Related: attribute estimation under conditions

---

## References

- [Attribute Recognition Under Lighting Variation](https://arxiv.org/abs/2108.04930) - Scale sensitivity analysis
- [ORCA: An Agentic Reasoning Framework](https://arxiv.org/abs/2509.15435) - Geometric reasoning failures
- [A Survey on Agentic Multimodal Large Language Models](https://arxiv.org/abs/2510.10991) - Scale reasoning in multimodal systems
- [Confidence Calibration in Vision Models](https://arxiv.org/abs/2303.11807) - Scale estimation confidence
