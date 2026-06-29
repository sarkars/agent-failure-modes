# Multi-Agent Handoff Drops VIP-Tier Flag Between Triage Bot and Routing Agent

## Issue: A Triage Bot Determines a Customer's VIP/Enterprise Status From a Free-Text Account-Notes Lookup, but the Structured Ticket Object It Hands Off to the Routing Agent Has No Field for That Status, So the Routing Agent Sends the Ticket to the Standard Queue Instead of the Premium Queue

**Frequency**: Occasional

**Symptoms**
- Enterprise or VIP-tier customers' tickets land in the standard routing queue despite the triage bot's own transcript showing it identified the account as premium-tier moments earlier
- The structured ticket object passed from triage bot to routing agent contains category, language, and priority fields, but no field for account tier, even when the triage step's free-text reasoning explicitly notes the account is enterprise
- Routing agents operating purely from the structured ticket schema show a materially higher standard-queue misroute rate for VIP accounts than routing agents given the full triage transcript alongside the structured fields
- The mismatch concentrates on accounts whose VIP status is determined by a free-text account-notes lookup (a CRM annotation, a contract-tier note) rather than by a flag already present in a structured account field the routing agent also queries
- Account managers escalate manually after noticing a premium account's ticket sat in the standard queue past the premium-tier response target, despite the triage transcript clearly identifying the account's tier

**Root Cause**
The routing agent's decision logic consumes only the structured ticket schema produced by the triage stage, and that schema was built to carry the fields routing explicitly checks (category, language, priority) rather than every fact the triage stage's free-text reasoning surfaced. When VIP/enterprise status is derived from an account-notes lookup rather than a field already present in a structured account record the routing agent itself queries, that status exists only in the triage bot's free-text output and is lost the moment the handoff narrows to the fixed schema, even though the same model, given the triage transcript, would readily act on it.

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
