# Adversarial Perturbation Vulnerability

## Issue: Model Misclassifies Images Modified by Small Adversarial Perturbations (Imperceptible to Human)

**Frequency**: Common

**Symptoms**
- Image modified by imperceptible noise → High confidence wrong prediction
- Robust to natural distortions but not adversarial
- Adversarial examples easily transferable to other models
- No robustness to L∞ or L2 perturbations

**Root Cause**
Neural networks learn brittle decision boundaries. High-dimensional models can have adversarial directions where small perturbations flip predictions. Adversarial training expensive; most models not trained to resist adversarial examples.

**Example**
```
Scenario: Traffic sign classification
Clean image: Stop sign → Correct classification (99% confidence)
Adversarial image: Stop sign + imperceptible noise → Classified as Speed Limit sign (98% confidence)

Perturbation: <0.01 pixel value change (imperceptible)
Impact: Autonomous vehicle misses stop sign
```

**Key Statistics**
- Adversarial accuracy (ε=8/255): 10-50% (vs. 95%+ clean)
- Transferability: 60-80% (adversarial examples transfer across models)

---

## Mitigation Strategies

### Prevention
1. **Adversarial Training with Perturbation Budget**: Train model using FGSM and PGD adversarial examples with ε=8/255 L∞ perturbation budget. Implement min-max optimization: minimize loss against worst-case adversarial perturbations within budget. Use progressive adversarial training: start with small ε, gradually increase during epochs. Augment training data with 30-40% adversarially-perturbed images. Validate on test set: measure clean accuracy drop (typically 2-5% when doing adversarial training) vs. adversarial accuracy gain.
2. **Input Preprocessing & Defensive Distillation**: Apply preprocessing transformations to remove adversarial patterns before classification: JPEG compression, input quantization, bit-depth reduction, median filtering. These are cheap computationally but only defend against specific attack types. Implement defensive distillation: train model against soft predictions from another model, flattens decision boundaries. Use temperature parameter to control distillation strength. Combine preprocessing + distillation for layered defense (not perfect but raises attacker cost).
3. **Ensemble Defenses with Orthogonal Architecture Diversity**: Train 3-5 independent models with diverse architectures (ResNet, VGG, EfficientNet) and initializations. Implement voting: require majority agreement (3/5 models) before accepting prediction. Orthogonal diversity reduces transferability of adversarial examples across ensemble members. For critical classifications, implement expensive secondary model (larger/slower) that must agree with primary on safety-critical decisions.

### Detection & Response
1. **Adversarial Pattern Detection**: Monitor model predictions for suspicious patterns indicating adversarial attack: (1) High confidence despite slight image modifications, (2) Prediction changes dramatically with tiny perturbations (sensitivity test), (3) Multiple misclassifications on semantically similar images (ensemble disagreement). Implement runtime detector: measure gradient magnitude in decision boundary (high gradient = brittle boundary = likely adversarial). Alert if gradient norm increases >3x from baseline.
2. **Robustness Evaluation & Degradation Tracking**: Run periodic adversarial robustness tests on production model using standardized attacks (FGSM, PGD, C&W) with ε=8/255 budget. Target clean accuracy: >95%, adversarial accuracy: >80%. If adversarial accuracy drops >10 points from previous checkpoint, halt deployment, investigate cause (model drift, training data contamination, architecture change). Implement automated rollback if robustness drops below threshold.
3. **Confidence Anomaly Detection Under Attack**: Establish baseline model confidence distribution on clean validation set. Monitor production confidence: alert if confidence scores systematically higher than baseline (suggests adversarial input fooling model into false confidence). Implement per-class confidence monitoring: if specific class gets >3 points higher confidence than historical baseline, investigate if class-specific adversarial attack ongoing.

### Architecture Patterns
1. **Randomized Smoothing Defense Layer**: For any critical classification, wrap model with randomized smoothing: perturb input with Gaussian noise (σ=0.5), run multiple forward passes (typically 100-500), take majority vote. Provides certified robustness: theoretical guarantee that classification robust to L2 perturbations within provable bound. Trade-off: 100-500x latency increase, typically unacceptable for real-time, best for offline verification of high-stakes decisions.
2. **Certified Robustness Verification Pipeline**: Use interval bound propagation (IBP) or complete verifiers (α-β-CROWN) to compute certified robustness of model predictions. For each classification, compute: "This prediction provably robust to all L∞ perturbations with ε ≤ X" or "Requires verification (expensive)". Use certified robustness info for routing: high-confidence + certified → trust; high-confidence + unverified → flag for manual review; low-confidence → reject.
3. **Ensemble with Adversarial Detection**: Deploy ensemble of base model + smaller anomaly detector trained to identify adversarial examples. Anomaly detector trained on: clean images (label=0) + adversarially-perturbed images (label=1) using various ε values. Route predictions: if ensemble agreement + anomaly detector confidence <0.3 (clean) → accept; if anomaly detector confidence >0.7 (adversarial) → reject or escalate.

### Metrics
1. **adversarial_accuracy_percent_epsilon_8_255**: Target: >80% accuracy on images adversarially perturbed with ε=8/255 (standard threat model). Measure: correct_predictions / total_adversarial_samples using FGSM, PGD, C&W attacks. Alert: <70%.
2. **clean_accuracy_percent**: Target: >95% on clean images (adversarial training overhead <2%). Measure: correct_predictions / total_clean_samples. Alert: <93% (indicates accuracy/robustness trade-off gone wrong).
3. **robustness_certification_gap_percent**: Target: <15% gap between empirical adversarial accuracy and certified robustness bound. Measure: (empirical_adversarial_acc - certified_bound) / certified_bound * 100. Alert: >25%, indicates verified bound too loose, robustness claims untrustworthy.
4. **gradient_norm_anomaly_ratio**: Target: <5% of predictions have gradient norm >2σ from baseline (potential adversarial). Measure: (predictions_high_gradient) / total_predictions. Alert: >10%.
5. **adversarial_attack_detection_latency_ms**: Target: <50ms per-sample anomaly detection overhead. Measure: detection_latency + small model inference. Alert: >100ms, impacts latency too much.

### Alerts
1. **Adversarial Attack Suspected** (P1): Condition - Single image triggers: (1) >3 points confidence above baseline, (2) Anomaly detector confidence >0.7, (3) Ensemble disagreement on prediction. Action: Flag image as suspicious, log for analysis, consider blocking classification, escalate to security team, sample related images for patterns.
2. **Robustness Accuracy Drop** (P1): Condition - Adversarial accuracy (ε=8/255) drops >10 points from baseline in any batch. Action: Halt production inference, investigate model drift, check training data for contamination, revert to previous checkpoint, run full robustness evaluation before redeployment.
3. **Widespread Misclassification Pattern** (P2): Condition - 2+ semantically-similar images all mispredicted with high confidence on same class (e.g., multiple stop signs → speed limit). Action: Analyze for potential adversarial attack pattern, check if images modified, update detection thresholds, consider deploying certified defense if pattern confirmed.

---

---

## References

- [Adversarial Examples in Deep Learning](https://arxiv.org/abs/1412.6572)
- [Adversarial Training Methods](https://arxiv.org/abs/1706.06083)
