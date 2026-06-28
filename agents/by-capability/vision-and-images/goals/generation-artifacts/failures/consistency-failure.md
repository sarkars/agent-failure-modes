# Consistency Failure: Identity Loss Across Generations

## Issue: Generated Images Lack Consistency Across Multiple Generations (Same Subject, Different Outputs)

**Frequency**: Common

**Symptoms**
- Same prompt generates visually different outputs (good for diversity)
- But can be bad when consistency is needed (character, product)
- Object identity shifts between frames
- Character appearance drastically changes across images

**Root Cause**
Generative models sample stochastically; they have no built-in mechanism to maintain identity/consistency across samples. This is a feature for diversity but a bug when consistency is needed (animation, character design, product continuity).

**Example**
```
Scenario: Animated character generation
Prompt: "Generate 10 frames of character walking"

Frame 1: Character with brown hair, blue shirt
Frame 2: Character with red hair, yellow shirt
Frame 3: Character with blonde hair, green shirt
Impact: Incoherent animation; perceived as different characters
```

**Key Statistics**
- Identity preservation: 40-60% across 10 generations
- Attribute drift: ~5% per frame on average

---

## Mitigation Strategies

1. **Seed Reuse**: Use same random seed across variations (for deterministic parts)
2. **Identity Embedding**: Extract identity token; reuse across generations
3. **LoRA Adaptation**: Fine-tune identity-specific model variant
4. **Reference Image**: Condition each generation on previous frame

### Metrics
- LPIPS distance (perceptual similarity between frames)
- Attribute consistency (face recognition: same identity across images)

### Alerts
- Identity score <50% → P2

---

## References

- [Consistent Image Synthesis](https://arxiv.org/abs/2202.09481)
- [Identity-Preserving Generative Models](https://arxiv.org/abs/2206.06202)
