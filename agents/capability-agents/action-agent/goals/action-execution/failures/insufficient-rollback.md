# Insufficient Rollback

## Issue: Agent cannot undo a bad action.

**Frequency**: Rare but Catastrophic

**Symptoms**
- No revert path after failure.
- [Add more specific symptoms]

**Root Cause**
Agent cannot undo a bad action.

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
1. Rollback workflows and reversible defaults.
2. [Add more prevention strategies]

### Detection
- No revert path after failure.

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

- [CSA-Agentic-Profile](https://labs.cloudsecurityalliance.org/agentic/agentic-nist-ai-rmf-profile-v1/)
- Note: Agentic AI governance profile built around NIST RMF.
