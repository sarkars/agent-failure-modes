# Paginated Comparable-Offer History Truncated to First Page Understates Counter-Offer Pattern

## Issue: An Offer-Generation Agent Calling an Internal Comparable-Offers API to Benchmark a Candidate's Counter-Request Against Recent Offers for the Same Role and Level Receives Only the First Page of Results Because It Never Issues the Follow-Up Paginated Calls, Then Generates a Final Counter-Offer Recommendation as If That First Page Were the Complete Set of Recent Comparables

**Frequency**: Occasional

**Symptoms**
- The agent's recommendation cites "recent comparable offers for this level" but the underlying API call's response metadata shows a `next_page_token` or `has_more: true` field that was never followed up on
- Counter-offer recommendations skew toward whatever offers happen to sort first from the comparable-offers API (commonly the oldest or alphabetically-first records), rather than the most recent or most relevant set
- The same candidate level and role, queried on different days, produces materially different "all recent comparables" recommendations depending solely on how the API happened to order the first page that day
- When the same query is manually re-run with all pages explicitly concatenated, the comparable set is two to four times larger than what the agent treated as complete, and the larger set shifts the recommended counter-offer band
- No log entry shows a second or third page request to the comparable-offers endpoint for any session, even though the endpoint's own documentation caps page size well below the actual number of recent offers at most levels

**Example**
```
Hiring manager asks the offer-generation agent to benchmark a senior engineer candidate's counter-request of $185K against recent comparable offers at the same level
Agent calls the comparable-offers API, which returns page 1 of 3 (25 of approximately 68 matching records) along with a has_more: true flag and a next_page_token
Agent does not issue a follow-up call for page 2 or 3, and proceeds to summarize "based on 25 recent comparable offers, the median is $171K, making the $185K request 8% above market"
Actual full dataset across all three pages has a median of $179K, because the unretrieved pages contain a cluster of more recent, higher offers extended after a comp-band adjustment two months prior
Recommendation understates the appropriate counter, and the hiring manager pushes back harder on the candidate's ask than the complete data would have supported
Candidate declines the under-market counter and accepts a competing offer; post-mortem reveals the agent only ever saw the first of three result pages
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| LLM agents frequently treat a single tool call's returned result as complete and propagate that incomplete state into downstream decisions, with the originating root-cause error cascading through later reasoning steps unless explicitly traced and isolated | [Where LLM Agents Fail and How They can Learn From Failures](https://arxiv.org/abs/2509.25370) |
| Agent failure taxonomies identify incomplete or partial tool-call results as a distinct system-level failure category, separate from reasoning or planning failures, because the agent's downstream behavior is correct given what it received but the received data was itself incomplete | [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933) |
| Agent-environment interaction research notes that agents frequently fail to recognize when an environment's response is partial rather than exhaustive, treating any successfully-returned response as the full answer regardless of pagination or result-set-size signals present in that same response | [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504) |

**Contributing Factors**
- The agent's tool-calling logic treats a successful (200-status) API response as a complete answer rather than checking response metadata fields like `has_more` or `next_page_token` before finalizing an answer
- The comparable-offers API's default page size is well below the typical number of matching records at common levels, making truncation the normal case rather than an edge case
- No deterministic wrapper around the comparable-offers tool call enforces pagination exhaustion before returning control to the agent's reasoning step
- The agent's prompt frames the task as "summarize recent comparable offers" without an explicit instruction or schema requirement to confirm the full result set was retrieved before summarizing

---

## Mitigation Strategies

1. **Deterministic Pagination Wrapper**: Wrap the comparable-offers tool call in non-LLM code that automatically follows `next_page_token` / `has_more` until exhausted, and only returns a single concatenated result set to the agent, removing pagination handling from the model's responsibility entirely
2. **Explicit Completeness Field in Tool Response**: Require the comparable-offers tool to return a `total_count` alongside `returned_count`, and have the agent's prompt require an explicit check that `returned_count == total_count` before treating the data as final
3. **Mandatory Result-Count Disclosure**: Require every comparable-offer benchmarking output to state the number of records the recommendation was based on and the number of records that existed in the underlying dataset, so under-sampling is visible to the reviewing hiring manager
4. **Random-Sample Completeness Audit**: Periodically re-run a sample of completed offer-benchmarking sessions with forced full pagination and compare the resulting median/band to what the agent originally reported, flagging sessions where the discrepancy exceeds a defined threshold

### Metrics
- Percentage of comparable-offer benchmarking calls where `returned_count` is less than `total_count` at the time the agent generates its recommendation
- Average ratio of records retrieved to records available across all comparable-offer queries
- Number of offer recommendations later found to be based on a truncated first page during completeness audits

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Truncated comparable set used in recommendation | Agent finalizes a counter-offer recommendation while `returned_count < total_count` on the comparable-offers call | P1 | Block the recommendation from being sent to the hiring manager until full pagination completes and the benchmark is regenerated |
| Pagination wrapper bypass detected | A comparable-offers call completes without the deterministic pagination wrapper being invoked | P2 | Route the session to engineering review; treat any output from that session as unverified |
| Completeness audit discrepancy | Forced-full-pagination re-run produces a median or band shift greater than 5% versus the original agent output | P2 | Notify the hiring manager who received the original recommendation and offer to re-benchmark |

---

## References

- [Where LLM Agents Fail and How They can Learn From Failures](https://arxiv.org/abs/2509.25370)
- [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933)
- [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504)
