# Query Planning Timeout

## Issue
Before a complex query ever executes, the tool's query planner (a database optimizer, a GraphQL resolver-planning phase, a distributed-query coordinator) has to determine an execution strategy — and for sufficiently complex queries, this planning phase itself can time out, independent of and prior to any execution timeout. This produces a distinct failure class from an execution timeout: the query never ran at all, no partial work was done, and no rows were touched, yet the error returned to the agent often looks identical to a generic timeout, so the agent's error handling treats it the same as a slow-but-progressing query and applies the wrong recovery strategy.

**Frequency**: Occasional

**Symptoms**
- Timeout errors that occur almost immediately (well under the configured execution timeout), inconsistent with a query that was actually executing
- Retries of a planning-timeout query fail at the same fast, consistent latency every time, rather than the variable latency typical of execution timeouts under load
- Error messages or codes that don't distinguish planning-phase failure from execution-phase failure (both surfaced as a generic `504` or `QueryTimeout`)
- Agents applying execution-oriented recovery (e.g., "retry with a longer timeout") to a planning failure that a longer execution timeout cannot fix, since the query never reached execution
- Complex queries (many joins, many optional filters, large `IN` clauses) that fail consistently regardless of the underlying data volume, because planning cost depends on query shape, not data size

## Root Cause
Query planning — choosing join order, index usage, and execution strategy — is itself a search problem whose cost grows with query shape complexity (number of joins, number of predicate combinations, size of `IN`/`OR` clause lists), and planners impose their own timeout on this search independent of how long the resulting plan would take to execute. Agents that construct queries programmatically (e.g., building a large `IN` clause from a dynamically sized ID list, or adding optional filter branches based on available context) can produce query shapes that are planning-expensive even when the underlying data volume is small or the eventual plan would execute quickly. Because most client-side error handling has one code path for "timeout," and the tool's response often doesn't clearly flag "this timed out during planning, not execution," the agent cannot tell the two apart and applies execution-timeout remedies (longer timeout, add an index hint, wait and retry) to a problem those remedies don't address.

## Example
```
An agent building a fraud-review report constructs a SQL-backed API query
with a dynamically generated `WHERE customer_id IN (...)` clause
containing 8,000 IDs pulled from an upstream flagged-accounts list, joined
against 4 other tables with several OR-combined optional filters
(region, signup_date range, risk_score threshold, each conditionally
included based on what filters the user specified). The query planner,
faced with an enormous number of possible join orderings and index-choice
combinations from the large IN list and OR-combined filters, exceeds its
internal 2-second planning budget and aborts before generating an
execution plan. The API returns `504 Gateway Timeout` after 2.1 seconds —
looking, from the agent's perspective, like a normal slow-query timeout.
The agent's retry logic increases the request timeout to 60 seconds and
retries, but the failure recurs at the same ~2 second mark every time,
because the bottleneck is planning cost, not the configured execution
timeout, which was never reached.
```

## Statistics
| Finding | Context |
|---------|---------|
| Query planners commonly impose their own internal timeout, often in the 1-5 second range, well below typical execution timeouts of 30-60 seconds | Common in relational database optimizers and distributed query engines |
| Large `IN` clauses (thousands of literals) and heavily branched optional-filter queries are a common trigger for planning-time blowup, disproportionate to actual data volume | Based on typical query-planner complexity characteristics |
| Planning-timeout failures are frequently misclassified as execution timeouts by client error handling because the returned status code/class is often identical | Structural gap in most generic timeout error handling |

## Mitigations
1. **Distinguish planning-phase failures from execution-phase failures in error handling**: Where the tool exposes a distinguishing signal (fast, consistent failure latency; a specific error code; a `phase: planning` field), route planning timeouts to a different recovery path than execution timeouts.
2. **Reduce query shape complexity rather than increasing timeout on retry**: For planning timeouts, the fix is a simpler query shape (smaller `IN` lists via chunking, fewer optional filter branches, precomputed filter combinations) — not a longer timeout, which does not address a planning-phase failure.
3. **Chunk large literal lists instead of one giant IN clause**: Split an oversized `IN (...)` list into several smaller queries executed separately (or converted to a temp-table/join pattern where supported) to keep planner search space bounded.
4. **Avoid dynamically combinatorial optional filters**: Where a query builder conditionally includes many optional filter branches, prefer a fixed set of pre-planned query shapes (parameterized, with NULL-able bind variables) over dynamically assembled SQL with varying structure per call.
5. **Track failure latency as a classification signal**: Log the elapsed time before each timeout; failures well under the configured execution timeout are a strong signal of planning-phase failure and should be flagged for query-shape review rather than blind retry.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `query.timeout_latency_vs_configured_execution_timeout` | Ratio of actual failure latency to the configured execution timeout | Alert when ratio < 0.2 (strong planning-timeout signal) |
| `query.in_clause_size` | Size of dynamically constructed IN-clause literal lists | Alert when > 1,000 elements |
| `query.planning_timeout_rate` | Rate of timeouts classified (via latency heuristic or explicit signal) as planning-phase | Alert if > 1% of queries against a given tool |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Suspected planning-phase timeout | Timeout error with failure latency far below configured execution timeout | Medium | Route to query-shape simplification, not retry-with-longer-timeout |
| Repeated identical-latency timeout on retry | 2+ retries fail at consistent, fast latency after increasing execution timeout | High | Halt naive retries, escalate for query restructuring |

## Related Patterns
- [Query Complexity Limit](./query-complexity-limit.md) - a scored-cost rejection that can occur pre-execution for similar underlying reasons as a planning timeout
- [Join Depth Limit](./join-depth-limit.md) - deep joins are one of the query shapes most likely to drive planning cost past its timeout
- [Request Timeout No Graceful Handling](./request-timeout-no-graceful-handling.md) - the general pattern of hard timeouts with no partial-result signal, of which planning timeout is a specific pre-execution variant
