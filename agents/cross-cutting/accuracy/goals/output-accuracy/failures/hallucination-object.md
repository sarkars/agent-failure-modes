# Hallucination: Objects

## Issue: Model Hallucinates Objects or Fields Not Present in Input

**Frequency**: Occasional

**Symptoms**
- Model describes elements not present in the document/image
- Phantom tables, signatures, fields, or objects extracted
- Non-existent fields populated with plausible values
- Confidence high despite hallucinated content
- More common for optional/rarely-present elements

**Root Cause**
The model's statistical prior about "what typically appears in this context" overrides what this specific input actually contains. When a model is trained on documents/images that usually contain a field (e.g., "invoices typically have a PO number"), it defaults to assuming presence and generating a plausible value rather than explicitly determining absence. The model conflates "this field usually exists" with "this field exists in this specific instance."

**Example**
```
Scenario 1 (Document Processing):
Input: Simple invoice without purchase order reference
Model output: "PO Number: PO-2024-0892"
Reality: No PO field in this invoice; model hallucinated based on "typical invoice" template
Impact: Fake PO number causes ERP lookup failure or matches wrong purchase order

Scenario 2 (Vision):
Image: Shelf with mostly empty space, one blue box, packaging debris
Model detects:
- Blue box (correct)
- Red box (hallucinated - debris interpreted as object)
- Green bottle (hallucinated - lighting artifact)
Impact: Warehouse robot attempts to pick up "green bottle" → gripper hits empty space → collision

Scenario 3 (Multimodal):
Report contains 3 tables (verified in document)
Model extracts: 4 tables (hallucinated 1 table that doesn't exist)
Impact: Downstream analysis fails due to phantom table; report validation catches it only after processing
```

**Key Statistics**
- 10-20% of optional/rarely-present fields hallucinated by extraction models
- Vision models: 15-25% false positive rate on object detection in cluttered scenes
- Hallucination rate increases with low resolution (can be 2-3x higher at 64px vs. 512px)
- Temperature/sampling increases hallucinations: 0.5°C = 5% false positives, 1.0°C = 18% false positives
- Rare objects hallucinated 40%+ more often than common objects

**Contributing Factors**
- Training data imbalance (certain objects/fields overrepresented)
- Input ambiguity (cluttered scenes, low resolution, compression artifacts)
- Model defaults to presence when uncertain rather than explicitly determining absence
- Optional fields not marked clearly as "must determine absence"
- High diversity/temperature in generation

---

## Test Scenario & Reproduction

