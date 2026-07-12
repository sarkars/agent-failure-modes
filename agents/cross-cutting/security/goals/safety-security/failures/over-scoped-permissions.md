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

## Mitigation Strategies

### Prevention
1. **Least-privilege per-task credential minting**: Issue narrowly scoped credentials matching the specific task (e.g., candidate-matching only) rather than letting the agent inherit the full access of the integration layer, since the root cause is that AI agents "often inherit the full access of their integration points" like LiteLLM or LangChain. Trade-off: requires building and maintaining a credential-minting service rather than reusing one broad, convenient service account.
2. **Hard data-layer authorization checks independent of agent-layer filtering**: Enforce access control at the database/API layer itself rather than trusting that the agent only requested what it needed, directly closing the "No data layer checks" anti-pattern and the "data layer trusts application-layer filtering" contributing factor named in the file. Trade-off: duplicating authorization logic at both the agent and data layers increases maintenance surface and risk of the two falling out of sync.
3. **Segregated agent tiers by data sensitivity**: Run separate agents/service identities for candidate data, partner data, and scheduling instead of one agent spanning all of them, so a compromise doesn't expose co-mingled partner data as happened in the Mercor/LiteLLM incident. Trade-off: more agents and service identities to deploy, monitor, and keep permission-synchronized.

### Detection & Response
1. **Continuous access-vs-need auditing**: Compare each agent's granted permissions against its actual task-driven usage on a recurring basis, flagging unused scopes as permission-creep candidates for revocation, since "permission models not updated for AI workloads" is a named contributing factor.
2. **Data-volume anomaly detection**: Flag when an agent scoped for a narrow function (matching candidates) suddenly performs bulk reads across the full data lake, mirroring the "Read-all for convenience" anti-pattern and the incident's rapid escalation from vulnerability to full data access.
3. **Integration-layer vulnerability correlation**: When a routing/integration dependency (LiteLLM-style) discloses a CVE, immediately audit everything every agent behind that integration could have reached during the exposure window, given the incident's documented "6 hours from vulnerability to data access."

### Architecture Patterns
1. **Per-task credential broker**: Issue time-boxed, scope-limited tokens per task rather than a shared service account with standing broad access, eliminating the "Shared service accounts" anti-pattern where all agents use the same credentials.
2. **Zero-trust data-access gateway**: Independently authorize every data request against the requesting agent's declared task, regardless of what the underlying integration layer is technically capable of reaching, so an RCE in the integration layer (as in the Mercor/LiteLLM case) doesn't automatically grant data access.
3. **Tiered agent architecture with hard segmentation**: Enforce network/data segmentation between sensitivity tiers (candidate data, partner data, scheduling) so a breach in one integration path structurally cannot reach across tiers, unlike the incident where one RCE exposed "EVERYTHING the AI integration can reach."

### Metrics
1. **permission_vs_actual_usage_gap**: Target: <10% of granted scopes unused after 30 days; Alert on any agent using <20% of its granted access (over-provisioning signal).
2. **cross_tier_data_access_attempts**: Target: 0; Alert on any occurrence of an agent accessing data outside its assigned sensitivity tier.
3. **standing_credential_age**: Target: 0 credentials without expiry/rotation; Alert on any credential exceeding policy TTL.
4. **integration_layer_blast_radius**: Target: minimize distinct data stores reachable per integration point; Alert on any integration point reachable to more than one sensitivity tier.

### Alerts
1. **Bulk Data Access Outside Task Scope** (P1): Condition - an agent scoped for a narrow task performs bulk/volume access inconsistent with that task, matching the LiteLLM incident pattern. Action: revoke the credential immediately, isolate the integration point, begin breach investigation.
2. **New Integration-Layer CVE Disclosed** (P1): Condition - a routing/integration dependency (e.g., LiteLLM) discloses a vulnerability. Action: audit all data reachable through that integration within the exposure window, rotate affected credentials.
3. **Cross-Tier or Partner Data Access Detected** (P2): Condition - an agent accesses data outside its assigned sensitivity tier (e.g., partner data from a candidate-matching agent). Action: investigate the co-mingling, enforce tier segregation, review the access path.

## References

- [Foresiet: AI Security Incidents April 2026](https://foresiet.com/blog/ai-security-incidents-attack-paths-april-2026/) - Meta AI exposure, Mercor supply chain
- [VentureBeat: 88% Enterprises Breached](https://venturebeat.com/security/most-enterprises-cant-stop-stage-three-ai-agent-threats-venturebeat-survey-finds/) - AI agent security enforcement gap
- [Kiteworks: 65% of Firms Hit by AI Agent Security Incidents](https://www.kiteworks.com/cybersecurity-risk-management/ai-agent-security-incidents-2026/) - Enterprise survey
