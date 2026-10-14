# Support Services AI Agent Failures by Goal: 31 Patterns, Causes, and Fixes

**Support Services failures in AI agents are grouped here into 5 goals, each with a catalog of named failure patterns, the symptoms you will see, the root cause, and mitigations you can copy.** Start from the symptom you are debugging, pick the matching goal below, and open its failure list.

## Key Takeaways

- This use case covers 5 goals and 31 documented failure patterns.
- The largest goal is [Ticket Routing](ticket-routing/) with 8 patterns.
- Each goal page explains the failure class, how to tell it apart from its neighbors, and which mitigations apply across its patterns.
- Each failure page covers the symptoms, an example, the root cause, and how to fix it.

## Support Services Goals

| Goal | What goes wrong | Patterns |
|---|---|---|
| [Issue Resolution](issue-resolution/) | Issue-resolution agents fail when they select a canned response by keyword similarity without verifying situational fit, when a multi-agent handoff loses a prior troubleshooting attempt the customer already described | 7 |
| [Self Service Deflection](self-service-deflection/) | Self-service deflection agents fail when they offer the same unhelpful suggestion repeatedly without escalating, when they direct customers through closed loops of cross-referencing FAQ articles | 6 |
| [Sentiment Escalation](sentiment-escalation/) | Sentiment-escalation agents fail when they select an escalation playbook by textual similarity rather than by confirming the ticket's actual severity tier | 6 |
| [Sla Management](sla-management/) | SLA-management agents fail when they apply an incorrect SLA tier because retrieval selected a boilerplate-heavy but wrong-tier policy document, when a multi-agent handoff loses a customer-specific SLA override negotiated during support | 4 |
| [Ticket Routing](ticket-routing/) | Ticket-routing agents fail when they classify a ticket's product category by embedding similarity to a taxonomy node without verifying the account actually has that product | 8 |

**Total: 31 patterns**

## Frequently Asked Questions

### Where do I start if my support services agent is failing?

Match the symptom to a goal in the table above, then open that goal's page for how to tell its failures apart and where to look first. Each failure page ends in mitigations you can apply directly.

### How are these support services failure patterns organized?

By goal: the outcome the agent is supposed to achieve. Under each goal, a `failures` folder holds one page per pattern. For the full picture see the [Support Services overview](../).

## Related

- [Support Services overview](../)
- [All agent failure patterns](../../../)
