# Spatial Attention Bias

## Issue: Model Fixates on Image Center or Edges; Misses Objects in Peripheral Regions

**Frequency**: Common

**Symptoms**
- High detection accuracy in center; near-zero at edges/corners
- Attention maps concentrated on image center
- Objects at image edges frequently missed
- Asymmetric accuracy across quadrants

**Root Cause**
Convolutional networks have implicit positional bias due to pooling and receptive field size. Training datasets often compose objects near center (photographer bias). Models learn "objects are in center" rather than learning uniformly across image.

**Example**
```
Scenario: Panoramic warehouse scan
Image: Small object in corner of frame
Model: 95% accuracy (center); 10% accuracy (corners)
Impact: Missed inventory items in peripheral vision
```

**Key Statistics**
- Center accuracy: 90-95%
- Edge accuracy: 40-60%
- Corner accuracy: 20-40%

---

## Mitigation Strategies

1. **Uniform Training Data**: Ensure training data has objects distributed across image uniformly
2. **Positional Augmentation**: Random crops, rotations to decorrelate position from object
3. **Attention Regularization**: Penalize attention concentrated in center
4. **Ensemble by Crop**: Apply model to multiple overlapping crops; aggregate

### Metrics
- Accuracy by image quadrant
- Attention entropy (uniform = high entropy)

### Alerts
- Quadrant accuracy variance >30% → P2

---

## References

- [Spatial Bias in CNNs](https://arxiv.org/abs/2004.07141)
- [Vision Transformer Positional Embeddings](https://arxiv.org/abs/2103.14030)
