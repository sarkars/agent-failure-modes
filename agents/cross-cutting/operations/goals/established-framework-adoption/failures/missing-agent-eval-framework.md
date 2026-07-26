# Missing Agent Eval Framework

## Issue: Team builds a custom eval harness (a handful of manually-written test prompts checked by eyeballing the output) instead of adopting an established agent/RAG evaluation framework, missing standardized metrics and automatic test-case generation.

**Frequency**: Occasional

**Symptoms**
- "Evaluation" consists of a small, manually maintained prompt list with human eyeballing, rather than standardized metrics computed against a growing test set
- [Add more specific symptoms]

**Root Cause**
Team builds a custom eval harness instead of adopting an established agent/RAG evaluation framework, missing standardized metrics and automatic test-case generation.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- No evaluation of established eval frameworks (standardized metrics, automatic test-set generation, regression tracking) was done before building an ad hoc, manually-maintained test list
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

- [No Regression Testing](../../../../accuracy/goals/verification/failures/no-regression-testing.md) - a related downstream symptom this pattern's missing standardized framework would help systematize
- [Happy Path Only Evals](../../../../accuracy/goals/verification/failures/happy-path-only-evals.md) - a related downstream symptom; established eval frameworks' automatic test-case generation is exactly the kind of coverage a hand-maintained list tends to miss

## References

- [The Best RAG Frameworks in 2026](https://martinuke0.github.io/posts/2026-01-06-the-best-rag-frameworks-in-2026-a-comprehensive-guide-to-building-superior-retrieval-augmented-generation-systems/) - RAGAS for comprehensive evaluation with objective context precision/recall/faithfulness/relevancy metrics and automatic test-dataset generation
- [10 LLM Observability Tools to Evaluate & Monitor AI in 2026](https://www.confident-ai.com/knowledge-base/compare/10-llm-observability-tools-to-evaluate-and-monitor-ai-2026) - survey including DeepEval-class evaluation frameworks with standardized metric suites
