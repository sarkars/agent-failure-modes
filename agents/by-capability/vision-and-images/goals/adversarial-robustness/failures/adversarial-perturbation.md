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

1. **Adversarial Training**: Train on adversarial examples
2. **Certified Defenses**: Randomized smoothing, interval bound propagation
3. **Input Preprocessing**: Image transformations to remove adversarial noise
4. **Ensemble Defenses**: Combine multiple classifiers

### Metrics
- Adversarial accuracy (standard metrics: FGSM, PGD, C&W attacks)
- Robustness certification (provable bounds)

### Alerts
- Adversarial accuracy drop >50% → P1

---

## References

- [Adversarial Examples in Deep Learning](https://arxiv.org/abs/1412.6572)
- [Adversarial Training Methods](https://arxiv.org/abs/1706.06083)
