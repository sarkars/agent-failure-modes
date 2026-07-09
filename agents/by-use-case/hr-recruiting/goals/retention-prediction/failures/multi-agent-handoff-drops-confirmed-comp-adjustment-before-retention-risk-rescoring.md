# Multi-Agent Handoff Drops Confirmed Comp Adjustment Before Retention-Risk Rescoring

## Issue: A Compensation-Review Agent That Confirms a Manager-Approved Off-Cycle Pay Adjustment for an Employee Hands Off Its Output to a Downstream Retention-Prediction Agent Through a Structured Schema That Has No Field for a Pending or Just-Approved Comp Change, So the Retention-Prediction Agent Computes the Employee's Updated Attrition-Risk Score From Stale Compensation Data and Continues Flagging Them as High-Risk Even Though the Underlying Driver of That Risk Was Already Resolved

**Frequency**: Occasional

**Symptoms**
- The compensation-review agent's own output log shows the off-cycle adjustment was confirmed and approved, but the retention-prediction agent's next risk-score computation for the same employee uses the prior, pre-adjustment compensation figure
- The structured handoff payload passed between the two agents contains fields for role, tenure, performance rating, and manager, but no field for a recently approved or pending compensation change
- The retention-prediction agent's risk-score narrative cites "below-market compensation relative to peers" as a contributing factor for an employee whose compensation was, by the time the score was computed, no longer below market
- Re-running the retention-prediction agent with the approved adjustment manually included in its input produces a materially lower risk score, confirming the original elevated score was an artifact of the missing handoff field rather than a reassessment of other risk factors
- HR business partners continue receiving high-risk alerts and initiating retention conversations for employees whose comp-related risk driver was already addressed weeks earlier, causing redundant outreach and confusing the employee about what action was actually taken

**Example**
```
Manager submits an off-cycle pay adjustment request for an employee previously flagged as high attrition-risk partly due to below-market compensation
Compensation-review agent processes the request, confirms approval, and updates the employee's compensation record in the HRIS
Compensation-review agent's handoff to the retention-prediction agent uses a structured schema covering role, tenure, last performance rating, and manager change history, with no field representing the just-approved comp adjustment or its effective date
Retention-prediction agent's next scheduled rescoring run for the employee pulls from the handoff schema and a separate compensation snapshot that has not yet been refreshed past the adjustment's effective date, producing an unchanged high-risk score
Risk-score narrative again lists "compensation below department median" as a top contributing factor, even though the approved adjustment, confirmed weeks earlier, had already closed that gap
HR business partner, acting on the unchanged score, schedules a retention conversation framed around a compensation concern the employee already knows was resolved, undermining confidence in the program
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Agent failure taxonomies identify state loss across structured handoffs between cooperating agents as a distinct system-level failure category, arising when a schema's fixed fields fail to represent a transient but consequential state change | [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933) |
| Agent-environment interaction research notes that multi-agent systems frequently lose recently confirmed state during a handoff when the receiving agent's expected input schema was not designed to anticipate that state, leading downstream stages to operate as if the upstream confirmation never occurred | [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504) |
| Analyses of cascading agent failures find that an upstream agent's correctly confirmed action frequently fails to propagate into a downstream agent's decision when the two are connected only through a fixed structured schema rather than a shared, continuously updated state store | [Where LLM Agents Fail and How They can Learn From Failures](https://arxiv.org/abs/2509.25370) |

**Contributing Factors**
- The handoff schema between the compensation-review agent and the retention-prediction agent was designed around stable employee attributes and was never extended to carry transient, recently-confirmed changes like an off-cycle comp adjustment
- The retention-prediction agent's compensation input comes from a periodic snapshot rather than a live query against the current HRIS record, so even a well-designed handoff field could still be undercut by snapshot staleness
- No reconciliation step compares the compensation-review agent's most recent confirmed actions against the compensation data the retention-prediction agent is about to use before a risk score is finalized
- The two agents are operated as independent pipelines with no shared event log that either side can check for recent, relevant actions taken by the other

---

## Mitigation Strategies

1. **Shared Event Log Instead of Fixed Schema**: Replace the fixed structured handoff with a shared, append-only event log of confirmed actions (comp adjustments, role changes, manager changes) that the retention-prediction agent queries directly before computing or updating a risk score, rather than relying solely on a point-in-time handoff payload
2. **Live Compensation Lookup at Scoring Time**: Require the retention-prediction agent to query current compensation data directly from the HRIS at the moment of scoring rather than from a periodic snapshot, eliminating one source of staleness independent of the handoff schema issue
3. **Pre-Score Reconciliation Check**: Before finalizing any risk score, run an automated check for any compensation-review actions confirmed for that employee since the last score was computed, and force a rescore if a relevant action is found
4. **Schema Versioning for Transient State**: When extending a handoff schema to add fields like "pending/recent comp adjustment," version the schema explicitly and audit historical handoffs that predate the new field to identify employees who may have been scored on stale data

### Metrics
- Number of employees whose risk score cites a compensation factor that contradicts a compensation-review action confirmed before the score was computed
- Average time lag between a confirmed comp adjustment and its reflection in the employee's next retention-risk score
- Percentage of retention-prediction scoring runs that include a pre-score reconciliation check against the compensation-review agent's event log

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Risk score cites resolved comp factor | Risk-score narrative cites a compensation-related risk factor for an employee with a confirmed comp adjustment predating the score | P1 | Suppress the score from HRBP-facing alerts; trigger an immediate rescore with current compensation data |
| Stale compensation snapshot detected | Retention-prediction agent's compensation input is older than the defined freshness threshold relative to the scoring run | P2 | Block scoring until a live compensation lookup is performed |
| Reconciliation check skipped | A scoring run completes without a pre-score reconciliation check against the compensation-review event log | P2 | Flag the run for manual review; do not distribute the resulting score until reconciliation is confirmed |

---

## References

- [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933)
- [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504)
- [Where LLM Agents Fail and How They can Learn From Failures](https://arxiv.org/abs/2509.25370)
