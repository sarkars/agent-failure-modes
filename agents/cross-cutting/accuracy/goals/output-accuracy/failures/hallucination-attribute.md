# Hallucination: Attributes

## Issue: Model Hallucinates Object Attributes Not Present in Input

**Frequency**: Common

**Symptoms**
- Object identified correctly, but properties are wrong
- Colors, dates, quantities, or other attributes don't match input
- Model "corrects" unusual but valid values to common patterns
- Confidence high despite wrong attribute
- Hallucinations more common on ambiguous inputs (shadows, poor resolution, degraded quality)

**Root Cause**
When the model correctly identifies an object but must assign properties, it defaults to the most probable attribute from its training distribution rather than grounding in the actual input. This is especially pronounced when input is ambiguous (shadows make color unclear, compression artifacts obscure details, or the attribute appears in the training data far more often in one form than another). The model has no structural requirement to ground attribute assignment in visual/textual evidence.

**Example**
```
Scenario 1 (Document Processing):
Input: Invoice dated "2024-02-29" (leap year, valid but uncommon)
Model output: "Invoice date: 2024-02-28" (model "corrected" to non-leap-year)
Reality: 2024-02-29 is the actual date; model hallucinated a "corrected" value
Impact: Payment terms calculated from wrong date → missed deadline

Scenario 2 (Vision):
Image: Package in shadow, actually red but appears gray-blue
Model output: "Blue box, 95% confidence"
Reality: Box is red; model inferred from lighting prior
Impact: Warehouse sorting agent routes to wrong bin → customer receives wrong item

Scenario 3 (Multimodal):
Chart shows "2,847 units" (odd number)
Model reads: "Approximately 3,000 units" (rounded to common pattern)
Reality: Exact number is 2,847; model hallucinated nearest round number
Impact: Inventory calculations off → stock-outs or overstock
```

**Key Statistics**
- 20-30% of attribute extractions include at least one hallucinated detail
- Uncommon-but-valid values hallucinated 40%+ more often than common values
- Low-light/ambiguous conditions increase hallucination rate by 2-3x
- Confidence on hallucinated attributes: avg 75-85% (only 5-10% lower than correct)

**Contributing Factors**
- Ambiguous input (low resolution, shadows, occlusions, compression artifacts)
- Uncommon but valid attribute values (leap-year dates, non-standard colors, unusual quantities)
- Strong prior from training data (e.g., "red boxes are common" → assume red when unsure)
- Domain-specific expectations (e.g., "invoices usually have round numbers" → round up values)

---

## Test Scenario & Reproduction

### Scenario Setup
Environment where you can:
- Vary input quality (resolution, lighting, clarity)
- Control attribute commonness (common vs. uncommon values)
- Measure attribute accuracy and confidence
- Compare model outputs across similar inputs with different attributes

### Trigger Mechanism
Attribute hallucinations reliably occur when:
1. Input is ambiguous or low-quality (shadows, compression, degradation)
2. Attribute is uncommon in training data (leap-year dates, non-standard colors)
3. Model is asked about optional attributes (may not exist in input)
4. Multiple valid interpretations of input exist

**Example Reproduction Steps:**
```
1. Create dataset: objects with ground-truth attributes, vary input quality
2. Include specifically: 50% common attribute values, 50% uncommon-but-valid
3. Run model on high-quality inputs → measure accuracy on common and uncommon attributes
4. Run model on degraded inputs (shadows, low-res, compression) → repeat measurement
5. Compare: accuracy drops differently for common vs. uncommon attributes?
6. Expected failure: accuracy on uncommon values drops 20-40% more than common values
7. Measure confidence on each attribute type
```

### Expected Failure State
- Model produces confident wrong attributes on ambiguous inputs
- Uncommon-but-valid attributes are "corrected" toward common patterns
- Confidence on wrong attributes nearly matches confidence on correct attributes
- Hallucination patterns consistent across similar inputs
- Vision models: attribute changes with lighting despite same object

### Mitigation Validation Protocol

**Test Checklist:**
- [ ] Reproduce attribute hallucination on baseline (especially on uncommon values)
- [ ] Apply mitigation (e.g., grounding validation, dual-path extraction, adversarial testing)
- [ ] Re-run on same test set including uncommon-value cases
- [ ] Measure improvement: accuracy on uncommon values improved by ≥20%
- [ ] Verify no regression: accuracy on common values unchanged

