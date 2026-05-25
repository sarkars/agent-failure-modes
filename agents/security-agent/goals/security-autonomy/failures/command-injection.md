# Command Injection

## Issue: Agent passes unsafe user/tool input into shell/API commands.

**Frequency**: Rare but Catastrophic

**Symptoms**
- Shell metacharacters or dangerous command patterns.
- [Add more specific symptoms]

**Root Cause**
Agent passes unsafe user/tool input into shell/API commands.

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
1. Input validation and command allowlists.
2. [Add more prevention strategies]

### Detection
- Shell metacharacters or dangerous command patterns.

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
