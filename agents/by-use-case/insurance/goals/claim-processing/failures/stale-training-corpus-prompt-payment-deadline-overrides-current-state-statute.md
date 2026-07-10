# Stale Training-Corpus Prompt-Payment Deadline Overrides Current State Statute

## Issue: A Claims-Processing Agent Determining the Statutory Deadline by Which a Claim Must Be Acknowledged, Investigated, or Paid Under a Given State's Prompt-Payment Law Answers From a General, Memorized Sense of Typical State Deadlines Formed During Pretraining Instead of Calling the Live Regulatory-Requirements Tool It Has Available, Producing a Processing Timeline Based on an Outdated or Generic Deadline Rather Than the State's Actual Current Statutory Requirement

**Frequency**: Occasional

**Symptoms**
- The agent's claim-processing timeline cites a prompt-payment deadline (e.g., "must pay within 30 days of proof of loss") that does not match the actual current statute for the claim's jurisdiction
- The agent had a live regulatory-requirements lookup tool available for the session but the trace shows no call to it before the deadline was stated
- The deadline cited matches a commonly cited generic or different-state figure rather than the specific state's actual current requirement, which was recently amended
- When explicitly instructed to "check the current regulatory-requirements tool for this state," the agent retrieves the correct, amended deadline and revises the processing timeline
- Claims in the affected state show a pattern of internal processing targets set to the wrong deadline, creating either premature payment pressure or a compliance gap depending on which direction the actual statute differs

