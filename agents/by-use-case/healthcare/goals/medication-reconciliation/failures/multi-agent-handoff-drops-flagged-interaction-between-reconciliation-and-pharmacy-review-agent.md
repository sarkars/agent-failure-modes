# Multi-Agent Handoff Drops Flagged Interaction Between Reconciliation and Pharmacy-Review Agent

## Issue: A Medication-Reconciliation Agent That Identifies a Specific Drug-Drug Interaction Risk Between a Newly Prescribed Medication and a Continuing Home Medication Records That Finding Only Within Its Own Free-Text Reasoning or Conversational Summary, and When the Reconciled Medication List Is Handed Off to a Downstream Pharmacy-Review Agent That Consumes Only the Structured Medication List, the Interaction Flag Never Crosses the Handoff Boundary, So the Pharmacy-Review Agent Approves the List as if No Interaction Risk Had Been Identified

**Frequency**: Occasional

**Symptoms**
- Reconciliation agent's own output or reasoning trace explicitly names a specific drug-drug interaction risk, but the structured medication list passed to the downstream pharmacy-review agent contains no corresponding flag or annotation field for it
- Pharmacy-review agent's approval or sign-off makes no reference to the interaction the upstream agent identified, proceeding as if the medication list were unremarkable
- Re-running the reconciliation agent in isolation reliably surfaces the same interaction, confirming the detection capability exists upstream and the loss occurs specifically at the handoff
- The interaction is only caught when a human pharmacist independently cross-checks the full list against an interaction database after the automated review has already completed
- Audit of the structured payload passed between the two agents shows no field exists for carrying an unresolved risk flag forward, only the final reconciled drug list itself

**Example**
```
Patient is admitted with a home medication list including a long-standing anticoagulant
Reconciliation agent processes the admission orders and identifies that a newly prescribed NSAID for pain control has a clinically significant interaction with the home anticoagulant
Reconciliation agent's conversational output states: "Note: newly added NSAID order has a significant interaction with patient's home anticoagulant; recommend pharmacy review before dispensing"
The structured medication list object handed to the downstream pharmacy-review agent contains only drug names, doses, and schedules -- no field carries the interaction note forward
Pharmacy-review agent receives the structured list, finds no flagged interaction field set, and returns "no interaction concerns identified" as its review outcome
NSAID is dispensed; the interaction is only caught two days later when a unit pharmacist manually cross-references the full list against an interaction-checking tool during routine chart review
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Analysis of multi-agent LLM system failures finds that information established by one agent is frequently lost or never communicated when handed to a downstream agent, and these inter-agent handoff failures account for a substantial share of overall multi-agent task failures | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Execution-provenance research for LLM agents argues that without explicit evidence tracing across agent boundaries, a finding established upstream has no mechanism to remain attached to a derived artifact as it moves through a multi-agent pipeline | [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1) |
| Research on agent-environment failure interactions finds that structured handoff interfaces between agents frequently omit fields needed to carry forward risk annotations generated upstream, causing downstream agents to operate on an incomplete view of the case | [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504) |

**Contributing Factors**
- Interaction flag exists only in the reconciliation agent's free-text reasoning or conversational summary, not in a structured field of the medication-list object passed downstream
- No schema requirement that the handoff payload include an explicit risk/flag carryforward field distinct from the plain drug list
- Pharmacy-review agent's prompt instructs it to assess the medication list it receives, with no instruction to request or verify whether the upstream agent surfaced any unresolved concerns
- No automated check comparing entities or risks mentioned in the upstream agent's reasoning trace against fields present in the structured handoff payload before the downstream agent proceeds

---

## Mitigation Strategies

1. **Structured Risk-Flag Field**: Require the handoff payload between reconciliation and pharmacy-review agents to include an explicit, structured field for unresolved interaction flags, separate from the plain medication list, that cannot be silently dropped
2. **Handoff Completeness Check**: Automatically diff entities and risks named in the upstream agent's reasoning trace against fields present in the structured handoff payload, blocking handoff completion on any unexplained discrepancy
3. **Downstream Acknowledgment Requirement**: Require the pharmacy-review agent to explicitly acknowledge or resolve any flag present in the handoff payload before issuing an approval, rather than allowing silent pass-through
4. **Cross-Agent Audit Trail**: Maintain a single shared case record that both agents read from and write to, rather than agent-local conversational summaries, so a finding logged by one agent is visible by construction to the next

### Metrics
- Rate of interaction flags identified by the reconciliation agent that are absent from the structured handoff payload to the pharmacy-review agent
- Number of interactions caught only by manual pharmacist review after automated review had already completed
- Mean time between an upstream flag being raised and a downstream resolution or acknowledgment being recorded

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Flag-handoff mismatch | Risk flag present in upstream reasoning trace absent from structured handoff payload | P1 | Block pharmacy-review approval; route to manual pharmacist review |
| Silent downstream approval | Pharmacy-review agent approves a list despite an unresolved upstream flag | P1 | Reverse approval; escalate to pharmacist |
| Recurring schema gap | Multiple cases show the same category of finding consistently dropped at handoff | P3 | Audit and extend handoff payload schema |

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
- [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504)
