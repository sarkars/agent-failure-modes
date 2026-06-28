# 3D Reasoning Collapse

## Issue: Model Cannot Reason About 3D Structure from Single 2D Image

**Frequency**: Common

**Symptoms**
- Fails to infer 3D structure (height, depth, volume)
- Cannot determine if object fits in space
- Incorrect volume/size estimates for grasping
- No understanding of surface normals or geometry

**Root Cause**
3D reasoning from 2D images requires strong geometric priors and training on diverse 3D shapes. Most vision models trained on classification don't learn 3D structure — only surface texture and appearance. Single-image 3D reconstruction is inherently ambiguous without depth cues.

**Example**
```
Scenario: Robot trying to grasp object
Image: Tall, narrow vase
Model: Estimates volume ≈ small box (confuses height for depth)
Actual: Large volume vase; won't fit in gripper
Impact: Gripper jam, object breaks
```

**Key Statistics**
- 3D shape accuracy: 40-60% on ambiguous objects
- Size estimation error: ±30-50% for single-image depth
- Geometry hallucination: 15-20% of predictions describe impossible 3D shapes

---

## Mitigation Strategies

1. **3D Synthetic Training**: Train on 3D models (ShapeNet, ModelNet) with rendered images
2. **Multi-view Confirmation**: Use stereo or multiple angles when available
3. **Semantic Priors**: Use object category to constrain 3D hypotheses
4. **Conservative Estimates**: Always overestimate size/volume for safety

### Metrics
- Chamfer distance (predicted vs. GT point cloud)
- Volume estimation error
- Geometric plausibility (% predictions that describe impossible shapes)

### Alerts
- >20% geometric impossibilities → P2
- Volume error >40% → P2

---

## References

- [3D Object Detection from 2D Images](https://arxiv.org/abs/2103.00633)
- [Single-Image 3D Shape Reconstruction](https://arxiv.org/abs/2105.02999)
