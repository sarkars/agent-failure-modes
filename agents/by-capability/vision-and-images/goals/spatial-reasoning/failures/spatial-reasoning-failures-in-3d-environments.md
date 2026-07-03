# Spatial Reasoning Failures in 3D Environments

## Issue: Vision models fail to correctly reason about 3D spatial relationships (above/below, left/right, inside/outside, containment) from single or multiple images; errors increase with scene complexity and ambiguous viewing angles

**Frequency**: Common

**Symptoms**
- Model misidentifies spatial relationships (object A is "inside" container but actually outside)
- Errors concentrate on occluded objects (objects hidden from camera view)
- Non-frontal camera angles produce contradictory spatial reasoning
- Model reasons about positions it cannot see (hallucinating occluded structure)
- Complex scenes (multiple objects, partial occlusions) show 40-60% error rates
- Simple scenes (frontal view, clear visibility) show <10% error rates

**Root Cause**
Spatial reasoning requires mental 3D reconstruction from 2D projections. When objects are occluded, model must infer 3D positions from partial information. Model's 3D reconstruction learned from training data (biased toward common object arrangements). When actual 3D arrangement differs from training distribution (e.g., unusual stacking, non-standard orientations), model's inferred spatial relationships diverge from reality. Model can't verify its reasoning against unseen regions.

**Examples**

### Example 1: Robotic Manipulation in Cluttered Bin
```
Scene: Multiple objects in bin; some occluded by others
Camera: Top-down view (can't see beneath objects)
Model reasoning: "Red ball is inside the bin, blue cube is above the red ball"
Model action: Reach to remove blue cube (confident it's accessible)
Actual: Red ball is above blue cube (obstructed from top camera); blue cube unreachable
Impact: Robot reaches to wrong position; wastes grasp attempts; operation fails
Root cause: Model inferred spatial relationship it couldn't verify
```

### Example 2: Autonomous Vehicle in Complex Traffic
```
Scene: Multi-lane highway; vehicles partially occluded by trucks
Camera: Front-facing camera (limited side visibility)
Model reasoning: "Red car is in adjacent lane, 50m ahead"
Actual: Red car is in same lane as autonomous vehicle, 20m ahead (occluded by truck)
Model decision: Change lanes toward "empty" adjacent lane
Impact: Collision with vehicle in actual adjacent lane
Root cause: Misidentified spatial position of occluded vehicle
```

### Example 3: Inventory Management in Warehouse
```
Scene: Shelving unit with 5 levels; many items stacked, some occluded
Camera: Fixed angle (can't see behind items)
Model task: "Count items on shelf level 3"
Model reasoning: "I see 12 items on level 3; one item appears to be missing" (hallucinating empty space where occlusion exists)
Actual: 15 items on level 3; 3 are hidden behind level 2 items
Impact: Inventory miscount; ordering mistakes; stockouts
Root cause: Hallucinated spatial reasoning about occluded regions
```

### Example 4: Surgical Scene Understanding
```
Scene: Operating room; surgical instruments overlapping, partially hidden by drapes
Camera: Endoscopic view (very limited field of view)
Model reasoning: "Retractor is positioned above surgical site, ready for use"
Actual: Retractor is below surgeon's current working area (outside frame), not ready
Model suggestion: Proceed with next surgical step (assuming retractor is ready)
Impact: Surgical error; procedure delayed for repositioning
Root cause: Spatial relationship inferred without full scene visibility
```

**Key Statistics**
| Finding | Source |
|---|---|
| Spatial reasoning error: 40-60% in complex scenes; <10% in simple frontal views | arXiv:2605.31354 |
| Occlusion reasoning: 60%+ error rate when objects are partially hidden | arXiv:2605.31354 |
| Non-frontal angles: 30-40% increase in spatial reasoning errors | arXiv:2605.31354 |
| Hallucinated spatial relationships: 50-70% of errors involve inferring unseen regions | arXiv:2605.31354 |

---


## Test Scenario & Reproduction

### Scenario Setup
- 3D scene understanding model
- Test scenes with complex spatial relationships
- Objects occluded, overlapping, or ambiguous
- Model has limited 3D training data

### Trigger Mechanism
```
1. Provide 3D scene image with complex spatial layout
2. Ask model spatial reasoning question
3. Model fails to correctly infer 3D relationships
4. Compare to simpler scenes
5. Analyze error patterns
```

