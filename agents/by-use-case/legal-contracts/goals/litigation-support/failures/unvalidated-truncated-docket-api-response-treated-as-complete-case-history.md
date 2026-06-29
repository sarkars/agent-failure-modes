# Unvalidated Truncated Docket API Response Treated as Complete Case History

## Issue: A Litigation-Support Agent Calling a Court Docket or Document-Management API to Retrieve the Full Filing History for a Case Receives a Paginated or Length-Capped Response Covering Only Part of the Docket, and Proceeds to Summarize, Cite, or Build a Production/Privilege Determination on That Partial Result as if It Were the Complete Case Record, Without Checking the Response for a Continuation Token, Total-Count Field, or Other Indicator That Additional Pages Existed

**Frequency**: Common

**Symptoms**
- Case-history summary or privilege log omits entries that exist later in the docket, because the API response used to build it stopped at a page or length boundary the agent did not detect
- The tool response itself contains a `next_page_token`, `has_more: true`, or total-count field indicating more results exist, but the agent's summary or determination proceeds without querying further or surfacing the incompleteness to the requesting attorney
- A motion or brief citing "the docket reflects no prior motions on this issue" is later contradicted when a human reviewer or opposing counsel points to an earlier-filed motion that existed in a later page of the same docket query
- Re-running the identical API call with explicit pagination handling (following every continuation token until the response indicates no further pages) returns additional entries the original summary omitted, confirming the gap was a retrieval-completeness failure rather than a genuine absence of those entries
- The failure recurs specifically on cases with high filing volume (lengthy multi-year litigation, multi-party actions), since those are the cases most likely to exceed a single page or length-capped response

**Example**
```
Litigation-support agent is asked to confirm whether a motion to compel has previously been filed in a long-running case before drafting a new one
Agent calls the court's docket API, which returns the first 50 of 187 total docket entries along with a "has_more": true field and a continuation token
Agent's response, built directly from the 50 returned entries, states "no prior motion to compel appears in the docket" and the drafting agent proceeds to draft a new motion on that basis
Opposing counsel's response brief points out that a motion to compel on the identical issue was filed and denied 14 months earlier, appearing on docket entry 142 -- well past the 50 entries the agent's API call actually returned
Re-running the docket query while following the continuation token through all pages surfaces the earlier motion immediately; the original 50-entry response had clearly indicated more results were available via its has_more field, which the agent's summary never checked
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| LLM agents frequently assert task completion (here, "no prior motion exists") based on the apparent shape of a returned result rather than verifying the result reflects the complete underlying state, a pattern documented as false success driven by surface-level closing signals rather than ground-truth verification | [From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents](https://arxiv.org/html/2606.09863) |
| Tool-use error detection research finds agents frequently fail to treat an incomplete, capped, or paginated tool result as a distinct error condition requiring follow-up, instead generating output as if a complete result had been returned | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Legal RAG hallucination research documents that incomplete retrieval over case-law or docket sources is a distinct contributor to unsupported legal claims, independent of the generation model's own reasoning quality | [Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) |

**Contributing Factors**
- No explicit instruction or guardrail requires the agent to check a tool response for pagination or completeness indicators (continuation tokens, total-count fields, `has_more` flags) before treating it as the full record
- High-filing-volume cases are exactly the cases most likely to need a docket-history check before drafting a new motion, and also the cases most likely to exceed a single page of API results, compounding the risk
- The agent's output does not visibly distinguish a determination based on a confirmed-complete record from one based on a possibly-partial result, so reviewers cannot tell which conclusions rest on full data
- Pagination-handling logic is treated as a generic engineering concern rather than a legal-accuracy-critical control, so it is not consistently enforced across every docket or document-API integration the agent uses

---

## Mitigation Strategies

1. **Mandatory Completeness Check Before Use**: Require the agent to check every paginated or length-capped tool response for a continuation token, `has_more` flag, or total-count field, and to follow pagination to exhaustion (or explicitly flag the result as partial) before using the result in any summary, citation, or drafting decision
2. **Hard Stop on Unconfirmed Completeness**: Block any downstream legal conclusion ("no prior motion exists," "docket reflects X") that is not explicitly tagged as derived from a confirmed-complete record
3. **Total-Count Reconciliation**: Require the agent to compare the number of entries actually retrieved against any total-count field in the API response and treat a mismatch as a hard stop requiring further pagination, not a result to summarize as-is
4. **Confirmed-Complete Labeling in Output**: Require any docket-derived determination presented to an attorney to state explicitly whether it rests on a confirmed-complete docket pull or a partial one, so reviewers can immediately judge reliability

### Metrics
- Rate of docket/document API calls where the agent's summary was built from a response containing an unaddressed pagination or completeness indicator
- Number of legal conclusions later contradicted by docket entries that existed outside the originally retrieved page
- Percentage of docket pulls that included an explicit completeness confirmation before being used in drafting

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Unaddressed pagination indicator | Tool response contains a continuation token or has_more flag with no evidence of follow-up pagination before use | P1 | Block downstream drafting reliance on the result; re-query to completion |
| Total-count mismatch | Retrieved entry count does not match the response's total-count field | P1 | Treat result as incomplete; re-query before any legal conclusion is drawn |
| Conclusion drawn from unconfirmed-complete record | Drafting or summary output lacks an explicit completeness confirmation tag | P2 | Flag for attorney review before filing or sending |

---

## References

- [From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents](https://arxiv.org/html/2606.09863)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf)
