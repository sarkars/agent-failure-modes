# Partial Rank-Tracking API Response Treated as Confirmed No-Cannibalization Result

## Issue: An SEO Agent's Call to a Rank-Tracking or Site-Search-Console Tool, Made to Confirm a Newly Drafted Page Will Not Cannibalize an Existing Page's Rankings for the Same Target Keyword, Times Out or Returns a Partial Result Covering Only Some of the Queried Keywords, and the Agent Reports the Cannibalization Check as Passed Rather Than Flagging the Response as Incomplete

**Frequency**: Occasional

**Symptoms**
- Agent's summary states "no ranking overlap detected" or "cannibalization check passed" immediately after a tool call whose raw response covers fewer keywords than were requested
- The tool's own response payload includes a partial-result, pagination, or timeout indicator that is present in the trace but never referenced in the agent's summary
- Pages later found to be splitting rankings and traffic with an existing page on the site had been cleared by an agent-run cannibalization check shortly before publication
- Re-running the same check with the full, non-truncated result set reveals the omitted keywords were exactly the ones with overlapping rankings
- The gap is only caught when an editor manually re-runs the rank check after noticing traffic anomalies post-publication

**Example**
```
Agent drafts a new page targeting "best budget noise-cancelling headphones" and calls the rank-tracking API to check whether
any existing site page already ranks for this term or close variants
The API call requests rankings for 12 keyword variants but times out after returning data for the first 7; the response
payload includes a "partial: true, returned: 7/12" field
Agent's summary to the editor: "Ran cannibalization check against existing content -- no overlapping rankings found, safe to publish"
The new page is published; two weeks later analytics show it competing directly with an existing page for "best cheap
noise cancelling headphones," one of the 5 keyword variants never returned by the timed-out call
Editor pulls the tool trace and finds the "partial: true" flag was present in the raw response the entire time
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Tool-use error detection research finds agents frequently fail to surface partial, truncated, or error-flagged tool results as a distinct condition, instead proceeding as though a complete, successful result had been returned | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Execution-provenance research argues that without explicit tracing linking an agent's stated conclusion back to the actual tool output it relied on, reviewers cannot verify whether a "check passed" claim corresponds to a complete result or a degraded one | [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1) |
| Survey work on agent hallucination documents a pattern of agents producing confident summary claims that outrun what the underlying tool evidence actually supports, particularly when that evidence is incomplete | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |

**Contributing Factors**
- The agent's summarization step compresses the tool response into a pass/fail statement without first checking the response's own completeness metadata
- No explicit instruction requiring the agent to treat a partial or timed-out result as a distinct "check inconclusive" outcome rather than a pass
- The cannibalization check is run once, late in the drafting pipeline, with no automatic retry on partial results before the agent reports back
- Editors reviewing the agent's summary have no easy way to see the underlying tool response without separately pulling the trace, so the gap between "tool returned partial data" and "agent reported pass" goes unnoticed

---

## Mitigation Strategies

1. **Completeness Gate on Tool Summaries**: Require the agent to check the tool response's own completeness/partial-result indicator before generating any pass/fail summary, and to report "inconclusive -- partial data" rather than "passed" when the indicator is set
2. **Automatic Retry on Partial Result**: Configure the rank-tracking tool call to automatically retry or re-page on a partial/timeout response before the agent is allowed to summarize the result
3. **Surface Raw Completeness Status to Reviewers**: Include the tool response's coverage ratio (e.g., "7/12 keywords returned") directly in the editor-facing summary, not just the agent's pass/fail conclusion
4. **Block Publication on Inconclusive Check**: Treat an inconclusive cannibalization check as a hard publication blocker requiring a successful re-run, rather than a soft warning the pipeline can proceed past

### Metrics
- Rate of cannibalization checks where the underlying tool response was partial/timed-out but the agent's summary reported a pass
- Number of published pages later found to cannibalize existing rankings that had passed an automated check
- Average completeness ratio (keywords returned / keywords requested) across rank-tracking calls

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Pass reported on partial tool data | Agent summary states check passed while underlying tool response has partial/timeout flag set | P1 | Block publication; force re-run of cannibalization check |
| Repeated tool timeouts | Rank-tracking tool returns partial results above a rolling-window threshold rate | P2 | Investigate tool reliability; raise timeout or reduce batch size |
| Post-publication cannibalization detected | Analytics show new page splitting rankings with existing page within 30 days of publish | P2 | Audit pre-publication check trace for missed partial-result flag |

---

## References

- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
