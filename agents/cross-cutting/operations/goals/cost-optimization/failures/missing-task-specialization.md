# Missing Task Specialization

## Issue: Agent stays on generic frontier-model prompting for a high-volume, narrow, repetitive task long after fine-tuning or distillation would outperform it on both cost and quality.

**Frequency**: Common

**Symptoms**
- A single task type accounts for a large share of monthly request volume, still served by a general-purpose prompt on a frontier model
- [Add more specific symptoms]

**Root Cause**
Agent stays on generic frontier-model prompting for a high-volume, narrow, repetitive task long after fine-tuning or distillation would outperform it on both cost and quality.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- No recurring review of task volume/narrowness against the fine-tune/distill decision threshold (commonly cited around 10K+ requests/day or 50M+ tokens/month for a locked, narrow task)
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

- [Model Selection Waste](../../cost-efficiency/failures/model-selection-waste.md) - the tier-routing failure (choosing among existing off-the-shelf models); this pattern is the distinct case of never specializing a model to the task at all
- [Non-Generalized Plan Template](./non-generalized-plan-template.md) - a related but distinct specialization gap at the plan level rather than the model level

## References

- [Is Fine-Tuning Better Than Prompt Engineering in 2026?](https://llm-stats.com/blog/research/fine-tuning-vs-prompt-engineering-2026) - decision thresholds: fine-tune above ~10K requests/day or when a hyper-specific format can't be reliably enforced by prompting alone
- [The AI Project Distillation Case: When a Smaller Fine-Tune Beats a Bigger Model](https://sfailabs.com/guides/the-ai-project-distillation-case-when-a-smaller-fine-tune-beats-a-bigger-model) - a fine-tuned 8B model can match a 70B model on a narrow, repetitive task
- [Distilling Step-by-Step: Outperforming Larger Language Models with Less Training](https://research.google/blog/distilling-step-by-step-outperforming-larger-language-models-with-less-training-data-and-smaller-model-sizes/) - Google Research on distillation outperforming larger general-purpose models on specialized tasks