**Success Criteria:**
- Attribute accuracy >95% on both common and uncommon values (gap <5%)
- Confidence-accuracy correlation >0.7 per attribute type
- Hallucination rate on uncommon values reduced by ≥50%
- Overall latency impact <15%

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Uncommon value | Leap-year date, non-standard color | Correct attribute detected | Model "corrects" to common pattern |
| Ambiguous visual | Shadowed object, compression artifacts | Low confidence or explicit uncertainty | High confidence despite ambiguity |
| Mixed attributes | Some common, some uncommon | Consistent accuracy across both | Uncommon attributes more error-prone |
| Lighting variation | Same object, different lighting | Stable attribute across lighting | Attribute changes with lighting (model following context) |
| Quality degradation | High-res then low-res input | Graceful degradation in accuracy | Sharp accuracy cliff at resolution threshold |

### Evaluation Dataset
- **Source**: Real documents with uncommon values, images with lighting variations, multimodal data
- **Size**: 1,000+ examples with attribute annotations
- **Key variations**: Attribute commonness (0-100th percentiles), input quality (32px-512px), lighting conditions (bright/normal/low-light)

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Attribute Accuracy (Common) | >98% | % of common-value attributes correct |
| Attribute Accuracy (Uncommon) | >90% | % of uncommon-but-valid attributes correct |
| Accuracy Gap | <5% | Common accuracy - Uncommon accuracy |
| Confidence-Accuracy Correlation (per attribute) | >0.7 | Correlation for each attribute type |

### Automated Checks
```python
def evaluate_attribute_hallucination(model, test_data):
    """Detect attribute hallucination patterns"""
    results = {'common': [], 'uncommon': []}
    
    for obj, ground_truth_attrs, attribute_commonness in test_data:
        pred_attrs = model.extract_attributes(obj)
        
        for attr_name, pred_val in pred_attrs.items():
            gt_val = ground_truth_attrs[attr_name]
            is_correct = pred_val == gt_val
            is_uncommon = attribute_commonness[attr_name] < 0.25  # Bottom quartile
            
            bucket = 'uncommon' if is_uncommon else 'common'
            results[bucket].append({
                'correct': is_correct,
                'confidence': pred_attrs.confidence(attr_name),
                'attribute': attr_name
            })
    
    common_acc = mean(r['correct'] for r in results['common'])
    uncommon_acc = mean(r['correct'] for r in results['uncommon'])
    gap = common_acc - uncommon_acc
    
    assert gap < 0.05, f"Accuracy gap too large: {gap:.2%} (common {common_acc:.1%} vs uncommon {uncommon_acc:.1%})"
    assert uncommon_acc > 0.90, f"Uncommon attribute accuracy too low: {uncommon_acc:.1%}"
    
    return {
        'common_accuracy': common_acc,
        'uncommon_accuracy': uncommon_acc,
        'gap': gap
    }
```

---

## Mitigation Strategies

### Prevention

1. **Raw Extraction + Normalization Separation**: Always retain raw extracted values (exact character-level reads) alongside normalized versions. Store both immutably, with normalization as a separate versioned transformation layer that can be re-run or rolled back. This preserves the original input so hallucinated "corrections" can be detected and reverted.

2. **Domain-Rule Validation on Every Attribute**: Maintain domain-specific validation rules per attribute type (leap-year calendar checks for dates, valid color values for colors, plausible range checks for quantities). Route any value that fails validation to human review rather than trusting the model's "corrected" version.

3. **Uncomfortable-Value Adversarial Testing**: Curate test sets specifically containing statistically uncommon-but-valid values (leap-year dates, non-round-number quantities, unusual colors). Test extraction accuracy on these to catch attribute hallucination that aggregate metrics might miss.

### Detection & Response

1. **Dual-Path Extraction with Divergence Flagging**: Run both a generative (model-based) extraction path and a traditional deterministic OCR/rule-based path in parallel. Flag any attribute where the two diverge for human review, since divergence is a strong signal of model-side correction/hallucination.

2. **Statistical Outlier Detection**: Monitor for patterns where extracted attributes cluster suspiciously toward common/round values (round-number quantities, non-leap-year dates, standard colors) at higher rates than the true document population would predict. This signature indicates systematic attribute hallucination.

3. **Field-Level Accuracy Audits on Adversarial Samples**: Periodically audit attribute accuracy specifically on documents containing known uncommon-but-valid values, independent of aggregate accuracy metrics which can look fine while this failure mode silently corrupts a minority of high-value records.

### Architecture Patterns

1. **Dual-Path Validation Gateway**: Separate the extraction pipeline into two independent paths (generative + deterministic), compare outputs, and gate disagreements to human review. This structurally prevents hallucinated attributes from reaching downstream systems.

2. **Domain-Rule Validation Layer**: Insert a deterministic validation gateway between extraction and consumption that validates every attribute against domain rules (valid calendar dates, plausible ranges, format compliance) before allowing the value downstream.

3. **Versioned Normalization Pipeline**: Implement normalization (date formatting, currency parsing, unit conversion) as a separate, versioned transformation layer on top of immutable raw extractions. If hallucination is detected, normalization can be rolled back without re-extracting.

---

