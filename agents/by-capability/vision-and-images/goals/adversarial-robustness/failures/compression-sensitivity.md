# Compression Artifacts & Quality Sensitivity

## Issue: Model Fails When Images Compressed (JPEG Artifacts); Accuracy Sensitive to Compression Quality

**Frequency**: Common

**Symptoms**
- High accuracy on lossless images; drops with JPEG compression
- Sensitivity to compression quality (Q factor)
- Hallucination of compression artifacts as objects
- No robustness to common image formats

**Root Cause**
Training data typically high-quality, uncompressed. Real-world data compressed (JPEG, WebP). JPEG artifacts are statistically different from natural images; models learn spurious patterns or struggle with artifact textures. Fine details lost in compression cause accuracy drop.

**Example**
```
Scenario: Mobile image classification app
Training: High-quality PNG files
Deployment: JPEG compressed (Q=75) for network efficiency

Model accuracy on PNG: 94%
Model accuracy on JPEG(Q=75): 78%
Impact: Performance drop in production
```

**Key Statistics**
- Accuracy on uncompressed: 92-95%
- JPEG Q=75: 85-90%
- JPEG Q=50: 75-85%
- JPEG Q=30: 60-75%

---

## Mitigation Strategies

1. **Compression Augmentation**: Train on JPEG-compressed images at various Q factors
2. **Preprocessing**: Denoise before classification
3. **Compression-Invariant Features**: Train on image features robust to compression
4. **Accept Degradation**: Set lower accuracy targets for compressed inputs

### Metrics
- Accuracy vs. compression quality (Q factor)
- Graceful degradation curve

### Alerts
- Accuracy drop >15% with JPEG → P3

---

## References

- [Robustness to JPEG Compression](https://arxiv.org/abs/2012.08391)
- [Image Compression and Deep Learning](https://arxiv.org/abs/2002.09137)
