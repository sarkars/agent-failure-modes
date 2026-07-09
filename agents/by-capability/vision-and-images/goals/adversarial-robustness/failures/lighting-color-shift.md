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

### Prevention
1. **Diverse Lighting-Augmented Training**: Augment training data by systematically varying illumination: brightness (±30%), contrast (±25%), color temperature (2700K-6500K range, warm to cool), saturation (±40%). Use realistic augmentation: simulate specific lighting conditions (LED, fluorescent, incandescent, daylight) rather than uniform shifts. Implement stratified sampling: 30% brightness extreme (very bright +30% or very dim -30%), 30% normal, 40% mid-range. Target: model accuracy stable within ±5% across illumination range [0.3x to 2.0x baseline brightness].
2. **Illumination-Invariant Feature Learning via Normalization**: Pre-process images using illumination-invariant transforms: (1) Compute local contrast normalization or local binary patterns (LBP)—these are inherently lighting-invariant. (2) Use color constancy preprocessing: estimate lighting (white-balancing) and normalize colors before classification. (3) Train on log-space (ε-logarithmic transform): reduces lighting variance while preserving edges. (4) Convert RGB to perceptually-uniform color space (CIELAB) where lighting appears as single channel, separable from color.
3. **Multi-Scale Color & Grayscale Robustness**: Train model with both RGB and grayscale inputs simultaneously (multi-task learning). Model learns that color information subject to lighting noise, but grayscale structure remains stable. Use attention mechanism: model learns which modality to trust based on input (if lighting extreme, rely on grayscale; if normal, use RGB). Implement input augmentation: randomly convert to grayscale with probability 0.2-0.3 during training, forcing model to work without color cues.

### Detection & Response
1. **Lighting Condition Detection & Severity Scoring**: Automatically detect lighting characteristics of incoming images: (1) Compute image brightness histogram, classify as {very_dim, dim, normal, bright, very_bright}. (2) Estimate color temperature (warm/cool). (3) Compute local contrast. Use detector to assign lighting score [0,1] representing deviation from training lighting. Alert on extreme lighting (score >0.7 = unusual).
2. **Illumination Variance Monitoring**: Segment accuracy by detected lighting condition. Target: ±5% accuracy across all lighting ranges. Alert if accuracy in any lighting bin drops >10% from average. Monthly audit: identify lighting conditions where accuracy systematically lower, flag for targeted augmentation.
3. **Color Constancy Effectiveness Tracking**: For color-augmentation-trained model, track accuracy on grayscale vs. full-color inputs. If grayscale accuracy significantly higher (>5%), indicates color channels contain adversarial patterns or noise, not semantic information. Implement correction: increase grayscale augmentation percentage, verify model not overfitting to color patterns.

### Architecture Patterns
1. **Illumination-Robust Preprocessing Pipeline**: Pre-classifier, apply sequence of normalization steps: (1) White-balance: estimate ambient light, scale R/G/B channels. (2) Adaptive histogram equalization: locally normalize contrast. (3) Gamma correction: apply power law (x^gamma) to compress intensity range. (4) Convert to perceptually-uniform space (CIELAB if needed). Implement preprocessing as configurable pipeline: can be enabled/disabled based on input lighting detector. Measure latency overhead (<10ms target).
2. **Dual-Input Ensemble (RGB + Grayscale)**: Train separate lightweight models on RGB and grayscale inputs. At inference, pass image through both paths, compute weighted average of predictions: (RGB_pred * confidence_rgb + Grayscale_pred * confidence_gs). Confidence weights learned during training: under extreme lighting, grayscale gets higher weight. Implement fallback: if either model very confident, use that prediction; if both uncertain, escalate.
3. **Adaptive Lighting-Correction Module**: Small learned network that estimates lighting parameters (brightness scale, color temperature) from input image, applies correction, outputs normalized image. Train jointly with main classifier using adversarial loss: try to make classifier invariant to lighting-corrected vs. uncorrected images. Implement lightweight: 1-2 small conv layers. Can be retrofitted to existing models.

### Metrics
1. **accuracy_across_illumination_ranges**: Measure accuracy separately for detected brightness levels: very_dim (brightness<0.3x), dim (0.3-0.6x), normal (0.6-1.4x), bright (1.4-2.0x), very_bright (>2.0x). Target: <5% difference between lowest and highest accuracy. Alert: >10% difference in any range.
2. **lighting_robustness_score**: Compute as: 1 - (max_accuracy - min_accuracy) / mean_accuracy across lighting range. Target: >0.95 (tight accuracy). Alert: <0.85.
3. **color_temperature_sensitivity**: Train model on dataset with varied color temperature (2700K-6500K). Measure accuracy at each K level. Target: <3% accuracy change per 1000K shift. Alert: >5% per 1000K.
4. **illumination_detector_accuracy**: Automatic lighting detector should correctly classify lighting category. Measure: accuracy of detector vs. ground truth labels. Target: >85%. Alert: <75%.
5. **preprocessing_latency_ms**: Illumination normalization preprocessing overhead. Target: <15ms per image. Alert: >30ms impacts throughput.

### Alerts
1. **Extreme Lighting Condition Detected** (P2): Condition - Incoming image brightness >2.0x or <0.3x training range. Action: Enable illumination-correction preprocessing, reduce confidence threshold by 10%, request user confirmation for critical decisions, log for analysis.
2. **Lighting-Induced Accuracy Degradation** (P2): Condition - Accuracy in specific lighting bin (e.g., very_dim, very_bright) drops >10% from normal lighting. Action: Collect more training data for that lighting condition, retrain with focused augmentation, implement adaptive confidence thresholds by lighting.
3. **Color Dependency Issue** (P2): Condition - Grayscale accuracy significantly exceeds RGB accuracy (>5% difference), indicating model learning spurious color patterns instead of semantic features. Action: Investigate if color channels contain artifacts, increase grayscale augmentation rate, retrain model to be less color-dependent.

---

---

## References

- [Illumination Robustness in Vision](https://arxiv.org/abs/2008.02868)
- [Color Constancy for Robust Recognition](https://arxiv.org/abs/2002.03969)
