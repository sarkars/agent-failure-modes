# Hallucinated Clear Sanctions-Screening Result When Screening API Times Out

## Issue: A Supplier-Onboarding Agent Calls a Sanctions/Watchlist-Screening API as Part of an Onboarding Checklist and, When the Call Times Out or Returns an Error Instead of a Result, Generates an Onboarding Summary Stating the Supplier "Cleared Screening," Treating the Absence of a Result as Equivalent to a Clean Result

**Frequency**: Rare but high-severity

**Symptoms**
- An onboarding summary states that a supplier "passed" or "cleared" sanctions/watchlist screening, but the session log shows the screening API call returned a timeout or error rather than a result
- Re-running the same screening query against the same API, after the fact, either succeeds and surfaces a genuine match or non-match, or fails again, in neither case confirming the original "cleared" claim was ever actually produced by the screening system
- The onboarding summary's "cleared" language is indistinguishable in format and confidence from summaries where the screening API genuinely returned a clean result, with no flag distinguishing a real clearance from an assumed one
- The gap is most visible for screening calls made during periods of API instability or rate-limiting, since those are the conditions under which a timeout or partial error is most likely to occur silently
- Procurement staff approving the onboarding based on the summary have no visibility into whether the screening call actually completed, since the summary text does not distinguish a completed check from an uncompleted one

**Root Cause**
When a tool call returns an error or times out, the agent generating the onboarding summary is not constrained to treat that as a hard stop; absent an explicit instruction that a non-result must produce an explicit incomplete-screening flag rather than a narrative conclusion, the model can complete the onboarding checklist with a plausible "cleared" statement that fills the gap left by the missing tool output. Because the summary-generation step is not the same computation as the screening call itself, a fluent "cleared" narrative can be produced with no actual screening result behind it.

**Example**
```
Supplier-onboarding agent calls the sanctions-screening API for a new supplier as a required onboarding checklist item
API call times out due to a transient rate-limiting issue, returning no result
Agent proceeds to generate the onboarding summary, stating "Sanctions screening: cleared" as one of the completed checklist items
Procurement staff approve the onboarding based on the summary, with no indication that the screening call never actually completed
Supplier is later found, when screening is genuinely run during an unrelated audit, to be on a current watchlist that was never actually checked at onboarding time
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Tool-use error taxonomies for dialogue and agentic systems identify completing a plausible narrative result from a failed or timed-out tool call as a distinct failure category, since downstream reasoning treats both error types identically unless the response is explicitly checked for a valid result before proceeding | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Surveys of LLM agent hallucination document that agents frequently complete a plausible, complete-looking output when a required tool call fails, rather than surfacing the failure as a blocker to the dependent task | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Research on agentic LLMs in the supply chain identifies unverified completion of compliance-critical checklist items as a distinct risk category from forecasting or routing errors, given the binary and high-severity nature of a missed sanctions match | [Agentic LLMs in the Supply Chain: Towards Autonomous Multi-Agent Consensus-Seeking](https://arxiv.org/pdf/2411.10184) |

**Contributing Factors**
- No validation step distinguishes a screening API call that returned a genuine clean result from one that returned an error or timeout before the onboarding summary is generated
- The onboarding-summary template presents "cleared" as a default-style completed checklist item rather than requiring the underlying API response to be explicitly attached or referenced
- Procurement approval workflow does not require independent confirmation that each compliance-critical checklist item's underlying tool call actually succeeded

---

## Mitigation Strategies

1. **Hard-Stop on Screening API Failure**: Require any sanctions-screening API timeout or error to block the onboarding summary from stating a "cleared" result, generating an explicit incomplete-screening flag instead and halting onboarding approval until the screening call succeeds
2. **Result-Attachment Requirement**: Require the onboarding summary to reference the specific screening API response (a match/non-match result and timestamp) it is reporting, rejecting any "cleared" statement with no attached underlying result
3. **Compliance-Checklist Tool-Call Audit**: Automatically verify, before onboarding approval, that every compliance-critical checklist item's underlying tool call returned a genuine successful result, flagging any item resting on a failed or missing call
4. **Retry-and-Escalate on Repeated Failure**: Configure automatic retries for a failed screening call, with escalation to manual compliance review if retries continue to fail, rather than allowing the checklist item to be marked complete by default

### Metrics
- Rate of onboarding summaries stating a "cleared" screening result with no corresponding successful API response in the session log
- Mean time between a screening API failure and either a successful retry or a manual compliance review escalation
- Rate of post-onboarding audits finding a supplier was never actually screened despite an onboarding summary stating clearance

### Alerts
- An onboarding summary states a sanctions-screening "cleared" result with no successful API response logged → P1
- A compliance-critical checklist item is marked complete following a tool-call failure with no retry or escalation recorded → P1
- Hallucinated-clearance rate across all supplier onboardings exceeds zero for any rolling window → P1

---

## References

- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [Agentic LLMs in the Supply Chain: Towards Autonomous Multi-Agent Consensus-Seeking](https://arxiv.org/pdf/2411.10184)
