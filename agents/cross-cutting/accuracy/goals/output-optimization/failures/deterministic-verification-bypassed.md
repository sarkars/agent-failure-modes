# Deterministic Verification Bypassed

## Issue: Agent relies solely on an LLM-judge to assess its own output when a deterministic, executable check (schema validation, test suite, linter, tool-call format check) was available and would have caught the error at near-zero cost.

**Frequency**: Common

**Symptoms**
- Output errors that a schema validator, linter, or test suite would catch deterministically instead surface only through LLM-judge review, if at all
- [Add more specific symptoms]

**Root Cause**
Agent relies solely on an LLM-judge to assess its own output when a deterministic, executable check (schema validation, test suite, linter, tool-call format check) was available and would have caught the error at near-zero cost.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- No inventory of which output types have an available deterministic check versus which genuinely require subjective LLM-judge assessment
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

- [Wrong Verifier](../../verification/failures/wrong-verifier.md) - the broader case of using checks too weak for the task's risk level; this pattern is the specific case where a deterministic check existed and was skipped in favor of LLM-judge-only assessment
- [Verifier Hallucination](../../verification/failures/verifier-hallucination.md) - a related failure where the LLM-judge itself hallucinates its assessment

## References

- [GroundEval: A Deterministic Replacement for LLM-as-Judge in Stateful Agent Evaluation](https://arxiv.org/html/2606.22737v2) - deterministic evaluation as a replacement for LLM-as-judge in stateful agent settings
- [LLM Agent Evaluation Metrics in 2026](https://www.confident-ai.com/blog/llm-agent-evaluation-complete-guide) - deterministic checks (schema validation, tool-call format, output length bounds, JSON parsing) run on 100% of outputs and catch the most common errors at essentially zero cost; Tool Correctness is named as a deterministic, non-LLM-judge metric
- [Why Your Agent Evaluation Stack is About to Get Weirder (and Better)](https://medium.com/@Micheal-Lanham/why-your-agent-evaluation-stack-is-about-to-get-weirder-and-better-dc9f8cfb9b07) - LLM-as-judge as a scalable weak supervisor, not dependable ground truth by default
