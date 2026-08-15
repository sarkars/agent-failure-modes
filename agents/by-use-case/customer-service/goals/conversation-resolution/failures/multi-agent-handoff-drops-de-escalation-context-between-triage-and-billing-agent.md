# Multi-Agent Handoff Drops De-Escalation Context Between Triage and Billing Agent

## Issue: A Triage Agent That Determines a Customer Is Already Frustrated and Has Explicitly Requested Not to Repeat Their Account Details Again Records That Context Only in Its Own Conversational Reasoning, and When the Conversation Is Routed to a Downstream Specialized Billing Agent That Operates on a Structured Ticket Object Containing Only the Stated Issue Category, the De-Escalation Context and Already-Provided Details Never Cross the Handoff Boundary, So the Billing Agent Re-Opens the Conversation by Asking the Customer to Re-Authenticate and Re-Explain Everything From Scratch

**Frequency**: Common

**Symptoms**
- The billing agent opens by requesting information — account number, order details, description of the issue — that the same customer already gave the triage agent minutes earlier in the same interaction
- Triage's transcript explicitly flags the customer's frustration and lists which details are already collected, none of which appears in the structured ticket the billing agent receives
- The customer reacts by pointing out they just explained this to a different agent, escalating irritation rather than resolving it
- Reading the full session end to end shows every requested item was already stated once; the information existed, it just didn't survive the handoff
- The ticket object itself carries only a category label and minimal metadata, confirming there was never a field for verbatim details or a "don't re-ask" list in the first place

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
- The ticket schema was built to route a case by category, not to carry forward what happened in the conversation that produced that category, so collected details and emotional-state notes have nowhere to go
- The only structured place the already-provided details and frustration signal exist is the conversational log itself, which the billing agent's input pipeline is not wired to read before responding
- The billing agent's instructions are self-contained: gather what it needs to resolve the category it was handed, with no step that first checks whether the customer already supplied that information to a prior agent
- Nothing compares the entities a customer stated during triage against the fields the billing agent is about to ask for, so a repeat request looks identical to a first request from the system's point of view

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
