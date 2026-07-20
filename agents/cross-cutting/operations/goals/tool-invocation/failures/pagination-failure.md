# Pagination Failure

## Issue: Agent Reads Only the First Page of a Paginated or Length-Capped Tool Response and Proceeds as if That Page Were the Complete Result Set

An agent calls a tool or API that returns results in pages, or caps a single response at a fixed row/record count, and the response includes an explicit completeness signal (`has_more`, a `next_page_token`/continuation cursor, or a `returned_count` vs. `total_count` mismatch) that the agent's reasoning never inspects. The agent treats the first page as exhaustive and generates a downstream conclusion, summary, or decision that depends on completeness — "no prior tickets," "all references reviewed," "batch fully validated," "no prior motion on this issue" — when the true answer lives partly or entirely on an unretrieved page. This is a single underlying mechanism (a completeness signal present in the tool's own response but never checked before the agent commits to a conclusion) that recurs across essentially every domain with a paginated lookup or search tool; the domain-specific consequence differs (a missed negative reference, an understated counter-offer, a stale price treated as fresh, a missed prior court filing), but the failure and its fix are identical.

**Frequency**: Common

**Symptoms**
- The tool's raw response includes `has_more: true`, a `next_page_token`/continuation cursor, or a `returned_count` lower than a known `total_count`/`requested_count`, but the agent's reasoning and output make no reference to it
- The agent's summary asserts a negative or exhaustive claim ("no prior X," "all N reviewed," "complete history") that is only true of the first page, not the full result set
- No follow-up tool call using the pagination cursor/offset appears in the session log, even when the API's documented page size is well below the typical size of the underlying data
- Re-running the same lookup to exhaustion (following every page) surfaces a materially different answer than the agent originally reported
- The rate of this failure correlates with default page size relative to typical result-set size — customers, cases, or records with larger-than-average history are disproportionately affected, since they are the ones most likely to exceed page one

## Root Cause
Pagination and length-capping exist so that a single tool call doesn't return unbounded data, and well-designed APIs surface an explicit signal (a boolean flag, a cursor, or a count mismatch) indicating more data exists. That signal is data in the tool's response payload, not a separate alert — nothing forces the agent to read it, and prompt templates that inject "the returned items" into the agent's context frequently drop the surrounding metadata (has_more, total count) along the way, leaving the agent with only the items themselves and no structural indication they're incomplete. Because the returned page is real, well-formed data, and the agent's summarization is fluent, the output looks indistinguishable from a genuinely complete answer to anyone downstream who doesn't re-check the raw tool-call log — the gap is invisible unless something forces a completeness check before the conclusion is finalized.

## Example
```
A support agent calls get_ticket_history(customer_id) to check whether a
customer's complaint is a first-time report or a repeat issue.

The API returns the 10 most recent tickets (page 1 of 3) along with
has_more: true, but the prompt template that injects the tool result
into the agent's context surfaces only the ticket list itself, not the
pagination metadata.

The agent concludes "I don't see any prior tickets about this issue"
and offers a standard first-time-issue script. Tickets 14 and 22, on
the unretrieved page 2, show the customer reported the identical issue
twice before and was promised an escalation.

The customer, contacting support a third time, says "I've already told
you this twice" -- which the agent has no record of, because it only
ever read page one.
```

### Domain Examples
The same mechanism recurs with different nouns across at least these domains, each previously documented as a separate by-use-case pattern before being consolidated here:
- **HR / candidate screening**: a reference-check API returns page 1 of 2; the unretrieved page 2 contains a negative reference from the candidate's most recent manager, and the agent's "all reviewers positive" summary drives an offer that shouldn't have been extended as-is.
- **HR / offer generation**: a comparable-offers API returns 25 of ~68 matching records; the unretrieved pages contain a cluster of more recent, higher offers, and the agent's benchmark understates the appropriate counter-offer by ~5%, contributing to a declined offer.
- **Financial services / market-data freshness**: a batch price API returns 1,000 of 1,200 requested instruments; the 200 omitted instruments are silently absent rather than flagged unchecked, and a three-day-stale price on one of them is carried into end-of-day NAV uncaught.
- **Financial services / data quality**: a reference-data batch-validation query returns 6,500 of 8,000 submitted records but the agent's certification claims "8,000 records reviewed"; a misclassified security among the 1,500 never-checked records later drives an unexplained exposure-limit breach.
- **Legal / litigation support**: a court docket API returns the first 50 of 187 entries; a prior motion to compel on entry 142 is missed, and the agent proceeds to draft a duplicate motion that opposing counsel then points out was already filed and denied.
- **Sales / deal management**: a deal-activity-history API returns the 50 most recent records; an open pricing hold recorded further back is missed, and a renewal quote goes out that contradicts a promise already made to the customer.

