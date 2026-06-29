# Multi-Agent Handoff Drops De-Escalation Context Between Triage and Billing Agent

## Issue: A Triage Agent That Determines a Customer Is Already Frustrated and Has Explicitly Requested Not to Repeat Their Account Details Again Records That Context Only in Its Own Conversational Reasoning, and When the Conversation Is Routed to a Downstream Specialized Billing Agent That Operates on a Structured Ticket Object Containing Only the Stated Issue Category, the De-Escalation Context and Already-Provided Details Never Cross the Handoff Boundary, So the Billing Agent Re-Opens the Conversation by Asking the Customer to Re-Authenticate and Re-Explain Everything From Scratch

**Frequency**: Common

**Symptoms**
- Billing agent's opening message asks for account details, order numbers, or a description of the issue that the customer already provided to the triage agent earlier in the same overall conversation
- Triage agent's own reasoning or transcript explicitly notes the customer's frustration level and which details were already collected, but none of that appears in the structured ticket object the billing agent receives
- Customer's response to the billing agent expresses frustration at having to repeat themselves immediately after having just explained the situation to a different agent
- Re-reading the full session transcript (triage plus billing) confirms all the requested information was already stated once, earlier in the same overall interaction, and the loss occurs specifically at the inter-agent handoff
- The structured handoff ticket contains only a category label and minimal metadata, with no field for carrying forward the verbatim details or de-escalation notes the triage agent gathered

**Example**
```
Customer contacts support angry about a billing discrepancy, stating upfront: "I already spent 20 minutes on this last week, please don't make me repeat my account number and the charge details again"
Triage agent collects the account number, the disputed charge amount, and the date, and notes in its own reasoning that the customer is frustrated and these details should not be re-requested
Triage agent routes the case to a specialized billing-dispute agent via a structured ticket containing only: category = "billing_dispute", customer_id, timestamp
Billing agent opens with: "I'd be happy to help -- can you provide your account number and details about the charge you're disputing?"
Customer: "I just gave all of this to the other agent two minutes ago. Why am I starting over?"
Review of the full session confirms the account number, charge amount, and date were all captured by the triage agent but never included in the structured handoff payload the billing agent actually received
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Analysis of multi-agent LLM system failures finds that information and context established by one agent is frequently lost or never communicated to a downstream agent operating on its own narrower input, and such inter-agent handoff failures are a leading cause of overall task failure | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Execution-provenance research for LLM agents argues that without explicit evidence tracing across agent boundaries, context gathered upstream has no mechanism to remain attached to a case as it is handed to a downstream agent | [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1) |
| Research on agent-environment failure interactions finds structured handoff interfaces between cooperating agents frequently omit fields needed to carry forward conversational context gathered during an upstream interaction phase | [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504) |

**Contributing Factors**
- Details and de-escalation notes exist only in the triage agent's own conversational reasoning or transcript, not in a structured field of the ticket object passed to the billing agent
- Handoff schema carries only a category label and customer identifier, with no field for verbatim collected details or an explicit "do not re-ask" list
- Billing agent's prompt instructs it to open by gathering the information it needs for its task, with no instruction to first check whether that information was already collected upstream
- No automated check comparing entities and stated preferences captured by the triage agent against fields present in the structured handoff payload before the billing agent's first message is sent

---

## Mitigation Strategies

1. **Structured Detail-Carryforward Field**: Require the handoff payload between triage and specialized downstream agents to include all customer-provided details and an explicit "already collected, do not re-ask" list, not just a category label
2. **Handoff Completeness Check**: Automatically diff entities and stated preferences captured in the triage transcript against fields present in the structured handoff payload, blocking handoff completion on any unexplained discrepancy
3. **Pre-Send Re-Ask Guard**: Require the downstream agent to check its planned opening message against the carried-forward detail list before sending, rewriting any request for information already provided
4. **Shared Session Record**: Replace agent-local conversational summaries with a single shared session record both triage and downstream agents read from and write to, so information gathered upstream is visible by construction to the next agent

### Metrics
- Rate of downstream-agent opening messages that re-request information already present in the upstream agent's transcript
- Customer-expressed-frustration rate ("I already told the other agent") immediately following an inter-agent handoff
- Completeness rate of structured handoff payloads relative to entities actually captured upstream

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Re-ask after handoff | Downstream agent requests information already present in the upstream transcript | P1 | Block message; auto-populate from shared session record |
| Handoff payload incomplete | Structured handoff payload missing entities present in upstream transcript | P2 | Block handoff; require payload completion |
| Recurring schema gap | Multiple cases show the same category of detail consistently dropped at handoff | P3 | Audit and extend handoff payload schema |

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
- [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504)
