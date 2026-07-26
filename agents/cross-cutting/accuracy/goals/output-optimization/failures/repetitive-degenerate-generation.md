# Repetitive Degenerate Generation

## Issue: A single generation call falls into repeated phrases, loops, or degenerate text (distinct from repeating tool-call actions across turns) because no repetition/frequency penalty or diversity control is applied to open-ended output.

**Frequency**: Occasional

**Symptoms**
- A single response contains the same phrase, sentence, or clause repeated multiple times within one generation, rather than across separate turns
- [Add more specific symptoms]

**Root Cause**
A single generation call falls into repeated phrases, loops, or degenerate text because no repetition/frequency penalty or diversity control is applied to open-ended output.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- No repetition/frequency penalty configured for long, open-ended generation tasks (long-form writing, extended summaries)
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
1. **[Add Alert Name]** (P3 - Info): Condition - [Add]. Action: [Add].

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Low |

---

## Related Patterns

- [Step Repetition](../../../../operations/goals/cost-efficiency/failures/step-repetition.md) - the distinct multi-turn action/tool-call repetition failure; this pattern is repetition within a single generation's text output, a decoding-level issue rather than a state-tracking one
- [Verbose Reasoning](../../../../operations/goals/cost-efficiency/failures/verbose-reasoning.md) - a related but distinct output-bloat failure (excessive length without necessarily repeating content verbatim)

## References

- [Decoding Strategies: How LLMs Choose The Next Word](https://www.assemblyai.com/blog/decoding-strategies-how-llms-choose-the-next-word) - repetition penalty, temperature, top-k, and top-p as decoding-level controls over degenerate/repetitive output
- [Advancing Decoding Strategies: Enhancements in Locally Typical Sampling for LLMs](https://arxiv.org/pdf/2506.05387) - locally typical sampling as a technique balancing diversity and coherence to avoid degenerate repetition
