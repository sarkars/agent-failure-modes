# Multi-Image Spatial Inconsistencies: Conflicting 3D Reconstructions

## Issue: When given multiple images of same scene/object from different angles, vision models produce inconsistent spatial reasoning; 3D reconstruction conflicts across views; same object described differently depending on which image model processes first

**Frequency**: Common

**Symptoms**
- Object position described differently across two images of same scene
- Object size estimate differs 20-30% when processing different images
- Spatial relationships ("A is left of B") contradict between views
- 3D reconstruction from Image 1 contradicts reconstruction from Image 2
- Model reasoning doesn't account for multi-image consistency constraint
- Sequential processing: description of Image 1 influences Image 2 (context-dependent errors)

**Root Cause**
Vision models process images independently; each image generates independent 3D reconstruction. When processing multiple images sequentially, model doesn't enforce consistency between reconstructions. Models trained on single-image understanding; multi-image consistency is not optimized during training. Sequential processing means Image 1's reconstruction can influence Image 2's description (context effects); this can amplify inconsistencies if Image 1 error biases Image 2.

**Examples**

### Example 1: 3D Model Creation from Multiple Photos
```
User captures 8 photos of car from different angles for 3D model creation
Photo 1 (side view): Model estimates "Car width: 1.8m, length: 4.5m, height: 1.5m"
Photo 2 (front view): Model estimates "Car width: 1.9m, height: 1.6m"
Photo 3 (rear angle): Model estimates "Car length: 4.7m" (20cm difference from Photo 1)
Photo 4-8: Further inconsistencies

Result: 3D model is distorted; door spacing wrong; proportions off
Impact: 3D visualization looks unrealistic; manufacturing specs wrong
Root cause: Model processes each image independently; no consistency constraint
```

### Example 2: Autonomous Vehicle: Multi-Camera Obstacle Detection
```
Vehicle has 4 cameras (front, rear, left, right)
Scene: Pedestrian in intersection

Front camera image: Model detects "Pedestrian at position (x=2m, y=1m)"
Left camera image: Model detects "Pedestrian at position (x=-0.5m, y=1.5m)" (different coordinates!)
Right camera image: Model detects "Pedestrian at position (x=0m, y=1m)"
Rear camera image: "No pedestrian visible"

System receives 4 different position estimates; inconsistent
Impact: Vehicle can't triangulate true position; collision avoidance confused
Root cause: Models don't enforce multi-camera consistency
```

### Example 3: Medical Imaging - Tumor Tracking Across Slices
```
Doctor captures 12 consecutive CT slices of same tumor
Slice 1: Model measures "Tumor at (x=5, y=3, z=0), diameter 3cm"
Slice 2: Model measures "Tumor at (x=5.1, y=2.9, z=0.1), diameter 3.2cm"
Slice 3: Model measures "Tumor at (x=6.0, y=2.0, z=0.2), diameter 3.8cm" (inconsistent trajectory)
...

Result: Tumor center position estimated inconsistently across slices
Impact: Surgical planning based on inconsistent 3D position; wrong incision point
Root cause: Model processes each slice independently; no 3D continuity enforcement
```

### Example 4: Building Inspection - Structural Consistency
```
Inspector captures 15 photos of building from 3 angles for damage assessment
Angle 1 (south side): "Building wall is plumb (vertical)"
Angle 2 (west side): "Building wall is plumb (vertical)"
Angle 3 (southwest corner, 45°): "Building wall appears to lean 2° inward"

3D reconstruction combines these: Building appears to lean at corner (impossible)
Impact: Inspector thinks building is structurally compromised; recommends repairs
Root cause: Perspective inconsistency not resolved; model doesn't enforce 3D consistency
```

**Key Statistics**
| Finding | Source |
|---|---|
| Multi-image inconsistency: 20-40% of spatial relationships contradict across views | arXiv:2602.15382 |
| Sequential processing bias: Image 1 error influences Image 2 (15-25% error amplification) | arXiv:2602.15382 |
| Models don't enforce multi-view consistency | arXiv:2602.15382 |
| Triangulation from inconsistent estimates: 30-50% error in final 3D position | arXiv:2602.15382 |

---


## Test Scenario & Reproduction

