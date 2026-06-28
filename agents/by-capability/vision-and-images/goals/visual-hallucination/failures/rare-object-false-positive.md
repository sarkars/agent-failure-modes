# Rare Object False Positive

## Issue: Model Detects Rare/Uncommon Objects Not Present in Image

**Frequency**: Common (specifically for rare objects)

**Symptoms**
- Low-frequency objects hallucinated more often than common objects
- False positive rate 40%+ higher for rare objects in training
- High confidence on hallucinated rare objects
- Rare object: any class with <1% frequency in training

**Root Cause**
Training data imbalance creates a "rarity trap": rare objects are underrepresented, so the model learns weak features for rare object detection. When ambiguous features appear in production, the model defaultsto guessing common objects, but also produces false positives on rare objects as it tries to learn rare object features from limited examples.

**Example**
```
Training: 10,000 images with 100 instances of "telescope"
Production: Images without telescopes

Model: Detects "telescope" in 5% of production images (false positives)
Reason: Learned spurious features (white + circular = telescope)
```

**Key Statistics**
- Rare object FP rate: 40% higher than common object FP rate
- Imbalance ratio (most common / rarest) >100x → FP spike
- Long-tail objects: <1% of training → highest false positive rate

---

## Mitigation Strategies

### Prevention
1. **Class Weighting**: Up-weight rare classes during training
2. **Oversampling**: Duplicate rare examples or use mixup
3. **Focal Loss**: Down-weight easy examples, focus on hard rare-object examples
4. **Balanced Validation**: Evaluate on balanced subset; don't trust overall metrics

### Detection & Response
1. **Per-Class Metrics**: Separate FP rate for rare vs. common classes
2. **Rare Object Alerts**: Flag detections of rare objects for human review
3. **Continuous Monitoring**: Monthly rare-class false positive audits

---

## References

- [Long-Tail Recognition in Vision](https://arxiv.org/abs/2106.07099)
- [Class Imbalance in Object Detection](https://arxiv.org/abs/2008.11934)
