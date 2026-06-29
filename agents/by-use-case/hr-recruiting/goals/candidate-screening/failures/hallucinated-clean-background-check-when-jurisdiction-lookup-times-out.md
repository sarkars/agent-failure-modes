# Hallucinated Clean Background Check When Jurisdiction Lookup Times Out

## Issue: A Candidate-Screening Agent Reports "No Criminal Record Found" for a Candidate When the Background-Check API Only Successfully Returned Results for Some of the Candidate's Residency Jurisdictions and Timed Out on the Rest, Treating the Partial Response as a Complete Clean Result Instead of Flagging the Missing Jurisdictions as Unverified

**Frequency**: Occasional

**Symptoms**
- A candidate's screening summary states "background check clear, no criminal record found" even though the underlying background-check API response shows results returned for only 2 of 3 jurisdictions the candidate listed as prior residences
- The agent's summary does not distinguish "jurisdiction returned a clean result" from "jurisdiction lookup timed out and was never checked"
- Asking the agent to show its source for the clean determination surfaces a raw API response with a timeout or partial-result status code for the missing jurisdiction, which the agent's narrative summary omitted
- The miss concentrates on candidates with multi-state or multi-country residency history, where the background-check vendor's API is most likely to time out on at least one jurisdiction query
- Re-running the same jurisdiction query later, after the vendor's API is no longer under load, sometimes returns a non-clean result the original screening missed entirely

**Root Cause**
The screening agent's downstream report-generation step composes a single fluent "clear" or "not clear" summary from whatever fields the background-check API populated, without checking that every requested jurisdiction returned a definitive status before that summary is generated. Because a partial response and a complete clean response are structurally similar -- both contain populated jurisdiction fields with no flagged record -- the agent's natural-language summarization smooths over the missing jurisdiction's timeout status rather than treating it as a hard stop requiring re-query or escalation.

**Example**
```
Candidate lists prior residences in California, Texas, and Ontario (Canada) on the screening intake form
Background-check agent submits all three jurisdictions to the vendor API in a single batch request
Texas and California return clean results; the Ontario query times out and the API returns a partial-batch status with an empty result for that jurisdiction
Agent generates candidate summary: "Background check complete: no criminal record found"
Recruiter advances candidate to offer stage without anyone re-querying the Ontario jurisdiction, which was never actually checked
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Tool-use agents frequently fail to distinguish a tool call that returned an error or partial result from one that returned a complete result, producing confident downstream summaries from incomplete data | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Surveys of LLM agent hallucination identify completion of plausible values from incomplete tool or retrieval output as a distinct and recurring failure category, separate from pure knowledge hallucination | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Audits of agentic workflow failures in production platforms find that partial or timed-out tool responses are a recurring root cause of downstream errors, particularly when the orchestration layer does not propagate a per-field completion status | [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735) |

**Contributing Factors**
- The background-check API's partial-batch response format does not clearly separate "jurisdiction returned clean" from "jurisdiction not yet returned," and the agent's summarization step does not check for the latter before composing a "clear" determination
- No mandatory rule requires every requested jurisdiction to reach a definitive status before the agent is permitted to generate a final clear/not-clear summary
- Multi-jurisdiction candidates are not flagged for a stricter completion check, even though they are the population most likely to trigger a partial vendor response

---

## Mitigation Strategies

1. **Per-Jurisdiction Completion Gate**: Require the agent to verify a definitive status (clean or flagged) for every requested jurisdiction before generating any "background check complete" summary; treat any jurisdiction without a definitive status as blocking, not as defaulting to clean
2. **Structural Distinction Between Timeout and Clean**: Modify the background-check API integration so a timeout or partial-batch response is surfaced to the agent as a distinct status code that cannot be summarized as "no record found"
3. **Mandatory Re-Query on Timeout**: Automatically re-submit any jurisdiction that times out, with a capped retry count, before allowing the screening workflow to proceed to a final determination
4. **Multi-Jurisdiction Candidate Flagging**: Route candidates with more than one listed residency jurisdiction through a stricter completion check given their higher likelihood of triggering a partial vendor response

### Metrics
- Rate of "background check clear" determinations later found, on audit, to have had at least one jurisdiction with a non-definitive (timeout/partial) status at the time of the determination
- Average time-to-completion for multi-jurisdiction background checks, broken out by whether all jurisdictions returned on the first request or required retry
- Rate of background-check API responses with partial-batch status, by jurisdiction

### Alerts
- A "background check clear" summary is generated while one or more requested jurisdictions still show a timeout or partial status in the underlying API response → P1
- A candidate advances to offer stage with an unresolved jurisdiction timeout on file → P2
- Partial-batch response rate from the background-check vendor exceeds the defined threshold for a rolling window → P3

---

## References

- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735)
