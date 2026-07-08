# Missing Memory Recall

## Issue: Agent fails to use relevant durable information.

**Frequency**: Rare

**Symptoms**
- User says they already told the agent.
- [Add more specific symptoms]

**Root Cause**
Agent fails to use relevant durable information.

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
1. **Hybrid Retrieval (Semantic + Keyword + Structured Index)**: Relying on pure vector similarity misses relevant facts phrased differently than the current query. Combine embedding search with keyword/BM25 matching and a structured preference index (explicit subject/predicate lookups) so a fact stored as "vegetarian" is still retrieved when the user asks about "dinner options" even without close semantic overlap.
2. **Proactive Memory Surfacing Before Response**: Before generating a response, the agent runs a mandatory retrieval step scoped to the current task's entities/topics and reviews returned facts, rather than only recalling memory when the model "decides" to look something up — this removes reliance on the model noticing it should search.
3. **Recall Coverage Testing in Eval**: Maintain a regression suite of (stored_fact, later_query) pairs representing realistic paraphrase gaps; every retrieval pipeline change must pass a minimum recall rate on this suite before deploying, catching silent regressions in retrieval breadth.

### Detection & Response
1. **"I Already Told You" Signal Capture**: Detect user utterances indicating the agent missed known context ("I already said...", "as I mentioned...") and log the (query, expected_fact) pair. Feed these into the recall regression suite so real misses become permanent test cases.
2. **Retrieval Recall Rate Monitoring**: For a sampled set of production queries with known-relevant stored facts (via labeling or the above signal), compute what fraction were actually retrieved into context. Track this recall rate over time to catch index degradation.
3. **Empty-Result Alerting on Entity-Matched Queries**: When a query mentions an entity (product, order, person) for which the memory store has records, but retrieval returns zero relevant hits, flag as a potential missing-recall event for review rather than silently proceeding.

### Architecture Patterns
1. **Preference Index Service**: A structured, queryable index (keyed by user_id + entity/topic) sits alongside the vector store, allowing exact-match lookups for known preference categories (dietary, communication channel, product history) that don't depend on embedding similarity working well for short or oddly-phrased queries.
2. **Query Expansion Layer**: Before retrieval, expand the current query into related terms/synonyms (using the conversation topic and known entity aliases) to widen the semantic search net, reducing misses caused by vocabulary mismatch between how a fact was stored and how it's later referenced.
3. **Mandatory Pre-Response Recall Step**: Architect the agent loop so memory retrieval is a required step in the pipeline (not an optional tool call the model may skip), with the retrieved facts passed into context construction unconditionally for every turn involving a returning user.

### Metrics
1. **recall_coverage_rate_percent**: Target: > 95% on regression suite; Alert threshold: < 90%
2. **user_reported_missed_recall_rate_percent**: Target: < 0.5% of sessions; Alert threshold: > 1.5%
3. **empty_result_on_known_entity_rate_percent**: Target: < 2%; Alert threshold: > 5%
4. **mean_relevant_facts_retrieved_per_query**: Target: tracked baseline, no regression > 10% week-over-week

### Alerts
1. **Recall Regression Suite Failure** (P2 - Warning): Condition - a deploy drops recall_coverage_rate_percent below 90% on the regression suite. Action: Block deploy/rollback, investigate embedding model or index change, re-run suite before re-attempting release.
2. **Spike in User-Reported Missed Recall** (P2 - Warning): Condition - user_reported_missed_recall_rate_percent exceeds 1.5% over a rolling week. Action: Sample affected sessions, identify common query patterns, add to regression suite, tune hybrid retrieval weighting.
3. **Entity Index Gap** (P3 - Info): Condition - empty_result_on_known_entity_rate_percent trending upward. Action: Audit preference index coverage for the affected entity types, backfill missing structured index entries.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Low |

---

## References

- [MS-Agentic-Failure-Taxonomy](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf)
- Note: Agentic AI failure modes; safety/security; memory poisoning; tool use; multi-agent risks.
