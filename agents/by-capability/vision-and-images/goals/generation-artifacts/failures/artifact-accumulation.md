# Artifact Accumulation in Regeneration

## Issue: Repeated Generation/Regeneration of Same Content Introduces Synthetic Artifacts

**Frequency**: Common

**Symptoms**
- Regenerated images contain unnatural patterns, distortions
- Artifacts cluster in specific regions (eyes, hands, textures)
- Quality decreases with each regeneration round
- Visible "compression" or "bleaching" artifacts

**Root Cause**
Generation models learn from training data that rarely contains regenerated/resampled images. Repeated generation exposes model to distribution mismatch — the model's own outputs are not well-represented in training data. Leads to increasingly unnatural patterns.

**Example**
```
Scenario: Iterative product image refinement
Initial: Photo-realistic product image
Regenerate to "rotate 10 degrees": Artifacts appear around edges
Regenerate again: More artifacts, distortion amplifies
Impact: Eventually unusable image
```

**Key Statistics**
- Artifact detection: 10% (1st gen) → 40% (3rd gen)
- User rejection rate: 5% (1st) → 30% (3rd)

---

## Mitigation Strategies

1. **One-Shot Generation**: Prefer single generation over iterative refinement
2. **Regeneration Threshold**: Limit regeneration rounds (max 2-3)
3. **Artifact Detection**: Run artifact detector before accepting regenerated image
4. **Human Review**: Manual approval for regenerated content

### Metrics
- Artifact detection rate per generation round
- User rejection rate per round

### Alerts
- Artifact rate >25% → Reject regeneration

---

## References

- [Synthetic Artifact Detection in Generative Models](https://arxiv.org/abs/2309.14842)
- [Mode Coverage in Diffusion Models](https://arxiv.org/abs/2304.04812)
