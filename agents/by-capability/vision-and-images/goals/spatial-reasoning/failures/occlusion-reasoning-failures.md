# Occlusion Reasoning Failures: Hallucinated Structure

## Issue: Vision models fail to correctly reason about occluded objects; assume objects have properties they can't see (like internal structure, color, or continuation behind occluding object)

**Frequency**: Common

**Symptoms**
- Model describes properties of objects it can't fully see (hallucinating unseen parts)
- Model is confident about occluded object features (high confidence + no visual basis)
- Model fails to recognize that two visible parts belong to same occluded object
- Model counts visible fragments separately, missing that they're one object
- Model describes objects as having features they don't actually have (hallucinated structure)
- Occlusion-heavy images (20%+ of objects partially hidden) show 40-60% error rates

**Root Cause**
Humans use experience and physics to infer hidden structure ("behind the wall is likely more wall, not a void"). Models train on images where most objects are visible. When objects are heavily occluded, model must infer unseen parts. Model's training data may have been biased: images with minor occlusions (10-20%) but complete information for reasoning. Heavy occlusions (50%+) are underrepresented. Model hallucinates based on learned priors (most probable continuation of visible parts).

**Examples**

### Example 1: Robotic Bin Picking - Hidden Component Recognition
```
Scene: Bin with objects; some partially hidden under others
Object: Motor with visible front panel (metal, rectangular, black)
Occlusion: Back of motor is hidden; motor shaft is hidden
Model reasoning: "Black metal rectangular object → likely a basic plastic-bodied motor"
Model confidence: "I can see the type and estimate weight"
Actual: Motor has large metal heat sink and copper windings on hidden side; much heavier
Impact: Robot gripper underpowers; motor drops during pickup
Root cause: Hallucinated structure for hidden side; confident about unseen components
```

### Example 2: Medical Image - Tumor Boundary Detection
```
Scene: CT scan; tumor partially outside field of view (off-screen)
Visible: 70% of tumor boundary; 30% extends beyond image edge
Model reasoning: "Tumor boundary curves smoothly; I can extrapolate the hidden 30%"
Model tumor size: 4.2cm diameter
Actual tumor: 6.8cm diameter (30% is much larger off-screen)
Impact: Surgical plan underestimates tumor size; incomplete resection
Root cause: Hallucinated continuation of tumor; confident about off-screen structure
```

### Example 3: Inventory Counting - Partial Box Visibility
```
Scene: Warehouse shelf; boxes partially stacked/occluded
Task: Count individual items visible
Model observation: "Box 1 visible, Box 2 visible (behind Box 1), Box 3 visible"
Model reasoning: "Visible boxes are 3; estimate total is 3"
Actual: Box 2 is actually 2 boxes stacked (not visible as two separate boxes); total is 4
Impact: Inventory undercount; stock management error
Root cause: Model failed to recognize two objects behind occlusion; counted as one
```

### Example 4: Autonomous Driving - Pedestrian Reasoning
```
Scene: Pedestrian partially visible behind parked car
Visible: Head and upper shoulders visible
Model reasoning: "Pedestrian upper half visible; confident about full body position"
Actual: Pedestrian is crouching (lower body is not where model extrapolated)
Model prediction: "Pedestrian at intersection at time T+2 seconds" (based on visible motion + hallucinated lower body)
Impact: Collision; vehicle doesn't brake in time (wrong predicted pedestrian position)
Root cause: Hallucinated body position from visible head motion
```

**Key Statistics**
| Finding | Source |
|---|---|
| Occlusion reasoning error: 40-60% when 30%+ of object is hidden | arXiv:2605.31354 |
| Model confidence unchanged despite occlusion | arXiv:2605.31354 |
| Fragment misidentification: Separate fragments of same object counted as 2-3 objects | arXiv:2605.31354 |
| Heavy occlusions underrepresented in training data | arXiv:2605.31354 |

---


## Test Scenario & Reproduction

### Scenario Setup
- Vision model with occlusion reasoning capability
- Test images with partially occluded objects
- Varying degrees of occlusion (25%-75%)
- Model must infer hidden parts

### Trigger Mechanism
```
1. Create test image: object 50% occluded by another object
2. Ask model: identify occluded object or complete structure
3. Model fails to infer structure correctly
4. Tries to describe visible parts only
5. Cannot reason about hidden portions
```

