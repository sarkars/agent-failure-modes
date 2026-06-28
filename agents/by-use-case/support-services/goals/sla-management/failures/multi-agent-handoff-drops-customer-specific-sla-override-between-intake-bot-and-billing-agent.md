# Multi-Agent Handoff Drops Customer-Specific SLA Override Between Intake Bot and Billing Agent

## Issue: An Intake Bot That Learns, During a Support Conversation, That a Customer Has a Negotiated SLA Override -- For Example, an Extended Response-Time Allowance Granted as Part of a Contract Renegotiation -- Records That Override Only in Its Conversation Summary, and a Downstream Billing or SLA-Compliance Agent That Calculates Breach Penalties From a Structured Account Field Never Receives the Override, Applying the Standard SLA Instead

**Frequency**: Occasional

**Symptoms**
- A billing or SLA-compliance agent calculates a breach penalty against a customer using the standard SLA terms, even though the intake bot's conversation transcript shows the customer has a negotiated override extending the allowed response window
- Re-reading the intake bot's conversation summary clearly states the override and its terms; the structured account record the billing agent queries shows no override field set
- The override is most often dropped when it was negotiated verbally during a support escalation rather than processed through the standard contract-amendment workflow, since the structured account schema has a field for contract amendments but not for support-negotiated overrides
- The billing agent's penalty calculation completes without error and is presented with full confidence, with no indication that an override might exist outside the structured fields it checked
- The error surfaces only when the customer disputes the penalty by referencing the earlier support conversation, requiring a manual transcript review to confirm the override

**Root Cause**
The intake bot and the billing or SLA-compliance agent communicate through a structured account-record schema that has fields for standard SLA tier and formal contract amendments, but no field for an informally negotiated, support-context override. When such an override is captured only in the intake bot's conversation summary rather than as a structured field the downstream agent's penalty-calculation query explicitly checks, the override is invisible to the agent that actually computes breach penalties, regardless of how clearly it was recorded during the original conversation.

**Example**
```
Customer escalates a recurring service issue; support lead, working through the intake bot, agrees to extend the customer's SLA response window from 4 hours to 8 hours for the next billing cycle as a goodwill gesture
Intake bot's conversation summary correctly notes: "Customer granted temporary SLA override: response window extended to 8 hours through end of current billing cycle"
Structured account record is not updated with any override field, since the support workflow has no schema field for temporary, support-negotiated SLA changes
Three weeks later, a ticket response taking 6 hours triggers the billing agent's standard 4-hour SLA breach calculation, applying a contractual penalty credit to the customer's account that the negotiated override should have prevented
Customer disputes the penalty by referencing the earlier support conversation, requiring manual transcript review to confirm and reverse the incorrectly applied penalty
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Multi-agent LLM systems exhibit a documented failure category where a determination established by one agent is lost or never reaches a downstream agent's effective input, distinct from either agent reasoning incorrectly on its own | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Business-scenario evaluations of LLM agents in CRM-adjacent tasks identify structured state propagation between conversational and transactional agents as a distinct reliability requirement from either agent's individual task accuracy | [CRMArena-Pro: Holistic Assessment of LLM Agents Across Diverse Business Scenarios and Interactions](https://arxiv.org/abs/2505.18878) |
| Generalist multi-agent system designs are shown to require explicit, structured task and constraint specification between agents, since narrative conversation summaries alone do not reliably propagate to a downstream agent acting on a fixed schema | [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://arxiv.org/abs/2411.04468) |

**Contributing Factors**
- The structured account-record schema has fields for standard SLA tier and formal contract amendments, but no field for an informally negotiated, support-context SLA override
- The billing or SLA-compliance agent's penalty calculation queries only the structured account record, never the intake bot's conversation transcripts
- No reconciliation step compares override language in support conversation summaries against the structured account fields the billing agent will actually act on

---

## Mitigation Strategies

1. **Structured Temporary-Override Field in Account Schema**: Extend the account-record schema to carry a structured, time-bound SLA-override field, and require any agent that negotiates an override during a support conversation to populate it directly rather than leaving it in a conversation summary only
2. **Mandatory Pre-Penalty Override Check**: Before any billing or SLA-compliance agent calculates a breach penalty, require an automated check of the structured override field for that account and time period, blocking penalty calculation on any unresolved discrepancy with recent support conversation summaries
3. **Conversation-to-Schema Reconciliation Pass**: Run an automated pass comparing every SLA-override statement in recent support conversation transcripts against the structured account record, flagging any override mentioned in conversation but absent from structured fields
4. **Formal Confirmation Workflow for Support-Negotiated Overrides**: Require any support-negotiated SLA override to trigger a structured confirmation step that updates the account record before the override takes effect, rather than relying solely on the intake bot's own summary as the record of the change

### Metrics
- Rate of SLA breach penalties calculated against an account with an unresolved override mentioned in a recent support conversation transcript
- Rate of support conversations containing override language with no corresponding structured account-field update
- Number of penalty disputes attributable to a missed support-negotiated SLA override

### Alerts
- A breach penalty is calculated for an account with an override mentioned in a support conversation transcript within the relevant time period but absent from the structured record → P1
- A support conversation grants an SLA override with no corresponding structured account-field update within the defined grace period → P2
- Override-reconciliation mismatch rate exceeds the defined threshold for a rolling window → P3

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [CRMArena-Pro: Holistic Assessment of LLM Agents Across Diverse Business Scenarios and Interactions](https://arxiv.org/abs/2505.18878)
- [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://arxiv.org/abs/2411.04468)
