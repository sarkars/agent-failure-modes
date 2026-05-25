# Base Agent

Cross-cutting failure patterns that apply to **all AI agents** regardless of domain.

## Sub-Agents

| Agent | Description | Goals | Patterns |
|-------|-------------|-------|----------|
| [Security Agent](security-agent/) | Security, trust, runtime protection, data loss prevention | 5 | 57 |
| [Accuracy Agent](accuracy-agent/) | Output correctness, anti-hallucination, evaluation | 5 | 53 |
| [Operations Agent](operations-agent/) | Tools, cost, coordination, memory, context, state | 12 | 112 |
| [Governance Agent](governance-agent/) | Compliance, audit, accountability, policy | 1 | 12 |
| [Learning Agent](learning-agent/) | Self-improvement, feedback loops, safe learning | 1 | 12 |

**Total: 246 patterns across 24 goals**

## Structure

```
base-agent/
├── security-agent/     # Security, trust, DLP
├── accuracy-agent/     # Output correctness, evaluation
├── operations-agent/   # Tools, cost, coordination
├── governance-agent/   # Compliance, accountability
└── learning-agent/     # Self-improvement
```

## How to Use

1. **Start with Security** - Review security patterns first
2. **Check Accuracy** - Ensure agent doesn't hallucinate
3. **Optimize Operations** - Tool reliability, cost efficiency
4. **Add Governance** - Compliance and accountability
5. **Enable Learning** - Safe self-improvement

These patterns complement domain-specific agents (RAG, OCR, Voice, etc.).
