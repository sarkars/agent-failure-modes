# Bounding Box Errors

## Issue: Inaccurate Object Localization; Bounding Boxes Don't Match Actual Object Boundaries

**Frequency**: Common

**Symptoms**
- Boxes miss parts of objects (underestimate)
- Boxes include background (overestimate)
- Off-by-one errors in pixel coordinates
- Boxes drift for same object across frames

**Root Cause**
Bounding box prediction is a regression task orthogonal to classification. Models trained for classification don't necessarily learn accurate localization. Small receptive fields, coarse feature maps, or training on imprecise annotations cause boxes to be inaccurate by 5-20% of object size.

**Example**
```
Scenario: Robotic arm using bounding boxes to grasp objects

Predicted box: [100, 100, 180, 150] (80×50 region)
Actual object: [95, 95, 185, 155] (90×60 region)

Gripper centers on predicted box → Misses object corner
Impact: Grasp failure, item dropped
```

**Key Statistics**
- Bounding box error: 10-15% of object size on average
- Corner points more inaccurate than center
- Errors larger for small objects (<50px) and occluded objects

---

## Eval Recipes

### Test Cases
| Test | Metric | Target |
|------|--------|--------|
| IoU (Intersection over Union) | >0.7 | <0.6 = fail |
| Corner accuracy (4 corners) | <10px error | >20px = fail |
| Small object detection | IoU >0.6 | <0.5 = fail |

### Metrics
- **IoU Score**: (intersection / union) of predicted vs. ground truth box
- **Corner Error**: Euclidean distance of predicted corners from GT corners
- **Size Error**: |predicted_area - gt_area| / gt_area

---

## Mitigation Strategies

### Prevention
1. **Anchor Refinement**: Train separate networks for box corner prediction vs. classification
2. **High-Res Features**: Use FPN (Feature Pyramid Networks) for multi-scale localization
3. **Precise Annotations**: Ensure training data boxes are accurately labeled
4. **IoU Loss**: Use IoU-based loss (GIoU, DIoU) instead of L2 regression loss

### Detection & Response
1. **IoU Monitoring**: Alert if average IoU drops below 0.65
2. **Post-Processing**: Apply NMS (Non-Maximum Suppression) to remove overlapping low-quality boxes
3. **Ensemble Refinement**: Average boxes from multiple models

### Architecture Patterns
1. **Multi-Task Learning**: Joint classification + precise localization head
2. **Feature Pyramid**: Coarser predictions for large objects, finer for small
3. **Context Expansion**: Expand boxes by 10-15% before downstream use (conservative margin)

---

## Production Signals

### Metrics
| Metric | Alert |
|--------|-------|
| `vision.avg_iou` | <0.65 |
| `vision.corner_error_pixels` | >15px |
| `robot.grasp_failure_rate` | >5% (correlated with bbox error) |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Low Localization Accuracy | IoU <0.6 | P2 |
| Small Object Blindness | IoU on <50px objects <0.5 | P2 |

---

## References

- [Faster R-CNN: Object Detection](https://arxiv.org/abs/1506.01497)
- [IoU-Loss for Bounding Box Regression](https://arxiv.org/abs/1902.09630)