### Expected Failure State
- Spatial relationships incorrectly inferred
- Occlusion handling fails (can't infer hidden objects)
- Impossible 3D configurations described
- Relative positions wrong (left/right, near/far)

### Mitigation Validation Protocol
**Test Checklist:**
- [ ] Reproduce: Spatial reasoning errors on complex scenes
- [ ] Apply mitigation (3D scene graphs, explicit annotation)
- [ ] Re-run → reasoning accuracy improves
- [ ] Test on benchmark 3D datasets

**Success Criteria:**
- Spatial relationships inferred correctly
- Occlusion reasoning sound
- 3D configurations geometrically valid

## Mitigation Strategies

1. **Multi-View Spatial Verification**
   - Don't infer spatial relationships from single view
   - Capture images from multiple angles (3-4 viewpoints)
   - Compare spatial reasoning across views; only trust consistent inferences
   - Inconsistencies between views indicate hallucination
   - Trade-off: Requires multiple camera captures

2. **Occlusion-Aware Confidence Scoring**
   - Identify occluded objects; mark regions as "not directly visible"
   - For spatial reasoning about occluded objects: Reduce confidence by 50%+
   - Don't use high-confidence spatial reasoning for hidden objects
   - Example: "Ball position inferred from occlusion; confidence 30% (was 80%)"
   - Prevents confident reasoning about unseen structure

3. **Constraint-Based Reasoning**
   - Encode physical constraints: objects can't overlap, gravity applies, stacking rules
   - Use constraints to validate inferred spatial relationships
   - If inferred arrangement violates constraints: Flag as hallucination
   - Example: "Ball can't be 'inside' a closed box if box is sealed"

4. **Interactive Verification**
   - For critical spatial decisions, use active probing
   - Robot can gently push/probe object to verify position
   - Spatial reasoning updated based on actual response
   - Trade-off: Adds time; requires physical interaction capability

5. **Depth + Segmentation + Reasoning**
   - Combine three signals: depth map, instance segmentation, spatial reasoning
   - If all three agree on spatial relationship: High confidence
   - If they conflict: Hallucination detected; require additional verification
   - Redundancy catches errors individual models miss

6. **Learned Spatial Uncertainty**
   - Train model to output spatial relationship + uncertainty
   - Use uncertainty to identify hallucinations (high uncertainty = low confidence)
   - Don't rely on spatial reasoning with high uncertainty
   - More robust than single confidence metric

### Metrics
- Spatial relationship accuracy: % of spatial claims verified correct
- Error by complexity: Track separately for simple vs complex scenes
- Occlusion handling: Separate accuracy for visible vs partially visible objects
- Consistency across views: % agreement between spatial reasoning from different angles
- Hallucination rate: % of spatial claims about unseen regions

### Alerts
- Spatial reasoning about occluded object → P2 (possible hallucination)
- Spatial contradiction between views → P2 (inconsistency detected)
- Complex scene + high confidence spatial reasoning → P2 (verify)
- Critical domain (surgery, driving, manipulation) with spatial uncertainty → P1 (safety)

---

## Related Patterns
- [Depth Estimation Hallucination](./depth-estimation-hallucination-monocular-vision.md) — Related: inferring 3D from 2D
- [Occlusion Reasoning Failures](./occlusion-reasoning-failures.md) — Specific to occluded objects
- [Vision Model Patch Tokenization Boundary](../../../vision-and-images/goals/visual-hallucination/failures/vision-model-patch-tokenization-boundary-failure.md) — Related: missing structure

---

## References

- [Diagnosing Failure Modes of Shared-State Collaboration in Resource-Constrained Visual Agents](https://arxiv.org/abs/2605.31354) - Core reference; spatial reasoning in visual agents
- [The Vision Wormhole: Latent-Space Communication in Heterogeneous Multi-Agent Systems](https://arxiv.org/abs/2602.15382) - Multi-agent spatial coordination
- [MTA-Agent: An Open Recipe for Multimodal Deep Search Agents](https://arxiv.org/abs/2604.06376) - Multimodal spatial reasoning
- [ORCA: An Agentic Reasoning Framework](https://arxiv.org/abs/2509.15435) - Vision reasoning failures