**Example**
```
A state legislature amends its prompt-payment statute this year, shortening the deadline for acknowledging a claim
from 15 business days to 10 calendar days following catastrophe-related legislative reform
Claims-processing agent is assigned a new claim from that state and sets an internal acknowledgment deadline of
15 business days, the figure consistent with the state's prior, since-amended statute and with the more commonly
cited general figure for prompt-payment acknowledgment windows
The agent had a live regulatory-requirements tool available that reflects the current statute, but the trace shows
the deadline was stated directly from the agent's own reasoning with no tool call beforehand
The claim is acknowledged on day 12, which was within the old standard but is a statutory violation under the
amended 10-calendar-day requirement, exposing the carrier to a regulatory compliance finding
When a compliance reviewer later asks the agent to verify the deadline via the regulatory-requirements tool, it
retrieves the correct amended figure and confirms the original timeline was non-compliant
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Survey research on LLM agent hallucination identifies reliance on memorized, static training-time facts in place of an available live tool result as a distinct failure mechanism producing confidently wrong outputs without outright fabrication | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Tool-use error detection research finds agents frequently default to an internally generated answer in situations where a tool call would resolve whether a regulatory figure is current, particularly when the agent already has a plausible-sounding figure from general knowledge | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Execution-provenance research argues that without traceable evidence linking a stated regulatory deadline to an actual current tool call, there is no way to distinguish a grounded current figure from one based on outdated or generic memorized knowledge | [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1) |

**Contributing Factors**
- The agent treats state prompt-payment deadlines as stable general knowledge rather than as jurisdiction-specific, independently amendable statutes requiring live verification each time
- No standing instruction requiring a regulatory-requirements tool call specifically when setting a processing deadline, regardless of whether the agent believes it already knows the figure
- General familiarity with commonly cited prompt-payment deadlines across states competes with, rather than defers to, the specific current statute for the claim's actual jurisdiction
- No automated alert notifies the claims pipeline when a state's prompt-payment statute changes, so there is no trigger forcing re-verification of deadlines for claims already in process in that state

---

## Mitigation Strategies

### Prevention

1. **Forced regulatory-tool-call gate before deadline setting**: Implement gating: any claim-processing workflow that needs to set a processing deadline (acknowledgment, investigation start, payment target) is blocked from proceeding until a mandatory regulatory-requirements tool call is made and its result explicitly logged. The tool call must return: (state, deadline_type, days/calendar_days, effective_date_of_statute, data_source_timestamp). Fail-safe: if tool call fails or result is stale (data source timestamp >30 days old), return "Cannot proceed - current regulatory requirement unavailable; halt deadline setting" rather than defaulting to agent's own reasoning. Root cause mitigation: Prevents parametric-knowledge-only reasoning by enforcing explicit tool-use with result validation.

2. **Statute amendment monitoring with in-flight claim re-verification triggers**: Maintain automated subscription to state prompt-payment law change feeds. On amendment detected: (a) Identify all claims in that state currently in-flight, (b) Flag them for deadline re-verification, (c) Re-run regulatory-requirements tool call for each affected claim, (d) Alert if internal deadline no longer matches updated statute, (e) Generate escalation report with compliance exposure estimate. Root cause: Catches statute changes that would otherwise silently invalidate prior deadline settings.

3. **Execution-trace validation with tool-call provenance checking**: Implement post-hoc audit: after claim processing, verify execution trace includes mandatory regulatory-tool-call. If trace shows deadline-setting step without tool-call in preceding steps, flag as compliance violation. Auto-review such claims for potential deadline mismatches. Generate audit report: "Claims processed without tool-call provenance: [N]; deadline audit: [X matches statute, Y mismatch]". Root cause: Detects tool-use bypass by tracing execution provenance.

### Detection & Response

1. **Deadline-accuracy audit logging with source validation**: For every claim-processing deadline set, log: (a) jurisdiction (state), (b) deadline type (ack, investigate, pay), (c) regulatory-tool call result (days, effective date, data source timestamp), (d) internal deadline set, (e) match/mismatch vs. tool result, (f) execution trace (was tool call made). Alert when: (1) deadline set without tool call in trace, (2) deadline differs from tool result, (3) tool result stale (data source >30 days old). Target: 100% of deadlines have validated tool-call provenance.

2. **Post-statute-amendment compliance re-audit**: On each state statute amendment, trigger batch re-audit: scan all claims processed in past 6 months in affected state. Re-run regulatory-tool call for each. Categorize: (a) claims compliant under old statute but now violate new statute, (b) claims that remained compliant despite statute change, (c) claims processed after amendment with correct new deadline. Generate exposure report and escalate category (a) for potential remediation (timing adjustment, claimant notification).

### Architecture Patterns

1. **Forced Regulatory-Tool Gate**: Claim-processing workflow step: (claim_state, deadline_type) → FORCED: call regulatory-requirements tool → Retrieve: (required_days, effective_statute_date, data_source_timestamp) → VALIDATE: data_source_timestamp <30 days → SET: internal_deadline = today + required_days → LOG: (tool_call, result, deadline_set, match_status) → PROCEED: only if all validations pass; HALT: otherwise.

2. **Statute Amendment Monitoring & In-Flight Escalation**: Service subscribes to state prompt-payment law changes (state legislature feeds, insurance commissioner notices). On amendment: Trigger batch job → Query: "All claims in state X processed between [old effective date, new effective date]" → For each: re-call regulatory-tool → Compare old vs. new deadline → Flag mismatches → Generate compliance escalation.

3. **Execution-Trace Validator**: Post-processing audit. Input: claim_processing_session_trace → Validates: (1) deadline-setting steps have preceding regulatory-tool-call steps in trace, (2) tool-call result matches stated deadline, (3) tool result timestamp validates freshness. Output: compliance_status (PASS/VIOLATION) with details.

### Key Metrics

| Metric | Target | Alert Threshold | Measurement Method |
|--------|--------|-----------------|--------------------|
| Regulatory-Tool-Call Provenance Rate | 100% | <99% | % of deadline-setting steps with documented regulatory-tool-call in execution trace |
| Deadline-Accuracy Compliance Rate | 100% | <99% | # of processed deadlines matching current regulatory-requirements tool result / total claims |
| Tool-Call Freshness Rate | 100% | <95% | % of regulatory-tool calls with data source timestamp <30 days old (current statutory data) |
| Post-Amendment Compliance Rate | 100% | <99% | % of claims processed post-statute-amendment that use updated deadline (vs. pre-amendment deadline) |
| Statute-Change Detection Latency | <5 days | >14 days | Time from state statute amendment effective date to detection by monitoring system and flag generation |

### Alerts & Escalation

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Deadline Set Without Tool-Call | Execution trace shows deadline-setting step with no preceding regulatory-requirements tool call | CRITICAL | Audit claim for deadline accuracy; re-run regulatory tool; verify deadline against current statute; escalate if mismatch |
| Deadline-Statute Mismatch | Internal processing deadline does not match current regulatory-requirements tool output for claim's jurisdiction | CRITICAL | Halt claim processing; re-calculate deadline from tool result; notify claimant if acknowledgment/payment already sent at wrong deadline |
| Stale Tool-Call Data | Regulatory-requirements tool returns data older than 30 days (statute may have changed); deadline based on stale data | HIGH | Escalate to compliance; attempt to retrieve fresh data from state legislature; re-verify deadline when fresh data available |

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
