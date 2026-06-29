# Multi-Agent Handoff Drops Negotiated Payment-Terms Exception Before Deal-Desk Approval

## Issue: An Account Executive's Free-Text Email Negotiation Establishing Extended Payment Terms for an Enterprise Deal Is Not Captured in the Structured Approval Request Passed to the Deal-Desk Agent, Which Approves the Deal Under Standard Payment Terms That Contradict What the Customer Was Told

**Frequency**: Common

**Symptoms**
- A customer is told in an email thread that payment terms will be net-90 instead of the standard net-30 in exchange for a multi-year commitment, but the deal-desk approval record shows the deal approved under standard net-30 terms
- The deal-management agent's structured approval-request object includes deal value, discount percentage, and contract length, but has no field for a non-standard payment-terms exception
- Asking the deal-desk agent why it approved standard terms shows it only received the structured approval-request fields and had no input describing the negotiated payment-terms deviation from the AE's email thread
- The miss concentrates on deals with any negotiated term outside the standard approval-request schema, such as payment terms, early-termination clauses, or non-standard renewal pricing
- The customer or AE catches the discrepancy only when the contract is generated from the approved deal record, after the deal-desk approval has already been logged

**Root Cause**
The handoff between the deal-management agent tracking the negotiation and the deal-desk agent issuing approval passes only a fixed structured schema of deal parameters, with no mechanism for surfacing a negotiated term that does not map to one of the schema's predefined fields. The negotiation history contains the payment-terms exception in free text, but nothing in the handoff forces a check for "does this deal's negotiation history contain any term not represented in the structured approval request" before deal-desk approval is granted, so a real commitment made to the customer is silently dropped at the agent-to-agent boundary.

**Example**
```
AE negotiates with the customer over email: "We can offer net-90 payment terms in exchange for a three-year commitment instead of our standard one-year"
Customer confirms acceptance of the three-year term with net-90 payment
Deal-management agent hands off to the deal-desk agent for approval using the standard structured schema: deal value, discount percentage, contract length -- no field exists for "non-standard payment terms"
Deal-desk agent approves the deal under standard net-30 payment terms, since that field was never populated with the negotiated exception
Contract generated from the approved deal record specifies net-30 terms, contradicting what the customer was told and accepted
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Multi-agent LLM systems show a recurring failure mode where information established in one agent's reasoning or conversation is not correctly specified or transferred to a downstream agent operating on a fixed schema | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Agentic CRM and sales-workflow research identifies handoff between negotiation-tracking and approval-issuing agents as a point where unstructured deal context is frequently lost when the receiving agent operates on a fixed schema | [CRMWeaver: Building Powerful Business Agent via Agentic RL and Shared Memories](https://arxiv.org/pdf/2510.25333) |
| Audits of agentic workflow failures in production platforms identify schema mismatches at agent-to-agent handoff boundaries as a recurring root cause of dropped task-relevant information | [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735) |

**Contributing Factors**
- The deal-approval schema passed between the deal-management and deal-desk agents has no free-text or exception field for negotiated terms outside the standard set
- No check runs before deal-desk approval to compare the deal's negotiation conversation history against the structured approval request for unrepresented commitments
- Non-standard terms (payment terms, early-termination clauses) are especially likely to fall outside the standard schema, since they are by definition exceptions to the default approval path

---

## Mitigation Strategies

1. **Exception Field in Deal-Approval Schema**: Add a structured "negotiated exception" field to the deal-desk approval-request schema that the deal-management agent is required to populate whenever the negotiation conversation contains a commitment outside the standard fields
2. **Pre-Approval Negotiation Reconciliation Check**: Before deal-desk approval is granted, require a check that compares the deal's negotiation conversation history against the structured approval request and flags any commitment not represented in the schema
3. **Human Review Gate for Non-Standard Terms**: Route any deal with a populated exception field to human deal-desk review before approval is finalized, rather than allowing the deal-desk agent to resolve it automatically
4. **Negotiation-to-Contract Traceability Log**: Maintain a log linking each approved deal record to the negotiation conversation it was derived from, so discrepancies can be caught by audit before being caught by the customer at contract signing

### Metrics
- Rate of approved deals later found, on review, to omit a negotiated term present in the customer-facing negotiation conversation
- Rate of deals with a populated "negotiated exception" field versus deals where a downstream audit found an exception that should have been populated but wasn't
- Average time between deal-desk approval and discrepancy detection, when discrepancies occur

### Alerts
- A deal is approved with a negotiated exception present in the conversation history but absent from the structured approval request → P1
- A customer or AE reports a discrepancy between the generated contract and the negotiated terms → P1
- Rate of deals requiring post-approval correction for missed negotiated terms exceeds the defined threshold for a rolling window → P3

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [CRMWeaver: Building Powerful Business Agent via Agentic RL and Shared Memories](https://arxiv.org/pdf/2510.25333)
- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735)
