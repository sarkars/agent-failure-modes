# Multi-Agent Handoff Drops Affected-Customer Segment Before Comms Notification

## Issue: A Triage Agent That Determines, in Its Own Investigation Output, That an Incident Affects Only a Specific Customer Segment -- e.g., Enterprise Customers in the EU Region Using a Particular API Version -- Hands Off to a Customer-Communications Agent Through a Structured Incident Ticket That Carries Only a Severity Field, Not the Segment Scope the Triage Agent Actually Determined, So the Comms Agent Notifies Either All Customers or the Wrong Subset

**Frequency**: Occasional

**Symptoms**
- Triage agent's investigation narrative explicitly states the affected scope ("impact limited to EU enterprise tier customers on API v2"), but the incident ticket's structured fields contain only severity and a generic title
- Comms agent, reading only the structured ticket, sends a status-page update or customer notification to the full customer base, including customers who were never affected
- Alternatively, comms agent under-notifies, missing affected customers outside the structured ticket's default audience field
- Customers outside the actual affected segment file support tickets asking why they received an outage notification for a service they were not using or were not impacted by
- The scoping information is recoverable by reading the triage agent's full investigation transcript, but the comms agent's workflow does not consume that transcript, only the structured handoff ticket
- Incidents with a single, service-wide cause rarely trigger the problem, since "notify everyone using this service" is already the schema's default path; the failure needs a cause narrowed to a cross-cutting slice, like EU-plus-v2-plus-enterprise, that the ticket's severity/title pair was never built to carry

**Root Cause**
The incident ticket was designed around what severity and routing require -- how bad, and which on-call rotation -- because those are the fields that drive paging. Customer-facing scope was never part of that design brief, so when the triage agent narrows the impact to EU-region API v2 enterprise clients, it has no ticket field to put that conclusion in and states it only in the investigation summary instead. The comms agent's drafting step was built to turn a ticket into a notification, not to re-derive scope from investigation prose, so absent a structured field it falls back to the only audience it can safely construct from severity alone: everyone.

**Example**
```
Incident: a config rollout breaks token refresh specifically for API v2 clients in the EU region, used predominantly by enterprise-tier customers
Triage agent investigates and concludes: "Impact is isolated to API v2 clients in EU region; v1 clients and non-EU regions are unaffected" -- stated clearly in its investigation summary
Triage agent opens an incident ticket using the standard schema: { severity: "P1", title: "Token refresh failure", status: "investigating" } -- no field exists for affected segment
Comms agent, triggered by the P1 ticket, drafts and sends a status-page update and customer email to the entire customer base: "We are experiencing an issue affecting token refresh"
US-region and v1-API customers, entirely unaffected, receive the notification and file support tickets asking about an outage they never experienced
Triage agent's own transcript, which the comms agent never reads, already contained the correct scoping that would have prevented the over-broad notification
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Multi-agent failure analysis identifies information loss at agent-to-agent handoff boundaries -- where one agent's correct internal determination is not propagated into the structured interface the next agent consumes -- as one of the most common recurring failure categories | [Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) |
| Failure taxonomies for platform-orchestrated agentic workflows describe handoff schemas lacking fields for context the upstream agent determined as a structural driver of downstream errors, independent of either agent's individual correctness | [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735) |
| Orchestration research for incident-response-specific multi-agent systems notes that decision support quality depends on what is explicitly carried across agent boundaries, not what any single agent internally concluded | [Multi-Agent LLM Orchestration Achieves Deterministic, High-Quality Decision Support for Incident Response](https://arxiv.org/pdf/2511.15755) |

**Contributing Factors**
- Incident-ticket schema has no structured field for affected-segment scope, only severity and free-text summary
- Comms agent's workflow consumes only structured ticket fields, not the triage agent's full investigation transcript
- No validation step checks whether the comms agent's notification audience matches the triage agent's determined affected scope before the notification is sent
- Default behavior under ticket-schema ambiguity favors over-broad notification ("notify everyone to be safe") rather than holding for scope clarification

---

## Mitigation Strategies

1. **Structured Scope Field**: Add an explicit, structured affected-segment field (region, tier, API version, or similar) to the incident-ticket schema that the triage agent is required to populate before handoff
2. **Scope-Audience Validation**: Require an automated check that the comms agent's intended notification audience matches the triage agent's structured scope field before any customer-facing notification is sent
3. **Transcript-Aware Comms Drafting**: Require the comms agent to consult the triage agent's investigation summary, not only the structured ticket, when drafting notification audience and content
4. **Default-to-Narrow on Ambiguity**: When scope is not explicitly populated, default to the narrowest determinable audience and hold broader notification for explicit confirmation, rather than defaulting to all customers

### Metrics
- Rate of customer notifications sent to an audience broader than the triage agent's determined affected scope
- Number of support tickets filed by customers outside the actual affected segment following an incident notification
- Mean time between scope determination in triage and accurate scope propagation into the comms handoff

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Scope-audience mismatch | Comms notification audience does not match triage agent's structured scope field | P1 | Hold or recall notification; correct audience |
| Unaffected-customer complaint spike | Support tickets from customers outside the affected segment spike following a notification | P2 | Audit handoff schema for missing scope field |
| Persistent scope-field omission | Multiple incidents in a rolling window have an unpopulated affected-segment field at handoff | P3 | Enforce schema validation at ticket creation |

---

## References

- [Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657)
- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735)
- [Multi-Agent LLM Orchestration Achieves Deterministic, High-Quality Decision Support for Incident Response](https://arxiv.org/pdf/2511.15755)
