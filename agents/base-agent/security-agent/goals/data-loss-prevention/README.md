# Goal: Data Loss Prevention

Prevent AI agents from exposing, leaking, or exfiltrating sensitive data through outputs, logs, tool calls, or cross-session contamination. DLP for agents requires understanding that traditional perimeter-based controls don't apply - the agent itself processes sensitive data and must be constrained in what it can emit.

## Business Context

- Agents process PII, credentials, proprietary data - any output channel is a potential leak
- Compliance requirements (GDPR, HIPAA, PCI-DSS) apply to agent outputs
- Traditional DLP tools weren't designed for LLM output streams
- A single leak can result in regulatory fines, lawsuits, and reputation damage
- Agent logs and traces create secondary exposure risks

## Failure Patterns

| Failure Pattern | Frequency | Impact |
|-----------------|-----------|--------|
| [PII Exposure](failures/pii-exposure.md) | Very Common | Critical |
| [Credential Leakage](failures/credential-leakage.md) | Common | Critical |
| [Training Data Extraction](failures/training-data-extraction.md) | Occasional | High |
| [Cross-Session Data Bleed](failures/cross-session-bleed.md) | Common | Critical |
| [Sensitive Data in Logs](failures/sensitive-data-in-logs.md) | Very Common | High |
| [Tool-Based Exfiltration](failures/tool-based-exfiltration.md) | Occasional | Critical |
| [Compliance Boundary Violation](failures/compliance-boundary-violation.md) | Common | Critical |
| [Context Injection Leakage](failures/context-injection-leakage.md) | Common | High |

## Key Statistics

| Finding | Source |
|---------|--------|
| 61% of AI agent security incidents involved sensitive data exposure | CSA Report April 2026 |
| 88% of enterprises reported AI agent security incidents | VentureBeat/Kiteworks 2026 |
| 52% of enterprise AI responses contain data from ungoverned sources | Enterprise Survey 2026 |
| Samsung employees leaked confidential code via ChatGPT | News Reports |
| GDPR fines for AI data breaches exceeded $50M in 2025 | Regulatory Reports |

## Key Metrics

- PII detection rate in outputs (should be 0%)
- Credential exposure incidents
- Cross-session data contamination rate
- Compliance violation count
- Log sanitization coverage
- Exfiltration attempt blocks

## DLP Architecture for Agents

```
Input → [Input Sanitization] → Agent Processing → [Output Filtering] → Output
                                      ↓
                              [Log Redaction]
                                      ↓
                              Sanitized Logs
```

## Related Patterns

- [Data Leakage](../safety-security/failures/data-leakage.md) - General data leakage (safety focus)
- [Credential Exposure](../safety-security/failures/credential-exposure.md) - Credential handling failures
- [Cross-Tenant Leakage](../runtime-security/failures/cross-tenant-leakage.md) - Multi-tenant isolation