### Expected Failure State
- Occluded object misidentified or not identified
- Model refuses to speculate about hidden parts
- Cannot complete partially visible structure
- Occlusion reasoning degrades with occlusion percentage

### Mitigation Validation Protocol
**Test Checklist:**
- [ ] Reproduce: Occlusion reasoning fails >50% occlusion
- [ ] Apply mitigation (occlusion-aware training, inference)
- [ ] Re-run → occlusion handling improved
- [ ] Test at 25%, 50%, 75% occlusion

**Success Criteria:**
- Occluded objects identified correctly
- Partial structures reasoned about properly
- Accuracy remains >80% at 50% occlusion

## Mitigation Strategies

1. **Occlusion-Aware Confidence Reduction**
   - Identify occluded regions (use occlusion detection algorithms)
   - For properties of occluded objects: Reduce confidence by 50-70%
   - Don't use high-confidence estimates for hidden parts
   - Example: "Object color is blue (visible part), but hidden part unknown → confidence 20%"
   - Trade-off: Reduces usable information; requires explicit occlusion detection

2. **Fragment Linking & Continuation Estimation**
   - Identify visible fragments of partially occluded objects
   - Use motion, edge continuity, and appearance to link fragments
   - Estimate most likely continuation; flag estimation confidence as low
   - Trade-off: Complex computation; requires sophisticated fragment linking

3. **Physics-Based Occlusion Reasoning**
   - Encode physics constraints: objects have thickness, gravity applies, materials have consistency
   - Use constraints to validate inferred hidden structure
   - Example: "Visible front is metal → hidden side likely metal too"
   - But: Don't assume specific structure without evidence
   - Trade-off: Domain-specific; only works for constrained object types

4. **Multi-View Occlusion Bypass**
   - Capture images from different angles to see hidden parts
   - Process all views; aggregate information
   - Trade-off: Requires multiple images; not always possible

5. **Explicit Uncertainty for Occlusion**
   - Output structure estimates + uncertainty for each part
   - Separate confidence for visible vs extrapolated structure
   - Example: "Visible part: 95% confidence; extrapolated part: 30% confidence"
   - Don't combine confidences; treat separately
   - Trade-off: More complex output; requires training model to output per-part confidence

6. **Interactive Probing for Critical Occlusions**
   - For safety-critical decisions, use active sensing (robot moves object, changes angle)
   - Verify hidden structure before making decision based on extrapolation
   - Trade-off: Adds latency; requires active capability

### Metrics
- Occlusion detection accuracy: % of occluded regions correctly identified
- Hallucination rate: % of inferred hidden structure that's wrong
- Fragment linking accuracy: % of fragments correctly linked to same object
- Confidence calibration for occlusion: Confidence vs accuracy for extrapolated properties
- Error by occlusion percentage: Separate accuracy for 10%, 30%, 50%, 70% occlusion levels

### Alerts
- High-confidence estimate for occluded part → P2 (verify visible part only)
- Multiple visible fragments likely same object but model treats as separate → P2 (investigate)
- Heavy occlusion (>50%) + confidence estimate → P1 (manual verification required)
- Critical domain (surgery, driving, safety) + occlusion reasoning → P1 (use visible-only data)

---

## Related Patterns
- [Spatial Reasoning Failures in 3D](./spatial-reasoning-failures-in-3d-environments.md) — Related: inferring structure
- [Confident Fabrication](../../../../../cross-cutting/accuracy/goals/output-accuracy/failures/confident-fabrication.md) — High confidence about unseen parts
- [Vision Model Patch Tokenization Boundary](../../../vision-and-images/goals/visual-hallucination/failures/vision-model-patch-tokenization-boundary-failure.md) — Related: missing information at boundaries

---

## References

- [Diagnosing Failure Modes of Shared-State Collaboration in Resource-Constrained Visual Agents](https://arxiv.org/abs/2605.31354) - Occlusion in visual agents
- [Amodal Completion in Vision](https://arxiv.org/abs/2105.06378) - Inferring occluded structure
- [ORCA: An Agentic Reasoning Framework](https://arxiv.org/abs/2509.15435) - Occlusion reasoning failures
- [A Survey on Agentic Multimodal Large Language Models](https://arxiv.org/abs/2510.10991) - Occlusion handling in multimodal systems
