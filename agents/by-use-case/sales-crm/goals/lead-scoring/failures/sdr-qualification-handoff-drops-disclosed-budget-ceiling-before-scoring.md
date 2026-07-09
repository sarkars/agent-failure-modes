# SDR-Qualification Handoff Drops a Disclosed Budget Ceiling Before Lead Scoring

## Issue: An SDR-Qualification Agent That Talks to a Prospect and Learns an Explicit, Hard Budget Ceiling Hands the Qualified Lead Off to a Downstream Lead-Scoring Agent via a Structured Summary That Omits the Budget Ceiling Because It Was Captured Only in the Free-Text Notes Field Rather Than the Summary's Defined Fields, Causing the Scoring Agent to Assign a Deal-Size Score Based on Firmographic Inference That Exceeds What the Prospect Actually Said They Can Spend

**Frequency**: Occasional

**Symptoms**
- A lead is scored with a projected deal size well above a budget ceiling the prospect explicitly stated during SDR qualification, with no trace of that ceiling in the scoring agent's inputs
- The SDR agent's conversation transcript contains the prospect's stated budget ceiling verbatim, but the structured handoff summary passed to the scoring agent has no field for it and the free-text notes containing it were not included in what the scoring agent ingests
- The scoring agent's deal-size estimate instead derives from firmographic proxies (company headcount, industry, funding stage), producing a number inconsistent with what was actually disclosed in the qualification call
- Re-running the handoff with the SDR's full call notes included, rather than only the structured summary fields, produces a deal-size score consistent with the disclosed ceiling
- Sales managers reviewing high-scored leads that stall in the pipeline find the disclosed budget ceiling in the original SDR notes, which was never carried into the score or surfaced to the AE who inherited the lead

**Example**
```
SDR-qualification agent runs a discovery call and the prospect states: "We have budget
approved up to $40K for this initiative, not a dollar more this fiscal year"
SDR agent logs the call as qualified and generates a structured handoff summary with
fields for company size, industry, role, and pain point -- there is no defined field
for "stated budget ceiling," so it goes into a free-text notes field only
Downstream lead-scoring agent ingests the structured summary fields to compute a
deal-size score, inferring a likely deal size of $85K based on the account's headcount
and industry benchmarks; it does not ingest the free-text notes field
Lead is scored as high-value based on the $85K inferred deal size and routed to an AE
expecting an enterprise-size close
AE proposes a $75K package; prospect reiterates the $40K ceiling stated weeks earlier
to the SDR, and the AE has no visibility that this constraint was ever disclosed
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Taxonomy work on multi-agent system failures identifies inter-agent misalignment, including loss of task-relevant information at agent-to-agent handoff boundaries, as one of three major failure categories observed across production multi-agent frameworks | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Agent failure taxonomy research classifies handoff and coordination failures, including information that exists in one agent's working context but is not propagated through a structured interface to the next agent, as a distinct system-level failure mode | [Where LLM Agents Fail and How They can Learn From Failures](https://arxiv.org/abs/2509.25370) |
| General LLM agent system failure analysis notes that structured hand-off schemas which omit a field for a given fact type create a systematic blind spot, since downstream agents typically consume only the defined schema rather than the full upstream context | [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933) |

**Contributing Factors**
- The SDR-to-scoring handoff schema has defined fields for firmographic attributes but no defined field for a disclosed budget ceiling or other hard constraints stated verbally during qualification
- The scoring agent's pipeline ingests only the structured summary fields and does not parse the SDR's free-text call notes, so any disclosed constraint not mapped to a schema field is invisible to it
- The SDR agent has no instruction to escalate or flag a disclosed hard constraint as a required field when the handoff schema lacks a slot for it, so the information is logged but not propagated
- No reconciliation step compares the scoring agent's deal-size inference against any budget figures present in the upstream qualification notes before the score is finalized

---

## Mitigation Strategies

1. **Required Constraint Field in Handoff Schema**: Add an explicit, required field for disclosed hard constraints (budget ceiling, timeline deadline, do-not-contact preference) to the structured SDR-to-scoring handoff schema, so this fact class cannot be silently dropped into unparsed free text
2. **Full-Context Ingestion for Deal-Size Scoring**: Require the scoring agent to ingest the SDR's full qualification notes, not only the structured summary fields, specifically when computing deal-size or budget-sensitive scores
3. **Disclosed-Constraint Reconciliation Check**: Before finalizing a deal-size score, run an automated check that scans upstream qualification notes for explicit budget or constraint language and flags any score that conflicts with a disclosed figure
4. **Mandatory Field Escalation on Schema Gap**: Require the SDR agent to flag any disclosed hard constraint that has no matching field in the handoff schema as an explicit escalation item, rather than allowing it to be absorbed silently into general notes

### Metrics
- Rate of scored leads where a disclosed budget ceiling or hard constraint exists in upstream SDR notes but is absent from the structured handoff fields used for scoring
- Number of AE-escalated deal-size mismatches traced back to a disclosed constraint lost at the SDR-to-scoring handoff
- Reconciliation-check catch rate: share of conflicting deal-size scores caught before reaching the AE versus discovered after

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Disclosed-constraint conflict | Scoring agent's deal-size estimate exceeds a budget ceiling figure found in upstream qualification notes | P1 | Hold score from AE-facing view; recompute using disclosed ceiling; notify SDR-to-AE handoff owner |
| Schema-gap escalation missed | SDR notes contain hard-constraint language with no corresponding structured handoff field and no escalation flag raised | P2 | Audit handoff schema for missing field types; backfill from notes |
| Free-text-only constraint | Scoring agent computes a deal-size score without ingesting the upstream free-text notes field | P3 | Require full-context ingestion before publishing deal-size score |

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [Where LLM Agents Fail and How They can Learn From Failures](https://arxiv.org/abs/2509.25370)
- [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933)
