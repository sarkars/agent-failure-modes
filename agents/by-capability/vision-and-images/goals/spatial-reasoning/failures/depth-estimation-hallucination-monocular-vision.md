# Depth Estimation Hallucination: Monocular Vision Failure

## Issue: Vision models fail to accurately estimate depth from single images; hallucinate depth cues when monographic features (shadows, perspective, texture) are ambiguous or misleading

**Frequency**: Common

**Symptoms**
- Model estimates object depth significantly different from actual 3D positioning
- Errors increase when depth cues conflict (e.g., size suggests close, perspective suggests far)
- Ambiguous images (minimal shadows, flat lighting, uniform texture) show 30-50% depth error rates
- Same object in different lighting/angles produces inconsistent depth estimates
- Model expresses high confidence despite producing contradictory depth estimates
- Model "hallucinates" depth structure for featureless regions (e.g., flat wall)

**Root Cause**
Vision models estimate depth from monocular (single image) cues: relative size, perspective lines, texture gradients, shadows, occlusion. When images have minimal depth cues (flat lighting, uniform texture, no shadows, frontal view), model must infer depth from learned priors. Learned priors (training data) may hallucinate depth structure (assuming 3D shape where image is actually flat). Confidence remains high because model's reasoning appears sound ("perspective lines suggest depth"); actual error is in depth cue extraction.

**Examples**

### Example 1: Autonomous Driving Distance Estimation
```
Scene: Car ahead on flat road with minimal shadow, overcast lighting
Monographic cues: Size suggests ~30 meters; no perspective lines; flat lighting
Model estimates: "Vehicle at 50 meters" (confidence 92%)
Actual distance: 20 meters
Impact: Collision avoidance system fails; incorrect braking pressure
Root cause: Model overestimated distance due to flat lighting eliminating shadow cue
```

### Example 2: Robotics Manipulation Task
```
Scene: Object on white table under bright, shadowless lighting
Monocular cues: Object size; no texture gradients; no shadows; frontal camera
Model estimates: "Object 15cm above table" (confidence 88%)
Actual height: 2cm (object lies flat on table)
Impact: Robot gripper positioned too high; misses object entirely
Root cause: Model hallucinated 3D height; learned prior assumed objects are 3D, not flat
```

### Example 3: Medical Imaging (CT to 3D Reconstruction)
```
Scene: CT scan slice with minimal variation in intensity (homogeneous region)
Monographic cues: None (2D scan slice is inherently flat)
Model estimates: "Structure has significant 3D depth" 
Actual: Homogeneous region; no structure
Impact: 3D reconstruction artifact; false findings
Root cause: Model hallucinated depth from noise; learned that variation = structure
```

### Example 4: 3D Scene Reconstruction from Single Photo
```
Scene: Flat painting/artwork on wall, photographed straight-on
Monocular cues: Flat texture; no shadows; no perspective; frontal view
Model estimates: "Relief sculpture with 5cm depth variation"
Actual: Completely flat artwork
Impact: 3D model incorrectly shows relief; museum exhibit reconstruction wrong
Root cause: Model learned that art objects are 3D; hallucinated depth from texture
```

**Key Statistics**
| Finding | Source |
|---|---|
| Monocular depth estimation error: 20-50% in ambiguous scenes | arXiv:2103.02175 |
| Errors correlate with minimal depth cues (flat lighting, uniform texture) | arXiv:2103.02175 |
| Model confidence unchanged despite depth errors | arXiv:2103.02175 |
| Hallucinated depth in featureless regions: 60-80% occurrence | arXiv:2103.02175 |

---


## Test Scenario & Reproduction

### Scenario Setup
- Monocular vision model (single image, no stereo)
- Test images with ambiguous depth cues
- Model trained to estimate 3D from 2D
- No ground truth depth for comparison

### Trigger Mechanism
```
1. Provide 2D image with depth ambiguity
2. Model estimates depth map
3. Hallucinate plausible but incorrect depth
4. Multiple interpretations exist (model picks wrong)
5. No depth ground truth to verify
```

