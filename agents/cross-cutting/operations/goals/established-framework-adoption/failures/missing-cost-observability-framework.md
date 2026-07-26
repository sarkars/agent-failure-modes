# Missing Cost Observability Framework

## Issue: Team tracks LLM spend via manual log scraping or spreadsheet exports instead of adopting an established gateway/observability framework, losing real-time budget enforcement and per-call cost attribution.

**Frequency**: Common

**Symptoms**
- Cost data is reconstructed after the fact from raw provider billing exports rather than attributed per-call, per-session, or per-customer in real time
- [Add more specific symptoms]

**Root Cause**
Team tracks LLM spend via manual log scraping or spreadsheet exports instead of adopting an established gateway/observability framework, losing real-time budget enforcement and per-call cost attribution.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- No evaluation of established LLM gateway (budget enforcement before spend) or tracing/observability (cost attribution after the fact) frameworks was done before building custom logging
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

- [Cost Anomaly Blindness](../../cost-tracking/failures/cost-anomaly-blindness.md) - the downstream symptom of not noticing cost spikes; this pattern is the upstream root cause of not adopting a framework that would surface them by default
- [Budget Enforcement Bypass](../../cost-tracking/failures/budget-enforcement-bypass.md) - a related downstream failure this pattern's missing gateway layer would help prevent

## References

- [LLM Gateway 2026: OpenRouter vs LiteLLM vs Portkey vs Helicone](https://klymentiev.com/blog/llm-gateway-guide) - layered architecture: Layer 1 gateway/proxy (LiteLLM, Helicone, Portkey) enforces budget limits before spend; Layer 2 observability/tracing (Langfuse, LangSmith, Braintrust) attributes cost after the fact
- [Best LLM Cost Tracking Tools (2026)](https://leanlm.ai/blog/llm-cost-tracking-tools) - comparison of cost-tracking tooling options
- Langfuse (MIT), Opik (Apache 2.0), and MLflow (Apache 2.0) are named as fully open-source, no-restriction options for cost/observability tracing
