# Multi-Agent Handoff Drops Flagged Interaction Between Reconciliation and Pharmacy-Review Agent

## Issue: A Medication-Reconciliation Agent That Identifies a Specific Drug-Drug Interaction Risk Between a Newly Prescribed Medication and a Continuing Home Medication Records That Finding Only Within Its Own Free-Text Reasoning or Conversational Summary, and When the Reconciled Medication List Is Handed Off to a Downstream Pharmacy-Review Agent That Consumes Only the Structured Medication List, the Interaction Flag Never Crosses the Handoff Boundary, So the Pharmacy-Review Agent Approves the List as if No Interaction Risk Had Been Identified

**Frequency**: Occasional

**Symptoms**
- The pharmacy-review agent's sign-off makes no reference to an interaction the reconciliation agent's own output explicitly named, proceeding as though the list were unremarkable
- Re-running reconciliation on the same admission in isolation reliably resurfaces the same interaction, showing the detection worked upstream and the loss is specific to the handoff
- The only thing that catches the interaction is a pharmacist manually cross-checking the full list against a reference tool well after the automated review already cleared it
- The structured object handed to pharmacy-review carries drug names, doses, and schedules and nothing else — there was never a field capable of carrying a flag forward in the first place
- The reconciliation agent's own reasoning trace states the interaction and even recommends pharmacy review before dispensing, language with no corresponding structured counterpart anywhere in the payload

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
- The medication-list object passed downstream is built to represent the reconciled drug list itself — names, doses, schedules — not any risk finding the reconciliation agent generated while producing that list
- The interaction note is written into the reconciliation agent's own output text, which the pharmacy-review agent's input pipeline does not parse or consume as part of its review
- Pharmacy-review's task is defined as evaluating the medication list it's handed; nothing in its instructions has it ask whether the upstream agent flagged anything beyond what's in that list
- There's no step that cross-references what the reconciliation agent actually found against what made it into the structured list before the pharmacy-review agent signs off, so a real finding and a clean list are indistinguishable to the downstream agent

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
