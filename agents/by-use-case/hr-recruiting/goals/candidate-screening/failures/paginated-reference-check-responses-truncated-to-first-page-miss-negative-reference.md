# Paginated Reference-Check Responses Truncated to First Page Miss Negative Reference

## Issue: A Candidate-Screening Agent Calling a Reference-Check Service's API to Compile All Submitted References for a Candidate Receives Only the First Page of a Multi-Page Response and Treats It as the Complete Set, Producing a Favorable Screening Recommendation That Omits a Negative Reference Contained Only in a Later, Unretrieved Page

**Frequency**: Occasional

**Symptoms**
- The agent's screening summary states "all N references reviewed, consistently positive" while the reference-check API's response metadata for that call shows a result count lower than the candidate's actual total submitted references
- The agent never issues a follow-up call using the response's pagination cursor or offset parameter, even though the API's documentation specifies a page-size cap below the number of references many candidates submit
- When the full reference set is manually retrieved by exhausting all pages, a reference contained only on a later page raises a specific concern (performance, conduct, rehire eligibility) that materially changes the recommendation
- The same candidate's reference count, if re-queried weeks apart, surfaces a different first-page ordering depending on submission timestamp sort order, meaning the same negative reference is sometimes captured and sometimes missed purely by chance of where it falls in the unretrieved pages
- No log entry shows the agent's reasoning ever acknowledging an unretrieved page existed, consistent with the omission being a silent completeness gap rather than a deliberate decision to exclude a reference

**Example**
```
Candidate submits five references through the reference-check vendor's portal; the vendor's API returns reference results in pages of three
Candidate-screening agent calls the reference-check API and receives page 1 of 2, containing three positive references, with a response field indicating two additional records exist
Agent does not issue the follow-up call for page 2 and generates a screening summary stating "reference checks complete, all reviewers describe candidate positively, recommend proceeding to offer"
Page 2, never retrieved, contains a reference from the candidate's most recent manager describing a performance improvement plan that was in progress at the time the candidate left
Hiring team proceeds to offer based on the agent's "all positive" summary
Performance concern surfaces only after the candidate starts, when a new manager requests the complete reference file and discovers the unretrieved second-page reference for the first time
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| LLM agents frequently treat a single tool call's returned result as complete and propagate that incomplete state into downstream decisions, with the originating root-cause error cascading through later reasoning steps unless explicitly traced and isolated | [Where LLM Agents Fail and How They can Learn From Failures](https://arxiv.org/abs/2509.25370) |
| Agent failure taxonomies identify incomplete or partial tool-call results as a distinct system-level failure category, separate from reasoning or planning failures, because the agent's downstream behavior is correct given what it received but the received data was itself incomplete | [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933) |
| Agent-environment interaction research notes that agents frequently fail to recognize when an environment's response is partial rather than exhaustive, treating any successfully-returned response as the full answer regardless of pagination or result-set-size signals present in that same response | [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504) |

**Contributing Factors**
- The agent's tool-calling logic treats a successful API response as a complete answer rather than checking response metadata fields like total-record counts or pagination cursors before finalizing a recommendation
- The reference-check vendor's default page size is below the number of references candidates commonly submit, making truncation routine rather than exceptional
- No deterministic wrapper enforces pagination exhaustion for the reference-check tool call before control returns to the agent's reasoning step
- The agent's prompt frames the task as "summarize the candidate's references" without an explicit requirement to confirm the retrieved count matches the total submitted count before summarizing

---

## Mitigation Strategies

1. **Deterministic Pagination Wrapper**: Wrap the reference-check tool call in non-LLM code that automatically follows pagination cursors until exhausted, returning a single concatenated, complete result set to the agent
2. **Mandatory Count-Match Check**: Require the agent to compare retrieved-reference count against the candidate's total-submitted-reference count before issuing any "all references reviewed" statement, and to explicitly flag and halt if the counts do not match
3. **Negative-Signal-Weighted Completeness Gate**: Require that any reference summary disclose the number of references reviewed out of the number submitted, so a hiring manager can see at a glance whether the recommendation covers the full set
4. **Random-Sample Completeness Audit**: Periodically re-run a sample of completed reference-check sessions with forced full pagination and compare the resulting summary to what the agent originally reported, flagging any session where a previously unsurfaced concern appears

### Metrics
- Percentage of reference-check summaries issued while retrieved-reference count is less than total-submitted count
- Average ratio of references retrieved to references submitted across all candidate reference checks
- Number of post-hire performance or conduct concerns traced back to a reference missed due to truncated pagination

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Reference summary issued on truncated set | Agent finalizes a "references reviewed" summary while retrieved count is less than total-submitted count | P1 | Block the summary from reaching the hiring team until full pagination completes and the summary is regenerated |
| Pagination wrapper bypass detected | A reference-check call completes without the deterministic pagination wrapper being invoked | P2 | Route the session to engineering review; treat any output from that session as unverified |
| Completeness audit surfaces missed concern | Forced-full-pagination re-run surfaces a reference concern absent from the original agent summary | P1 | Escalate to the hiring manager and recruiting lead immediately, regardless of where the candidate is in the pipeline |

---

## References

- [Where LLM Agents Fail and How They can Learn From Failures](https://arxiv.org/abs/2509.25370)
- [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933)
- [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504)
