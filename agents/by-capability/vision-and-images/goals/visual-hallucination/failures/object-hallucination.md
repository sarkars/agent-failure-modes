# Object Hallucination

## Issue: Vision Model Detects Objects Not Present in Image

**Frequency**: Occasional

**Symptoms**
- Model confidently identifies objects that aren't in the image
- Agent takes action based on hallucinated object (e.g., tries to pick up non-existent item)
- False detections more common in low-resolution or cluttered images
- Hallucination rate increases with model temperature/sampling

**Root Cause**
Vision models are trained on diverse visual data and learn statistical associations between visual features. When presented with ambiguous or low-confidence regions, the model's language prior about "what objects typically appear in this context" overrides what's actually visible. Salient features (bright colors, edges) can trigger false object predictions, and the model defaults to high-confidence predictions even when visual evidence is weak. This is compounded by imbalanced training data where certain objects are overrepresented.

**Example**
```
Scenario: Warehouse inventory agent using vision model to count items

Image: Shelf with mostly empty space, one blue box, and some packaging debris

Model output: 
- Blue box (correct)
- Red box (hallucinated - debris interpreted as red box)
- Green bottle (hallucinated - lighting artifact)
- Plastic bag (correct)

Agent action: Attempts to pick up green bottle → gripper hits empty space → collision detected

Impact: Inventory count incorrect (3 items vs. 2), robot malfunction from unexpected collision
```

**Key Statistics**
From Vision Hallucination Survey (arXiv 2404.18930):
- 15-25% of vision models produce hallucinated objects in cluttered scenes
- Hallucination rate higher in low-resolution images (below 256×256)
- Temperature/sampling increases hallucination: 0.5°C = 5% false positives, 1.0°C = 18% false positives
- Rare objects (bottom 10% of training frequency) hallucinated 40% more often than common objects

**Contributing Factors**
- Training data imbalance (certain objects overrepresented)
- Low image resolution or compression artifacts
- Cluttered backgrounds that create ambiguous features
- High model temperature or sampling diversity
- Context priming (if model expects certain objects in a scene type)
- Partial occlusion creating ambiguous shapes

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Empty scene | Image of blank wall | No detections or very low confidence | Model detects >1 objects with >70% confidence |
| Cluttered noise | Image of texture/noise | No object detections | Model detects recognizable objects |
| Ambiguous shapes | Shadows, reflections | No false objects | Model detects solid objects where only optical artifacts exist |
| Low-resolution | 64×64 downsampled image | Reduced detection count (quality degradation acceptable) | Detection count similar to 512×512 (model confabulating detail) |
| OOD objects | Objects outside training distribution | Uncertain/low confidence | High-confidence detections of completely novel objects |
| Temperature sweep | Same image, vary temperature | Increasing hallucinations with temperature | Same temperature produces inconsistent detections (sampling noise) |

### Evaluation Dataset
- **Source**: COCO dataset subset (cluttered scenes) + synthetic noise images + low-resolution variants
- **Size**: 1,000 images (500 with ground truth labels, 500 deliberately empty/noisy)
- **Key variations**: 
  - Resolution: 64×64, 128×128, 256×256, 512×512
  - Scene complexity: empty, simple (1-2 objects), cluttered (5+ objects)
  - Object types: common (chair, person), rare (telescope, microscope)

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| False Positive Rate (FPR) | <5% on empty scenes | % of objects detected in blank images |
| Hallucination Rate | <8% on cluttered scenes | % of detections not in ground truth |
| Confidence-Accuracy Correlation | >0.7 | Spearman correlation between model confidence and detection correctness |
| Resolution Robustness | <10% variance | Detection count ratio: 512px / 64px (should be ~1.0, not 3.0+) |
| Temperature Stability | <5% variance across 0.5-1.0 range | Std dev of detection counts at different temperatures |

### Automated Checks
```python
def evaluate_hallucination(model, test_images, gt_annotations):
    """
    Detect hallucination patterns in vision model outputs.
    """
    fps = []  # false positives per image
    confidences = []
    
    for img, gt_objects in zip(test_images, gt_annotations):
        detections = model.detect(img, confidence_threshold=0.3)
        
        # False positives: detections not in ground truth
        false_pos = [d for d in detections 
                     if d.class_id not in gt_objects]
        fps.append(len(false_pos) / max(len(detections), 1))
        
        # Confidence stats for hallucinated objects
        for fp in false_pos:
            confidences.append(fp.confidence)
    
    # Hallucination metrics
    fpr = sum(fps) / len(fps)  # False positive rate
    mean_halluc_confidence = mean(confidences)
    
    # Flag issues
    assert fpr < 0.05, f"FPR too high: {fpr:.2%}"
    assert mean_halluc_confidence < 0.5, \
        f"Hallucinations too confident: {mean_halluc_confidence:.2f}"
    
    return {
        "false_positive_rate": fpr,
        "hallucination_confidence": mean_halluc_confidence,
        "passed": fpr < 0.05 and mean_halluc_confidence < 0.5
    }
```

---

## Mitigation Strategies