### Expected Failure State
- Depth estimates inconsistent with image content
- Impossible 3D reconstruction from hallucinated depth
- Model expresses high confidence in incorrect depth
- Errors largest in ambiguous regions

### Mitigation Validation Protocol
**Test Checklist:**
- [ ] Reproduce: Depth hallucinations on ambiguous images
- [ ] Apply mitigation (multi-view consistency, stereo where possible)
- [ ] Re-run → depth estimates more plausible
- [ ] Compare to ground truth depth where available

**Success Criteria:**
- Depth estimates consistent with image geometry
- Errors reduced in ambiguous regions
- 3D reconstruction plausible from estimated depth

## Mitigation Strategies

1. **Multi-View Depth Confirmation**
   - Don't estimate depth from single image
   - Capture 2-3 images from different angles
   - Triangulate depth; confirm consistency across views
   - Trade-off: Requires multiple camera captures; increases latency

2. **Active Depth Sensing Fallback**
   - Use monocular for initial estimate
   - For critical regions, verify with active sensing (LIDAR, structured light, time-of-flight)
   - Monocular + active fusion provides robust depth
   - Trade-off: Requires additional hardware; cost increase

3. **Depth Cue Confidence Scoring**
   - Score confidence in depth cues: high if shadows present, perspective clear, texture rich
   - If cue score <threshold: Don't trust monocular estimate; flag for manual verification
   - Example: Flat lighting → cue score 20% → flag region as uncertain
   - Prevents high-confidence hallucinations in ambiguous scenes

4. **Consistency Checking Across Frames**
   - In video/sequence: depth should vary smoothly with motion
   - Sudden depth jumps despite smooth object motion → hallucination detected
   - Use optical flow to predict expected depth; flag deviations
   - Trade-off: Requires video context (not single image)

5. **Learned Uncertainty Quantification**
   - Train model to output depth + uncertainty estimate
   - Don't use predictions with high uncertainty
   - Uncertainty high in featureless regions → signals hallucination risk
   - More robust than confidence score (which is often miscalibrated)

6. **Domain-Specific Priors**
   - For specific domains (driving, robotics), encode domain knowledge
   - Example: In driving, assume flat road (no arbitrary vertical structures)
   - Example: In robotics, assume objects are on table surface (known plane)
   - Priors constrain hallucinations to realistic space

### Metrics
- Depth estimation error: |estimated_depth - actual_depth| / actual_depth
- Error by cue richness: Track separately for high-cue vs low-cue scenes
- Confidence calibration: % of high-confidence predictions that are wrong
- Hallucination rate: % of regions where depth is hallucinated

### Alerts
- Depth estimation >30% error → P2 (significant error)
- Low depth cue confidence + high depth estimate → P2 (possible hallucination)
- Depth changes rapidly despite smooth object motion → P2 (inconsistency)
- Critical domain (driving, medical) with uncertain depth → P1 (safety risk)

---

## Related Patterns
- [Confident Fabrication](../../../../../cross-cutting/accuracy/goals/output-accuracy/failures/confident-fabrication.md) — High confidence despite depth hallucination
- [Vision Model Patch Tokenization Boundary Failure](../../../vision-and-images/goals/visual-hallucination/failures/vision-model-patch-tokenization-boundary-failure.md) — Related: missing depth cues
- [Spatial Reasoning Failures in 3D](./spatial-reasoning-failures-in-3d-environments.md) — Related: geometric reasoning

---

## References

- [Depth Estimation Benchmarks](https://arxiv.org/abs/2103.02175) - Monocular depth error analysis
- [3D Object Detection from 2D Images](https://arxiv.org/abs/2103.00633) - Depth inference in 3D detection
- [ORCA: An Agentic Reasoning Framework for Hallucination and Adversarial Robustness](https://arxiv.org/abs/2509.15435) - Hallucination in vision reasoning
- [A Survey on Agentic Multimodal Large Language Models](https://arxiv.org/abs/2510.10991) - Multimodal depth reasoning failures
