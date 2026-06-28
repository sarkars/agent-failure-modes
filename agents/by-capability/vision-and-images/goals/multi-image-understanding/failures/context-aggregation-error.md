# Context Aggregation Error Across Multiple Images

## Issue: Model Fails to Properly Aggregate Context from Multiple Images; Makes Decisions Based on Incomplete Context

**Frequency**: Common

**Symptoms**
- Inference correct when all images seen; wrong when image subset shown
- Context dependencies ignored
- Missing information not compensated for
- Hallucination of information not in provided images

**Root Cause**
Multi-image reasoning requires maintaining awareness of what was learned from each image, what gaps exist, and how to reason under uncertainty. Models often hallucinate rather than admit "don't know." Aggregating evidence from multiple imperfect sources is inherently difficult.

**Example**
```
Scenario: Medical diagnosis from multiple imaging modalities
Image 1 (X-ray): Possible fracture
Image 2 (CT): Confirms fracture, shows severity
Image 3 (MRI): Shows soft tissue damage

Model trained to use all 3 images: Comprehensive diagnosis
Model given only Image 1: Overconfident in tentative diagnosis
Impact: Misdiagnosis when not all imaging available
```

**Key Statistics**
- Accuracy with all images: 90%
- Accuracy with 50% of images: 65%
- Hallucination rate (claims info not in provided images): 10-15%

---

## Mitigation Strategies

1. **Context Tracking**: Explicitly track what's been seen/not seen
2. **Uncertainty Quantification**: Model confidence based on available info
3. **Query Mechanism**: Ask for specific missing information
4. **Graceful Degradation**: Performance should degrade smoothly with missing data

### Metrics
- Accuracy vs. number of images available
- Hallucination detection rate
- Calibration of uncertainty

### Alerts
- Accuracy drops >20% with missing images → Check model robustness

---

## References

- [Multi-Modal Context Aggregation](https://arxiv.org/abs/2107.01767)
- [Uncertainty in Multi-Source Information Fusion](https://arxiv.org/abs/2206.03939)
