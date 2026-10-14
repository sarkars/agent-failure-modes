# Governance AI Agent Failures by Goal: 33 Patterns, Causes, and Fixes

**Governance failures in AI agents are grouped here into 4 goals, each with a catalog of named failure patterns, the symptoms you will see, the root cause, and mitigations you can copy.** Start from the symptom you are debugging, pick the matching goal below, and open its failure list.

## Key Takeaways

- This cross-cutting concern covers 4 goals and 33 documented failure patterns.
- The largest goal is [Approval Workflows](approval-workflows/) with 14 patterns.
- Each goal page explains the failure class, how to tell it apart from its neighbors, and which mitigations apply across its patterns.
- Each failure page covers the symptoms, an example, the root cause, and how to fix it.

## Governance Goals

| Goal | What goes wrong | Patterns |
|---|---|---|
| [Agent Oversight](agent-oversight/) | Agents using reinforcement learning or feedback-driven fine-tuning gradually drift from original goals toward unintended behaviors or reward-hacked alternatives that technically achieve the stated metric but violate the underlying intent | 1 |
| [Approval Workflows](approval-workflows/) | Multi-step approval chains break partway through because handoffs between stages fail silently, individual stages timeout without escalation, or decision authorities conflict over who can approve what | 14 |
| [Governance](governance/) | Agents operate without accountability, transparency, or compliance controls | 12 |
| [Tool Compliance Limits](tool-compliance-limits/) | Agents execute tool calls without compliance guardrails — audit logging is not enforced at dispatch, so sensitive actions leave no record; PII data is retained past policy expiration; data is deleted without proper audit trail | 6 |

**Total: 33 patterns**

## Frequently Asked Questions

### Where do I start if my governance agent is failing?

Match the symptom to a goal in the table above, then open that goal's page for how to tell its failures apart and where to look first. Each failure page ends in mitigations you can apply directly.

### How are these governance failure patterns organized?

By goal: the outcome the agent is supposed to achieve. Under each goal, a `failures` folder holds one page per pattern. For the full picture see the [Governance overview](../).

## Related

- [Governance overview](../)
- [All agent failure patterns](../../../)
