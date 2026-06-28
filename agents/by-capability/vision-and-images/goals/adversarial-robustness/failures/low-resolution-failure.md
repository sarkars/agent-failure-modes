# Low-Resolution Image Failure

## Issue: Model Performance Collapses on Low-Resolution Images; Cannot Recognize Objects When Downsampled

**Frequency**: Very Common

**Symptoms**
- High accuracy on 224×224; fails at 32×32
- Fine detail features lost → Accuracy drops dramatically
- Models overfit to resolution seen in training
- No resolution invariance

**Root Cause**
Downsampling loses information; very low resolution is inherently ambiguous. Models learn features at training resolution; don't learn to work with information loss. Neural networks have implicit resolution bias based on architecture receptive fields.

**Example**
```
Scenario: Surveillance with bandwidth-limited streams
High-res training: 1920×1080 → 95% accuracy
Low-res deployment: 480×270 (25% of area) → 60% accuracy
Ultra-low-res: 240×135 (6% of area) → 20% accuracy
Impact: Cannot recognize faces in compressed streams
```

**Key Statistics**
- 224×224: 94% accuracy
- 112×112: 88% accuracy
- 56×56: 70% accuracy
- 28×28: 40% accuracy
- 14×14: <20% accuracy

---

## Mitigation Strategies

1. **Multi-Scale Training**: Train on diverse resolutions
2. **Super-Resolution Preprocessing**: Upscale before classification
3. **Resolution-Aware Thresholds**: Lower confidence for low-res inputs
4. **Context Expansion**: Use surrounding context to compensate for low detail

### Metrics
- Accuracy vs. image resolution
- Graceful degradation curve

### Alerts
- Accuracy <70% for target resolution → Adjust expectations or upgrade camera

---

## References

- [Resolution Robustness in Deep Networks](https://arxiv.org/abs/2010.13886)
- [Super-Resolution for Robust Recognition](https://arxiv.org/abs/2011.04944)
