# Multi-Agent Handoff Drops Mid-Quarter Territory Realignment Before Quota-Credit Calculation

## Issue: A Sales-Operations Agent's Free-Text Approval Notes Recording a Mid-Quarter Territory Realignment and Its Effective Date Are Not Captured in the Structured Schema Passed to the Quota-Crediting Agent, Which Calculates Credit Against the Stale, Pre-Realignment Territory Map

**Frequency**: Occasional

**Symptoms**
- A rep's quota credit for the quarter is calculated using their pre-realignment territory assignment, even though a sales-operations agent approved a mid-quarter territory change (accounts moved between reps) with a documented effective date in free-text approval notes
- The structured schema passed to the quota-crediting agent includes fields for rep ID, quota target, and closed-deal value, but has no field for a mid-period territory-assignment change with an effective date
- Asking the quota-crediting agent why the realignment was not reflected shows it received only the structured crediting fields and had no input describing the mid-quarter territory change from the sales-operations agent's approval notes
- The miss concentrates on realignments approved outside the standard start-of-quarter territory-assignment process, since those are the changes least likely to have a corresponding field in the crediting schema
- Reps affected by the realignment catch the discrepancy only when reviewing their quota-attainment statement at quarter close, after compensation has already been calculated

**Root Cause**
The handoff between the sales-operations agent, which approves territory realignments and records the effective date in free-text approval notes, and the quota-crediting agent, which calculates credit from a fixed structured schema, has no mechanism for surfacing a realignment that does not map to one of the schema's predefined fields. The sales-operations agent's notes record the change and its effective date, but nothing in the handoff forces a check for "does this quarter's approval history contain a territory change not represented in the structured crediting inputs" before the quota-crediting agent proceeds, so a real, comp-affecting change is silently dropped at the agent-to-agent boundary.

**Example**
```
Sales-operations agent approves a mid-quarter request to move a set of named accounts from Rep A to Rep B, effective the 15th of the second month of the quarter, and records the approval and effective date in free-text notes
Sales-operations agent hands off quota-crediting inputs to the quota-crediting agent using the standard structured schema: rep ID, quota target, closed-deal value -- no field exists for "mid-period territory reassignment effective date"
Quota-crediting agent calculates Rep A's and Rep B's quota attainment using the original, pre-realignment account assignments for the full quarter, since the realignment was never represented in the structured fields it received
Rep B closes a large deal on a reassigned account after the effective date but receives no quota credit for it, while Rep A receives credit for a deal closed on an account no longer theirs after the effective date, discovered only when both reps review their quarter-close attainment statements
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Multi-agent LLM systems show a recurring failure mode where information established in one agent's reasoning or approval process is not correctly specified or transferred to a downstream agent operating on a fixed schema | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Generalist multi-agent systems require explicit mechanisms for passing task-relevant context between agents with different input schemas, and gaps in this transfer are identified as a common source of downstream task failure | [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://arxiv.org/abs/2411.04468) |
| Audits of agentic workflow failures in production platforms identify schema mismatches at agent-to-agent handoff boundaries as a recurring root cause of dropped task-relevant information | [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735) |

**Contributing Factors**
- The quota-crediting schema passed between the sales-operations and quota-crediting agents has no field for a mid-period territory-assignment change with an effective date
- No check runs before quota-credit calculation to compare the quarter's territory-realignment approval history against the structured crediting inputs for an unrepresented change
- Mid-quarter realignments approved outside the standard start-of-quarter process are especially likely to fall outside the schema, since the schema was built around the standard process's cadence

---

## Mitigation Strategies

1. **Effective-Dated Territory-Change Field in Crediting Schema**: Add a structured "mid-period territory reassignment" field, including effective date, to the quota-crediting handoff schema that the sales-operations agent is required to populate whenever it approves a realignment
2. **Pre-Calculation Realignment Reconciliation Check**: Before calculating quota credit, require a check that compares the quarter's territory-realignment approval history against the structured crediting inputs and flags any change not represented in the schema
3. **Human Sales-Ops Review Gate for Effective-Dated Splits**: Route any quota calculation spanning a mid-period territory realignment to human sales-operations review before compensation is finalized, rather than allowing the quota-crediting agent to resolve the date split automatically
4. **Realignment-to-Crediting Traceability Log**: Maintain a log linking each quarter's quota-credit calculation to the territory-realignment approvals in effect during that quarter, so a missing realignment can be caught by audit before compensation is paid

### Metrics
- Rate of quota-credit calculations later found, on review, to omit a territory realignment present in the quarter's approval history
- Rate of crediting handoffs with a populated "mid-period territory reassignment" field versus handoffs where a downstream audit found a realignment that should have been populated but wasn't
- Average time between quota-credit calculation and realignment-gap detection, when gaps occur

### Alerts
- A quota-credit calculation is finalized with a mid-period territory realignment present in the approval history but absent from the structured crediting inputs → P1
- A rep disputes their quota attainment citing a territory realignment not reflected in the calculation → P1
- Rate of quota calculations requiring post-payment correction for missed realignments exceeds the defined threshold for a rolling window → P2

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://arxiv.org/abs/2411.04468)
- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735)
