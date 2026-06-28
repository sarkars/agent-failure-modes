# Training Data Leakage & Memorization

## Issue: Model Hallucinates Training Data Artifacts, Overfitting to Dataset Biases

**Frequency**: Occasional

**Symptoms**
- Model detects objects that match training data distribution but absent in production
- Hallucination specific to dataset-endemic objects/scenes
- Model "memorizes" training examples; reproduces them in new contexts
- Accuracy drops when dataset composition shifts

**Root Cause**
Vision models memorize training examples when dataset is small or biased. During training on COCO, MS-COCO, or curated corporate datasets, models learn spurious correlations (e.g., "apples always in fruit bowls"). When production data lacks these spurious features, model hallucinates them anyway.

**Example**
```
Training: 80% of images contain green grass in background
Production: Indoor warehouse images with no grass

Model: Detects grass in 15% of indoor warehouse images (hallucinated)
Impact: False positive rate spike in new environment
```

---

## Mitigation Strategies

### Prevention
1. **Dataset Auditing**: Identify overrepresented features; ensure balanced distribution
2. **Domain Randomization**: Train on synthetic data with varied backgrounds/contexts
3. **Continual Learning**: Retrain quarterly on production data to remove dataset biases
4. **Transfer Learning Awareness**: Fine-tune on production data; don't rely solely on ImageNet pretraining

### Detection & Response
1. **Production vs. Training Comparison**: Measure feature distributions; alert on divergence
2. **Memorization Testing**: LEARNABILITY metric—if model achieves high accuracy on random labels, it's memorizing
3. **Domain Drift Detection**: Monitor for dataset shift; retrain if hallucination rate spikes

---

## References

- [Understanding Memorization in Deep Neural Networks](https://arxiv.org/abs/1909.03025)
- [Data Leakage in Vision Models](https://arxiv.org/abs/2211.04529)
