# Confidence Miscalibration

## Issue: Model Confidence Doesn't Match Hallucination Probability

**Frequency**: Very Common

**Symptoms**
- High confidence on hallucinated objects (>80%)
- Actual accuracy lower than predicted confidence would suggest
- Calibration curve shows poor agreement between confidence and accuracy
- Overconfidence especially pronounced on ambiguous images

**Root Cause**
Vision models are trained to predict object presence/attributes confidently. They optimize for accuracy, not calibration. As a result, they output high confidence even on ambiguous samples where they're uncertain. The softmax function naturally produces high probabilities, and models don't learn to distinguish between "correct with high evidence" vs. "correct with low evidence".

**Example**
```
Model output: "Object detected, 95% confidence" 
Actual accuracy on similar images: 60%
→ Systematic overconfidence by 35 percentage points
```

**Key Statistics**
- Vision models typically miscalibrated by 20-40 percentage points
- Calibration worse on out-of-distribution images
- High-confidence errors (>80% confidence, actually wrong): 5-15% of predictions

---

## Eval Recipes

### Test Cases
| Test | Expected | Indicator |
|------|----------|-----------|
| Confidence vs. Accuracy | Spearman correlation >0.8 | Correlation <0.7 |
| Expected Calibration Error (ECE) | <10% | >15% |
| Maximum Calibration Error (MCE) | <20% | >30% |
| Brier Score | <0.2 | >0.3 |

### Metrics
| Metric | Target |
|--------|--------|
| ECE (Expected Calibration Error) | <10% |
| Spearman corr(confidence, accuracy) | >0.80 |
| Overconfidence (ECE_over - ECE_under) | ~0% (balanced) |

---

## Mitigation Strategies

### Prevention
1. **Temperature Scaling**: Apply post-hoc calibration using validation set
2. **Mixup/CutMix**: Train-time techniques reduce overconfidence
3. **Label Smoothing**: Prevents model from outputting extreme probabilities
4. **Uncertainty Quantification**: Use ensembles or Monte Carlo dropout to estimate true uncertainty

### Detection & Response
1. **Calibration Testing**: Monthly evaluation of calibration curve
2. **Confidence Monitoring**: Alert if average confidence increases without accuracy improvement
3. **Selective Prediction**: Use confidence thresholds; defer low-confidence to human review

### Architecture Patterns
1. **Post-Hoc Calibration**: Apply temperature scaling before deployment
2. **Ensemble Calibration**: Multiple models; agreement serves as confidence proxy
3. **Uncertainty-Aware Thresholding**: Dynamic thresholds based on calibration curve

---

## Production Signals

### Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `vision.ece_calibration_error` | >15% |
| `vision.high_conf_error_rate` | >10% of >80% confidence predictions |
| `vision.conf_accuracy_correlation` | <0.70 |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Calibration Drift | ECE increases >5% month-over-month | P2 |
| Overconfident Errors | Errors with >85% confidence spike | P1 |

---

## References

- [On Calibration of Vision Models](https://arxiv.org/abs/2106.08254)
- [Predictive Uncertainty Quantification with MLLMs](https://arxiv.org/abs/2303.05205)
