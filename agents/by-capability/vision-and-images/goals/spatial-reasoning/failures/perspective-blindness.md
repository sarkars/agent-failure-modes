# Perspective & Viewpoint Blindness

## Issue: Model Fails to Recognize Objects Viewed from Unusual Angles or Perspectives

**Frequency**: Common

**Symptoms**
- Object unrecognizable when rotated (e.g., upside-down or sideways)
- High variance in accuracy across viewpoints
- Confidence drops dramatically for non-frontal views
- Gripper failures on objects in awkward orientations

**Root Cause**
Training data biases toward frontal/canonical views. Models don't generalize well to extreme rotations or viewpoints not well-represented in training. Convolutional features capture local patterns that vary dramatically with viewpoint.

**Example**
```
Training: 95% frontal views of chairs
Production: Chair lying on side, upside-down

Model: Fails to detect upside-down chair (accuracy: 20% vs. 95% for frontal)
Impact: Robot can't identify object in its current orientation
```

**Key Statistics**
- Accuracy variance across 0°-360° rotation: 30-50% variance
- >30° tilt from canonical: accuracy drops 40%
- Extreme angles (>60°): often <40% accuracy

---

## Mitigation Strategies

1. **3D-Aware Training**: Use synthetic 3D models; rotate before training
2. **Data Augmentation**: Random rotations during training
3. **Viewpoint Invariance**: Train on objects from all angles
4. **Conservative Confidence**: Lower thresholds for non-frontal detections

### Metrics
- Accuracy variance across viewpoints
- Accuracy at >30° rotation

### Alerts
- Accuracy <60% for non-frontal views → P2

---

## References

- [ViewCo: 3D Object Recognition with Viewpoint-Consistent Embeddings](https://arxiv.org/abs/2105.12580)
- [Rotation Robustness for Vision Models](https://arxiv.org/abs/2212.14437)
