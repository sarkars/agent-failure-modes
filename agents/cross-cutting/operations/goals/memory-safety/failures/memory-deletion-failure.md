# Memory Deletion Failure

## Issue: Agent fails to forget information when requested.

**Frequency**: Common

**Symptoms**
- Deleted fact still influences later responses.
- [Add more specific symptoms]

**Root Cause**
Agent fails to forget information when requested.

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
1. **Full-Fanout Deletion Propagation**: A forget request triggers deletion across every store that could hold a copy of the fact — primary memory DB, vector/embedding index, derived summaries, cached prompt contexts, and any downstream analytics extract. Deletion is modeled as a single logical transaction with a manifest of all target stores, not a single DELETE against the primary table.
2. **Tombstone Records Instead of Silent Removal**: Deleting a fact writes a tombstone (subject, predicate, deleted_at, request_id) rather than just removing the row. Any retrieval path that finds a matching subject/predicate must check the tombstone and suppress the value even if a stale copy still exists in a cache or replica.
3. **Deletion Verification Job**: After a delete request is processed, an automated verification pass re-queries every target store (including the vector index by re-embedding the deleted text and checking for near-duplicate hits) and confirms zero matches before marking the forget request complete.

### Detection & Response
1. **Post-Deletion Recall Probe**: Immediately after processing a forget request, run a synthetic recall query for the deleted fact against the live retrieval pipeline used in production. If the fact still surfaces, treat it as a critical deletion failure, not a background bug.
2. **Derived-Artifact Scan**: Search summaries, cached embeddings, and prompt-cache entries generated before the deletion request for the deleted content (via substring/semantic match) on a rolling schedule, since these are the most common places deletions silently fail to propagate.
3. **Compliance Deletion Ledger**: Every forget request and its per-store completion status is logged in an auditable ledger; requests that don't reach "fully propagated" status within SLA are automatically escalated rather than left open indefinitely.

### Architecture Patterns
1. **Deletion Orchestrator Service**: A dedicated service owns the fanout — it receives a forget request, enumerates every registered store via a store registry (primary DB, vector index, cache, analytics sink), issues deletes to each, and only marks the request complete when all stores confirm.
2. **Tombstone-Aware Retrieval Middleware**: All read paths (RAG retrieval, cache lookups, summary generation) pass through a middleware layer that filters out tombstoned subject/predicate pairs before results reach the model context, providing defense-in-depth even if a physical delete was missed somewhere.
3. **Immutable Deletion Audit Trail**: Store request_id, requester, scope, per-store completion timestamps, and verification probe results in an append-only compliance log, satisfying right-to-be-forgotten audit requirements independent of whether the underlying data stores are perfectly synchronized.

### Metrics
1. **deletion_full_propagation_rate_percent**: Target: 100%; Alert threshold: < 100% for any request past SLA
2. **post_deletion_recall_probe_failure_count**: Target: 0; Alert threshold: > 0 (any resurfaced deleted fact is critical)
3. **mean_deletion_completion_time_minutes**: Target: < 15 min across all stores; Alert threshold: > 60 min
4. **tombstone_bypass_count**: Target: 0; Alert threshold: > 0 (retrieval returned tombstoned content)

### Alerts
1. **Deleted Fact Resurfaced in Response** (P1 - Critical): Condition - post-deletion recall probe or live user interaction shows a deleted fact still influencing output. Action: Immediate incident, re-run fanout deletion across all stores, notify compliance/legal, notify affected user if required.
2. **Deletion Request Stuck Incomplete** (P2 - Warning): Condition - a forget request has not reached full-propagation status within SLA (e.g., 60 min). Action: Escalate to on-call, manually verify each store, investigate the store that failed to acknowledge.
3. **Store Registry Drift** (P3 - Info): Condition - a new data store (cache layer, analytics sink) was added to the system but is not registered with the deletion orchestrator. Action: Add to store registry, backfill audit of any deletions issued since the store went live.

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
