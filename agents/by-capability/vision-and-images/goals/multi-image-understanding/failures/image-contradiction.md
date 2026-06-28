# Image Contradiction Detection Failure

## Issue: Model Fails to Detect Logical Contradictions Across Multiple Images

**Frequency**: Common

**Symptoms**
- Same object has contradictory properties across images
- Model doesn't flag inconsistencies
- High confidence in contradictory statements
- No cross-image reasoning

**Root Cause**
Most vision models process images independently. Cross-image reasoning requires explicit multi-image architecture. Models don't naturally learn to check consistency across images unless explicitly trained to do so.

**Example**
```
Scenario: Multi-angle product inspection
Image 1: "Product is red"
Image 2: "Product is blue" (different angle/lighting)
Image 3: "Product has no defects"
Image 2 contradicts Image 1

Model: Treats each image independently; assigns high confidence to both
Expected: Flag contradiction; escalate for review
Impact: Missed quality control issue
```

**Key Statistics**
- Contradiction detection rate: 30-50% (baseline)
- False positives (flags non-contradictions): 10-20%

---

## Mitigation Strategies

1. **Multi-Image Fusion**: Process all images jointly, not independently
2. **Consistency Scoring**: Compute pairwise consistency across images
3. **Contradiction Detector**: Train separate model to flag contradictions
4. **Confidence Reduction**: Lower confidence for properties detected in only some images

### Metrics
- Contradiction detection precision/recall
- Cross-image consistency score

### Alerts
- Contradiction detected → P2 (escalate for review)

---

## References

- [Visual Reasoning Across Multiple Images](https://arxiv.org/abs/2109.01987)
- [Multi-Image Consistency](https://arxiv.org/abs/2208.03139)
