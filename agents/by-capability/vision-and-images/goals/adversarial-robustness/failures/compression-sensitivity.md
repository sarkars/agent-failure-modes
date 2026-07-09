# Compression Artifacts & Quality Sensitivity

## Issue: Model Fails When Images Compressed (JPEG Artifacts); Accuracy Sensitive to Compression Quality

**Frequency**: Common

**Symptoms**
- High accuracy on lossless images; drops with JPEG compression
- Sensitivity to compression quality (Q factor)
- Hallucination of compression artifacts as objects
- No robustness to common image formats

**Root Cause**
Training data typically high-quality, uncompressed. Real-world data compressed (JPEG, WebP). JPEG artifacts are statistically different from natural images; models learn spurious patterns or struggle with artifact textures. Fine details lost in compression cause accuracy drop.

**Example**
```
Scenario: Mobile image classification app
Training: High-quality PNG files
Deployment: JPEG compressed (Q=75) for network efficiency

Model accuracy on PNG: 94%
Model accuracy on JPEG(Q=75): 78%
Impact: Performance drop in production
```

**Key Statistics**
- Accuracy on uncompressed: 92-95%
- JPEG Q=75: 85-90%
- JPEG Q=50: 75-85%
- JPEG Q=30: 60-75%

---

## Mitigation Strategies

### Prevention
1. **Compression-Aware Training Pipeline**: Augment training data with JPEG-compressed images at multiple quality factors (Q=95, 85, 75, 60, 50, 30). Use stratified sampling: 70% uncompressed + 30% JPEG at random Q ∈ [30, 95]. This trains model to recognize features that survive compression, ignores fine details lost to JPEG. Measure model accuracy at each Q level on validation set (should show graceful degradation, not cliffs). Target: <5% accuracy drop from Q=95 to Q=75, <10% drop from Q=95 to Q=50.
2. **Compression-Invariant Feature Learning**: Use techniques that learn compression-robust features: (1) Use perceptual loss functions (e.g., LPIPS) that ignore compression artifacts during training. (2) Train on DCT (discrete cosine transform) coefficients directly instead of pixel space—JPEG operates in DCT domain, so learning from DCT more natural. (3) Implement multi-scale feature extraction: low-frequency features (survive compression) weighted more than high-frequency (lost to compression). (4) Fine-tune on compressed images from deployment environment.
3. **Adaptive Decompression & Enhancement**: Before feeding images to model, apply lightweight preprocessing: (1) JPEG artifact removal (median filter, bilateral filter targeting block boundaries). (2) Adaptive histogram equalization to recover contrast lost to compression. (3) Edge enhancement to restore details. Implement preprocessing as optional tier: if image quality <threshold, apply enhancement; else use raw image. Measure accuracy gain from preprocessing vs. latency cost.

### Detection & Response
1. **Compression Quality Detection & Dynamic Routing**: Automatically detect compression quality of incoming images (using JPEG quality estimation algorithm). Route to appropriate confidence threshold: Q>80 use standard threshold (0.75), Q=60-80 use medium (0.65), Q<60 use conservative (0.55). Implement graceful degradation: explicit to user "Lower quality image, I'm less confident" with explanation. Alert on unexpectedly high variance in image quality arriving in production (might indicate data pipeline issue).
2. **Accuracy Degradation Tracking**: Monitor accuracy separately by compression level. For each image, estimate JPEG Q factor, then track accuracy for Q ∈ [80-95], [60-80], [30-60]. Target: maintain within 5% accuracy of uncompressed at all Q levels. Alert if accuracy on Q<60 images drops >10% from 7-day baseline. Segment false positives by compression level: high false positive rate at low Q suggests threshold too aggressive.
3. **Compression Artifact Anomaly Detection**: Train small auxiliary model to detect JPEG compression artifacts (block boundaries, ringing effects). Monitor predictions: if high confidence but many artifacts detected, flag as potential false positive. Use artifact detector as confidence adjuster: reduce confidence score by 10-20% if heavy compression artifacts present. Alert if artifact detector consistently mis-predicts (e.g., detects artifacts in uncompressed images = possible compression injection attack).

### Architecture Patterns
1. **DCT-Domain Feature Extraction**: Train model that operates in DCT (discrete cosine transform) coefficient domain instead of pixel domain. Pre-processing: decode JPEG, extract DCT coefficients (bypass full decompression). Feed DCT coefficients to model. Advantage: naturally robust to compression (can drop high-frequency coefficients without latency). Disadvantage: incompatible with standard pretrained models (ResNet on DCT coefficients needs retraining from scratch or adaptation layer).
2. **Multi-Quality Ensemble with Confidence Fusion**: Train separate lightweight models for different compression ranges: model_high (Q>80), model_medium (Q=60-80), model_low (Q<60). Deploy all three. On incoming image, detect Q, run appropriate model + 1-2 neighbors for robustness. Fuse predictions: weight by Q estimation confidence. Also useful for detecting Q-mismatch attacks (e.g., claimed high-Q image that's actually low-Q).
3. **Degradation-Aware Confidence Calibration**: Train post-hoc confidence adjuster that takes (raw_model_confidence, estimated_compression_Q) → adjusted_confidence. Learns empirically how much to reduce confidence based on compression level. Calibrate on validation set with known compression levels. Use isotonic regression or neural network for mapping function. Implement re-calibration quarterly as model drifts.

### Metrics
1. **accuracy_vs_jpeg_quality_curve**: Measure accuracy at Q = 95, 85, 75, 60, 50, 30. Target: <5% drop from Q=95 to Q=75, <12% drop to Q=50. Alert: >8% drop from Q=95 to Q=75.
2. **graceful_degradation_smoothness**: Measure rate of accuracy change: (acc_q75 - acc_q85) / 10, (acc_q50 - acc_q75) / 25, etc. Target: smooth degradation (no cliffs >3% per 10-point Q drop). Alert: cliff >5% indicates sudden model brittleness.
3. **compression_quality_detection_accuracy**: Estimate Q factor on images of known Q. Target: ±5 points detection error. Measure: MAE(estimated_Q, true_Q). Alert: >10 points error.
4. **compression_robust_confidence_calibration**: For each Q level, check if confidence scores well-calibrated (ECE <5% per Q level). Measure Expected Calibration Error separately for Q>80, Q=60-80, Q<60. Alert: ECE >8% for any level.
5. **compression_artifact_detection_false_positive_rate**: On uncompressed validation images, artifact detector should have <2% false positive rate. Measure: (FP_detections) / (uncompressed_images). Alert: >5%.

### Alerts
1. **Unexplained Accuracy Drop on Low-Q Images** (P2): Condition - Accuracy on Q<60 images drops >10% from baseline in 24-hour window, while accuracy on Q>80 unchanged (suggests model-specific issue, not just compression). Action: Investigate recent model changes, check training data for Q-level imbalance, retrain with proper compression augmentation.
2. **Compression Mismatch Attack** (P2): Condition - Image header claims Q=95 but artifact detector estimates Q<60 (possible manipulation). Action: Flag as suspicious, log for investigation, apply high-confidence threshold (require 0.85+ confidence instead of 0.75), escalate to security if pattern detected.
3. **Quality Threshold Breach** (P2): Condition - Incoming images show unusual compression distribution (e.g., >50% of images Q<50, normally <5%) indicating data pipeline issue. Action: Alert data team, investigate image source, check for degraded camera sensors or network compression, consider halting inference if quality too low across batch.

---

---

## References

- [Robustness to JPEG Compression](https://arxiv.org/abs/2012.08391)
- [Image Compression and Deep Learning](https://arxiv.org/abs/2002.09137)
