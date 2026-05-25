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

**Mitigation Strategies**
1. **Version tracking**: Track which model version indexed each document
2. **Atomic updates**: Re-index all documents when changing models
3. **Blue-green indexes**: Build new index before switching
4. **Compatibility testing**: Test retrieval quality before deploying new model
5. **Rollback capability**: Keep previous index for quick rollback
6. **Gradual migration**: Migrate documents in batches with validation

**Detection**
- Monitor retrieval metrics after model changes
- Track embedding model version across index
- Alert on retrieval score distribution shifts
- A/B test model versions before full rollout

## References

- [FloTorch: 2026 RAG Performance Landscape](https://www.flotorch.ai/blogs/the-2026-rag-performance-landscape-what-every-enterprise-leader-needs-to-know) - Model versioning challenges
- [Braintrust: Agent Observability Guide 2026](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Monitoring embedding quality
