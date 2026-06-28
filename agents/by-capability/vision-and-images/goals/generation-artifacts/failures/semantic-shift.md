# Semantic Drift in Generated Images

## Issue: Generated Images Slowly Diverge from Original Prompt Intent Over Iterations

**Frequency**: Common

**Symptoms**
- Prompt: "blue car"
- Gen 1: Blue car (correct)
- Gen 2: Bluer car, slightly modified shape
- Gen 3: Car is now purple, misshapen
- Progressive deviation from specification

**Root Cause**
Generative models sample from probability distributions, not deterministic paths. Repeated sampling with slight conditioning changes (temperature, noise) causes gradual drift from original semantic intent. No explicit "anchor" to original specification.

**Example**
```
Scenario: Product customization via iteration
Original prompt: "Red leather wallet, compact, professional"
Gen 1: Matches specification
Gen 2: Wallet slightly larger, color more orange
Gen 3: Now brown fabric, oversized
Impact: Final product mismatches original request
```

**Key Statistics**
- Semantic similarity drop: 3-5% per iteration
- User-perceived drift: >20% after 5 iterations

---

## Mitigation Strategies

1. **CLIP Anchoring**: Compute semantic distance to original prompt; reject if >threshold
2. **Constrained Generation**: Fix semantic attributes (color, size) during generation
3. **Prompt Reinforcement**: Re-inject original prompt constraints between iterations
4. **Single-Pass**: Avoid iterative refinement; generate once, carefully

### Metrics
- CLIP similarity to original prompt
- Attribute consistency (color, size, style maintained)

### Alerts
- Semantic drift >15% → Warn user

---

## References

- [Semantic Robustness in Diffusion Models](https://arxiv.org/abs/2310.03693)
- [CLIP-Guided Image Generation](https://arxiv.org/abs/2112.05139)
