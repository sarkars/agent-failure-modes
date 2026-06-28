# Attribute Hallucination

## Issue: Vision Model Detects Incorrect Attributes of Existing Objects

**Frequency**: Common

**Symptoms**
- Object detected correctly, but color/size/material wrong
- Agent takes action based on wrong attribute (e.g., picks red box when it's blue)
- Confidence high despite incorrect attribute
- Hallucination more common in low-light or occluded objects

**Root Cause**
Models learn statistical correlations between object shape and typical attributes (e.g., "red boxes are common"). When attributes are ambiguous due to lighting, occlusion, or texture similarity, the model defaults to the most probable attribute from training data rather than the actual visual evidence.

**Example**
```
Scenario: Warehouse agent sorting packages by color

Image: Box in shadow appears dark gray, but is actually red

Model output: "Red box, 95% confidence"
Actual: Box is red but appears gray due to lighting

Agent action: Routes to "red" bin → Sorting error

Later: Item ends up in wrong customer shipment → Return/refund cost
```

**Key Statistics**
- 20-30% of attribute errors in low-light conditions
- Color hallucination most common (red/blue confusion in shadows)
- Confidence on incorrect attributes: avg 78% vs. 85% on correct attributes (only 7% variance)

**Contributing Factors**
- Lighting conditions different from training data
- Object occlusion or partial visibility
- Similar object categories with different attributes
- Imbalanced training (common attributes overrepresented)

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Color consistency | Same object, varied lighting | Stable color across lighting | Color changes with lighting (model follows context, not object) |
| Occlusion | Partially hidden object | Attribute inferred from visible part | Confidence >70% on fully occluded attribute |
| Lighting extremes | Very bright/dark images | Graceful degradation or low confidence | High confidence despite poor lighting |
| Attribute diversity | Objects with non-standard attributes | Correct attribute detection | Hallucination of "typical" attribute |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Attribute Accuracy | >95% | % of attributes matching ground truth |
| Attribute Confidence Calibration | >0.8 Spearman corr | Correlation between confidence and correctness |
| Lighting Robustness | <5% variance | Attribute consistency across lighting levels |

### Automated Checks
```python
def check_attribute_hallucination(model, images_with_gt_attributes):
    errors = []
    for img, gt_attr in images_with_gt_attributes:
        pred_obj = model.detect(img)
        pred_attr = pred_obj.attributes  # color, size, material, etc.
        
        for attr_name, pred_val in pred_attr.items():
            gt_val = gt_attr[attr_name]
            if pred_val != gt_val:
                errors.append({
                    'attribute': attr_name,
                    'predicted': pred_val,
                    'ground_truth': gt_val,
                    'confidence': pred_obj.confidence
                })
    
    attr_acc = 1 - len(errors) / len(images_with_gt_attributes)
    assert attr_acc > 0.95, f"Attribute accuracy too low: {attr_acc:.2%}"
    return errors
```

---

## Mitigation Strategies

### Prevention
1. **Attribute-Specific Confidence**: Use separate confidence scores per attribute; trust each attribute independently
2. **Multi-Source Validation**: Use color histogram analysis to cross-check detected color vs. image statistics
3. **Lighting-Normalized Features**: Use color constancy algorithms (e.g., Gray World) to normalize for lighting before model inference
4. **Attribute Disaggregation**: Train separate models for each attribute; ensemble predictions

### Detection & Response
1. **Confidence Thresholding**: Require >85% confidence for attributes; log all <70% confidence predictions
2. **Attribute-Level Alerts**: Alert separately for color vs. size vs. material errors (different false-positive costs)
3. **Post-Action Validation**: Use secondary sensor (scale for weight, spectrometer for color) to validate critical attributes

### Architecture Patterns
1. **Human-in-the-Loop**: Route all ambiguous attributes (<75% confidence) to human verification
2. **Conservative Defaults**: Default to "unknown" attribute if confidence <70% rather than guessing
3. **Attribute Voting**: Ensemble across models; require 2+ agreement on attribute value

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `vision.attribute_error_rate` | >5% |
| `vision.color_hallucination_rate` | >3% |
| `vision.confidence_on_wrong_attribute` | >0.7 (too confident despite error) |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Attribute Mismatch | Predicted attribute conflicts with secondary sensor | P1 |
| Color Confidence Anomaly | High confidence despite lighting extremes | P2 |
| Systematic Attribute Bias | Certain attributes (e.g., all blues → reds) | P2 |

---

## References

- [Hallucination of Multimodal LLMs Survey](https://arxiv.org/html/2404.18930v2)
- [Attribute Recognition Under Lighting Variation](https://arxiv.org/abs/2108.04930)
- [Color Constancy for Vision Models](https://arxiv.org/abs/2211.07292)
