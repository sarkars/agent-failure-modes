# Over-Scoped Agent Permissions

## Issue: Agents Provisioned with Excessive Access Beyond Task Requirements

**Frequency**: Very Common

**Symptoms**
- Agent has read access to data it doesn't need
- Compromise of agent exposes unrelated systems
- Single agent can access entire data pipelines
- No separation between agent tiers
- Supply chain attacks gain broad access through AI layer

**Root Cause**
AI agents are often provisioned with broad permissions for convenience or because the integration layer (e.g., LiteLLM, LangChain) requires access to function. Unlike traditional applications with well-defined permission boundaries, AI agents often inherit the full access of their integration points. This creates attack surfaces where compromising one AI component exposes all connected data stores.

**Example**
```
Intended agent function:
- Match candidates to job requirements
- Generate interview schedules

Actual permissions granted:
- Read access to all candidate profiles
- Read access to all resumes  
- Read access to partner company data (Meta collaboration)
- Write access to scheduling system
- API access to email system

Attack scenario (Mercor/LiteLLM incident):
1. Vulnerability in LiteLLM routing layer (RCE)
2. Attacker exploits RCE via single request
3. Gains access to EVERYTHING the AI integration can reach
4. Exfiltrates candidate data, resumes, partner data

Impact: One vulnerability → complete data breach
```

**Key Statistics**
From AI Security Incidents Report (April 2026):
- Meta AI agent data exposure rated 85/100 risk score (Critical)
- Mercor/LiteLLM supply chain attack rated 95/100 risk score (Critical)
- "Over-scoped provisioning" identified as Stage 1 attack enabler
- 6 hours from LiteLLM vulnerability to data access in confirmed attack

**Permission Anti-Patterns**
| Pattern | Risk | Example |
|---------|------|---------|
| Integration inherits all | Critical | LiteLLM host with full DB access |
| Shared service accounts | High | All agents use same credentials |
| Read-all for convenience | High | Agent scans entire data lake |
| No data layer checks | Critical | App trusts agent's internal filtering |
| Partner data co-mingled | High | Third-party data on same access path |

**Contributing Factors**
- AI integrations designed for rapid prototyping
- Permission models not updated for AI workloads
- "The AI needs access to work" reasoning
- No least-privilege templates for AI agents
- Data layer trusts application-layer filtering

**Mitigation Strategies**
1. **Least-privilege provisioning**: Grant only minimum required access
2. **Hard data-layer checks**: Enforce at database, not agent level
3. **Per-task credentials**: Different permissions for different functions
4. **Zero-trust data access**: Verify every data request independently
5. **Segregated agent tiers**: Different agents for different sensitivity levels
6. **Supply chain auditing**: Track all dependencies in AI pipeline

**Detection**
- Audit agent access patterns vs. actual needs
- Monitor data access outside task scope
- Track permission creep over time
- Alert on unusual data volume access

## References

- [Foresiet: AI Security Incidents April 2026](https://foresiet.com/blog/ai-security-incidents-attack-paths-april-2026/) - Meta AI exposure, Mercor supply chain
- [VentureBeat: 88% Enterprises Breached](https://venturebeat.com/security/most-enterprises-cant-stop-stage-three-ai-agent-threats-venturebeat-survey-finds/) - AI agent security enforcement gap
- [Kiteworks: 65% of Firms Hit by AI Agent Security Incidents](https://www.kiteworks.com/cybersecurity-risk-management/ai-agent-security-incidents-2026/) - Enterprise survey
