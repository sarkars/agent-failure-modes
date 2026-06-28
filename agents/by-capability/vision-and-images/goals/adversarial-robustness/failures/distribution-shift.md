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

1. **Domain Adaptation**: Fine-tune on target domain data
2. **Domain-Invariant Training**: Learn features robust to domain variations
3. **Test-Time Adaptation**: Adapt model based on test samples
4. **Ensemble Across Domains**: Train multiple models on different domains

### Metrics
- Source accuracy vs. target accuracy
- Negative transfer (target worse than untrained)

### Alerts
- Target accuracy drop >25% → Domain adaptation needed

---

## References

- [Domain Adaptation Survey](https://arxiv.org/abs/1702.05740)
- [Out-of-Distribution Detection](https://arxiv.org/abs/1810.09136)
