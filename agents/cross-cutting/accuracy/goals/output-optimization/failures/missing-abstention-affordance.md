# Missing Abstention Affordance

## Issue: Agent's output space has no low-friction "insufficient information, cannot answer" option, so it produces a best-guess answer even when grounding is inadequate.

**Frequency**: Common

**Symptoms**
- Agent answers confidently on questions where its own retrieved/available context is insufficient to support a grounded answer
- [Add more specific symptoms]

**Root Cause**
Agent's output space has no low-friction "insufficient information, cannot answer" option, so it produces a best-guess answer even when grounding is inadequate.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- No explicit abstention/refusal-to-guess path built into the response schema or prompt instructions
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

- [Bad Refusal](../../../../../by-use-case/customer-service/goals/conversation-resolution/failures/bad-refusal.md) - the inverse failure of refusing when the agent actually had enough information to help; this pattern is the failure to refuse/abstain when it genuinely lacked grounding
- [Confidence Calibration Failure](./confidence-calibration-failure.md) - a related failure where even a well-calibrated low-confidence signal goes unused because there's no abstention path to route it to

## References

- [Task Abstention for Large Language Models in Code Generation](https://arxiv.org/pdf/2605.17029) - task abstention as an explicit, measurable output-space option distinct from low-confidence answering
- [Knowledge Boundary of Large Language Models: A Survey](https://arxiv.org/pdf/2412.12472) - the model's knowledge boundary and the mechanisms (or absence of mechanisms) for recognizing and acting on it
