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

1. **Mandatory Regulatory-Tool Call Before Setting Any Deadline**: Require a live regulatory-requirements tool call before any claim-processing deadline is set or communicated, regardless of whether the agent's own reasoning already produces a plausible figure
2. **Statute-Change Trigger for In-Flight Claims**: When a state's prompt-payment statute changes, automatically flag claims already in process in that state for deadline re-verification against the updated requirement
3. **Jurisdiction-Tagged Deadline Snapshot**: Pass the regulatory-requirements tool's last-updated timestamp and jurisdiction alongside the deadline figure in tool results so the agent can recognize when general cross-state knowledge might not reflect this state's current requirement
4. **Compliance Cross-Check Before Acknowledgment Sent**: Run an automated check comparing the internal processing deadline against the live regulatory-requirements tool's current figure before any acknowledgment or payment communication is sent to the claimant

### Metrics
- Rate of claim-processing deadlines that do not match the current regulatory-requirements tool's figure for the claim's jurisdiction
- Number of claims processed without a corresponding regulatory-requirements tool call in the session trace
- Time lag between a statute amendment and the first claim correctly processed under the new deadline

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Deadline mismatch with live statute | Internal processing deadline does not match current regulatory-requirements tool output for the claim's jurisdiction | P1 | Halt processing clock; recalculate deadline from live tool result |
| Deadline set without regulatory-tool call | Processing deadline set with no regulatory-requirements tool call in trace | P2 | Flag for compliance audit; reinforce mandatory-call instruction |
| Post-amendment violation spike | Rate of deadline mismatches rises in the claims following a statute amendment in a given state | P1 | Trigger mandatory re-verification mode for all in-flight claims in that state |

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
