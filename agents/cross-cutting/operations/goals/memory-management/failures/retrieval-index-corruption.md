# Retrieval Index Corruption

## Issue
The retrieval index itself — the vector index's internal graph/tree structure, an inverted index's postings lists, or a search engine's shard metadata — becomes structurally corrupted, from a bad write during an index rebuild, a version mismatch between index format and query engine, a crashed process leaving a partial index update, or disk/memory corruption at the infrastructure level. Unlike corruption of an individual memory record, this degrades retrieval quality or availability across the entire index (or a whole shard/partition of it), producing wrong, missing, or inconsistent results for many unrelated queries at once rather than for one specific fact.

**Frequency**: Rare

**Symptoms**
- Retrieval quality degrades broadly and suddenly across many unrelated queries, not localized to one entity or record
- Some queries return zero or far fewer results than expected despite the underlying data being present in the primary store
- Search results become inconsistent between repeated identical queries (index in an internally contradictory state)
- Index rebuild or repair operations resolve the issue, confirming the problem was structural rather than data-level
- Issue often correlates with a recent index rebuild, version upgrade, or infrastructure incident (disk error, out-of-memory kill during indexing)

## Root Cause
Retrieval indexes are complex data structures (approximate-nearest-neighbor graphs, B-trees, inverted-index postings lists, sharded metadata) that are expensive to rebuild from scratch, so systems favor incremental updates — but incremental updates to these structures are harder to make atomic than a simple key-value write, and a crash, timeout, or bug partway through an incremental update (adding a node to a graph index, updating a postings list, rebalancing a shard) can leave the structure in a state that is neither the old valid state nor the new valid state. Because the index's internal structure isn't validated on every query (that would defeat the performance purpose of having a specialized index at all), a structurally corrupted index doesn't fail loudly — queries against it still return *something*, just wrong, incomplete, or inconsistent something, until an integrity check or rebuild specifically targets the structure itself.

## Example
```
A production vector index (HNSW graph, ~4M records) undergoes a
routine incremental update to add 15,000 new records. Partway
through the batch, the indexing worker is OOM-killed by the
orchestrator due to an unrelated memory spike from a co-located
process.

The graph structure is left with roughly 8,000 of the 15,000 new
nodes inserted, some with fully-formed edge connections and some
with partial or missing edges (the insert process adds a node and
then wires its edges in a follow-up step, which never completed
for the last ~3,000 nodes before the kill).

Post-incident: no error is surfaced anywhere; the index continues
serving queries. However, approximate-nearest-neighbor search
quality silently degrades for any query whose true nearest
neighbors happen to live in the poorly-connected region of the
graph near those partially-wired nodes — searches "skip over" the
correct nearest neighbors because the graph traversal can't reach
them through the missing edges, returning less relevant results
with no error, for an estimated 2-3% of queries touching that
region, for the following 11 days until a scheduled full index
rebuild happens to catch and correct the issue as a side effect.
```

## Statistics
| Finding | Context |
|---------|---------|
| Incremental index updates interrupted mid-operation (crash, OOM, timeout) are a common root cause of structural index corruption in graph-based and tree-based retrieval indexes | Typical pattern for approximate-nearest-neighbor and inverted-index systems |
| Structural index corruption often affects only a localized region of the index (nodes/shards near the interrupted operation), making it detectable only via targeted integrity checks rather than aggregate quality metrics | Reported pattern across teams operating large-scale vector/search indexes |
| Periodic full index integrity checks or scheduled rebuilds catch the substantial majority of structural corruption before it's identified through user-facing quality complaints | Estimated from teams running scheduled integrity verification |

## Mitigations
1. **Atomic incremental updates**: Wrap multi-step index update operations (node insert + edge wiring, postings update + metadata update) in a mechanism that can detect and roll back a partial update rather than leaving the structure half-modified.
2. **Scheduled integrity checks**: Run periodic structural validation (graph connectivity checks, postings-list consistency checks) independent of query-time behavior, since corruption doesn't reliably surface through normal query patterns.
3. **Shadow index validation**: Before promoting a rebuilt or incrementally-updated index to serve production traffic, validate its query results against a known-good reference set to catch quality regressions from structural issues.
4. **Graceful degradation on detected corruption**: When integrity checks detect a corrupted region, fall back that portion of query traffic to a backup index or a slower-but-correct search path rather than continuing to serve degraded results silently.
5. **Full rebuild cadence**: For index types prone to incremental-update corruption, schedule periodic full rebuilds from the source of record even in the absence of detected issues, treating incremental updates as inherently accumulating small risk over time.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| index_integrity_check_failure_rate | Fraction of scheduled structural integrity checks that detect an anomaly | Alert if > 0 |
| query_result_consistency | Rate at which repeated identical queries against the index return differing result sets | Alert if > 0.1% |
| localized_quality_regression | Recall/precision on a benchmark query set, segmented by index region/shard, to detect region-specific degradation | Alert if any region drops > 15% below baseline |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Structural corruption detected | A scheduled integrity check fails on the retrieval index | High | Failover affected shard/region to backup, schedule targeted repair or full rebuild |
| Interrupted index update | An incremental index update job is killed or times out mid-operation | High | Flag the affected region for integrity check, avoid serving queries against it until verified |

## Related Patterns
- [Memory Corruption Detection Failure](./memory-corruption-detection-failure.md) - corruption at the individual-record level rather than the index's own structure, though both stem from non-atomic multi-step writes
- [Memory Fragmentation](./memory-fragmentation.md) - both degrade retrieval performance over time, though fragmentation is accumulated bloat rather than structural damage
- [Retrieval Confidence Miscalibration](./retrieval-confidence-miscalibration.md) - a corrupted index can produce results whose similarity scores are especially unreliable, compounding an existing miscalibration risk
