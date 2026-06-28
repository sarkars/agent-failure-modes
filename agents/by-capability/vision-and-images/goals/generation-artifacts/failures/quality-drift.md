# Quality Drift in Generated Images

## Issue: Generated Image Quality Degrades Over Multiple Generation Iterations or Long Sequences

**Frequency**: Common

**Symptoms**
- First generated images: high quality
- Later images: artifacts, blur, degradation
- Cumulative noise across iterations
- Model collapse in extended generation (>100 steps)

**Root Cause**
Iterative generation (diffusion, autoregressive) accumulates noise across steps. Error correction is imperfect; each step's small errors compound. Models don't have explicit mechanisms to prevent quality drift over long sequences.

**Example**
```
Scenario: Generate 10 images of product variations
Image 1: Sharp, clear product
Image 10: Blurred, artifacts, malformed details
Impact: Later images unusable; high rejection rate
```

**Key Statistics**
- Quality degradation: 5-10% per generation step
- Mean quality at step 50: 60% of baseline
- Quality variance across sequence: high (>30%)

---

## Mitigation Strategies

1. **Noise Scheduling**: Carefully tune diffusion schedule to prevent accumulation
2. **Error Correction**: Add refinement step between generations
3. **State Reset**: Periodically reset internal state to prevent drift
4. **Anchor to Prompts**: Re-condition on original prompt at regular intervals

### Metrics
- Quality score decay over generations
- Artifact detection rate across sequence

### Alerts
- Quality drop >20% vs. step 1 → P2

---

## References

- [Diffusion Model Stability](https://arxiv.org/abs/2210.16559)
- [Error Propagation in Generative Models](https://arxiv.org/abs/2304.12386)
