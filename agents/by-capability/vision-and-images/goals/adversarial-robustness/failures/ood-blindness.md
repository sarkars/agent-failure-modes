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

1. **OOD Detection Layer**: Train separate model to detect OOD inputs
2. **Uncertainty Estimation**: Use Bayesian deep learning; high uncertainty = OOD
3. **Entropy Thresholding**: Reject predictions below confidence threshold
4. **Learned Rejection**: Add "reject" class during training

### Metrics
- OOD detection AUROC
- False positive rate (reject in-distribution)
- False negative rate (accept OOD)

### Alerts
- OOD detection AUROC <70% → Retrain or add detection layer

---

## References

- [A Baseline for Detecting Misclassified and Out-of-Distribution Examples in Neural Networks](https://arxiv.org/abs/1610.02136)
- [Deep Anomaly Detection with Outlier Exposure](https://arxiv.org/abs/1812.04606)
