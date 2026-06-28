# Safety Filter Bypass in Image Generation

## Issue: Model Generates Unsafe Content Despite Safety Filters (Bypasses Moderation)

**Frequency**: Occasional

**Symptoms**
- Unsafe content generated despite safety classifier
- Prompt manipulation circumvents filters
- Adversarial prompts unlock restricted generation
- Filters ineffective for edge cases

**Root Cause**
Safety classifiers are independently trained models; they can be fooled by adversarial prompts. Generative model has no inherent understanding of safety — only learns statistical patterns. Mismatch between what generator learned and what safety classifier catches.

**Example**
```
Scenario: Content moderation for user-generated images
Direct prompt: "Generate violent scene" → Blocked
Adversarial prompt: "Generate renaissance painting of battle" → Generated
Impact: Unsafe content bypasses filter
```

**Key Statistics**
- Filter bypass rate: 5-15% for adversarial prompts
- False negative rate (unsafe content passes): 3-10%

---

## Mitigation Strategies

1. **Ensemble Classifiers**: Use multiple safety detectors; require all to pass
2. **Adversarial Training**: Train safety classifier on known bypasses
3. **Prompt Inspection**: Pre-filter prompts for known jailbreaks
4. **Human Review**: Sample generations; verify safety on regular basis

### Metrics
- False negative rate (unsafe passes through)
- False positive rate (safe rejected)

### Alerts
- False negative >5% → P1
- Bypass detection → P1

---

## References

- [Adversarial Attacks on Safety Classifiers](https://arxiv.org/abs/2304.12231)
- [Diffusion Model Safety](https://arxiv.org/abs/2305.13860)
