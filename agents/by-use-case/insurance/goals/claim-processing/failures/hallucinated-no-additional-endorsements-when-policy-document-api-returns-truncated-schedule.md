# Hallucinated "No Additional Endorsements" When Policy-Document API Returns Truncated Schedule

## Issue: A Claims-Processing Agent's Call to the Policy-Document Retrieval API Returns a Truncated Endorsement Schedule Due to Pagination, and Instead of Flagging the Retrieval as Incomplete, the Agent Concludes No Additional Endorsements Apply and Approves Payment Without Applying an Existing Sublimit Endorsement

**Frequency**: Occasional

**Symptoms**
- A claim is approved and paid at the full policy limit, even though the policy file contains a sublimit endorsement for that specific peril that should have capped the payout, because the endorsement was on a page of the schedule the retrieval call never reached
- The claims-processing agent's summary states "no additional endorsements apply to this claim," but the underlying policy-document API response shows a pagination cursor indicating additional endorsement-schedule pages were never retrieved
- Asking the agent to show its source for the "no additional endorsements" conclusion surfaces a raw API response covering only the first page of the endorsement schedule, with no indication the agent checked for further pages
- The miss concentrates on policies with longer endorsement schedules, since those are the ones most likely to span multiple pages and trigger a pagination cutoff
- Re-running the same retrieval and explicitly paging through the full schedule surfaces the sublimit endorsement the original claim approval missed

**Root Cause**
The claims-processing agent's summarization step concludes "no additional endorsements apply" from whatever portion of the endorsement schedule the policy-document API returned, without checking whether a pagination cursor indicated further pages remained unretrieved. Because a truncated first page and a complete single-page schedule are both well-formed, populated responses, the agent's natural-language summarization treats the truncated page as the complete schedule rather than treating an unresolved pagination cursor as a hard stop requiring further retrieval before a "no additional endorsements" conclusion is reached.

**Example**
```
Claim is filed for water damage under a commercial property policy with an eleven-page endorsement schedule
Claims-processing agent calls the policy-document API to check for applicable endorsements; the API returns the first three pages along with a pagination cursor for the remaining eight pages, then the call is not continued
Agent concludes "no additional endorsements apply to this claim" based on the three pages retrieved and approves payment at the full policy limit
A water-damage sublimit endorsement on page seven of the schedule, which the agent never retrieved, caps this specific peril at a lower amount
Claim is overpaid relative to the actual policy terms, an error caught only during a later audit
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Tool-use agents frequently fail to distinguish a tool call that returned a partial or paginated result from one that returned a complete result, producing confident downstream conclusions from incomplete data | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Surveys of LLM agent hallucination identify completion of a plausible negative conclusion ("nothing further applies") from incomplete tool or retrieval output as a distinct and recurring failure category | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Hierarchical multi-agent healthcare and claims-adjacent safety research identifies incomplete document retrieval, where a downstream agent acts on a partial document set without verifying completeness, as a recurring source of decision error | [Tiered Agentic Oversight: A Hierarchical Multi-Agent System for Healthcare Safety](https://arxiv.org/pdf/2506.12482) |

**Contributing Factors**
- The policy-document API's paginated response format does not force the calling agent to check for a remaining pagination cursor before concluding the endorsement schedule has been fully reviewed
- No mandatory rule requires the claims-processing agent to confirm full pagination completion before generating a "no additional endorsements" conclusion that affects payout
- Policies with longer endorsement schedules, the ones most likely to trigger a pagination cutoff, are not flagged for a stricter completion check despite being the highest-risk case for a missed sublimit

---

## Mitigation Strategies

1. **Pagination Completion Gate Before Payout Conclusion**: Require the agent to confirm the policy-document API's pagination cursor is exhausted before generating any "no additional endorsements apply" conclusion that affects claim payout
2. **Structural Distinction Between Partial and Complete Schedule Retrieval**: Modify the policy-document integration so a partial or paginated retrieval is surfaced to the agent as a distinct status that cannot be summarized as a complete endorsement review
3. **Mandatory Retry on Pagination Timeout**: Automatically continue paginated retrieval, with a capped retry count, before allowing the claims workflow to proceed to a payout conclusion
4. **Endorsement-Schedule-Length Flagging**: Route claims on policies with longer endorsement schedules through a stricter completion check given their higher likelihood of triggering a pagination cutoff before a sublimit is reached

### Metrics
- Rate of "no additional endorsements apply" conclusions later found, on audit, to have been generated from a policy-document retrieval with an unresolved pagination cursor at the time of the conclusion
- Rate of claim overpayments traced to a missed sublimit or exclusion endorsement that existed on an unretrieved page of the schedule
- Rate of policy-document API responses with an unresolved pagination cursor, by endorsement-schedule length

### Alerts
- A "no additional endorsements apply" conclusion is generated while the underlying policy-document retrieval still shows an unresolved pagination cursor → P1
- A claim is approved for payment with a known-incomplete endorsement-schedule retrieval on record → P1
- Partial-pagination rate from the policy-document API exceeds the defined threshold for a rolling window → P3

---

## References

- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [Tiered Agentic Oversight: A Hierarchical Multi-Agent System for Healthcare Safety](https://arxiv.org/pdf/2506.12482)
