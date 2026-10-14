# Support Services AI Agent Failures by Goal: 31 Patterns, Causes, and Fixes

**Support Services AI agents fail in 5 distinct ways, grouped by the goal each failure breaks.** Find the goal that matches what you are seeing, open its list, and use the fix on each pattern page.

## Key Takeaways

- 31 documented patterns across 5 goals; the most documented is [Ticket Routing](ticket-routing/) with 8.
- Each pattern page gives the symptoms, an example, the root cause, and mitigations.

## Support Services Goals

| Goal | When it fails | Patterns |
|---|---|---|
| [Issue Resolution](issue-resolution/) | When they select a canned response by keyword similarity without verifying situational fit, when a multi-agent handoff loses a prior troubleshooting attempt the customer already described | 7 |
| [Self Service Deflection](self-service-deflection/) | When they offer the same unhelpful suggestion repeatedly without escalating, when they direct customers through closed loops of cross-referencing FAQ articles | 6 |
| [Sentiment Escalation](sentiment-escalation/) | When they select an escalation playbook by textual similarity rather than by confirming the ticket's actual severity tier | 6 |
| [Sla Management](sla-management/) | When they apply an incorrect SLA tier because retrieval selected a boilerplate-heavy but wrong-tier policy document | 4 |
| [Ticket Routing](ticket-routing/) | When they classify a ticket's product category by embedding similarity to a taxonomy node without verifying the account actually has that product | 8 |

**Total: 31 patterns**

## Frequently Asked Questions

### How do you verify a ticket is routed to a provisioned product line?

Query the account's provisioning record against the classified product line before routing finalizes; block routing to unprovisioned products regardless of taxonomy-similarity scores. See [Ticket Routing](ticket-routing/).

### How do you know when a canned response is situationally inappropriate?

Track first-contact-resolution rate and escalation rate separately for macro-resolved versus fully custom-written responses. See [Issue Resolution](issue-resolution/).

### How do you distinguish between successful deflection and customer abandonment from frustration?

Require an explicit customer-confirmation step ("yes, that resolved it") rather than inferring resolution from the absence of a follow-up message. See [Self Service Deflection](self-service-deflection/).

## Related

- [Support Services overview](../)
- [All agent failure patterns](../../../)
