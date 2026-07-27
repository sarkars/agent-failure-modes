# What Are the Most Common Governance Failures in AI Agents?

**Agents operate without approval gates, audit trails, human accountability, or compliance controls — decisions execute without authorization, actions leave no record, no one owns the outcome if something fails, and compliance requirements are unenforced at the tool level.** Governance failures are unique because they don't require the agent to make a *wrong decision* to constitute a failure — a correct decision with no audit trail, made by no one, is still a governance failure that violates compliance and accountability principles.

## Key Takeaways

- 33 distinct failure patterns affect governance across 4 goals: agent oversight (goal drift from feedback), approval workflows (broken chains, conflicting decisions), governance infrastructure (no audit logs, no human owner, no incident process), and tool compliance (audit logging gaps, data retention violations).
- Governance failures are often invisible during operation because the agent may make correct decisions — failures surface only during external audits when the organization can't prove compliance or when post-incident investigation reveals no decision history or owner.
- The reliable fix is mandatory infrastructure: every decision must have an audit trail (who decided, when, on what basis), every agent must have a human owner (accountable for decisions), every high-stakes decision must require approval before execution, every tool call touching sensitive data must be logged at dispatch layer (not optional per-tool).
- Governance failures concentrate wherever automation is prioritized over auditability, compliance is treated as optional, and accountability structures are undefined.

## Goals

| Goal | Patterns | Coverage |
|------|----------|----------|
| [Agent Oversight](goals/agent-oversight/) | 1 | Goal drift from feedback/RLHF |
| [Approval Workflows](goals/approval-workflows/) | 14 | Decision gates, chain execution, conflict resolution |
| [Governance](goals/governance/) | 12 | Accountability, audit, resilience, compliance infrastructure |
| [Tool Compliance Limits](goals/tool-compliance-limits/) | 6 | Audit logging enforcement, data retention, data residency |

**Total: 33 patterns across 4 goals**

Note: Empty scaffold folder with no patterns yet: policy-enforcement (planned for future expansion).

## When Governance Matters

- Agent makes decisions with regulatory consequences (financial, healthcare, legal, compliance decisions) where auditors require proof of decision process
- Multi-step approvals required for high-stakes decisions and chains fail silently or become ambiguous
- Compliance violations carry fines or license risk (GDPR, HIPAA, SOX, data residency) and governance gaps expose the organization
- Post-incident investigation reveals no audit trail, no clear decision owner, no way to understand what happened or prevent recurrence

## Architecture Principles for Governance

**The core insight across all 33 patterns:** governance requires structural enforcement, not policy documents. A governance policy is aspirational; a governance *mechanism* is enforceable. The mitigations fall into three architectural categories:

1. **Accountability and audit**: Assign a human owner to every agent (non-delegable). Maintain an audit trail of every decision with rationale. Log every sensitive action at dispatch layer (mandatory, not optional).

2. **Decision gates and approval**: Define approval boundaries clearly (who can approve what). Implement approval workflows as a single state machine (not distributed handoffs). Detect and alert on broken handoffs immediately.

3. **Compliance and control**: Map every business policy to technical enforcement. Tier decisions by risk (high-stakes get extra review). Implement data-handling controls (retention, deletion, residency) at tool dispatch layer. Make compliance infrastructure mandatory and non-bypassable.

## Related Categories

- [Accuracy](../accuracy/) — correctness of agent decisions, separate from governance of the decision process
- [Security](../security/) — preventing adversarial attacks and unauthorized access, complementary to governance
- [Operations](../operations/) — tool reliability and cost efficiency, upstream infrastructure that governance depends on

See [Core](../) for other cross-cutting patterns.
