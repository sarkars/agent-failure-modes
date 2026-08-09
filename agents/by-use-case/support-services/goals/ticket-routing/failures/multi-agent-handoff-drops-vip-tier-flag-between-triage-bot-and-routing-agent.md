# Multi-Agent Handoff Drops VIP-Tier Flag Between Triage Bot and Routing Agent

## Issue: A Triage Bot Determines a Customer's VIP/Enterprise Status From a Free-Text Account-Notes Lookup, but the Structured Ticket Object It Hands Off to the Routing Agent Has No Field for That Status, So the Routing Agent Sends the Ticket to the Standard Queue Instead of the Premium Queue

**Frequency**: Occasional

**Symptoms**
- Enterprise-tier tickets sit in the standard queue's ordinary order despite the triage bot's transcript naming the account's contract tier just before the ticket was created
- Category, language, and priority all populate correctly on these tickets; tier is the one attribute that never appears anywhere in the structured object, because it was never added to either the ticket schema or the account record the routing agent separately queries
- Comparing routing outcomes for accounts whose tier lives in a structured account flag against accounts whose tier is only a CRM note shows the note-only group routed to standard queues at a materially higher rate
- Premium-tier customers contact support asking why they weren't treated as premium; each investigation traces back to the same missing field rather than to a routing-logic error
- Account managers learn of a specific misroute only when a customer escalates directly, since no monitoring layer checks structured ticket fields against the transcript that produced them

**Root Cause**
Account tier here is a side effect of a CRM lookup the triage bot performs to confirm contract terms, not a first-class attribute the ticket schema was ever built to carry, so the lookup's output was never wired into the fields routing consumes. The routing agent's queue-selection logic was written once, against a three-field contract (category, language, priority), before tier-aware routing was ever a requirement, and it has no code path that would consult anything outside those fields even if one existed. The gap sits on both ends of the handoff: the ticket schema has no tier field, and the structured account record the routing agent already queries for other purposes was never extended to carry one either.

**Example**
```
Triage bot looks up the account in the CRM and notes in its free-text reasoning: "Account flagged as Enterprise tier per contract notes, premium routing applies"
Triage bot hands off a structured ticket object to the routing agent containing category=technical, language=en, priority=normal -- with no account-tier field
Routing agent, working only from the structured fields, routes the ticket to the standard technical queue
Enterprise account's ticket sits in the standard queue for the standard response window, missing the premium-tier response target by a wide margin
Account manager discovers the misroute only after the customer escalates directly, and traces it back to the triage bot's own transcript correctly identifying the tier
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Surveys of multi-agent LLM system failures identify narrow handoff interfaces between staged agents, where a downstream agent's structured input omits context an upstream agent had available, as a distinct and recurring failure category | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Generalist multi-agent system research documents that handoff interfaces between specialized agents must be deliberately designed to carry task-relevant context beyond a fixed set of classification fields, or downstream agents systematically underperform agents with full upstream context | [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://arxiv.org/abs/2411.04468) |
| Hybrid AI routing research for agent systems identifies that routing decisions made purely from a constrained structured schema, without access to upstream free-text determinations, are a documented source of misrouting distinct from routing-model accuracy itself | [Toward Super Agent System with Hybrid AI Routers](https://arxiv.org/pdf/2504.10519) |

**Contributing Factors**
- Structured ticket schema passed from triage bot to routing agent has no field for account tier, even though the triage stage's free-text reasoning routinely determines it
- Routing agent's decision logic is implemented to consume only the structured ticket schema, not the triage stage's free-text transcript, for latency and cost reasons
- No detection step flags when the triage transcript contains a tier or status determination absent from the corresponding structured handoff field

---

## Mitigation Strategies

1. **Add an Account-Tier Field to the Handoff Schema**: Require the triage bot to extract and pass forward a structured account-tier field whenever its reasoning determines VIP/enterprise status, rather than leaving that determination only in free text
2. **Routing Agent Cross-Checks Triage Transcript for Tier Mentions**: Require the routing agent to scan the upstream triage transcript for tier-determination language before finalizing a queue assignment, not just the structured fields
3. **Independent Account-Tier Lookup at Routing Time**: Have the routing agent independently query the account's tier from the structured CRM record it has access to, rather than relying solely on the triage bot's handoff to carry that determination
4. **Track Tier-Field-Absent Misroute Rate**: Continuously measure how often a VIP/enterprise account's ticket is routed to a standard queue when the handoff schema lacked a tier field versus when it carried one

### Metrics
- Rate of VIP/enterprise account tickets routed to a standard (non-premium) queue
- Misroute rate, segmented by presence vs. absence of an account-tier field in the triage-to-routing handoff
- Time between ticket creation and manual escalation for premium-tier accounts misrouted to the standard queue

### Alerts
- A VIP/enterprise account's ticket is routed to a standard queue while the triage transcript explicitly identifies the account's tier → P2
- Tier-field-absent misroute rate across a rolling window exceeds the defined threshold → P2
- A premium-tier account's ticket exceeds the premium response-time target while sitting in a standard queue → P1

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://arxiv.org/abs/2411.04468)
- [Toward Super Agent System with Hybrid AI Routers](https://arxiv.org/pdf/2504.10519)
