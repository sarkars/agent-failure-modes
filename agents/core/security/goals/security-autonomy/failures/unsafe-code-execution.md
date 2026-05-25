# Unsafe Code Execution

## Issue: Agent runs generated code without sandboxing.

**Frequency**: Rare but Catastrophic

**Symptoms**
- Generated code executes with broad permissions.
- [Add more specific symptoms]

**Root Cause**
Agent runs generated code without sandboxing.

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
1. Sandboxing and deny-by-default execution.
2. [Add more prevention strategies]

### Detection
- Generated code executes with broad permissions.

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
| [Alert name] | [Condition] | Critical |

---

## References

- [OWASP-LLM-Top10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- Note: LLM application risks including prompt injection, insecure output handling, supply chain, sensitive information disclosure, excessive agency.
