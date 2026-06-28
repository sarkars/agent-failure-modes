# Cross-Image Reference Loss

## Issue: Model Fails to Match or Reference Objects Across Different Images

**Frequency**: Common

**Symptoms**
- Same object in Image A and Image B treated as different
- Cross-image matching fails
- No object identity linking across views
- Cannot answer "Is this the same object?"

**Root Cause**
Matching objects across images requires learning discriminative embeddings invariant to viewpoint, lighting, and scale. Independent image processing loses this capability. Cross-image matching is a separate task from single-image classification.

**Example**
```
Scenario: Document verification (check if photos are of same person)
Image 1: Driver's license photo
Image 2: Selfie

Model: Cannot determine if same person
Expected: High confidence match if same person; low if different
Impact: Fraud detection failure
```

**Key Statistics**
- Cross-image matching accuracy: 70-85% for easy cases
- Hard cases (different angles/lighting): 40-60%
- False match rate: 5-15%

---

## Mitigation Strategies

1. **Siamese Networks**: Train architecture to learn matching embeddings
2. **Metric Learning**: Use triplet loss to pull same objects together
3. **Fine-Grained Features**: Capture discriminative details for matching
4. **Ensemble Matching**: Use multiple similarity metrics; average

### Metrics
- Cross-image matching F1 score
- False match rate (false positives)

### Alerts
- Cross-image matching <70% → P2

---

## References

- [Metric Learning for Image Matching](https://arxiv.org/abs/2002.08206)
- [Face Verification Benchmarks](https://arxiv.org/abs/1604.02878)
