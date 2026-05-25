# Retrieval Ranking Errors

## Issue: Relevant Documents Not Ranked Appropriately

**Frequency**: Common

**Symptoms**
- Answer exists in retrieved set but model misses it
- Relevant document at position 8 when top-3 used
- Irrelevant documents ranked above relevant ones
- Similar relevance scores for very different quality docs
- Position-dependent answer quality (top-1 vs top-5)

**Root Cause**
Even when relevant documents are retrieved, poor ranking means they may be positioned too low for effective use. Models have attention biases (favor early context), context windows limit how much can be passed, and top-k cutoffs may exclude relevant documents. RAGAS Context Precision specifically measures whether relevant chunks appear before irrelevant ones in the ranking.

**Example**
```
Query: "What are the tax implications of 401k early withdrawal?"

Retrieved documents (top 10):
Rank 1: General retirement planning guide (0.89 sim)
Rank 2: IRA withdrawal rules (0.87 sim) - wrong account type
Rank 3: Investment advice article (0.85 sim)
Rank 4: 401k contribution limits (0.84 sim) - wrong topic
Rank 5: 401k early withdrawal penalties ← BEST ANSWER (0.82 sim)
Rank 6: Roth vs Traditional comparison (0.81 sim)
Rank 7: 401k loan provisions (0.80 sim)
Rank 8: Tax penalty exceptions ← ALSO RELEVANT (0.78 sim)
Rank 9: General tax advice (0.77 sim)
Rank 10: Retirement age calculator (0.75 sim)

System uses top-3 for context.
Result: Answer based on wrong account type (IRA vs 401k)

RAGAS Context Precision calculation:
  Relevant docs at positions: 5, 8
  Total positions: 10
  Precision@3: 0/3 = 0.0 (no relevant in top 3)
  Precision@5: 1/5 = 0.2
  Average Precision: Low

  Ideal ranking would place positions 5,8 at 1,2
```

**Key Statistics**
From Ranking Research (RAGAS studies, 2026):
- Retrieval finds answer 80%+, ranking exposes it 60%
- Position 1 vs position 5: 25% answer quality drop
- Context Precision scores: median 0.65 in production
- "Lost in the middle" effect: 30% accuracy drop for middle positions
- MRR (Mean Reciprocal Rank) variance: 0.3-0.9 across queries

**Ranking Error Types**
| Error Type | Description | Impact |
|------------|-------------|--------|
| Similarity ≠ Relevance | High embedding similarity but wrong content | Wrong answer |
| Position bias | Relevant doc outside top-k | Answer missed |
| Tie-breaking failures | Similar scores, wrong ordering | Inconsistent |
| Query-type mismatch | Ranking tuned for different query types | Poor precision |
| Recency ignored | Older version ranked higher | Stale answer |

**Contributing Factors**
- Embedding similarity ≠ task relevance
- Fixed top-k regardless of query complexity
- No relevance-aware scoring
- Single-stage retrieval without refinement
- Ignoring document metadata in ranking
- Training data distribution mismatch

**Mitigation Strategies**
1. **Hybrid scoring**: Combine semantic + lexical + metadata signals
2. **Dynamic top-k**: Adjust based on score distribution
3. **Multi-stage retrieval**: Initial recall, then precision-focused reranking
4. **Score calibration**: Normalize scores for comparability
5. **Query classification**: Different ranking for different query types
6. **Relevance feedback**: Learn from user interactions

**Detection**
- Track RAGAS Context Precision scores
- Monitor Mean Reciprocal Rank (MRR)
- Analyze answer accuracy by best-doc position
- Compare retrieval recall vs. effective precision
- Log position of actually-used context

## References

- [RAGAS Context Precision](https://docs.ragas.io/en/latest/concepts/metrics/context_precision.html) - Precision metric
- [Lost in the Middle](https://arxiv.org/abs/2307.03172) - Position bias in long context
- [NDCG for RAG](https://en.wikipedia.org/wiki/Discounted_cumulative_gain) - Ranking evaluation
- [Hybrid Search](https://www.pinecone.io/learn/hybrid-search-intro/) - Multi-signal ranking
