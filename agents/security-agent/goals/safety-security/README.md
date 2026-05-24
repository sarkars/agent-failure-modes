# Goal: Safety & Security

Prevent prompt injection, data leakage, and unauthorized actions. Security failures can expose sensitive data, enable attacks, and cause serious harm.

## Business Context

- Prompt injection can hijack agent behavior
- Data leakage violates privacy and compliance
- Unauthorized actions can cause irreversible damage
- Security incidents destroy trust and carry legal liability

## Failure Patterns

| Failure Pattern | Frequency | Impact |
|-----------------|-----------|--------|
| [Prompt Injection](failures/prompt-injection.md) | Common | Critical |
| [Data Leakage](failures/data-leakage.md) | Common | Critical |
| [Unauthorized Actions](failures/unauthorized-actions.md) | Occasional | Critical |
| [Credential Exposure](failures/credential-exposure.md) | Common | Critical |
| [Privilege Escalation](failures/privilege-escalation.md) | Occasional | Critical |
| [Output Manipulation](failures/output-manipulation.md) | Common | High |
| [Supply Chain Attacks](failures/supply-chain.md) | Occasional | Critical |
| [Audit Evasion](failures/audit-evasion.md) | Rare | High |
| [Agent Injection](failures/agent-injection.md) | Emerging | Critical |
| [Excessive Agency](failures/excessive-agency.md) | Common | Critical |
| [Human-in-the-Loop Bypass](failures/human-loop-bypass.md) | Occasional | Critical |
| [Memory Poisoning](failures/memory-poisoning.md) | Emerging | Critical |
| [Insufficient Isolation](failures/insufficient-isolation.md) | Common | Critical |
| [Data Provenance Loss](failures/data-provenance-loss.md) | Common | High |
| [Shadow AI Exposure](failures/shadow-ai-exposure.md) | Very Common | Critical |
| [Autonomous System Safety](failures/autonomous-system-safety.md) | Occasional | Critical |
| [Chatbot Manipulation](failures/chatbot-manipulation.md) | Common | High |
| [Shutdown Resistance](failures/shutdown-resistance.md) | Occasional | High |
| [Over-Scoped Permissions](failures/over-scoped-permissions.md) | Very Common | Critical |

## Key Statistics

| Finding | Source |
|---------|--------|
| 88% of enterprises reported AI agent security incidents | VentureBeat/Kiteworks 2026 |
| 61% of incidents involved sensitive data exposure | CSA Report April 2026 |
| 45% of AI-generated code has security vulnerabilities | Veracode 2026 |
| MCP vulnerability affects 200,000+ servers | OX Security April 2026 |

## Key Metrics

- Injection detection rate
- Data leakage incidents
- Unauthorized action attempts
- Security audit pass rate
