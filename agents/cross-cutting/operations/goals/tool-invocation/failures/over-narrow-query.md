# Over-Narrow Query

## Issue: Agent misses correct data due to overly strict filters.

**Frequency**: Occasional

**Symptoms**
- Empty result despite known relevant records.
- Agent reports "no results found" or gives an incomplete answer despite the data existing under a different filter value.

**Root Cause**
The agent reaches for an exact-match filter in situations that actually needed fuzzy or range matching, implicitly assuming a real-world category (status, date, name) has one canonical value when in practice it has several valid synonyms or states a record could legitimately hold. Because no fallback or broadening step is defined for when a filtered query comes back empty, that zero-result response is taken at face value instead of being treated as a signal to relax a filter and retry, so a record sitting one status value away from the query is reported as if it didn't exist at all.

**Example**
```
A user asks for "my open support ticket." The agent filters strictly on
status = "open", but the ticket was reassigned to status "pending" during
triage. The exact-match filter excludes the record entirely, and the
agent tells the user no open ticket exists even though it's sitting one
status value away.
```

**Contributing Factors**
- Agent applies an exact-match filter where a fuzzy or range filter was needed (exact string vs. contains, exact date vs. range).
- Model assumes a single canonical field value for a real-world category that actually has several valid synonyms or states.
- No fallback/broadening step is defined for when a filtered query returns zero results, so the empty result is taken at face value.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Zero-result-should-retry case | Query with a filter value that excludes a known-relevant record (e.g. wrong status enum) | Agent detects the zero/near-zero result count as suspicious and retries with a broadened filter before concluding "no data" | Agent reports no results exist when a relevant record was excluded only by an overly strict filter |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| zero_result_query_rate | < 3% of queries return zero results without a retry-broadened follow-up | Track queries returning empty sets and whether the agent issued a broader follow-up query before answering |

---

## Mitigation Strategies

### Prevention
1. **Filter Necessity Justification**: The agent must be able to justify each filter it adds (why this date range, why this exact status) against the user's actual request; filters not traceable to an explicit user constraint are treated as agent-invented and discouraged through prompt guidance and few-shot examples.
2. **Fuzzy/Synonym Matching Defaults**: Text and categorical filters default to fuzzy or synonym-aware matching (stemming, close-date windows, status aliases) rather than exact string/enum match, so minor phrasing or data-entry variance doesn't silently exclude valid records.
3. **Filter Combination Sanity Bounds**: The query builder limits how many simultaneous AND-ed filters can be stacked without an intermediate result check; queries with more than N conjunctive filters are broken into a staged search with a "does narrowing this further still return results?" check at each step.

### Detection & Response
1. **Empty/Near-Empty Result Monitoring**: Any retrieval call returning zero or near-zero results on a query type that historically returns non-zero is flagged; the agent is required to attempt at least one relaxation pass (drop one filter) before treating the result as authoritative.
2. **Known-Record Recall Probes**: Synthetic canary records with known attributes are seeded into the searchable dataset (or a shadow index); periodic probe queries confirm they are still retrievable under typical filter combinations, catching silent over-narrowing caused by filter/index drift.
3. **Filter Relaxation Outcome Tracking**: When the agent's auto-relaxation logic drops a filter and subsequently finds results, that event is logged; a high rate of "found after relaxing" events indicates the initial filter-construction logic is systematically too strict and needs tuning.

### Architecture Patterns
1. **Automatic Query Relaxation Ladder**: On zero results, the retrieval wrapper automatically retries with a defined relaxation sequence (widen date range, drop least-specific filter, switch exact-match to fuzzy) up to a bounded number of steps, surfacing which relaxation finally succeeded.
2. **Filter Confidence Annotation**: Each filter the agent applies is tagged as "explicit" (stated by the user) or "inferred" (assumed by the agent); only explicit filters are treated as hard constraints, while inferred filters are automatically candidates for relaxation on empty results.
3. **Two-Pass Search Strategy**: A first pass executes a broad query to confirm relevant records exist at all; a second pass applies the full filter set. If pass one returns nonzero but pass two returns zero, the system flags the filters — not the dataset — as the likely cause.

### Metrics
1. **zero_result_query_rate_percent**: Target: < 3%; Alert threshold: > 8%
2. **relaxation_recovery_rate_percent**: Target: trending down over time; Alert threshold: > 25% of zero-result queries recovered via relaxation
3. **canary_record_retrieval_success_rate_percent**: Target: 100%; Alert threshold: < 100%
4. **inferred_filter_share_percent**: Target: < 30% of applied filters; Alert threshold: > 50%

### Alerts
1. **Canary Record Retrieval Failure** (P1 - Critical): Condition - a seeded known-good record is not returned by its standard probe query. Action: Investigate index/filter/search-pipeline regression immediately, page search infra owner.
2. **Zero-Result Spike** (P2 - Warning): Condition - zero_result_query_rate_percent exceeds threshold for a query type over 1 hour. Action: Inspect recent filter-construction prompt changes, enable the relaxation ladder if not already active.
3. **High Relaxation Recovery Rate** (P3 - Info): Condition - relaxation_recovery_rate_percent exceeds threshold over a week. Action: Tune default filter strictness/fuzzy-matching thresholds for the affected tool.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| zero_result_without_retry_percent | > 8% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Zero-Result Answer Without Broadening | Agent reports no data found after a single narrowly-filtered query with no retry | Medium |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
