# Multi-Agent Handoff Drops Negotiated Payment-Terms Exception Before Deal-Desk Approval

## Issue: An Account Executive's Free-Text Email Negotiation Establishing Extended Payment Terms for an Enterprise Deal Is Not Captured in the Structured Approval Request Passed to the Deal-Desk Agent, Which Approves the Deal Under Standard Payment Terms That Contradict What the Customer Was Told

**Frequency**: Common

**Symptoms**
- The deal-desk approval logs standard net-30 terms for a deal where the AE's email thread shows the customer explicitly accepted a three-year commitment in exchange for net-90
- Deal value, discount percentage, and contract length -- the levers the approval-request schema was built to carry -- reach the deal-desk agent intact every time; payment terms fail specifically because the schema treats them as fixed, not as something a negotiation can change
- The deal-desk agent's approval is internally correct given its inputs: nothing in deal value, discount, or contract length signals that payment terms were part of what got negotiated, so it approves the deal at the schema's implicit default
- The email thread itself is unambiguous -- net-90 offered, three-year term stated, customer confirmed -- but that exchange lives in a channel the deal-desk agent's approval workflow was never wired to read
- The contradiction only surfaces when the contract is generated from the approved record, by which point the customer has already been told terms the paperwork won't match

**Root Cause**
The AE's negotiation happens over email, where payment terms are just another line of agreed text, but the deal-management agent hands that negotiation to deal-desk approval through a schema of deal value, discount, and contract length -- fields chosen for the deals the approval workflow was originally built to gate, none of which was ever payment terms. Because the schema has no slot representing "payment terms," an exception negotiated on that specific axis has nowhere to be written down between the email thread and the approval record, regardless of how explicitly the customer and AE agreed to it.

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
