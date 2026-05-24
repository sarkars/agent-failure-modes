# Goal: Retrieval Quality

Find relevant documents that contain the information needed to answer user queries. Retrieval is the foundation of RAG - if the right documents aren't retrieved, the answer will be wrong or hallucinated.

## Business Context

- Poor retrieval means answers based on wrong or incomplete information
- Over-retrieval wastes context window and confuses the model
- Under-retrieval forces hallucination to fill gaps
- Retrieval failures are often invisible to end users

## Failure Patterns

| Failure Pattern | Frequency | Impact |
|-----------------|-----------|--------|
| [Semantic Mismatch](failures/semantic-mismatch.md) | Very Common | High |
| [Chunk Boundary Issues](failures/chunk-boundary.md) | Very Common | High |
| [Index Staleness](failures/index-staleness.md) | Common | High |
| [Over-Retrieval](failures/over-retrieval.md) | Common | Medium |
| [Under-Retrieval](failures/under-retrieval.md) | Common | High |
| [Embedding Model Drift](failures/embedding-drift.md) | Occasional | High |
| [Metadata Filtering Errors](failures/metadata-filtering.md) | Common | Medium |
| [Knowledge Base Poisoning](failures/knowledge-base-poisoning.md) | Emerging | Critical |
| [Temporal Relevance Failure](failures/temporal-relevance.md) | Common | High |
| [Jurisdictional Mismatch](failures/jurisdictional-mismatch.md) | Common | High |
| [Reranking Degradation](failures/reranking-degradation.md) | Occasional | High |
| [Retrieval Ranking Errors](failures/retrieval-ranking-errors.md) | Common | High |
| [Query Expansion Noise](failures/query-expansion-noise.md) | Common | Medium |

## Key Statistics

| Finding | Source |
|---------|--------|
| 70% of RAG failures are retrieval failures | Industry Analysis |
| Hybrid search improves recall by 15-30% over vector-only | Benchmark studies |
| Chunk size has 20%+ impact on retrieval quality | Research |

## Key Metrics

- Retrieval precision (relevant docs / retrieved docs)
- Retrieval recall (retrieved relevant / total relevant)
- Mean Reciprocal Rank (MRR)
- Normalized Discounted Cumulative Gain (NDCG)
