# Missing Memory Recall

## Issue: Agent fails to use relevant durable information.

**Frequency**: Rare

**Symptoms**
- User says they already told the agent.
- Retrieval returns zero relevant hits for a query even though a matching stored fact exists, because the query's wording doesn't closely resemble the original storage phrasing.
- Agent re-asks for information the user provided in an earlier session.
- A structured preference category (dietary, contact channel, order history) fails to surface simply because the current query isn't semantically close to how the fact was originally phrased.

**Root Cause**
Agent fails to use relevant durable information.

**Example**
```
Session 1 (January):
User: "Just so you know, I'm vegetarian."
[Stored: subject=user, predicate=dietary_preference, object=vegetarian]

Session 2 (June), different phrasing:
User: "What should I order for dinner tonight?"
Agent: "How about the grilled steak special?"
User: "I'm vegetarian, I told you that months ago."

[The embedding for "what should I order for dinner" was not close enough to
"I'm vegetarian" for pure vector retrieval to surface it, and there was no
structured dietary-preference index to fall back on.]
```

**Contributing Factors**
- Retrieval relies solely on embedding similarity without a keyword or structured-index fallback, missing facts phrased differently than the current query.
- No mandatory pre-response recall step, so memory is only searched when the model happens to decide to look something up.
- Lack of query expansion or synonym handling widens the vocabulary gap between how a fact was stored and how it's later referenced.
- No regression suite tracking realistic paraphrase gaps, so retrieval-breadth regressions ship unnoticed.
- Sparse or missing structured preference index for common categories (dietary, contact method, prior orders).

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Paraphrase-gap retrieval test | Stored fact "vegetarian"; later query "what should I eat for dinner" | Dietary preference is retrieved and applied to the recommendation | Recommendation ignores the stored preference |
| "Already told you" regression case | A real (stored_fact, later_query) pair captured from a past missed-recall incident | Fact surfaces on replay through the retrieval pipeline | Retrieval still returns empty or irrelevant results |
| Entity-matched empty-result test | Query referencing an entity (e.g., an order ID) for which stored records exist | Non-empty, relevant retrieval results are returned | Retrieval returns zero hits despite matching records existing |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| recall_coverage_rate_percent | > 95% on regression suite | Run the (fact, query) regression suite and measure the fraction where the fact is correctly retrieved |
| paraphrase_gap_miss_rate | < 5% | Run semantically-equivalent but lexically different query variants against stored facts and measure retrieval misses |
| structured_index_hit_rate | > 98% for known preference categories | Run exact subject/predicate lookups against the structured index in a test harness and measure hit rate |

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
| recall_coverage_rate_percent | < 90% |
| user_reported_missed_recall_rate_percent | > 1.5% |
| empty_result_on_known_entity_rate_percent | > 5% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Recall Regression Suite Failure | A deploy drops recall_coverage_rate_percent below 90% on the regression suite | Low |
| Spike in User-Reported Missed Recall | user_reported_missed_recall_rate_percent exceeds 1.5% over a rolling week | Low |

---

## References

- [MS-Agentic-Failure-Taxonomy](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf)
- Note: Agentic AI failure modes; safety/security; memory poisoning; tool use; multi-agent risks.
