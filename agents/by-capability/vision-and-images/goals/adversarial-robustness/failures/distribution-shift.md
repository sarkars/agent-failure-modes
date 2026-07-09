# Distribution Shift & Domain Adaptation Failure

## Issue: Model Trained on One Distribution Fails on Different (But Related) Data Distribution

**Frequency**: Very Common

**Symptoms**
- Trained on synthetic data; fails on real images
- Trained on clean images; fails with compression/noise
- Accuracy drops 20-40% on new domain
- High variance across different data sources

**Root Cause**
Models learn spurious correlations specific to training distribution. Real-world drift (camera models, lighting, objects) causes covariate shift. Model doesn't learn invariant features; instead memorizes training distribution.

**Example**
```
Scenario: Medical imaging model
Training: High-resolution ultrasound from Hospital A
Deployment: Different ultrasound machine from Hospital B (different sensor, resolution, contrast)

Model trained on A: 92% accuracy
Model on B: 58% accuracy
Impact: Model useless on new equipment
```

**Key Statistics**
- Domain shift accuracy drop: 20-40% typical
- Worst-case: 50-70% drop for extreme shifts

---

## Mitigation Strategies

### Prevention
1. **Domain-Aware Training & Source Diversity**: Don't train on single domain. Collect training data from multiple sources (camera models, lighting conditions, resolutions) that approximate production environment. Use stratified sampling: ensure all major domain variations represented in training. Implement data collection checklist: Hospital A ultrasound machines (versions 1-3), Hospital B machines, different lighting conditions, different image qualities. Target: training distribution overlap >80% with expected production distribution.
2. **Domain Randomization & Invariant Feature Learning**: Apply systematic domain randomization during training: randomly vary image properties that differ across domains (brightness ±20%, contrast ±20%, hue ±10%, blur kernel size, compression Q factor, etc.). Use semantic augmentation: object rotations, scales, translations are domain-invariant. Learn features using contrastive learning framework (SimCLR, MoCo): model learns representations where same object from different domains produces similar embeddings. Freeze backbone, only fine-tune classification head.
3. **Uncertainty-Aware Confidence with Out-of-Distribution Detection**: Train model to output confidence that accounts for domain shift. Use ensemble or Bayesian model that captures aleatoric (data noise) + epistemic (model uncertainty) uncertainty. Train OOD detector: auxiliary model that distinguishes in-distribution from out-of-distribution samples. Train on source domain (in-distribution) + synthetic OOD (random noise, adversarial perturbations, images from completely different domain). Use OOD score to adjust confidence: high OOD score → reduce confidence even if model confident.

### Detection & Response
1. **Domain Shift Detection & Severity Assessment**: Monitor incoming data distribution in production. Use statistical tests to detect shift: (1) Kernel density divergence (KL divergence, Wasserstein distance) from training distribution, (2) Batch statistics: mean/variance of image features, (3) Model prediction entropy (models under distribution shift often produce more uncertain predictions). Compute shift severity score: threshold shifts into low/medium/high. Alert on medium/high shift detection.
2. **Target Domain Performance Monitoring**: Immediately after deploying to new domain (e.g., Hospital B), actively monitor accuracy on sample of predictions with ground truth labels. Target: accuracy within 5% of source domain. If accuracy drops >15%, automatically trigger domain adaptation workflow. Maintain per-domain performance dashboard: Hospital A: 92% acc, Hospital B: 58% acc → visualizes need for adaptation.
3. **Negative Transfer Detection**: When fine-tuning model on target domain, monitor that target accuracy improves (positive transfer) and doesn't degrade (negative transfer). Implement early stopping: if fine-tuning causes target accuracy drop >3%, stop and roll back. Also monitor source accuracy: fine-tuning on target shouldn't drastically hurt source performance (should stay >90% of original).

### Architecture Patterns
1. **Federated Domain Adaptation**: Collect small labeled dataset from target domain (10-20% of source), fine-tune model on combined source + target data with domain weights. Optimize: (source_loss * w_source + target_loss * w_target) with w_target > w_source. Implement curriculum: start with w_target=0.1, gradually increase to 0.3-0.5 over epochs. Use data augmentation to simulate additional target domain samples (domain randomization). Implement early stopping: monitor source + target accuracy, stop if either degrades.
2. **Domain-Invariant Feature Space via Adversarial Domain Classifier**: Train model with two heads: (1) classification head (task), (2) domain classifier head (predicts source domain or target domain). Use adversarial training: classification head tries to learn features that confuse domain classifier; domain classifier tries to discriminate domains from features. Forces model to learn domain-invariant features. Use gradient reversal layer between shared features and domain classifier.
3. **Test-Time Adaptation with Entropy Minimization**: At test time on target domain, adapt model using unlabeled data. Use entropy minimization: for each batch of unlabeled target images, fine-tune model to minimize prediction entropy (encourage confident, low-entropy predictions). Implement batch-wise adaptation: after every 32 test samples, do 1-2 gradient steps of entropy minimization. Reset every hour to prevent error accumulation. Measure that adaptation doesn't hurt accuracy on source-like test samples.

### Metrics
1. **source_vs_target_accuracy_gap_percent**: Target: <5% accuracy gap between source and target domains. Measure: accuracy_source - accuracy_target. Alert: >15% gap indicates distribution shift.
2. **negative_transfer_indicator**: When fine-tuning on target, target accuracy should increase, source accuracy should stay stable. Measure: (source_acc_after_finetune / source_acc_before) * 100. Target: >95% retention. Alert: <90% indicates negative transfer (fine-tuning hurting original domain).
3. **domain_shift_detection_accuracy**: OOD detector should correctly identify out-of-distribution samples (target domain) vs. in-distribution (source domain). Measure: AUROC of OOD detector on held-out test set. Target: >0.85 AUROC. Alert: <0.75%.
4. **distribution_shift_severity_score**: Compute continuous score [0,1] of how far target distribution from training. Use kernel divergence or spectral method. Target: score <0.3 (minimal shift). Alert: score >0.5 (significant shift, adaptation needed).
5. **per_domain_accuracy_coverage**: Minimum accuracy across all deployed domains. Target: >85% minimum across all domains. Alert: any domain <80%.

### Alerts
1. **Domain Shift Detected** (P2): Condition - KL divergence from training distribution to incoming data exceeds threshold (score >0.5), indicating significant distribution shift. Action: Alert ML team, trigger domain analysis workflow, collect labeled samples from new domain, schedule domain adaptation retraining.
2. **Target Domain Accuracy Degradation** (P1): Condition - Accuracy on target domain drops >15% from source domain or 5+ points from baseline. Action: Investigate cause (camera change, new patient population, hardware upgrade), automatically trigger fine-tuning on target domain, monitor adaptation progress, consider reverting if adaptation doesn't improve >10 points.
3. **Negative Transfer During Adaptation** (P2): Condition - During fine-tuning on target domain, source domain accuracy drops >5% (indicator that model forgetting source distribution). Action: Stop fine-tuning, implement stronger regularization (reduce target learning rate, increase batch size), use stronger domain-invariant loss, consider ensemble with original model instead of full fine-tuning.

---

---

## References

- [Domain Adaptation Survey](https://arxiv.org/abs/1702.05740)
- [Out-of-Distribution Detection](https://arxiv.org/abs/1810.09136)
