# Missing Secrets Detection Framework

## Issue: Agent outputs, logs, and tool-call payloads are never scanned by an automated secrets/credential-detection framework, relying on manual review (or nothing) to catch API keys and tokens before they're persisted or displayed.

**Frequency**: Occasional

**Symptoms**
- Agent transcripts and logs are stored and surfaced without ever passing through an automated secrets scanner
- [Add more specific symptoms]

**Root Cause**
Agent outputs, logs, and tool-call payloads are never scanned by an automated secrets/credential-detection framework, relying on manual review (or nothing) to catch API keys and tokens before they're persisted or displayed.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- No evaluation of established secrets-detection frameworks (pattern-plus-entropy-based scanning of logs, transcripts, and tool payloads) was done before relying on manual review
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
1. **[Add Alert Name]** (P1 - Critical): Condition - [Add]. Action: [Add].

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

## Related Patterns

- [Credential Leakage](../../../../security/goals/data-loss-prevention/failures/credential-leakage.md) - the downstream symptom (a credential actually leaked); this pattern is the upstream root cause of never having an automated scanner in place to catch it
- [Missing PII Detection Framework](./missing-pii-detection-framework.md) - the same "ad-hoc versus established framework" mechanism applied to secrets/credentials rather than PII

## References

- [LLM Security Tools: 10 Open-Source Frameworks & Guardrails](https://www.turingpost.com/p/aisecuritytools) - survey of open-source security scanning tools applicable to agent logs and transcripts, including secrets-pattern detection alongside prompt-injection and PII scanning
- [LLM Guard 2026: Free Open-Source LLM Guardrails](https://appsecsanta.com/llm-guard) - includes secrets/credential-pattern scanners among its input/output scanner suite
