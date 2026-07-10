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

### Prevention

1. **Mandatory pagination-exhaustion protocol with completeness verification gates**: On every docket/document API call: (a) check response for pagination indicators (continuation_token, has_more, next_page_url, page_count, total_count), (b) if any indicator present, implement pagination loop: keep following continuation tokens until has_more=false or no next_token exists, (c) after all pages retrieved, reconcile: retrieved_count vs. total_count (if both present, verify they match; if mismatch, flag as INCOMPLETE and require human review), (d) output result only after completeness confirmed, with metadata tag {completeness: COMPLETE, total_entries_retrieved: X, pages_queried: Y}, (e) if pagination fails or max-retry limit hit, output result as INCOMPLETE and block any legal conclusion from relying on it. Root cause: Ensures agent cannot mistake a partial result for complete by enforcing exhaustive pagination.

2. **Hard-stop gate on legal conclusions from unconfirmed-complete results**: Implement conclusion-blocking rule: any statement the agent attempts to make about "no prior X exists", "docket does not reflect Y", "case history contains Z" must reference the completeness tag from the docket pull. If completeness != COMPLETE, block the statement with escalation message: "Cannot make definitive docket-based conclusions from partial result. Please confirm complete docket pull or note in output: 'based on partial docket retrieval, may be incomplete.'" Root cause: Prevents unqualified legal claims from partial data.

3. **Total-count reconciliation with entry-level validation**: For each docket pull, log: {query_params, pages_retrieved, total_count_from_api, actual_entries_retrieved, reconciliation_status (MATCH|MISMATCH)}. If mismatch: (a) flag for human review, (b) require secondary docket-API call using different pagination mechanism or manual confirmation, (c) only proceed with MATCH status. For high-volume cases (>100 entries), validate by category: ensure all categories of filings (motions, decisions, briefs) are represented across pages (not concentrated in first page), spot-check 10% of entries across first/middle/last pages for consistent data quality. Root cause: Catches systematic truncation or API errors before legal reliance.

### Detection & Response

1. **API-response audit logging with completeness tracking**: For each docket/document API call, log: {call_id, case_id, query_type, api_response_status, pagination_indicator_present (Y/N), continuation_token_present (Y/N), total_count_field_present (Y/N), total_count_value, pages_retrieved, entries_retrieved, completeness_confirmed (Y/N), completeness_tag_applied (Y/N), downstream_conclusion_attempted (Y/N)}. Daily audit: sample 20% of calls, verify: (a) if pagination_indicator_present=true, then pages_retrieved > 1 (or documented reason why single page was sufficient), (b) if total_count_field present, then entries_retrieved == total_count, (c) if conclusion_attempted, then completeness_confirmed=true. Alert if: >5% of sampled calls have unconfirmed completeness, or >10% have pagination indicators but only 1 page retrieved.

2. **Docket-based-conclusion audit with contradiction detection**: Track all legal conclusions derived from docket pulls. When new docket entries become available or when opposing counsel cites entries the agent missed, flag as contradiction. Trigger investigation: (a) was the original docket pull marked COMPLETE? (b) if yes but entries exist outside original pull, investigate API failure or timing issue, (c) if original was INCOMPLETE, verify original output carried appropriate caveat. Maintain trend dashboard: "Docket-based contradictions by case type, date range" to identify patterns.

### Architecture Patterns

1. **Pagination-Exhaustion Engine with Completeness Verification**: Docket API query → Collect first response → Check pagination indicators → If pagination present, loop pagination_handler: fetch next page, append to results, repeat until has_more=false → After loop, verify total_count reconciliation → Output result with completeness_tag. If API fails mid-pagination or max retries hit, output INCOMPLETE status + already-retrieved data.

2. **Conclusion Blocker with Completeness Gate**: When agent attempts to formulate statement about docket ("no motion exists", "docket shows"), intercept and check completeness_tag from underlying docket_pull. If INCOMPLETE, generate advisory message inserted into output: "[Note: Based on partial docket retrieval (X of Y total entries retrieved). Full docket pull may reveal additional entries.]" If user continues with unqualified claim despite advisory, escalate to attorney reviewer.

3. **API-Response Validator with Heuristic Reconciliation**: Validates API responses for completeness signals. Maintains registry of known API pagination behaviors (PACER court docket, Westlaw API, etc.) and expected response shapes. When response received, runs reconciliation: page_count field, total_count field, continuation_token presence, entry count consistency. Flags anomalies (e.g., single page but total_count=200) for investigation.

### Key Metrics

| Metric | Target | Alert Threshold | Measurement Method |
|--------|--------|-----------------|--------------------|
| Pagination-Exhaustion Compliance | 100% | <99% | # of paginated API responses where all pages were retrieved / total responses with pagination indicators present |
| Total-Count Reconciliation Pass Rate | 100% | <99% | # of docket pulls where entries_retrieved == total_count (or explained mismatch) / total pulls with total_count field |
| Completeness Confirmation Rate | 100% | <99% | # of docket pulls marked COMPLETE (all pages exhausted, count reconciled) / total docket pulls used in legal conclusions |
| Unconfirmed-Conclusion Blocking Rate | 100% | <95% | # of incomplete-docket-based conclusions blocked from output / total conclusions attempted on unconfirmed-complete results |
| Docket-Based-Conclusion Contradiction Rate | 0% | >0.5% | # of legal conclusions contradicted by subsequently discovered docket entries / total docket-based conclusions made (audited via opposing counsel citations, human attorney review) |

### Alerts & Escalation

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Unaddressed Pagination Indicator | API response contains continuation_token or has_more=true but agent attempts to use result without completing pagination | CRITICAL | Block downstream conclusion; require agent to complete pagination loop and reconcile total_count; re-query and re-process |
| Total-Count Mismatch | Retrieved entries do not match API's total_count field | CRITICAL | Mark result as INCOMPLETE; block any legal conclusion from this docket pull; require manual verification or secondary API call |
| Conclusion on Unconfirmed-Complete Docket | Agent outputs "no prior motion exists" or similar statement without completeness_tag=COMPLETE from underlying docket pull | HIGH | Escalate to attorney; require advisory note: "Based on partial docket; full history may contain additional entries"; may require redraft after complete docket pull |
| Pagination Loop Timeout/Failure | Agent exceeds max_retries while attempting to follow continuation tokens | HIGH | Output result as INCOMPLETE; surface error message to attorney; recommend manual docket verification before reliance |
| Post-Conclusion Docket Contradiction | Subsequent docket entry discovered that contradicts prior agent conclusion ("no prior motion on X exists") | CRITICAL | Audit all conclusions from that docket pull; investigate whether original pull was incomplete or API changed; assess whether conclusion-reliant work products (briefs, motions) require amendment |

---

## References

- [From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents](https://arxiv.org/html/2606.09863)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf)