### Scenario Setup
Environment where you can:
- Provide inputs deliberately lacking optional elements
- Measure false positive rate (elements hallucinated that aren't there)
- Compare model outputs to ground truth on presence/absence
- Vary input conditions (resolution, clutter, clarity)

### Trigger Mechanism
Object hallucinations reliably occur when:
1. Optional fields or rarely-present objects are queried
2. Model is asked to extract in a single pass without explicit presence detection
3. Input is degraded or ambiguous (low-resolution, cluttered, compressed)
4. Dominant training example contains the element frequently

**Example Reproduction Steps:**
```
1. Prepare test set: documents/images both with and without optional elements
2. For documents: 50% include PO number, 50% don't; same for other optional fields
3. For images: 50% contain target object, 50% deliberately empty or with distractors
4. Run model to extract all fields/objects without presence-detection step
5. Measure false positive rate (hallucinations on documents/images that lack the element)
6. Expected failure: FPR 5-20% (model invents optional elements it doesn't see)
7. Compare: is FPR different for common vs. rare elements?
```

### Expected Failure State
- Model populates optional fields that don't exist in input
- Vision detects objects in empty/sparse scenes
- Hallucinated values are well-formatted and plausible
- Confidence high despite element being absent from input
- False positive rate 5-20% on optional/rarely-present elements

### Mitigation Validation Protocol

**Test Checklist:**
- [ ] Reproduce object hallucination on baseline (especially on absent optional fields)
- [ ] Apply mitigation (e.g., presence-detection-first pipeline, grounding requirements, negative sampling)
- [ ] Re-run on same test set including deliberately absent elements
- [ ] Measure improvement: false positive rate reduced by ≥50%
- [ ] Verify no regression: true positive rate on actually-present elements unchanged

**Success Criteria:**
- False positive rate <5% on optional/rarely-present elements
- True positive rate >95% on elements actually in input
- Hallucination detectable via grounding checks (phantom elements lack spatial grounding)
- Latency impact <20%

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Empty scene | Image of blank wall or simple doc without optional fields | No detections/fields or very low confidence | Model detects >1 objects or populates absent fields with high confidence |
| Absent optional | Document/image clearly lacking optional field/object | Explicit "not present" or absence marking | Model populates field/detects object anyway |
| Cluttered noise | Noisy/low-quality input with distractors | No false detections or graceful degradation | Model confidently identifies phantom elements |
| Rare element actually present | Rarely-present element that truly exists | Detected correctly | Missed because model default-assumes absence of rare elements |
| Mix of presence/absence | Some fields present, some absent | Correct presence/absence determination for each | Indiscriminately high FPR on absent elements |

### Evaluation Dataset
- **Source**: COCO (cluttered scenes), synthetic empty images, real documents with varying field completeness
- **Size**: 1,000+ examples with ground-truth presence/absence annotations
- **Key variations**: Scene clutter (0-10+ objects), field completeness (0-100%), object rarity (common to rare), input quality (32px-512px)

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| False Positive Rate | <5% | % of absent elements detected/extracted |
| True Positive Rate | >95% | % of present elements correctly detected/extracted |
| Precision | >0.90 | TP / (TP + FP) — correctness of detections |
| Grounding Coverage | 100% | % of populated fields with spatial/textual grounding |

### Automated Checks
```python
def evaluate_hallucination(model, test_data):
    """Detect object/field hallucination patterns"""
    fps = []  # false positives per sample
    tps = []  # true positives per sample
    
    for input_sample, gt_presence, gt_annotations in test_data:
        predictions = model.extract(input_sample)
        
        for field_or_object, pred_value in predictions.items():
            is_present_gt = gt_presence[field_or_object]
            is_hallucinated = pred_value is not None and not is_present_gt
            
            if is_hallucinated:
                fps.append(1)
            elif pred_value is not None and is_present_gt:
                tps.append(1)
    
    fpr = sum(fps) / len(fps) if fps else 0
    tpr = sum(tps) / len(tps) if tps else 0
    
    assert fpr < 0.05, f"False positive rate too high: {fpr:.2%}"
    assert tpr > 0.95, f"True positive rate too low: {tpr:.2%}"
    
    return {
        'false_positive_rate': fpr,
        'true_positive_rate': tpr,
        'passed': fpr < 0.05 and tpr > 0.95
    }
```

---

## Mitigation Strategies

### Prevention

1. **Mandatory Grounding for Every Populated Field**: Require every extracted field—especially optional ones—to carry a spatial bounding box or textual grounding pointing to the exact source region. Fields cannot be populated without one. This structurally prevents inventing values the document doesn't contain.

2. **Negative-Sample Training on Absent Fields**: Explicitly fine-tune or few-shot-prompt on documents/images lacking commonly-expected fields. Train the model to recognize and output "field absent" as a valid, expected state rather than defaulting to its training-distribution prior that "fields usually exist."

3. **Two-Step Presence-Then-Value Pipeline**: Separate "does this field exist in this input?" (binary grounded detection) from "what is its value?" (extraction conditioned on confirmed presence). Single-pass extraction conflates the two and defaults toward assuming presence.

### Detection & Response

1. **Grounding-Absence Flagging**: Flag for review any populated field lacking valid spatial/textual grounding, since a value with no traceable source is very likely hallucinated. This catches hallucinations before they impact downstream systems.

2. **Downstream Lookup-Failure Correlation**: Monitor cases where an extracted reference value (PO number, order ID) fails lookup in the system of record. High rate of "extracted but not found" values signals object hallucination on optional fields.

3. **Field-Presence-Rate Monitoring**: Track what percentage of documents have a given optional field, and compare against the known population rate. Extraction pipeline populating an optional field far more often than the true population indicates systemic hallucination.

### Architecture Patterns

1. **Presence-Detection-Then-Extraction Two-Step**: Separate architecture: first model/rule determines presence (binary: yes/no), second model extracts value only if presence confirmed. Each step can use appropriate model/method for its task.

2. **Grounding-Required Validation Gate**: Insert validation between extraction and downstream consumption that rejects any populated field lacking valid grounding metadata. Prevents hallucinated ungrounded values from reaching production regardless of model that produced them.

3. **Reference-Value Verification Against System-of-Record**: For extracted values referencing external IDs, verify existence in authoritative system before accepting. Hallucinated but well-formatted IDs will fail this check even when they look plausible.

---

## Production Signals

### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `ungrounded_field_rate` | % of populated optional fields lacking bounding-box grounding | >2% (alert on any occurrence) |
| `field_presence_rate_vs_population` | Extraction populate rate vs. known true rate for optional fields | >15 points above true rate (systematic hallucination) |
| `reference_lookup_failure_rate` | % of extracted reference IDs (PO, order) that fail system-of-record lookup | >8% |
| `phantom_field_audit_rate` | % of "field not in document" sampled cases that were populated by extraction | >5% |
| `false_positive_rate` | % of objects/fields detected that don't exist in ground truth | >10% |

### Logs & Traces
- Log every populated field/detected object with: grounding metadata (location/citation), confidence, presence determination
- Track dual-path results (if using presence-detection-first approach)
- Include post-hoc validation: lookup result for reference IDs, grounding verification
- Log input quality metadata: resolution, scene complexity, field completeness

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Ungrounded Field in Production | Populated field without valid spatial grounding found | P1 | Treat as pipeline defect; audit recent output from that path |
| Field Presence Rate Anomaly | Optional field populated >15% more often than true population rate | P2 | Sample recently extracted documents; investigate presence-detection failure |
| Lookup Failure Spike | Extracted reference IDs fail system-of-record lookup >8% | P2 | Sample failed lookups; confirm whether field was hallucinated vs. data issue |
| High False Positive Rate | Object detection false positive rate >10% | P2 | Investigate model regression or data drift; check object thresholds |

### Dashboard Panels
- Panel 1: Ungrounded field rate over time (should be near 0%)
- Panel 2: Field presence rate vs. known population (should track closely)
- Panel 3: Reference ID lookup success rate (should be 90%+)
- Panel 4: False positive rate by object/field type
- Panel 5: Grounding coverage: % of extracted items with valid source citations

### Health Checks
```sql
-- Daily hallucination detection audit
SELECT 
  DATE(timestamp) as date,
  field_or_object_type,
  COUNT(*) as total_extracted,
  SUM(CASE WHEN has_grounding THEN 1 ELSE 0 END) as grounded_count,
  SUM(CASE WHEN NOT has_grounding AND value IS NOT NULL THEN 1 ELSE 0 END) as ungrounded_count,
  SUM(CASE WHEN is_hallucinated THEN 1 ELSE 0 END) as hallucinated_count,
  (SUM(CASE WHEN is_hallucinated THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0)) as hallucination_rate
FROM extracted_fields_objects
WHERE timestamp > NOW() - INTERVAL 1 DAY
GROUP BY DATE(timestamp), field_or_object_type
HAVING ungrounded_count > 0 OR hallucination_rate > 0.05
  THEN ALERT "Object/field hallucination detected"
```

---

## Related Patterns

**Parent Pattern**: [Hallucination: Base Mechanism](hallucination-base-mechanism.md) — This is a sub-pattern focusing on object/field hallucination specifically.

**Sibling Patterns**:
- [Hallucination: Attributes](hallucination-attribute.md) — Hallucinated properties of correct objects vs. entire object hallucination
- [Hallucination: Confidence Miscalibration](hallucination-confidence-miscalibration.md) — Why hallucinated objects come with high confidence

**Domain-Specific Variants**:
- **[Document Processing: Object Hallucination](../../../by-capability/document-processing/goals/multimodal-reliability/failures/object-hallucination.md)** — Phantom fields and phantom table hallucinations
- **[Vision: Object Hallucination](../../../by-capability/vision-and-images/goals/visual-hallucination/failures/object-hallucination.md)** — False object detection in cluttered or empty scenes

---

## References

- [Hallucination of Multimodal LLMs Survey](https://arxiv.org/html/2404.18930v2) — Object hallucination taxonomy and prevalence
- [Mitigating OCR Hallucinations in MLLMs](https://arxiv.org/html/2506.20168v2) — Phantom element detection techniques
- [Evaluating Multimodal LLMs for Production](https://galileo.ai/blog/multimodal-llm-guide-evaluation) — Grounding validation strategies for document and vision extraction
- [Evaluating Visual Hallucinations in Large Vision and Language Models](https://arxiv.org/abs/2310.01798) — Analysis of vision model false positives
