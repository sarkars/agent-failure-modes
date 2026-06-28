# Relative Position Confusion

## Issue: Model Misunderstands Spatial Relationships Between Objects

**Frequency**: Common

**Symptoms**
- "Object A is left of B" → Actually right of B
- Containment wrong (object inside vs. beside)
- Above/below reversed in images
- Relational queries fail (e.g., "pick up box to the left of the red ball")

**Root Cause**
Spatial reasoning requires understanding relative positions, which is harder than absolute localization. Models learn statistical shortcuts ("red objects usually left") instead of actual spatial relationships.

**Example**
```
Agent instruction: "Pick up the cup to the left of the bottle"
Model understanding: Picks up cup on the RIGHT (hallucinated relationship)
Impact: Wrong object grasped
```

**Contributing Factors**
- Training data imbalance (more "left" examples than "right")
- Symmetric objects (humans confuse left/right too)
- Occlusion hiding spatial context

---

## Mitigation Strategies

1. **Spatial Graphs**: Build scene graph of object relationships; reason over graph not raw image
2. **Relational Networks**: Train on balanced left/right/above/below examples
3. **Negative Sampling**: Include deliberately incorrect spatial relationships in training

### Metrics
- Relational accuracy: % of spatial relationship queries correct

### Alerts
- Systematic left/right bias detected (e.g., 70% of "left" queries succeed, 40% of "right")

---

## References

- [Scene Graphs for Vision](https://arxiv.org/abs/1811.12035)
- [Relational Reasoning in Vision](https://arxiv.org/abs/1706.01433)