## Statistics
| Finding | Context |
|---|---|
| Agent-environment interaction failure research documents agents proceeding to downstream conclusions based on an environment response that does not actually confirm the requested state, including treating a partial/paginated result as exhaustive | Aegis: Agent-Environment Failures, and Failure Modes in LLM Systems taxonomies (both cited across the domain instances of this pattern) |
| The failure recurs across at least six independently-documented domains (support, HR screening, HR compensation, financial market data, financial data quality, legal, sales) with an identical root cause and mitigation set, differing only in the paginated resource and the downstream decision affected | Consolidated from prior domain-specific pattern authorship in this repository |
| Failure rate is disproportionately concentrated on records/customers/cases whose true result count exceeds a single page — i.e. the paginated case is the harder case, and it is exactly the case most likely to be truncated | Structural to how pagination limits interact with real-world data-volume distribution |

## Mitigations
1. **Mandatory Pagination Loop**: The retrieval wrapper never returns a single page to the agent as "the result"; it auto-follows `next_page_token`/`cursor`/`has_more` until exhaustion (or an explicit cap) and returns the fully assembled set, so the agent never has the option to stop after page one.
2. **Total-Count Pre-Check**: Before iterating, the wrapper reads the total-result-count/total-pages field when the API exposes one, and asserts that the number of records ultimately collected matches it; mismatches raise an error before the agent uses the data.
3. **Explicit Completeness Contract in Tool Interface**: The tool's return schema includes a `complete: bool` and `pages_fetched`/`total_pages` field; agent prompts and downstream logic are required to check `complete == true` before treating a listing as exhaustive, making incompleteness visible rather than implicit.
4. **Pagination-Aware Context Injection**: Always surface pagination metadata (`has_more`, total count, current page) into the agent's reasoning context alongside the returned items, not just the item list itself — the recurring root cause across every domain instance of this pattern is that metadata gets dropped before the agent ever sees it.
5. **Completeness-Dependent-Claim Gate**: For any determination that depends on a complete result set (repeat-issue status, "no prior X," full benchmark, full portfolio check), require a non-LLM check comparing retrieved count against a known total before the agent is allowed to state an exhaustive or negative conclusion.

### Detection & Response
1. **Truncation Flag Monitoring**: Every paginated call logs whether `has_more`/`next_cursor` was still set when the agent's reasoning step consumed the data; any case where the agent proceeded with `has_more=true` unaddressed is flagged as a pagination-failure incident.
2. **Result-Count vs. Expected-Count Reconciliation**: Where the source system exposes a total record count, the sum of records actually retrieved is checked against it after each session; discrepancies trigger an automatic re-fetch and an incident log entry.
3. **Downstream Undercount Complaints**: User reports of "missing records" or "I know there are more" are tagged as a distinct category and cross-referenced against session logs for unresolved `has_more` flags to confirm pagination as the root cause versus a data issue.

### Architecture Patterns
1. **Auto-Paginating Client Wrapper**: All list/search tools are wrapped by a client library that transparently follows cursors/page tokens up to a safety cap (e.g., 10,000 records or 50 pages) and returns one assembled response plus a completeness flag, removing pagination logic from the agent's responsibility entirely.
2. **Streaming Aggregation for Large Sets**: For result sets that could exceed reasonable context size, the wrapper streams and aggregates (counts, sums, filters) across all pages server-side and returns a summarized result to the agent, rather than requiring the agent to hold every page in context.
3. **Cursor Exhaustion Guardrail**: A hard cap on pagination iterations returns an explicit "safety limit reached, results may be incomplete" flag to the agent instead of silently stopping, so runaway pagination fails loud rather than silently truncating.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| paginated_calls_with_unaddressed_has_more_percent | Share of paginated tool calls where `has_more`/`next_cursor` was still set when the agent's reasoning consumed the data | > 1% |
| result_count_reconciliation_mismatch_rate_percent | Share of sessions where retrieved record count didn't match the source-reported total | > 0.5% |
| avg_pages_fetched_per_listing_call | Average pages fetched per listing/search call, tracked against expected data-volume trend | Sudden drop, or safety-cap hit rate > 2% |
| completeness_dependent_claims_without_count_check_percent | Share of "all X reviewed" / "no prior Y" style conclusions issued without a retrieved-vs-total count reconciliation | > 0% |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Incomplete listing used | The agent produced an answer or took an action based on a page where `has_more=true`/`complete=false` | P1 | Block downstream use; force re-fetch of remaining pages before finalizing the response |
| Count reconciliation mismatch | The retrieved record count does not match the source-reported total | P2 | Re-run pagination; alert tool owner if mismatch persists after retry |
| Safety cap hit rate rising | The cursor exhaustion guardrail triggers on more than 2% of calls in a week | P3 | Review whether the cap is too low for current data volumes or whether upstream filters should narrow the query |