## Production Signals

### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `attribute_accuracy_gap` | Accuracy on uncommon vs. common attribute values | >5% gap (indicates selective hallucination) |
| `ocr_model_divergence_rate` | % of attributes where dual paths disagree | >8% (indicates model hallucination) |
| `domain_validation_failure_rate` | % of extracted attributes that fail validation | >4% |
| `uncommon_value_clustering` | Ratio of extracted to true population frequency for uncommon values | >1.2x (model clustering toward common) |
| `confidence_on_hallucinated_attrs` | Avg confidence on attributes that fail post-hoc validation | Should be 15-20% lower than on correct attributes |

### Logs & Traces
- Log every extracted attribute with: raw value, normalized value, confidence, validation result
- Include input quality metadata: resolution, lighting, compression, ambiguity score
- Track dual-path divergences (when model and deterministic path disagree)
- Include post-hoc validation result: passed/failed

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Accuracy Gap Spike | Uncommon vs. common attribute accuracy gap >10% | P2 | Sample recently extracted uncommon values; investigate hallucination |
| Divergence Rate High | Model/OCR paths diverge >8% for attribute type | P2 | Route affected documents to human review; investigate model regression |
| Validation Failures | Domain validation failures exceed 4% for attribute type | P1 | Halt automatic acceptance; investigate whether validation rules or extraction degraded |
| Clustering Bias | Extracted values cluster >20% more toward common patterns than population | P2 | Confirm hallucination via sampling; consider negative-example training |

### Dashboard Panels
- Panel 1: Attribute accuracy by commonness quartile (common vs. uncommon values)
- Panel 2: Model/OCR divergence rate over time (24h rolling window)
- Panel 3: Domain validation failure rate by attribute type
- Panel 4: Confidence distribution on hallucinated vs. correct attributes (histograms)
- Panel 5: Extraction accuracy vs. input quality (resolution, lighting, compression)

### Health Checks
```sql
-- Daily attribute quality audit
SELECT 
  DATE(timestamp) as date,
  attribute_type,
  COUNT(*) as total_extracted,
  SUM(CASE WHEN is_common_value THEN 1 ELSE 0 END) as common_value_count,
  SUM(CASE WHEN is_common_value AND is_correct THEN 1 ELSE 0 END) as common_correct,
  SUM(CASE WHEN NOT is_common_value THEN 1 ELSE 0 END) as uncommon_value_count,
  SUM(CASE WHEN NOT is_common_value AND is_correct THEN 1 ELSE 0 END) as uncommon_correct,
  (SUM(CASE WHEN NOT is_common_value AND is_correct THEN 1 ELSE 0 END) / NULLIF(SUM(CASE WHEN NOT is_common_value THEN 1 ELSE 0 END), 0)) as uncommon_accuracy,
  (SUM(CASE WHEN is_common_value AND is_correct THEN 1 ELSE 0 END) / NULLIF(SUM(CASE WHEN is_common_value THEN 1 ELSE 0 END), 0)) as common_accuracy
FROM extracted_attributes
WHERE timestamp > NOW() - INTERVAL 1 DAY
GROUP BY DATE(timestamp), attribute_type
HAVING (common_accuracy - uncommon_accuracy) > 0.05 
  THEN ALERT "Attribute hallucination on uncommon values detected"
```

---

## Related Patterns

**Parent Pattern**: [Hallucination: Base Mechanism](hallucination-base-mechanism.md) — This is a sub-pattern focusing on attribute hallucination specifically.

**Sibling Patterns**:
- [Hallucination: Objects](hallucination-object.md) — Hallucinated entire objects vs. just their attributes
- [Hallucination: Confidence Miscalibration](hallucination-confidence-miscalibration.md) — Why hallucinated attributes come with high confidence

**Domain-Specific Variants**:
- **[Document Processing: Attribute Hallucination](../../../by-capability/document-processing/goals/multimodal-reliability/failures/attribute-hallucination.md)** — Value correction errors in document extraction
- **[Vision: Attribute Hallucination](../../../by-capability/vision-and-images/goals/visual-hallucination/failures/attribute-hallucination.md)** — Color/size/material misattribution in object detection

---

## References

- [Hallucination of Multimodal LLMs Survey](https://arxiv.org/html/2404.18930v2) — Attribute hallucination taxonomy and prevalence
- [Why LLMs Hallucinate More on Enterprise Documents](https://www.adlibsoftware.com/news/why-llms-hallucinate-more-on-enterprise-documents) — Analysis of value correction errors
- [IDP Accuracy Reckoning 2026](https://idp-software.com/news/idp-accuracy-reckoning-2026/) — Production validation strategies for document extraction
- [Attribute Recognition Under Lighting Variation](https://arxiv.org/abs/2108.04930) — Vision model robustness on attribute extraction
