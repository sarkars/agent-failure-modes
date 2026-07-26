# Missing Self-Reflection for High-Stakes Output

## Issue: Agent skips a beneficial critique/revise pass on a high-stakes output, going straight to a single-shot answer where a reflection round would demonstrably have caught an error.

**Frequency**: Occasional

**Symptoms**
- High-stakes or irreversible-action-adjacent outputs ship from a single generation pass with no critique/verification step, even though the task type has a track record of benefiting from one
- [Add more specific symptoms]

**Root Cause**
Agent skips a beneficial critique/revise pass on a high-stakes output, going straight to a single-shot answer where a reflection round would demonstrably have caught an error.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- No difficulty/stakes classifier routes high-stakes outputs into a mandatory reflection pass; reflection (where it exists at all) is applied uniformly or not at all rather than being stakes-aware
- [List factors that make this failure more likely]

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| [Test name] | [Input] | [Expected output] | [What indicates failure] |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |

---

## Mitigation Strategies

### Prevention
1. **[Add Name]**: [Add description]

### Detection & Response
1. **[Add Name]**: [Add description]

### Architecture Patterns
1. **[Add Name]**: [Add description]

### Metrics
1. **[metric_name]**: Target: [Add]; Alert threshold: [Add]

### Alerts
1. **[Add Alert Name]** (P2 - Warning): Condition - [Add]. Action: [Add].

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Medium |

---

## Related Patterns

- [Redundant Self-Reflection Passes](../../../../operations/goals/cost-optimization/failures/redundant-self-reflection-passes.md) - the inverse failure of running reflection when it isn't needed; this pattern is the case of a stakes-aware gate being absent in the other direction, skipping reflection where it was warranted
- [Under-Planning Costly Rework](../../../../operations/goals/cost-optimization/failures/under-planning-costly-rework.md) - a related planning-level (rather than output-critique-level) failure to invest upfront effort proportional to task risk

## References

- [Evaluating LLM Self-Reflection Loops: The 3 Metrics That Matter (2026)](https://futureagi.com/blog/evaluating-llm-self-reflection-loops-2026/) - reflection's quality benefit is real but task-dependent, and most production systems never measure whether it's engaged where it should be
- [Reflection-Driven Control for Trustworthy Code Agents](https://arxiv.org/pdf/2512.21354) - stakes-aware reflection control for trustworthy agent output