## Related Patterns
- [Partial Result Misuse](./partial-result-misuse.md) - the broader category of treating any incomplete tool output (truncation, omitted fields, warnings) as complete; this pattern is the specific case where the incompleteness signal is a pagination cursor/count
- [Tool Capability Overestimation](../../tool-reliability/failures/tool-capability-overestimation.md) - a related but distinct failure where the agent assumes a tool supports functionality it doesn't, sometimes co-occurring with pagination failures when a capped result is also mistaken for a complete one
- [Silent Tool Failures](../../tool-reliability/failures/silent-failures.md) - a related but distinct failure where the tool call itself fails or errors and is misread as success, as opposed to this pattern's case of a successful call whose completeness signal is ignored

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| [Test name] | [Input] | [Expected output] | [What indicates failure] |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |

---

## Mitigation Strategies

### Prevention
1. **Mandatory Pagination Loop**: The retrieval wrapper never returns a single page to the agent as "the result"; it auto-follows `next_page_token`/`cursor`/`has_more` until exhaustion (or an explicit cap) and returns the fully assembled set, so the agent never has the option to stop after page one.
2. **Total-Count Pre-Check**: Before iterating, the wrapper reads the total-result-count/total-pages field when the API exposes one, and asserts that the number of records ultimately collected matches it; mismatches raise an error before the agent uses the data.
3. **Explicit Completeness Contract in Tool Interface**: The tool's return schema includes a `complete: bool` and `pages_fetched`/`total_pages` field; agent prompts and downstream logic are required to check `complete == true` before treating a listing as exhaustive, making incompleteness visible rather than implicit.

### Detection & Response
1. **Truncation Flag Monitoring**: Every paginated call logs whether `has_more`/`next_cursor` was still set when the agent's reasoning step consumed the data; any case where the agent proceeded with `has_more=true` unaddressed is flagged as a pagination-failure incident.
2. **Result-Count vs. Expected-Count Reconciliation**: Where the source system exposes a total record count, the sum of records actually retrieved is checked against it after each session; discrepancies trigger an automatic re-fetch and an incident log entry.
3. **Downstream Undercount Complaints**: User reports of "missing records" or "I know there are more" are tagged as a distinct category and cross-referenced against session logs for unresolved `has_more` flags to confirm pagination as the root cause versus a data issue.

### Architecture Patterns
1. **Auto-Paginating Client Wrapper**: All list/search tools are wrapped by a client library that transparently follows cursors/page tokens up to a safety cap (e.g., 10,000 records or 50 pages) and returns one assembled response plus a completeness flag, removing pagination logic from the agent's responsibility entirely.
2. **Streaming Aggregation for Large Sets**: For result sets that could exceed reasonable context size, the wrapper streams and aggregates (counts, sums, filters) across all pages server-side and returns a summarized result to the agent, rather than requiring the agent to hold every page in context.
3. **Cursor Exhaustion Guardrail**: A hard cap on pagination iterations returns an explicit "safety limit reached, results may be incomplete" flag to the agent instead of silently stopping, so runaway pagination fails loud rather than silently truncating.

### Metrics
1. **paginated_calls_with_unaddressed_has_more_percent**: Target: 0%; Alert threshold: > 1%
2. **result_count_reconciliation_mismatch_rate_percent**: Target: 0%; Alert threshold: > 0.5%
3. **avg_pages_fetched_per_listing_call**: Target: matches expected data volume trend; Alert threshold: sudden drop or safety-cap hit rate > 2%
4. **missing_records_user_reports_per_week**: Target: < 2; Alert threshold: >= 5

### Alerts
1. **Incomplete Listing Used** (P1 - Critical): Condition - the agent produced an answer or took an action based on a page where `has_more=true`/`complete=false`. Action: Block downstream use, force re-fetch of remaining pages before finalizing the response.
2. **Count Reconciliation Mismatch** (P2 - Warning): Condition - the retrieved record count does not match the source-reported total. Action: Re-run pagination, alert tool owner if mismatch persists after retry.
3. **Safety Cap Hit Rate Rising** (P3 - Info): Condition - the cursor exhaustion guardrail triggers on more than 2% of calls in a week. Action: Review whether the cap is too low for current data volumes or whether upstream filters should narrow the query.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Medium |

---

## References

- [Tool-Augmented-LLM-Testing](https://homes.cs.washington.edu/~rjust/publ/tallm_testing_ast_2025.pdf)
- Note: Failures in tool-augmented LLM systems and testing implications.
