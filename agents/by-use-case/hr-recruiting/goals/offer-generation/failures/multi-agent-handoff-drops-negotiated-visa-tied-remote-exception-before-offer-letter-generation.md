# Multi-Agent Handoff Drops Negotiated Visa-Tied Remote Exception Before Offer-Letter Generation

## Issue: A Recruiting-Coordinator Agent's Free-Text Negotiation Notes Recording a Visa-Status-Contingent Remote-Work Exception Are Not Captured in the Structured Handoff Schema Passed to the Offer-Letter-Generation Agent, Which Issues a Standard In-Office Offer That Contradicts What the Candidate Was Told

**Frequency**: Occasional

**Symptoms**
- A candidate is told in a negotiation chat that they can work remotely for the first six months while a work-visa transfer is pending, but the generated offer letter states the standard in-office work location with no mention of the exception
- The recruiting-coordinator agent's conversation log contains the negotiated exception in free text, but the structured "offer parameters" object passed to the offer-letter-generation agent has no field corresponding to a temporary or visa-contingent work-location exception
- Asking the offer-letter-generation agent why the exception was omitted shows it only received the standard structured fields (title, comp, start date, default work location) and had no input describing the negotiated deviation
- The miss concentrates on offers involving any negotiated term that falls outside the standard offer-parameter schema, such as relocation timing, equipment stipends tied to a specific condition, or visa-contingent arrangements
- The candidate or hiring manager catches the discrepancy only when comparing the offer letter against the original negotiation conversation, after the letter has already been generated and sometimes sent

**Root Cause**
The handoff between the recruiting-coordinator agent and the offer-letter-generation agent passes only a fixed structured schema of offer parameters, with no mechanism for surfacing a negotiated condition that does not map to one of the schema's predefined fields. The coordinator agent's free-text negotiation notes contain the exception, but nothing in the handoff forces a check for "does this candidate's negotiation history contain any term not represented in the structured offer parameters" before the offer letter is generated, so a real-but-nonstandard commitment is silently dropped at the agent-to-agent boundary.

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
