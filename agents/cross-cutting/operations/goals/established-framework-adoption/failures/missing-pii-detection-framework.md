# Missing PII Detection Framework

## Issue: Team relies on ad-hoc regex or manual review for PII detection/redaction instead of adopting an established, maintained framework, missing entity types and edge cases the framework would catch by default.

**Frequency**: Common

**Symptoms**
- PII redaction logic is a small set of hand-written regexes (email, phone, SSN patterns) rather than an NER-plus-pattern-plus-checksum pipeline
- [Add more specific symptoms]

**Root Cause**
Team relies on ad-hoc regex or manual review for PII detection/redaction instead of adopting an established, maintained framework, missing entity types and edge cases the framework would catch by default.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- No evaluation of established open-source PII frameworks (analyzer + anonymizer + confidence scoring) was done before building custom regex-based detection in-house
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
| [Alert name] | [Condition] | High |

---

## Related Patterns

- [PII Field Exposure](../../tool-access-scope-limits/failures/pii-field-exposure.md) - the downstream symptom (PII actually exposed); this pattern is the upstream root cause of not adopting a proven detection framework in the first place
- [PII Field Leakage in Responses](../../tool-access-scope-limits/failures/pii-field-leakage-in-responses.md) - a related downstream leakage symptom this pattern's missing framework would help prevent

## References

- [Microsoft Presidio: PII Detection Guide 2026](https://explainx.ai/blog/microsoft-presidio-pii-detection-anonymization-guide-2026) - open-source framework combining NER, regex, and checksum validation with confidence scoring, plus an anonymizer for redaction/masking/hashing
- [Preventing PII leakage when using LLMs: An introduction to Microsoft's Presidio](https://ploomber.io/blog/presidio/) - recommended pipeline placement: analyze input, anonymize, retrieve, redact chunks, assemble prompt, redact output before storing the trace
- [The complete guide to PII detection and redaction tools for AI pipelines in regulated industries](https://predictionguard.com/blog/pii-detection-redaction-llm-pipelines-regulated-industries) - survey of PII tooling options for regulated-industry AI pipelines