### Prevention
1. **Confidence Thresholding**: Only accept detections with >70% confidence in production; monitor calibration curve (actual accuracy vs. predicted confidence)
2. **Ground Truth Cross-Check**: Run object detection twice with different model checkpoints; only accept objects detected by both models
3. **Negative Sampling in Training**: Include deliberately empty/noisy images in training data to teach model to reject ambiguous detections
4. **Resolution Preprocessing**: Ensure minimum input resolution (256×256); upscale smaller images instead of downscaling
5. **Semantic Consistency**: Validate detected objects make sense in context (e.g., "watermelon on ceiling" is implausible; flag for review)

### Detection & Response
1. **Confidence Monitoring**: Log all detections with confidence < 60%; alert if hallucination rate spikes above 10%
2. **Disagreement Detection**: Compare outputs across model ensembles; disagreement indicates uncertainty
3. **Action Validation**: Before gripper/robot action, verify object with second sensor (e.g., depth camera confirms object exists)
4. **Post-Action Feedback**: Log gripper failures (attempted pickup with empty result) as hallucination incidents

### Architecture Patterns
1. **Human-in-the-Loop**: Route all low-confidence (<60%) detections to human review before action
2. **Conservative Thresholding**: Start with high threshold (>80%) in production; gradually lower as model proves reliable
3. **Ensemble Voting**: Use 3+ vision models; require agreement (2+ models) before accepting detection
4. **Degradation Mode**: If hallucination rate exceeds threshold, fall back to supervised labeling instead of autonomous detection

---

## Production Signals

### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `vision.object_detection_fpr` | False positive rate on production images | >10% (indicates model degradation) |
| `vision.hallucination_confidence_mean` | Mean confidence of hallucinated objects | >0.6 (model incorrectly confident) |
| `vision.empty_scene_false_detections` | Objects detected in empty/reference images | >2 per 100 images |
| `robot.gripper_empty_grasps` | Grasp attempts with no object detected on contact | >5% of total grasps |
| `model.detection_disagreement_rate` | Disagreement between ensemble members | >15% (indicates high uncertainty) |

### Logs & Traces
- Log all detections with confidence <60% in separate "uncertain_detections" stream
- Include image metadata: resolution, lighting, scene type
- Trace gripper contact state post-grasp: successful grip vs. empty grasp
- Include model checkpoint version in detection logs (for rollback correlation)

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Hallucination Rate Spike | FPR jumps >5% in 1 hour | P2 | Revert to prior model checkpoint; investigate data drift |
| High-Confidence False Positive | Hallucinated object with >80% confidence | P1 | Pause autonomous operation; escalate to human review |
| Resolution Degradation | Detection count variance >20% across 256-512px | P2 | Check for input preprocessing pipeline changes |
| Ensemble Disagreement | >25% of detections have <2/3 model agreement | P2 | Model ensemble out of sync; retrain or rollback |
| Post-Grasp Validation Failure | >10% of confident detections fail post-contact check | P1 | Enable human approval for detections <70% confidence |

### Dashboard Panels
- **Panel 1**: False positive rate over time (24h rolling window)
- **Panel 2**: Confidence distribution for hallucinated vs. correct detections (histogram)
- **Panel 3**: Detection rate by scene complexity (empty, simple, cluttered)
- **Panel 4**: Gripper grasp success rate by detection confidence bins
- **Panel 5**: Model ensemble agreement matrix (heatmap of pairwise disagreement)

### Health Checks
```sql
-- Daily hallucination audit
SELECT 
  DATE(timestamp) as date,
  COUNT(*) as total_detections,
  SUM(CASE WHEN is_hallucinated THEN 1 ELSE 0 END) as hallucinated_count,
  AVG(CASE WHEN is_hallucinated THEN confidence ELSE NULL END) as halluc_avg_confidence,
  SUM(CASE WHEN is_hallucinated AND confidence > 0.7 THEN 1 ELSE 0 END) as high_conf_halluc
FROM vision.detections
WHERE timestamp > NOW() - INTERVAL 1 DAY
GROUP BY DATE(timestamp)
HAVING hallucinated_count / total_detections > 0.1
  THEN RAISE ALERT "Hallucination rate >10%"
```

---

## Universal Pattern Reference

This is a domain-specific implementation of the universal pattern:
**[Hallucination: Objects (Cross-Cutting)](../../../cross-cutting/accuracy/goals/output-accuracy/failures/hallucination-object.md)**

The universal pattern covers why models hallucinate objects/fields. This variant focuses on **vision-based tasks** where models confidently detect objects that don't exist in the image (especially in cluttered or empty scenes).

### Related Domain Variants
- [Document Processing: Object Hallucination](../../../document-processing/goals/multimodal-reliability/failures/object-hallucination.md) — Hallucinated fields in document extraction

### Related Base Pattern
- [Hallucination: Base Mechanism](../../../cross-cutting/accuracy/goals/output-accuracy/failures/hallucination-base-mechanism.md) — Universal root cause of all hallucinations

---

## References

- [Hallucination of Multimodal LLMs Survey](https://arxiv.org/html/2404.18930v2) - Comprehensive taxonomy of object, attribute, and spatial hallucinations in vision models
- [Mitigating OCR Hallucinations in MLLMs](https://arxiv.org/html/2506.20168v2) - Phantom element detection techniques
- [Evaluating Multimodal LLMs for Production](https://galileo.ai/blog/multimodal-llm-guide-evaluation) - Grounding validation and confidence calibration
- [Confidence Calibration in Vision Models](https://arxiv.org/abs/2303.11807) - Analysis of confidence-accuracy gaps in vision transformers
