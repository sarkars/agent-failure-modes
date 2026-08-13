# Multi-Agent Handoff Drops Negotiated Visa-Tied Remote Exception Before Offer-Letter Generation

## Issue: A Recruiting-Coordinator Agent's Free-Text Negotiation Notes Recording a Visa-Status-Contingent Remote-Work Exception Are Not Captured in the Structured Handoff Schema Passed to the Offer-Letter-Generation Agent, Which Issues a Standard In-Office Offer That Contradicts What the Candidate Was Told

**Frequency**: Occasional

**Symptoms**
- The offer letter lists the default in-office location for a candidate who was explicitly told their start is contingent on a visa transfer and that they'd work remotely from their current location in the meantime
- Title, comp, and start date -- the fields the offer-parameters schema was designed to carry -- come through correctly every time; the work-location exception fails specifically because a visa-contingent arrangement was never one of the conditions that schema was built to express
- The offer-letter-generation agent isn't malfunctioning relative to its own inputs: given title, comp, start date, and default location, it produces exactly the letter those fields specify, with no signal that a condition was attached to any of them
- The coordinator agent's chat log shows it confirmed the arrangement to the candidate in real time -- the commitment existed and was acknowledged, it just never left the conversation it was made in
- Because the letter is the candidate's first written artifact from the process, the contradiction reads as the company reneging rather than as a data-transfer gap, even after the letter has already gone out

**Root Cause**
The coordinator agent negotiates in open-ended conversation, where a visa-contingent remote exception is just another sentence, but hands off through an offer-parameters object built around what an offer usually needs: title, comp, start date, location. That object has no slot for a condition attached to one of its own fields, so a location that is "in-office, unless visa transfer is pending" cannot be represented as anything other than "in-office" -- the generation agent receives a flattened value with the condition already stripped out, not a condition it failed to check.

**Example**
```
Candidate negotiates with the recruiting-coordinator agent: "I can start once my visa transfer to this role is approved, but I'd need to work remotely from my current location for the first six months while that's pending"
Coordinator agent confirms the arrangement in the chat and notes it will be reflected in the offer
Coordinator agent hands off to the offer-letter-generation agent using the standard structured offer-parameters schema: title, comp, start date, default work location -- no field exists for "temporary visa-contingent remote exception"
Offer-letter-generation agent produces a standard offer letter listing the default in-office work location with no mention of the six-month remote exception
Candidate receives an offer letter that contradicts what they were told during negotiation
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Multi-agent LLM systems show a recurring failure mode where information established in one agent's reasoning or conversation is not correctly specified or transferred to a downstream agent operating on a fixed schema | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Generalist multi-agent systems require explicit mechanisms for passing task-relevant context between agents with different input schemas, and gaps in this transfer are identified as a common source of downstream task failure | [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://arxiv.org/abs/2411.04468) |
| Audits of agentic workflow failures in production platforms identify schema mismatches at agent-to-agent handoff boundaries as a recurring root cause of dropped task-relevant information | [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735) |

**Contributing Factors**
- The offer-parameters schema passed between the recruiting-coordinator and offer-letter-generation agents has no free-text or exception field for negotiated terms outside the standard set
- No check runs before offer-letter generation to compare the candidate's negotiation conversation history against the structured offer parameters for unrepresented commitments
- Negotiated exceptions tied to external, time-bound conditions (visa status, relocation timing) are especially likely to fall outside the standard schema, since they are by definition non-standard

---

## Mitigation Strategies

1. **Exception Field in Offer-Parameters Schema**: Add a structured "negotiated exception" field to the offer-parameters handoff schema that the coordinator agent is required to populate whenever a negotiation conversation contains a commitment outside the standard fields
2. **Pre-Generation Negotiation Reconciliation Check**: Before generating the offer letter, require a check that compares the candidate's negotiation conversation history against the structured offer parameters and flags any commitment not represented in the schema
3. **Human Review Gate for Non-Standard Commitments**: Route any offer with a populated exception field to human recruiter review before the offer letter is sent, rather than allowing the offer-letter-generation agent to resolve it automatically
4. **Negotiation-to-Offer Traceability Log**: Maintain a log linking each generated offer letter to the negotiation conversation it was derived from, so discrepancies can be caught by audit before being caught by the candidate

### Metrics
- Rate of generated offer letters later found, on review, to omit a negotiated term present in the candidate's negotiation conversation history
- Rate of offers with a populated "negotiated exception" field versus offers where a downstream audit found an exception that should have been populated but wasn't
- Average time between offer-letter generation and discrepancy detection, when discrepancies occur

### Alerts
- An offer letter is sent with a negotiated exception present in the conversation history but absent from the structured offer parameters → P1
- A candidate or hiring manager reports a discrepancy between the offer letter and the negotiation conversation → P1
- Rate of offers requiring post-generation correction for missed negotiated terms exceeds the defined threshold for a rolling window → P3

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://arxiv.org/abs/2411.04468)
- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735)
