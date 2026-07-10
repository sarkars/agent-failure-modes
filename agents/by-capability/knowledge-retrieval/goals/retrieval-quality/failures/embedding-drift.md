# Embedding Model Drift

## Issue: Embedding Model Changes Break Retrieval

**Frequency**: Occasional

**Symptoms**
- Retrieval quality suddenly degrades
- Queries that worked before now fail
- Index requires full rebuild
- A/B testing shows regression

**Root Cause**
Embedding model updates, fine-tuning, or swaps create incompatible vector spaces. Old embeddings don't match new query embeddings.

**Example**
```
Original setup:
- Documents embedded with model v1.0
- Queries embedded with model v1.0
- Retrieval works well

After update:
- Documents still embedded with v1.0
- Queries now embedded with v1.1
- Vectors in different spaces

Query: "How to reset password?"
Similarity with correct doc: 0.45 (was 0.89 with v1.0)

Result: Correct document no longer retrieved
```

## Mitigation Strategies

### Prevention
1. **Embedding Version Pinning**: Tag every vector with the exact model name and version used to produce it, and only compare query embeddings against vectors from the same version. This prevents the silent cross-version comparison that dropped similarity from 0.89 to 0.45 in the example. Trade-off: requires version metadata storage and lookup on every query.
2. **Blue-Green Re-Embedding Pipeline**: Build the entire new index under the new model version in parallel, validate retrieval quality against a benchmark set, then atomically cut over; the old index stays available for immediate rollback. Trade-off: doubles storage cost during the migration window.
3. **Compatibility Gate Before Deploy**: Require a fixed regression suite of query-document relevance pairs to pass a defined similarity/recall threshold on the new embedding model before it touches production traffic, catching incompatible vector spaces before they reach users.

### Detection & Response
1. **Similarity-Score Distribution Monitoring**: Track the distribution of top-1 retrieval similarity scores; a sudden downward shift (like 0.89 to 0.45) signals a version mismatch and should auto-trigger an index audit.
2. **Mixed-Version Index Scanning**: Periodically scan the index for vectors tagged with a stale model version and quantify what fraction of queries are being compared against them.
3. **Canary Query Set Replay**: Replay a fixed set of known-good queries against the live index after any embedding-related deploy; alert if the retrieved document identities change unexpectedly.

### Architecture Patterns
1. **Dual-Write During Migration**: During the migration window, embed new/updated documents with both old and new models, tagged separately, so retrieval can serve from whichever version matches the query embedder until migration completes.
2. **Model Registry With Compatibility Matrix**: Maintain an explicit registry mapping which query-embedder versions are compatible with which document-embedder versions; reject retrieval calls that cross incompatible pairs instead of silently returning degraded matches.
3. **Gradual Batch Migration With Validation Gates**: Re-embed documents in batches (by collection or recency), validating retrieval quality after each batch rather than a single atomic full-corpus swap that has no intermediate checkpoint.

### Metrics
1. **embedding_version_consistency_rate**: Target: 100%; Alert threshold: < 99%
2. **top1_similarity_score_p50**: Target: within historical baseline +/-5%; Alert threshold: > 15% deviation
3. **index_migration_completion_percent**: Target: 100% within migration SLA; Alert threshold: stalled > 48h
4. **canary_query_retrieval_stability**: Target: > 95% same-document match rate; Alert threshold: < 90%

### Alerts
1. **Vector Space Incompatibility** (P1): Condition - top1_similarity_score_p50 drops > 15% within a rolling 24h window following a model change. Action: immediately roll back to the prior embedding model/index, investigate before retrying.
2. **Stale-Version Vectors Detected** (P2): Condition - embedding_version_consistency_rate falls below 99%. Action: prioritize the re-embedding backlog for flagged documents.
3. **Canary Regression** (P1): Condition - canary_query_retrieval_stability falls below 90% post-deploy. Action: block further rollout, revert the embedding model change.

## References

- [FloTorch: 2026 RAG Performance Landscape](https://www.flotorch.ai/blogs/the-2026-rag-performance-landscape-what-every-enterprise-leader-needs-to-know) - Model versioning challenges
- [Braintrust: Agent Observability Guide 2026](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Monitoring embedding quality
