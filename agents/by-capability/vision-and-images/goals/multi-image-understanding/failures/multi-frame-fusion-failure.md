# Multi-Frame Fusion Failure

## Issue: Information from Multiple Frames/Views Not Properly Combined; Fusion Produces Worse Results Than Single Frame

**Frequency**: Common

**Symptoms**
- Fusion architecture fails to benefit from multiple views
- Single best frame often more accurate than fused result
- Conflicting information not resolved
- Information loss during fusion

**Root Cause**
Fusing information from multiple sources is hard; requires alignment and conflict resolution. Naive concatenation or averaging can hurt performance if frames are misaligned or contain contradictory information. Fusion requires learned weighting or attention mechanisms.

**Example**
```
Scenario: 3D reconstruction from multi-view images
Image 1: Good front view
Image 2: Side view (slightly misaligned)
Image 3: Top view (very noisy)

Naive fusion: Average 3 views → mediocre 3D result
Smart fusion: Weight views by confidence; handle misalignment
Impact: Single-view sometimes better than fused
```

**Key Statistics**
- Single best frame accuracy: 85%
- Naive fusion (average): 75%
- Smart fusion (learned weights): 92%

---

## Mitigation Strategies

1. **Learned Fusion**: Train attention/weighting module to combine views
2. **Alignment First**: Align frames before fusion
3. **Soft Voting**: Weighted voting based on confidence
4. **Selective Fusion**: Use only high-quality frames; skip noisy ones

### Metrics
- Fusion gain (fused > single best frame)
- Weight distribution (is model using all frames?)

### Alerts
- Fusion performance <single best frame → Debug

---

## References

- [Multi-View Fusion in 3D Vision](https://arxiv.org/abs/2004.06961)
- [Attention-based Fusion](https://arxiv.org/abs/2106.00672)