### Scenario Setup
- Multi-image analysis (multiple photos of same scene)
- Images taken from different angles/times
- Model must maintain spatial consistency
- No explicit constraint on consistency

### Trigger Mechanism
```
1. Provide 2-3 images of same scene, different angles
2. Ask model questions about spatial relationships
3. Model gives inconsistent answers across images
4. Same object described differently in different images
5. Spatial relationships contradictory
```

### Expected Failure State
- Object positions inconsistent across images
- Same object identified differently in each image
- Spatial relationships contradictory
- No error detection of inconsistencies

### Mitigation Validation Protocol
**Test Checklist:**
- [ ] Reproduce: Multi-image inconsistencies evident
- [ ] Apply mitigation (consistency checking, multi-view reasoning)
- [ ] Re-run → consistent across images
- [ ] Verify geometric consistency

**Success Criteria:**
- Object positions consistent across views
- Same objects identified consistently
- Spatial relationships geometrically consistent

## Mitigation Strategies

1. **Multi-View Consistency Constraint**
   - Process all images jointly, not sequentially
   - Enforce consistency: 3D reconstruction must be consistent across all views
   - Use optimization to find 3D model that best explains all images
   - Trade-off: Requires joint processing; higher computational cost

2. **Temporal Continuity for Sequential Images**
   - If images are captured in sequence: impose continuity constraint
   - Object position should change smoothly between consecutive images
   - Flag sudden jumps in position/size as errors
   - Trade-off: Assumes smooth motion; fails for fast movements or occlusions

3. **Triangulation from Multiple Views**
   - Instead of independent per-view estimates, triangulate position from multiple views
   - Use camera geometry to compute consistent 3D position
   - Trade-off: Requires accurate camera calibration; geometry computation required

4. **Consensus Voting Across Views**
   - Process each image separately
   - Take median (not mean) of independent estimates across views
   - Median robust to outliers; one erroneous estimate doesn't dominate
   - Trade-off: Loses information; votes treat all views equally (not accounting for view quality)

5. **Learned Multi-View Representation**
   - Train model to process multiple images jointly
   - Learn implicit 3D representation that's consistent across views
   - Trade-off: Requires multi-view training data; model architecture changes

6. **Explicit Consistency Checking**
   - Compute per-image estimates independently
   - Then check: Do all estimates agree within tolerance?
   - If not: Flag as inconsistency; require manual review
   - Trade-off: Doesn't fix inconsistency; just detects it

### Metrics
- Multi-view consistency error: Max disagreement between views on same property
- Position estimate variance: Standard deviation of position across views
- Triangulation accuracy: Final 3D position vs ground truth
- View agreement percentage: % of properties that agree within 10% tolerance
- Sequential bias: Difference between joint vs sequential processing

### Alerts
- Position estimates differ by >10% across views → P2 (inconsistency detected)
- Spatial relationships contradict between images → P2 (manual verification)
- Sequential processing: Image 1 influences Image 2 estimates → P2 (enforce independence)
- Critical domain (medical, construction, manufacturing) + inconsistency → P1 (halt processing)

---

## Related Patterns
- [Spatial Reasoning Failures in 3D](./spatial-reasoning-failures-in-3d-environments.md) — Related: 3D consistency
- [The Vision Wormhole: Latent-Space Communication](../../../../../by-capability/multi-agent-systems/goals/communication-reliability/failures/vision-agent-communication-failure.md) — Multi-agent coordination
- [Confident Fabrication](../../../../../cross-cutting/accuracy/goals/output-accuracy/failures/confident-fabrication.md) — Confident about inconsistent data

---

## References

- [The Vision Wormhole: Latent-Space Communication in Heterogeneous Multi-Agent Systems](https://arxiv.org/abs/2602.15382) - Multi-view coordination
- [Diagnosing Failure Modes of Shared-State Collaboration in Resource-Constrained Visual Agents](https://arxiv.org/abs/2605.31354) - Multi-agent spatial consistency
- [ORCA: An Agentic Reasoning Framework](https://arxiv.org/abs/2509.15435) - Multi-view reasoning
- [A Survey on Agentic Multimodal Large Language Models](https://arxiv.org/abs/2510.10991) - Consistency in multimodal agents
