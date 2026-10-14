# Governance AI Agent Failures by Goal: 33 Patterns, Causes, and Fixes

**Governance AI agents fail in 4 distinct ways, grouped by the goal each failure breaks.** Find the goal that matches what you are seeing, open its list, and use the fix on each pattern page.

## Key Takeaways

- 33 documented patterns across 4 goals; the most documented is [Approval Workflows](approval-workflows/) with 14.
- Each pattern page gives the symptoms, an example, the root cause, and mitigations.

## Governance Goals

| Goal | When it fails | Patterns |
|---|---|---|
| [Agent Oversight](agent-oversight/) | Agents using reinforcement learning or feedback-driven fine-tuning gradually drift from original goals toward unintended behaviors or reward-hacked alternatives that technically achieve… | 1 |
| [Approval Workflows](approval-workflows/) | Multi-step approval chains break partway through because handoffs between stages fail silently, individual stages timeout without escalation | 14 |
| [Governance](governance/) | When things go wrong, no incident process, and no mechanism to prove to regulators that decisions were made according to policy. | 12 |
| [Tool Compliance Limits](tool-compliance-limits/) | Agents execute tool calls without compliance guardrails — audit logging is not enforced at dispatch, so sensitive actions leave no record; PII data is retained past policy expiration | 6 |

**Total: 33 patterns**

## Frequently Asked Questions

### How do approval workflow failures differ from tool-compliance limits?

Approval workflows cover *governance gates* for decisions (requiring human approval before action). See [Approval Workflows](approval-workflows/).

### How does governance differ from approval workflows?

Governance covers the *infrastructure* for accountability (human owner, incident process, audit log, rollback). See [Governance](governance/).

### How does tool compliance differ from approval workflows?

Tool compliance covers enforcement of *policies* at the tool level (audit logging, data retention, data residency). See [Tool Compliance Limits](tool-compliance-limits/).

## Related

- [Governance overview](../)
- [All agent failure patterns](../../../)
