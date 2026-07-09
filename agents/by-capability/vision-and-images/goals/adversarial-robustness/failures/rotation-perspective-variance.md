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

### Prevention
1. **Rotation-Aware Training with Extensive Augmentation**: Augment training data with rotations at multiple angles: ±0°, ±15°, ±30°, ±45°, ±60°, ±90°. Use stratified sampling: 30% rotated by 90° (common in real data), 30% rotated by ±45°, 20% rotated by ±15-30°, 20% unrotated. Implement random rotation: for each epoch, randomly rotate training images by angle ∈ [-45°, 45°]. Target: accuracy stable within ±5% across rotation range. Use rotation-specific augmentation: different crops may be valid at different rotations.
2. **Group-Equivariant Network Architecture (G-CNN)**: Use rotation-equivariant CNNs designed with group theory (C8, C4 groups for 8-way, 4-way rotation). These networks explicitly handle rotations as symmetry operations, learning features that transform predictably under rotation. Trade-off: 4-8x higher computational cost, less pretrained models available. Recommendation: use for rotation-critical applications (document scanning, traffic signs); standard CNN + augmentation for most cases.
3. **Perspective Correction & Orientation Detection**: Before classification, detect if image perspective-skewed or rotated. Use auxiliary model to detect document orientation (0°, 90°, 180°, 270°) or more fine-grained angle. Apply perspective correction (homography transformation) if needed. For documents: detect text/edge orientation, straighten before OCR. Implement adaptive: straighten only if confidence >0.8, else use raw image.

### Detection & Response
1. **Rotation-Specific Accuracy Monitoring**: Evaluate accuracy separately for each rotation bin: 0°, ±15°, ±30°, ±45°, ±60°, ±90°. Target: <5% accuracy variation across angles. Alert if accuracy at any rotation angle drops >10% from baseline (0°). Monthly audit: test model on held-out rotated validation set, verify robustness curve smooth.
2. **Perspective Distortion Tracking**: For images detected with perspective distortion (skew angle), track accuracy separately from straight images. Alert if perspective-distorted images have significantly lower accuracy (>10% drop). Segment by distortion angle: mild (<10°), moderate (10-30°), severe (>30°).
3. **Orientation Detection Accuracy Monitoring**: If using orientation detector, measure accuracy of orientation classification vs. ground truth. Target: >95% orientation accuracy. Alert if drops <90% (indicates detector degradation, orientation correction may be wrong).

### Architecture Patterns
1. **Rotation Ensemble with Ensemble Voting**: Create ensemble by running classifier on multiple rotations of same image (0°, 90°, 180°, 270°, and potentially 45°, 135°). Aggregate predictions via voting: use majority vote or confidence-weighted average. High-confidence agreement across rotations increases trust in prediction. Implement fallback: if ensemble disagreement >0.3 (high variance), escalate to manual review or request better-quality image.
2. **Trainable Spatial Transformer Network (STN)**: Add learnable transformation module before classifier. STN learns to predict optimal geometric transformation (rotation, perspective transformation) for input image, applies transformation, then classifies. End-to-end training: learns to orient/perspective-correct images for better classification. STN adds minimal overhead but requires end-to-end retraining. Particularly effective for document/form processing.
3. **Rotation-Invariant Feature Extraction**: Use feature extractors inherently invariant to rotation: (1) Polar coordinates (convert image to polar, frequency is rotation-invariant), (2) Multi-scale features (same object at different scales/rotations has similar features), (3) Handcrafted features like SIFT (rotation-invariant by design). Combine with standard CNN: extract rotation-invariant features, feed to classifier. Hybrid approach can be efficient.

### Metrics
1. **accuracy_vs_rotation_angle**: Measure accuracy at rotations 0°, 15°, 30°, 45°, 60°, 90°. Target: <5% variation across all angles. Alert: >10% variation indicates poor rotation robustness.
2. **rotation_robustness_score**: Compute as: 1 - (max_angle_accuracy - min_angle_accuracy) / mean_accuracy. Target: >0.95 (tight accuracy across rotations). Alert: <0.85.
3. **perspective_accuracy_gap**: Accuracy on perspective-distorted images vs. frontal images. Target: <5% gap. Alert: >15% gap.
4. **orientation_detection_accuracy**: For orientation detection model, measure accuracy vs. ground truth. Target: >95%. Alert: <90%.
5. **ensemble_rotation_agreement_score**: For rotation ensemble approach, measure prediction agreement across rotation variants. Target: >80% same-prediction agreement. Alert: <60% indicates high uncertainty.

### Alerts
1. **Rotation Accuracy Cliff** (P2): Condition - Accuracy drops >15% at specific rotation angle (e.g., 45° or 90°) compared to 0°. Action: Investigate if model underfitted to that angle, retrain with more augmentation at that angle, consider using rotation-equivariant network.
2. **Perspective Distortion Degradation** (P2): Condition - Accuracy on perspective-distorted images (skew angle >10°) drops >15% from frontal baseline. Action: Improve perspective correction preprocessing, augment training data with perspective transforms, consider requiring users to provide frontal image.
3. **Ensemble Rotation Disagreement** (P1): Condition - Rotation ensemble voting shows high disagreement (same image, different rotations give different predictions with similar confidence). Action: Flag sample as ambiguous, request human review, investigate if object genuinely ambiguous or model unstable.

---

---

## References

- [Group Equivariant CNNs](https://arxiv.org/abs/1602.07576)
- [Rotation-Invariant Representations](https://arxiv.org/abs/2102.16480)
