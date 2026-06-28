# Model Collapse in Generation

## Issue: Generator Produces Repetitive, Low-Diversity Outputs (Mode Collapse)

**Frequency**: Occasional (more common in custom-finetuned models)

**Symptoms**
- All generations very similar despite varied prompts
- Limited visual diversity
- Model "forgets" how to generate certain styles/objects
- Diversity metrics drop sharply during training/deployment

**Root Cause**
Generative models can collapse to a narrow set of high-probability outputs when training objective is misaligned or dataset is skewed. Fine-tuning on narrow data increases collapse risk. Happens especially if generator learns shortcut patterns ("always generate centered object").

**Example**
```
Scenario: E-commerce product image generation
Model trained on 1000 sneaker images

After fine-tuning:
All outputs: Nearly identical white sneaker, slightly rotated
Expected: Variety of shoe styles, colors, angles
Impact: Low user engagement; perceived as broken
```

**Key Statistics**
- Diversity (inception score): Drops 20-40% during collapse
- Unique output patterns: <10 distinct variations for 1000 prompts

---

## Mitigation Strategies

1. **Diverse Training Data**: Ensure training covers full output space
2. **Diversity Loss**: Add diversity penalty during training
3. **Latent Space Regularization**: Penalize generator for ignoring latent input
4. **Ensemble Decoding**: Use multiple checkpoints, aggregate

### Metrics
- Inception score (diversity metric)
- Feature diversity (embeddings should spread in latent space)

### Alerts
- Diversity drop >20% → P2

---

## References

- [Mode Collapse in Generative Models](https://arxiv.org/abs/2106.00672)
- [Diversity in Diffusion Models](https://arxiv.org/abs/2303.05556)
