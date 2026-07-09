# Out-of-Distribution Blindness

## Issue: Model Cannot Detect When Input Is Out-of-Distribution; Makes Confident Predictions on Unknown Objects/Scenes

**Frequency**: Very Common

**Symptoms**
- Model sees unknown object; still assigns high confidence to wrong class
- No "I don't know" mechanism
- OOD detection rate: <50% baseline
- Confidently wrong on OOD examples

**Root Cause**
Neural networks output probability distributions over trained classes regardless of input. No built-in mechanism to reject unknown inputs. Training assumes all test inputs are from known classes. OOD detection is hard because high-confidence regions in latent space are unbounded.

**Example**
```
Scenario: Wildlife classifier trained on common animals
Training classes: Dog, Cat, Bird, Squirrel
Deployment: Photo of exotic animal (pangolin)

Model: "This is a dog with 92% confidence"
Expected: "This doesn't match any known animal"
Impact: Misidentification; wildlife management fails
```

**Key Statistics**
- OOD detection AUROC: 60-75% (baseline, room for improvement)
- False confidence on OOD: 80-90% of OOD examples have >50% confidence

---

## Mitigation Strategies

### Prevention
1. **Outlier Exposure Training**: During training, include synthetic OOD examples (images from different domains, corrupted images, random noise). Train model to assign low confidence to OOD samples. Use diverse OOD: ImageNet images (for model trained on subset), random textures, blurred images, etc. Implement as data augmentation: 20-30% of training batches include OOD samples. Add explicit "reject" or "unknown" class during training (optional for some architectures). Target: model learns to produce low-confidence, high-entropy predictions on OOD.
2. **Uncertainty Estimation & Bayesian Inference**: Train model that outputs not just class probabilities, but also uncertainty estimates. Use Bayesian approaches: ensemble models with different initializations, Monte Carlo dropout (apply dropout at test time, sample multiple predictions), or parametric uncertainty (predict aleatoric + epistemic uncertainty). Combine aleatoric (data uncertainty) + epistemic (model uncertainty): high epistemic uncertainty on OOD. Implement threshold: (aleatoric + epistemic) > threshold → reject as OOD.
3. **Auxiliary OOD Detection Model**: Train small separate model specifically to distinguish in-distribution vs. OOD samples. Use features from main classifier's penultimate layer as input to OOD detector. Train on: (in-distribution samples labeled 0, OOD samples labeled 1). Use outlier exposure: train OOD detector on diverse OOD sources. Deploy OOD detector in series with classifier: if OOD detector confidence >0.7 → reject, else use classifier. Allows independent tuning of OOD detection vs. classification thresholds.

### Detection & Response
1. **OOD Detection Performance Monitoring**: Evaluate OOD detector on held-out OOD test set monthly. Measure: AUROC, precision (what % of rejected samples truly OOD), recall (what % of OOD samples detected). Target: AUROC >0.85. Alert if AUROC drops >0.10 from baseline (indicates detector drift or model change). Separately measure false positive rate (in-distribution samples mistakenly rejected) and false negative rate (OOD samples accepted). Target: FPR <2%, FNR <10%.
2. **OOD Rejection Rate Monitoring**: Track percentage of inputs rejected as OOD in production. Establish baseline (typically 2-5% normal). Alert if rejection rate spikes (>10%) indicating potential data distribution shift or adversarial OOD attack. Alert if rejection rate drops <0.5% (detector may have failed, too permissive). Segment by inferred object type if possible.
3. **Confidence-Entropy Analysis**: Monitor entropy of model predictions on accepted samples. OOD blindness manifests as high confidence + high entropy on OOD (conflicting signals). Implement anomaly detector: if (confidence > 0.80 AND entropy > threshold) → likely OOD, flag for review. Maintain baseline distribution of (confidence, entropy) pairs, alert on outliers.

### Architecture Patterns
1. **Ensemble OOD Detection**: Deploy ensemble of OOD detectors trained on different OOD sources (domain-shift OOD, corruption-based OOD, synthetic OOD). Combine decisions: unanimous agreement more confident than single detector. Use weighted voting: detector trained on realistic OOD (e.g., new camera type) weighted higher than synthetic OOD. Implement confidence aggregation: if ensemble disagreement on OOD decision, flag for manual review.
2. **Confidence-Entropy Rejection Region**: Learn elliptical or more complex decision boundary in (confidence, entropy) feature space that separates in-distribution from OOD. Use Gaussian Mixture Model or One-Class SVM trained on calibrated confidence and entropy computed on validation set. Predictions falling outside learned region rejected as OOD. Advantage: interpretable decision boundary, no need for separate OOD training.
3. **Cascade Detection with Escalation**: Stage 1: Quick entropy threshold rejection. Stage 2: If borderline, run more expensive OOD detector (Bayesian ensemble, small model). Stage 3: If still uncertain, escalate to human review or request additional data/clarification. Implement latency budget: Stage 1 <5ms, Stages 1-2 <50ms, escalation async. Allows balancing latency vs. detection accuracy.

### Metrics
1. **ood_detection_auroc**: Target: >0.85 (high ability to distinguish in-distribution from OOD). Measure: AUROC on held-out OOD test set with diverse OOD sources. Alert: <0.75.
2. **ood_false_positive_rate**: False rejections (in-distribution samples marked OOD). Target: <2% of in-distribution samples rejected. Alert: >5%.
3. **ood_false_negative_rate**: Missed OOD detection (OOD samples accepted as in-distribution). Target: <10% of OOD samples missed. Alert: >20%.
4. **ood_detection_confidence_precision**: Of samples flagged as OOD with confidence >0.8, what percentage truly OOD? Target: >90% precision. Alert: <75%.
5. **entropy_calibration_error_ood**: For in-distribution samples, entropy should be low. For OOD, entropy high. Measure: ECE of entropy-based OOD detection. Target: ECE <10%. Alert: >20%.

### Alerts
1. **OOD Detector Degradation** (P2): Condition - OOD detection AUROC drops >0.10 from baseline in any 7-day window. Action: Evaluate if model has changed, if new OOD patterns appearing in production, retrain OOD detector on recent data.
2. **Suspected OOD Attack** (P1): Condition - High volume (>5%) of samples rejected as OOD with very high OOD detector confidence (>0.95), indicating potential coordinated OOD attack or data source issue. Action: Alert security/ops, investigate source of OOD inputs, analyze sample of rejected images for attack patterns, consider blocking source.
3. **False Positive OOD Rejection** (P2): Condition - OOD false positive rate increases >2 points (e.g., from 1% to 3%) in 24-hour window. Action: Investigate if new in-distribution patterns (new camera model, new object type) causing false rejections, recalibrate OOD detector thresholds, consider retraining.

---

---

## References

- [A Baseline for Detecting Misclassified and Out-of-Distribution Examples in Neural Networks](https://arxiv.org/abs/1610.02136)
- [Deep Anomaly Detection with Outlier Exposure](https://arxiv.org/abs/1812.04606)
