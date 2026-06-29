# Multi-Agent Handoff Drops Disclosed Accommodation Request Before Interview Scheduling

## Issue: A Recruiter-Screening Agent's Free-Text Notes Recording a Candidate's Disclosed Accessibility Accommodation Request Are Not Captured in the Structured Handoff Schema Passed to the Interview-Scheduling Agent, Which Books an Interview Format That Does Not Provide the Requested Accommodation

**Frequency**: Occasional

**Symptoms**
- A candidate discloses during the phone screen that they will need a live captioner, an ASL interpreter, or extended response time for any video interview, and the screening agent's chat transcript records the request, but the scheduling agent books a standard video-interview link with no accommodation arranged
- The structured handoff schema passed to the interview-scheduling agent includes fields for role, level, timeslot, and interviewer panel, but has no field for an accommodation request disclosed only in the screening agent's free-text conversation notes
- Asking the scheduling agent why the accommodation was omitted shows it received only the structured scheduling fields and had no input describing the disclosed accommodation need from the screening agent's transcript
- The miss concentrates on accommodation types that fall outside the schema's predefined scheduling options (time zone, remote vs. onsite), since those are the only accessibility-adjacent fields the schema was built to carry
- The gap is most often caught only when the candidate raises the accommodation request again immediately before the interview, or after the interview has already started without it

**Root Cause**
The handoff between the recruiter-screening agent, which produces free-text conversation notes from the phone screen, and the interview-scheduling agent, which books the interview from a fixed structured schema, has no mechanism for surfacing an accommodation request that does not map to one of the schema's predefined fields. The screening agent's notes record the disclosed need, but nothing in the handoff forces a check for "does this candidate's screening transcript contain an accommodation request not represented in the structured scheduling fields" before the scheduling agent proceeds, so a real, legally significant request is silently dropped at the agent-to-agent boundary.

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
