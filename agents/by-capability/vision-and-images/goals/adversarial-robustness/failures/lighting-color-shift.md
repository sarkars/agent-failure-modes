# Lighting & Color Shift Sensitivity

## Issue: Model Highly Sensitive to Lighting Conditions and Color Changes; Fails Under Different Illumination

**Frequency**: Very Common

**Symptoms**
- Works well in daylight; fails in artificial lighting
- Works in cool white light; fails in warm light
- Color balance shifts → Accuracy drops
- No illumination invariance

**Root Cause**
Models learn color/intensity patterns specific to training lighting. Lighting is not semantic — it's a nuisance variable — but models learn it as feature. No built-in invariance to illumination; models must learn it from data.

**Example**
```
Scenario: Retail store product recognition
Training: Brightly lit showroom photos
Deployment: Dimly lit warehouse with different color temperature

Model: 88% accuracy in showroom
Model: 45% accuracy in warehouse
Impact: Shelf inventory system fails
```

**Key Statistics**
- Accuracy variance across lighting: 20-40%
- Extreme lighting (very bright/dim): >50% accuracy drop

---

## Mitigation Strategies

1. **Data Augmentation**: Train on diverse lighting conditions
2. **Illumination Normalization**: Preprocess images to remove lighting effects
3. **Color Augmentation**: Random brightness/contrast/saturation shifts
4. **Grayscale Robustness**: Train to be less dependent on color

### Metrics
- Accuracy across different illumination levels
- Lighting sensitivity coefficient

### Alerts
- Accuracy <70% in target lighting conditions → P2

---

## References

- [Illumination Robustness in Vision](https://arxiv.org/abs/2008.02868)
- [Color Constancy for Robust Recognition](https://arxiv.org/abs/2002.03969)
