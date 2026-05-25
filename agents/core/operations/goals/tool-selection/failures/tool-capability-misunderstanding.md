# Tool Capability Misunderstanding

## Issue: Agent assumes a tool can do something it cannot.

**Frequency**: Common

**Symptoms**
- Invalid tool arguments or impossible requested action.
- [Add more specific symptoms]

**Root Cause**
Agent assumes a tool can do something it cannot.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
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
1. Tool schema descriptions + capability tests.
2. [Add more prevention strategies]

### Detection
- Invalid tool arguments or impossible requested action.

### Recovery
- [Add recovery strategies]

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | High |

---

## References

- [Tool-Augmented-LLM-Testing](https://homes.cs.washington.edu/~rjust/publ/tallm_testing_ast_2025.pdf)
- Note: Failures in tool-augmented LLM systems and testing implications.
