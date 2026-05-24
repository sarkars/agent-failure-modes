# Reranking Degradation

## Issue: Reranker Makes Retrieval Quality Worse

**Frequency**: Occasional

**Symptoms**
- Initial retrieval finds relevant docs, final ranking buries them
- Reranker favors superficially similar but wrong documents
- Domain-specific content ranked below generic matches
- Top-k after reranking worse than before
- Performance regression after adding reranker

**Root Cause**
Rerankers (cross-encoders, LLM-based rankers) are added to improve precision but can degrade results when: the reranker isn't trained on domain data, query-document pairs differ from training distribution, or reranker optimizes for wrong signals (lexical similarity vs. semantic relevance). A reranker tuned on general web data may demote technical documents that don't match typical relevance patterns.

**Example**
```
Query: "What is the maximum tensile strength of Grade 5 titanium?"

Initial retrieval (vector search, top 5):
1. Technical spec sheet with exact answer ✓
2. General titanium properties overview
3. Manufacturing process document
4. Grade comparison table ✓
5. Marketing material about titanium

After cross-encoder reranking:
1. Marketing material about titanium (fluent, well-written)
2. General titanium properties overview (comprehensive)
3. Manufacturing process document (mentions "strength")
4. Grade comparison table ✓
5. Technical spec sheet (terse, abbreviations) ✓

Result: Best document demoted from #1 to #5

RAGAS Context Precision metrics:
  Before reranking: 0.85
  After reranking: 0.62
  Precision drop: -27%

The reranker preferred polished prose over the dense 
technical spec that actually answers the question.
```

**Key Statistics**
From Reranking Research (RAGAS studies, 2026):
- Reranking improves results in 70-80% of cases
- Degrades results in 15-25% of domain-specific queries
- Cross-encoder out-of-domain degradation: 20-40%
- LLM rerankers sensitive to prompt phrasing
- Domain adaptation improves reranker by 30%+

**Degradation Scenarios**
| Scenario | Cause | Impact |
|----------|-------|--------|
| Domain mismatch | Reranker not domain-trained | Technical docs demoted |
| Length bias | Prefers longer documents | Concise answers buried |
| Fluency bias | Prefers well-written text | Raw data demoted |
| Recency bias | Training on recent patterns | Older authoritative sources demoted |
| Format bias | Prefers certain structures | Tables, lists, specs hurt |

**Contributing Factors**
- Generic reranker on specialized domain
- No A/B comparison with baseline retrieval
- Reranker optimized for different task
- Insufficient domain fine-tuning
- Blind trust in reranker output
- No fallback to initial ranking

**Mitigation Strategies**
1. **A/B evaluation**: Compare retrieval with/without reranker
2. **Domain fine-tuning**: Train reranker on domain-specific relevance
3. **Ensemble approach**: Combine initial and reranked scores
4. **Threshold guards**: Don't rerank if initial confidence high
5. **Failure detection**: Monitor RAGAS precision before/after
6. **Selective reranking**: Only rerank ambiguous queries

**Detection**
- Track Context Precision before vs. after reranking
- Monitor cases where initial top-1 wasn't final top-1
- Analyze user satisfaction by reranker intervention
- Log score changes through pipeline stages
- Sample audit reranking decisions

## References

- [RAGAS Context Precision](https://docs.ragas.io/en/latest/concepts/metrics/context_precision.html) - Ranking quality metric
- [Cross-Encoder Reranking](https://www.sbert.net/examples/applications/cross-encoder/README.html) - Reranker architecture
- [Pinecone Reranking](https://www.pinecone.io/learn/series/rag/rerankers/) - When rerankers help/hurt
- [ColBERT v2 Analysis](https://arxiv.org/abs/2112.01488) - Domain transfer challenges
