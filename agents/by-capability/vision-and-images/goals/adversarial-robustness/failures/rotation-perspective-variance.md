# Rotation & Perspective Variance Failure

## Issue: Model Fails When Images Are Rotated or Viewed from Different Perspectives; Not Rotationally Invariant

**Frequency**: Common

**Symptoms**
- Object rotated 90° → Cannot recognize (already covered in perspective-blindness)
- High variance in predictions across rotations
- No built-in rotational invariance
- Perspective distortion causes errors

**Root Cause**
Convolutional networks lack rotational invariance (different from rotation-equivariance). Group equivariance not learned unless explicitly designed for it. Perspective distortion changes object appearance; models trained on canonical views struggle.

**Example**
```
Scenario: Document scanning OCR
Document upright: 98% character accuracy
Document rotated 90°: 20% accuracy
Document scanned from angle (perspective): 30% accuracy
Impact: OCR fails on casual photos
```

**Key Statistics**
- Rotation invariance: Drops 30-50% at 45° rotation
- Perspective distortion: Accuracy drops 20-40% for moderate angles

---

## Mitigation Strategies

1. **Rotation Augmentation**: Augment training data with rotations
2. **Group Equivariant Networks**: Use G-CNNs designed for rotation equivariance
3. **Preprocessing Alignment**: Detect and correct image orientation before classification
4. **Ensemble Rotations**: Test multiple rotations; aggregate

### Metrics
- Accuracy vs. rotation angle
- Perspective distortion robustness

### Alerts
- Accuracy drop >25% at moderate rotation → P2

---

## References

- [Group Equivariant CNNs](https://arxiv.org/abs/1602.07576)
- [Rotation-Invariant Representations](https://arxiv.org/abs/2102.16480)
