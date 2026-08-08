# Memory Deletion Failure

## Issue: Agent fails to forget information when requested.

**Frequency**: Common

**Symptoms**
- Deleted fact still influences later responses.
- Forget request succeeds against the primary database but the vector/embedding index or a cache still returns near-duplicate matches for the deleted content.
- A compliance audit discovers the deleted fact persisting inside a derived summary or cached prompt context generated before the deletion.
- A forget request is marked "complete" even though it was never verified against every store that could hold a copy.

**Root Cause**
Deletion is implemented as a single DELETE against the primary database with no fanout to the vector index, caches, or derived summaries that may hold their own copy of the same fact, so removing the canonical record does nothing to the copies scattered across the rest of the system. There's no tombstone mechanism to suppress a value that a stale replica or cache already loaded, and no post-deletion verification probe re-queries those other stores to confirm the fact is actually gone before the request is marked complete. Summaries and other derived artifacts generated before the deletion are never regenerated or scanned for the deleted content, and because the store registry used for fanout isn't kept current as new caches and analytics sinks get added, newer stores are silently excluded from the deletion path entirely.

**Example**
```
User: "Please delete my home address, I don't want it stored anymore."
Agent: "Done, your address has been removed."

[Primary DB row deleted. Vector index still holds the original embedding;
a nightly summary job generated a week earlier still contains the address
in its cached text.]

Two weeks later, unrelated session:
Agent: "Should I use your address on file, 42 Birch Lane, for the delivery estimate?"
User: "I told you to delete that."
```

**Contributing Factors**
- Deletion is implemented as a single DELETE against the primary store without fanning out to derived stores (embeddings, caches, summaries, analytics extracts).
- No tombstone mechanism, so replicas or caches that already loaded the value keep serving it after the primary delete.
- No post-deletion verification probe confirms removal took effect across every store before the request is marked complete.
- Summaries or other derived artifacts generated before the deletion are never regenerated or scanned for the deleted content.
- The store registry used for fanout is not kept current as new caches or analytics sinks are added to the system.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Full-store fanout test | A forget request for a fact known to exist in the primary DB, vector index, and cache | The fact is absent from every store after the request completes | Probe finds the fact still present in any one store |
| Derived-artifact residue test | Delete a fact after a summary referencing it was already generated | The cached summary is regenerated or scrubbed of the deleted content | The deleted fact still appears verbatim or paraphrased in the cached summary |
| Tombstone bypass test | Query the retrieval path directly against a replica that hasn't finished syncing the delete | Tombstone record suppresses the value even on the lagging replica | Stale replica value surfaces in the response |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| store_fanout_completeness_rate | 100% | In a test harness, issue a delete against a fact seeded in every registered store and verify each store confirms removal |
| post_deletion_recall_probe_pass_rate | 100% | Run synthetic recall queries against test fixtures immediately after simulated deletion and confirm zero hits |
| mean_test_deletion_latency | < 15 min (simulated) | Measure time from delete request to full-propagation confirmation across all stores in the test environment |

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
| deletion_full_propagation_rate_percent | < 100% for any request past SLA |
| post_deletion_recall_probe_failure_count | > 0 |
| tombstone_bypass_count | > 0 |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Deleted Fact Resurfaced in Response | Post-deletion recall probe or live user interaction shows a deleted fact still influencing output | Critical |
| Deletion Request Stuck Incomplete | A forget request has not reached full-propagation status within SLA (e.g., 60 min) | High |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
