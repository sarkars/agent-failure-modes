# Scale Confusion & Scale Drift

## Issue: Model Fails to Distinguish Objects of Different Scales; Confuses Small/Large Versions

**Frequency**: Common

**Symptoms**
- High confidence on wrong scale version
- Confuses toy/miniature objects with real objects
- Fails at "is this thing big enough?"
- Scale-variant accuracy variance >30%

**Root Cause**
Object recognition relies on visual patterns that are often scale-invariant (texture, color). Models trained on fixed resolutions struggle with extreme scale changes. Training data typically lacks diversity in object scales; datasets over-represent "typical" sizes.

**Example**
```
Scenario: Warehouse management
Image: Tiny model car (1cm) vs. actual car
Model: Treats both identically; assigns same class probability
Expected: Distinguish scale; apply size-dependent logic
Impact: Gripper grasps miniature; collision detection fails
```

**Key Statistics**
- Scale variance in training: 2-3x
- Accuracy at 10x scale: drops 40-50%
- Extreme scales (>100x): <30% accuracy

---

## Mitigation Strategies

1. **Multi-Scale Training**: Augment with diverse object sizes (0.1x-10x)
2. **Explicit Size Regression**: Add auxiliary head predicting object size
3. **Context Cues**: Use objects of known size (reference objects) to infer scale
4. **Rejection Threshold**: Reject predictions if scale is atypical for object class

### Metrics
- Accuracy vs. scale ratio (actual:expected)
- Scale regression error (predicted size / actual size)

### Alerts
- Scale prediction error >50% → P2
- Confidence-calibrated for scale → Track separately

---

## References

- [Multi-Scale Feature Learning](https://arxiv.org/abs/1612.03144)
- [Scale-Aware Object Detection](https://arxiv.org/abs/2008.06049)
