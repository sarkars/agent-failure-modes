# Multi-Agent Handoff Drops Disclosed Accommodation Request Before Interview Scheduling

## Issue: A Recruiter-Screening Agent's Free-Text Notes Recording a Candidate's Disclosed Accessibility Accommodation Request Are Not Captured in the Structured Handoff Schema Passed to the Interview-Scheduling Agent, Which Books an Interview Format That Does Not Provide the Requested Accommodation

**Frequency**: Occasional

**Symptoms**
- The scheduling agent sends a standard video-conferencing link for a candidate who told the screening agent, by name, that they are deaf and need a live captioner or ASL interpreter for any video round
- The scheduling schema's fields -- time zone, remote vs. onsite -- cover the accessibility-adjacent cases it was designed for, so time-zone and location accommodations pass through the handoff fine; a captioner or interpreter request fails specifically because no field in that set was ever meant to hold it
- Querying the scheduling agent about the omission shows it operating exactly as scoped: it received role, level, timeslot, and panel, and had no way to know the screening conversation contained anything more than that
- The screening agent's own transcript shows it acknowledged the request and told the candidate it would be arranged -- the commitment was made, just not by the agent capable of acting on it
- The gap surfaces at the worst possible moment: the candidate discovers nothing was arranged the morning of the interview, when a reschedule is the only remaining fix

**Root Cause**
The screening agent's phone-screen output is a conversation transcript, and the scheduling agent's input is a fixed set of logistics fields (role, level, timeslot, panel) built for booking, not for accessibility. Because accommodation requests are transmitted as free text embedded in a summary rather than as a field the scheduling agent's booking logic ever reads, a captioner or interpreter request the screening agent explicitly recorded is functionally indistinguishable, from the scheduler's side, from a request that was never made at all.

**Example**
```
Candidate tells the recruiter-screening agent during the phone screen: "I'm deaf and will need a live captioner or ASL interpreter for any video interview going forward"
Screening agent acknowledges the request in the chat and notes it will be arranged for the next round
Screening agent hands off to the interview-scheduling agent using the standard structured schema: role, level, timeslot, interviewer panel -- no field exists for "disclosed accommodation request"
Scheduling agent books a standard video-conferencing link with no captioner or interpreter arranged, since that requirement was never represented in the structured fields it received
Candidate discovers the morning of the interview that no accommodation was arranged and has to request a reschedule, damaging the candidate experience and creating ADA compliance exposure for the employer
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Multi-agent LLM systems show a recurring failure mode where information established in one agent's reasoning or conversation is not correctly specified or transferred to a downstream agent operating on a fixed schema | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Generalist multi-agent systems require explicit mechanisms for passing task-relevant context between agents with different input schemas, and gaps in this transfer are identified as a common source of downstream task failure | [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://arxiv.org/abs/2411.04468) |
| LLM agent frameworks applied to recruitment workflows are evaluated against realistic screening tasks where candidate-disclosed information not captured by structured fields is identified as a source of downstream pipeline error | [Application of LLM Agents in Recruitment: A Novel Framework for Resume Screening](https://arxiv.org/pdf/2401.08315) |

**Contributing Factors**
- The scheduling handoff schema has no free-text or accommodation-request field for needs disclosed during screening that fall outside standard logistics fields
- No check runs before interview scheduling to compare the screening agent's conversation transcript against the structured scheduling fields for an unrepresented accommodation request
- Accommodation requests are especially likely to fall outside the schema, since they are inherently candidate-specific and not part of the standard, role-generic scheduling fields

---

## Mitigation Strategies

1. **Accommodation-Request Field in Scheduling Schema**: Add a structured "disclosed accommodation request" field to the screening-to-scheduling handoff schema that the screening agent is required to populate whenever its conversation transcript contains an accessibility-related request
2. **Pre-Scheduling Transcript Reconciliation Check**: Before booking the interview, require a check that scans the screening agent's conversation transcript for accommodation-related language and flags any request not represented in the structured scheduling fields
3. **Human Recruiter Confirmation Gate for Flagged Accommodations**: Route any handoff where an accommodation request is detected to human recruiter-coordinator confirmation before the interview is booked, rather than letting the scheduling agent resolve it automatically
4. **Screening-to-Scheduling Traceability Log**: Maintain a log linking each scheduled interview to the screening transcript it was derived from, so a missing accommodation can be caught by audit before the interview rather than by the candidate on the day of it

### Metrics
- Rate of scheduled interviews later found, on review, to omit an accommodation request present in the screening transcript
- Rate of handoffs with a populated "disclosed accommodation request" field versus handoffs where a downstream audit found a request that should have been populated but wasn't
- Average time between interview scheduling and accommodation-gap detection, when gaps occur

### Alerts
- An interview is scheduled with an accommodation request present in the screening transcript but absent from the structured scheduling fields → P1
- A candidate reports that a disclosed accommodation was not arranged for a scheduled interview → P1
- Rate of interviews requiring post-scheduling correction for missed accommodation requests exceeds the defined threshold for a rolling window → P2

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://arxiv.org/abs/2411.04468)
- [Application of LLM Agents in Recruitment: A Novel Framework for Resume Screening](https://arxiv.org/pdf/2401.08315)
