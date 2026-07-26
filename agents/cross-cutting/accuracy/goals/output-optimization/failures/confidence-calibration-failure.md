# Confidence Calibration Failure

## Issue: Agent's verbalized or scored confidence does not correlate with its actual answer correctness, so confidence cannot be used to gate downstream decisions.

**Frequency**: Common

**Symptoms**
- Agent expresses high confidence on answers that turn out wrong at a similar rate to answers it expresses low confidence on
- [Add more specific symptoms]

**Root Cause**
Agent's verbalized or scored confidence does not correlate with its actual answer correctness, so confidence cannot be used to gate downstream decisions.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- No calibration measurement (e.g., comparing stated confidence bucket against actual accuracy in that bucket) run against production traffic
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

- [Overconfident Planning](../../reasoning-quality/failures/overconfident-planning.md) - the specific case of underestimating task complexity during planning; this pattern is the broader failure of verbalized confidence miscalibration across any output type
- [Over-Trusting Confidence Score](../../verification/failures/over-trusting-confidence-score.md) - the downstream-consumer-side failure of treating a stated confidence as correctness; this pattern is the upstream failure of the confidence score itself being uncalibrated in the first place

## References

- [Uncertainty Quantification and Confidence Calibration in Large Language Models: A Survey](https://dl.acm.org/doi/10.1145/3711896.3736569) - transformer-based LLMs are often miscalibrated and tend toward overconfidence, undermining the reliability of reported confidence
- [LLM Calibration and Uncertainty Quantification in Production AI Agents](https://zylos.ai/research/2026-04-18-llm-calibration-uncertainty-production-agents) - models can often verbalize uncertainty accurately in isolation but fail to use it to guide their own decisions; calibration failures persist in long-context and multi-answer regimes
- [Process Supervision of Confidence Margin for Calibrated LLM Reasoning](https://arxiv.org/pdf/2604.23333) - training-time approaches to jointly optimize reasoning performance and calibrated confidence
