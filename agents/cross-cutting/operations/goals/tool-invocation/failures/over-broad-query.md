# Over-Broad Query

## Issue: Agent retrieves too much data and reasons over irrelevant records.

**Frequency**: Occasional

**Symptoms**
- Large noisy result set; irrelevant citations.
- [Add more specific symptoms]

**Root Cause**
Agent retrieves too much data and reasons over irrelevant records.

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
1. **Mandatory Filter Enforcement**: The query-construction layer requires at least one narrowing filter (date range, entity ID, category) before a search/list tool call is allowed to execute; calls with only a free-text term and no scoping filter are rejected and the agent is prompted to add one.
2. **Result-Size Budgeting**: Each retrieval tool is called with an explicit max-results/page-size cap tuned to what the agent can meaningfully reason over (e.g., 20-50 records); the agent cannot request unbounded or "all" result sets, forcing progressive narrowing when the true set is larger.
3. **Query Specificity Scoring**: A lightweight pre-call heuristic (or small classifier) scores the constructed query's specificity based on filter count/breadth and flags overly generic queries (single common keyword, no date bound) for auto-refinement before submission.

### Detection & Response
1. **Result-Set Size Monitoring**: Every retrieval call logs its result count; calls returning above a tool-specific high-water mark are flagged as likely over-broad, and the downstream reasoning step is annotated with a "large/noisy result set" warning so answers drawing from it get lower confidence.
2. **Relevance-to-Result Ratio Check**: After the agent selects/cites records from a large result set, the system computes what fraction of retrieved records were actually referenced in the final answer; a persistently low ratio indicates queries are pulling much more than needed.
3. **Irrelevant-Citation Sampling**: Periodic human or LLM-judge review samples answers built on large result sets to check whether cited records are topically relevant; systemic irrelevance triggers a review of the retrieval filters/prompt for that tool.

### Architecture Patterns
1. **Progressive Narrowing Retriever**: The retrieval wrapper starts with a scoped query (recent window, primary category) and only widens scope in controlled increments if the initial narrow query returns too few results, rather than letting the agent issue one broad query up front.
2. **Faceted Search Interface**: The search tool exposes structured facets (date, status, owner, type) as first-class parameters rather than a single free-text field, nudging the agent toward composing filtered queries instead of broad keyword dumps.
3. **Post-Retrieval Reranker/Filter**: A lightweight reranking or relevance-filtering stage sits between raw retrieval and the agent's reasoning context, trimming an over-broad result set down to the top-K most relevant records before they ever reach the model's context window.

### Metrics
1. **avg_result_set_size_per_query**: Target: within tool's tuned band (e.g., 10-50); Alert threshold: > 3x band median
2. **queries_without_narrowing_filter_percent**: Target: < 5%; Alert threshold: > 15%
3. **cited_to_retrieved_ratio**: Target: > 30%; Alert threshold: < 10%
4. **oversized_result_flag_rate_percent**: Target: < 5% of retrieval calls; Alert threshold: > 20%

### Alerts
1. **Result Set Size Spike** (P2 - Warning): Condition - a retrieval call returns results far above the tool's tuned high-water mark. Action: Auto-annotate downstream answer as low-confidence, prompt agent to add filters and re-query.
2. **Chronic Low Relevance Ratio** (P2 - Warning): Condition - cited_to_retrieved_ratio stays below threshold for a week for a given tool. Action: Review query-construction prompt and add stronger filter-requirement guidance.
3. **Filterless Query Surge** (P3 - Info): Condition - queries_without_narrowing_filter_percent spikes above threshold. Action: Investigate recent prompt/tool-description changes that may have weakened filter guidance.

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

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
