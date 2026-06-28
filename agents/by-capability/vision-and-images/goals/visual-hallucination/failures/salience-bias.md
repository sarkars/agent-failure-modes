# Salience Bias

## Issue: Model Overemphasizes Visually Salient Features, Ignoring Context

**Frequency**: Common

**Symptoms**
- Bright colors or high-contrast edges trigger false detections
- Model ignores object category; focuses on visual salience
- Confidence high on false detections with high contrast/color
- Fails on grayscale or low-contrast versions of same object

**Root Cause**
Vision models learn shortcuts using salient visual features. During training, bright red objects are overrepresented as positive examples, so the model learns "bright red = target object" rather than actual object shape. Low-salience objects (white on white, same-color backgrounds) are missed entirely.

**Example**
```
Scenario: Quality control agent detecting defects on production line

Image: White part with subtle manufacturing crack (low salience)
Also present: Red sticker label on white part (high salience)

Model output: Detects only red sticker, misses actual defect

Impact: Defective part passes QC → reaches customer
```

**Key Statistics**
- Salience bias causes 25-35% of false positives in industrial QC
- Accuracy drops 40% on low-contrast versions of high-contrast training images
- High-saturation colors: 20% higher false positive rate than low-saturation

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Desaturation | Color image → grayscale | Performance stable | Accuracy drops >15% |
| Contrast reduction | Reduce contrast 50% | Graceful degradation | Model fails to detect |
| Salience mismatch | Target is low-contrast, background high-contrast | Correct target detection | Model detects background, misses target |
| Color invariance | Same object, different colors | Color-invariant detection | Different detection across colors |

### Metrics
| Metric | Target |
|--------|--------|
| Saturation Robustness | <5% accuracy variance across 0-100% saturation |
| Contrast Robustness | <10% accuracy variance from 0.5x to 2x contrast |
| Salience Invariance | Accuracy unchanged when high-salience distractors added |

---

## Mitigation Strategies

### Prevention
1. **Data Augmentation**: Train with low-contrast, low-saturation, grayscale variants
2. **Adversarial Examples**: Include deliberately low-salience true positives and high-salience false positives
3. **Feature Visualization**: Debug which features model relies on (saliency maps); retrain if salience-dependent
4. **Contrast Normalization**: Apply histogram equalization or adaptive contrast before inference

### Detection & Response
1. **Robustness Testing**: Evaluate model on desaturated/low-contrast versions quarterly
2. **Confidence Calibration**: Lower confidence on high-salience detections if salience-bias confirmed
3. **Feature Attribution**: Use LIME/SHAP to verify model isn't relying on color/contrast shortcuts

### Architecture Patterns
1. **Grayscale Fallback**: If salience bias suspected, run model on both color and grayscale images; ensemble results
2. **Adaptive Preprocessing**: Normalize contrast/saturation before inference to reduce salience dependence
3. **Ensemble Color Spaces**: Run model in RGB, HSV, Lab; require agreement across spaces

---

## Production Signals

### Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `vision.low_contrast_accuracy` | <80% (vs. high-contrast baseline) |
| `vision.salience_driven_fp_rate` | >10% of false positives in high-salience regions |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Salience Bias Detected | Accuracy variance >15% across contrast levels | P2 |
| Color Shift Impact | Accuracy drops >10% on desaturated images | P2 |

---

## References

- [Shortcuts and Leakage in Neural Networks](https://arxiv.org/abs/1905.04175)
- [Robustness to Contrast Changes in Vision Models](https://arxiv.org/abs/2211.14437)
