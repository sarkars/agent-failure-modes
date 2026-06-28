# Occlusion Mishandling

## Issue: Model Fails to Reason About Occluded (Partially Hidden) Objects

**Frequency**: Very Common

**Symptoms**
- Object detection fails when partially covered
- Occlusion reasoning missing (doesn't predict hidden parts)
- High accuracy drop for >30% occlusion
- Fails at "behind" or "underneath" spatial reasoning

**Root Cause**
Training data under-represents occluded objects. Models learn surface-level patterns; they don't learn to infer invisible geometry. Occlusion is particularly hard because it requires understanding 3D structure and depth from 2D cues.

**Example**
```
Scenario: Robot reaching for objects on shelf
Image: Box partially hidden behind another box (70% visible, 30% occluded)

Model: Fails to detect box (0% accuracy)
Actual: Box is there, just partially hidden
Impact: Object left behind; task incomplete
```

**Key Statistics**
- 0-20% occlusion: >95% accuracy
- 20-50% occlusion: 60-80% accuracy
- >50% occlusion: <40% accuracy

---

## Mitigation Strategies

1. **Amodal Completion**: Train on synthetic occlusion; augment with partially-hidden objects
2. **Geometric Priors**: Add 3D reconstruction loss to learn occluded geometry
3. **Semantic Context**: Use object co-occurrence ("boxes often stacked") to predict hidden parts
4. **Conservative Detection**: Only accept detections with <30% occlusion margin

### Metrics
- Accuracy vs. occlusion percentage
- Amodal completion error (predicted hidden geometry vs. actual)

### Alerts
- Accuracy <50% for >30% occluded objects → P2

---

## References

- [Amodal Completion in Vision](https://arxiv.org/abs/2105.06378)
- [Occluded Object Detection in Robotics](https://arxiv.org/abs/2204.10281)
