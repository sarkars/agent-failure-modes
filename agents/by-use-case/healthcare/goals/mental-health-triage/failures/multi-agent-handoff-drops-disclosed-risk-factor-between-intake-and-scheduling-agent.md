# Multi-Agent Handoff Drops Disclosed Risk Factor Between Intake and Scheduling Agent

## Issue: A Chat-Based Mental-Health Intake Agent That Elicits and Records a Significant Risk Disclosure During Conversation Captures That Finding Only in Its Own Conversational Reasoning or a Free-Text Summary, and When the Case Is Handed Off to a Downstream Scheduling/Routing Agent That Acts on a Structured Acuity Field to Determine Appointment Urgency, the Disclosed Risk Factor Never Crosses the Handoff Boundary, So the Case Is Scheduled at a Routine Priority as if the Disclosure Had Never Occurred

**Frequency**: Occasional

**Symptoms**
- A patient's disclosure of a specific risk factor is present in the intake transcript in plain language, but the case record the scheduling agent receives shows a routine or moderate acuity level with nothing to indicate it
- The scheduling agent's output — appointment timing, routing tier — is exactly what a low-acuity case would produce, with no acknowledgment of a disclosure that exists a level up in the same case
- The disclosure only gets acted on when a clinician reads the full intake transcript directly, typically during chart prep well after the lower-urgency appointment has already been scheduled and communicated
- Re-reviewing the intake transcript alone reliably reproduces the disclosure, which rules out the possibility that the information was never captured during intake in the first place
- The structured record connecting the two agents has no field capable of carrying a qualitative risk narrative — only the acuity score and appointment logistics — so there was nowhere for the disclosure to go even if someone tried to pass it forward

**Example**
```
Patient in a chat-based intake session discloses, partway through, that they have recently acquired access to a specific lethal means following a recent loss
Intake agent's conversational reasoning notes this disclosure and continues the structured screening questions to completion
Intake agent computes a moderate acuity score from the structured screening instrument responses and hands the case off to a scheduling agent via a structured record containing the acuity score, contact info, and requested appointment type
The qualitative disclosure about means access is present only in the full conversation transcript, not in any field of the structured handoff record
Scheduling agent reads only the structured record, sees a moderate acuity score, and schedules a routine next-available appointment two weeks out
A clinician reviewing the full transcript during chart prep before the appointment is the first person to register the means-access disclosure, well after the lower-urgency scheduling decision was already made and communicated to the patient
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Multi-agent LLM system failure analysis identifies inter-agent information loss -- where a finding established by one agent fails to reach a downstream agent that acts on its own narrower view of the case -- as a leading cause of overall task failure in agentic pipelines | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Execution-provenance research for LLM agents argues that without explicit evidence tracing across agent and task boundaries, a qualitative finding has no mechanism to remain attached to downstream decisions derived from a narrower structured summary | [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1) |
| Research on agent-environment failure interactions finds structured handoff interfaces between cooperating agents frequently omit fields needed to carry forward qualitative risk context generated during an upstream conversational phase | [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504) |

**Contributing Factors**
- The handoff to scheduling carries a numeric acuity score plus logistics fields; it was never built to carry a qualitative disclosure that falls outside what the screening instrument itself measures
- The disclosure lives only in the conversational transcript the intake agent produced, which the scheduling agent's input does not include or parse — only the computed score and logistics fields cross the boundary
- Scheduling's logic keys entirely off the acuity field it receives; nothing in its instructions has it check whether the source transcript contains content the score itself didn't capture
- Because the acuity instrument is structured and validated, it's treated as the complete signal for urgency — there's no independent path for a qualitative disclosure to override a moderate score if the instrument didn't weight it that way

---

## Mitigation Strategies

1. **Structured Risk-Narrative Field**: Require the intake-to-scheduling handoff payload to include an explicit field for qualitative risk disclosures distinct from the numeric acuity score, populated whenever the intake conversation contains risk-relevant content
2. **Handoff Completeness Check**: Automatically scan the intake transcript for risk-relevant disclosures and diff against the structured handoff payload, blocking routine scheduling on any unexplained discrepancy
3. **Acuity-Override Escalation Path**: Allow any unresolved qualitative risk flag to independently trigger an urgent-routing override regardless of the computed numeric acuity score, rather than requiring the score itself to capture every risk dimension
4. **Shared Case Record**: Replace agent-local conversational summaries with a single case record both intake and scheduling agents read from and write to, so a disclosure logged during intake is visible by construction to the scheduling step

### Metrics
- Rate of risk disclosures present in intake transcripts that are absent from the structured handoff payload to the scheduling agent
- Number of cases where a human reviewer identifies a missed risk disclosure after routine scheduling had already occurred
- Mean time between a risk disclosure being made during intake and an urgent-routing decision being triggered

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Disclosure-handoff mismatch | Risk-relevant content present in intake transcript absent from structured handoff payload | P1 | Block routine scheduling; route to immediate clinician review |
| Routine scheduling despite disclosure | Scheduling agent assigns routine priority to a case with an unresolved upstream risk flag | P1 | Reverse scheduling decision; escalate to urgent routing |
| Recurring schema gap | Multiple cases show the same category of disclosure consistently dropped at handoff | P3 | Audit and extend handoff payload schema |

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
- [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504)
