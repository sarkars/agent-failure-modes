# Pagination Failure

## Issue: Agent reads only first page and assumes completeness.

**Frequency**: Occasional

**Symptoms**
- Missing records beyond page 1.
- [Add more specific symptoms]

**Root Cause**
Agent reads only first page and assumes completeness.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- [List factors that make this failure more likely]

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
