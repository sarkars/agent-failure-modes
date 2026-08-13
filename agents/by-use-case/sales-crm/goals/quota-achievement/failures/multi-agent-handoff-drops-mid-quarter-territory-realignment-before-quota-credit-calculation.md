# Multi-Agent Handoff Drops Mid-Quarter Territory Realignment Before Quota-Credit Calculation

## Issue: A Sales-Operations Agent's Free-Text Approval Notes Recording a Mid-Quarter Territory Realignment and Its Effective Date Are Not Captured in the Structured Schema Passed to the Quota-Crediting Agent, Which Calculates Credit Against the Stale, Pre-Realignment Territory Map

**Frequency**: Occasional

**Symptoms**
- Rep B closes a large deal on an account reassigned to them mid-quarter but receives zero quota credit for it, while Rep A -- who no longer owns that account as of the effective date -- gets credited as though the realignment never happened
- Rep ID, quota target, and closed-deal value -- the schema's three fields -- are exactly what the quota-crediting agent needs for a quarter with no mid-period changes; the moment a territory shifts partway through, the schema has nothing to say about which half of the quarter each rep's credit should count from
- The quota-crediting agent's math is defensible given its inputs: it applies the account-to-rep mapping it was given uniformly across the full quarter, because nothing in its input distinguishes "assigned all quarter" from "assigned as of the 15th"
- The sales-operations agent's approval notes are specific -- named accounts, named reps, an exact effective date -- but that specificity lives in an approval record the crediting agent's pipeline was never pointed at
- Both affected reps only discover the error at quarter-close attainment review, after compensation tied to that attainment has already been run

**Root Cause**
Sales-operations approves realignments as discrete, dated events -- these accounts move from Rep A to Rep B as of this date -- but the quota-crediting agent's schema models territory as a single static assignment per rep per quarter, with no concept of an assignment that changes partway through. An effective-dated change has no field to occupy in a schema that was never designed to represent time-varying account ownership within a single crediting period, so the crediting agent applies whichever assignment it has as if it held for the entire quarter.

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
