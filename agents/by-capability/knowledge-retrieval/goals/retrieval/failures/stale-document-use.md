# Stale Document Use

## Issue: Agent uses outdated policy/doc/version.

**Frequency**: Common

**Symptoms**
- Source date older than current policy.
- Agent answers with a value from a superseded policy document while a newer version with a different value exists in the corpus.
- Retrieved document is tagged "deprecated" or "archived" in metadata but still surfaces in top-k results and gets cited.
- The cited document's effective date is more than one revision cycle behind the document type's expected update cadence.

**Root Cause**
The retrieval ranking function rewards historical engagement signals like click count and inbound links rather than recency or active/deprecated status, so a well-established old document can consistently outscore its replacement. This is compounded by an ingestion process that never records supersession relationships between document versions, meaning the system has no structural way to know the 2021 policy was replaced by the 2024 one. Because there is also no time-decay factor in scoring and no process for removing or flagging retired documents once a newer version is published, both versions sit in the index indefinitely as if equally current.

**Example**
```
Query: "What's the current mileage reimbursement rate?"
The corpus contains both the 2021 Travel Policy (rate = $0.56/mile) and the 2024
Travel Policy (rate = $0.67/mile, marked as the current active version). The 2021 doc
has more inbound links and a higher historical click count, so it ranks higher in
retrieval. The agent answers "$0.56 per mile" using the outdated 2021 document, without
checking that a newer, currently-active version supersedes it.
```

**Contributing Factors**
- Ranking signal weighted toward historical engagement (clicks, links) rather than document recency or active/deprecated status.
- No deprecation or supersession metadata attached to documents at ingestion, so old and new versions are treated as equally valid.
- No freshness/time-decay factor in the retrieval scoring function.
- Superseded documents not removed or flagged in the index after a newer version is published, leaving both versions retrievable indefinitely.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Superseded version returned | Query where both an old and a current version of the same policy exist in the corpus | Answer uses the current, active version and its value | Answer uses the outdated version's value |
| Deprecated doc still retrieved | Query surfaces a document explicitly tagged "deprecated" in metadata | Deprecated document is excluded from standard retrieval results | Deprecated document appears in top-k and is cited in the answer |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| median_document_age_in_retrieved_set_days | < 60 | Track median age (from last-updated timestamp) of documents in the retrieved top-10 for policy-type queries, sampled weekly |

---

## Mitigation Strategies

### Prevention
1. **Freshness Ranking Signal**: Incorporate document update/publish time as ranking signal. Newer documents boosted; older documents downranked (time_decay function). Example: document_age_days=1 scores higher than age=365.
2. **Deprecation Labels**: For documents marked deprecated/archived, add metadata flag. Exclude deprecated docs from standard retrieval (unless explicitly requested 'include_archived'). Display 'DEPRECATED' label if deprecated doc is retrieved.
3. **Document Validity Windows**: Define validity period for each document type (pricing valid 6mo, technical specs 12mo, regulations enforce immediately). Auto-mark stale after expiration. Exclude from retrieval.

### Detection & Response
1. **Freshness Metric Monitoring**: Track median age of retrieved documents per query type. Alert if median_age > threshold (policy docs should be < 3mo old). Baseline per document type.
2. **Stale Document Click-Through**: Monitor clicks/usage of retrieved documents. Flag documents with low CTR + high age (potential stale content). Review for deprecation.
3. **Document Update Audit Trail**: Track document update history. Alert if document not updated for > threshold period (potential stale/unmaintained content). Generate stale content reports.

### Architecture Patterns
1. **Temporal Index Partitioning**: Partition documents by update date (recent_30d, recent_90d, recent_1y, older). Prioritize recent partitions in retrieval. Example: 'Updated in last 30d' index queried first.
2. **Freshness Score Pipeline**: Compute freshness_score for each document (newer=higher). Update scores periodically as documents age. Use in ranking function with configurable weight.
3. **Document Lifecycle State Machine**: Model document states (active, deprecated, archived, expired). Enforce state transitions with validation. Only retrieve active docs. Track transitions in audit log.

### Metrics
1. **median_document_age_in_retrieved_set_days**: Target: < 60; Alert threshold: > 180; Track: median age per document type
2. **stale_document_click_through_rate_percent**: Target: < 5%; Alert threshold: > 15%
3. **deprecated_document_retrieval_rate_percent**: Target: < 0.1%; Alert threshold: > 0.5%
4. **document_update_frequency_median_days**: Target: 45; Alert if increases
5. **stale_content_user_complaints_per_month**: Target: 0; Alert if > 2

### Alerts
1. **Stale Document Retrieved** (P2 - Warning): Condition - document > 1yr old in top-10 results for document_type. Action: Review document relevance, consider deprecation, check if newer version exists.
2. **High Stale Content Rate** (P1 - Critical): Condition - > 20% of retrieved documents deprecated/archived. Action: Index refresh investigation, retrieval filter audit, potential index rebuild.
3. **Document Freshness Degradation** (P2 - Warning): Condition - median_document_age increases > 30 days month-over-month. Action: Investigate index staleness, document update delays, potential re-indexing.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| median_document_age_in_retrieved_set_days | > 180 |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Stale Document Surfaced | median_document_age_in_retrieved_set_days for policy queries exceeds 180 days | High |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
