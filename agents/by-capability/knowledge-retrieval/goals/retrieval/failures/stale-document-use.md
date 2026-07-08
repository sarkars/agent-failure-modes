# Stale Document Use

## Issue: Agent uses outdated policy/doc/version.

**Frequency**: Common

**Symptoms**
- Source date older than current policy.
- [Add more specific symptoms]

**Root Cause**
Agent uses outdated policy/doc/version.

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
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | High |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
