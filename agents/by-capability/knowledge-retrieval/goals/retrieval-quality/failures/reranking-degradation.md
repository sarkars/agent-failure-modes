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

## Mitigation Strategies

### Prevention
1. **Domain Fine-Tuning Before Deployment**: Fine-tune the cross-encoder/LLM reranker on domain-specific query-document relevance pairs, including terse technical spec sheets as positive examples, rather than deploying an off-the-shelf general-web-trained reranker that favors polished prose.
2. **Baseline-Guarded Rollout**: Require the reranker to demonstrably outperform the initial retrieval ranking on a held-out domain benchmark (measured via Context Precision) before it's allowed to replace the initial ranking in production.
3. **Bias-Aware Feature Audit**: Explicitly test the reranker against known bias patterns (length bias, fluency bias, format bias against tables/specs) using adversarial pairs — terse-correct vs. verbose-wrong — before trusting it on content like the titanium spec sheet in the example.

### Detection & Response
1. **Pre/Post Reranking Precision Comparison**: Continuously compute Context Precision on both the initial ranking and the reranked output for the same queries; a measurable regression (like the -27% drop in the example) is a direct signal to investigate.
2. **Top-1 Swap Auditing**: Log every case where reranking changes the top-1 result from the initial retrieval's top-1, and periodically sample these swaps for human review to catch systematic demotion of correct-but-terse answers.
3. **Query-Segment Degradation Tracking**: Break down reranker performance by query/document type, since degradation often concentrates in specific segments like domain-specific technical content rather than showing up in the overall average.

### Architecture Patterns
1. **Ensemble Score Blending**: Combine the initial retrieval score and the reranker score (weighted average or learned combination) rather than fully replacing the initial ranking, so a bad reranker judgment can't completely override a good initial semantic match.
2. **Confidence-Gated Selective Reranking**: Only invoke the reranker when the initial retrieval's top results are closely scored/ambiguous; skip reranking when the initial ranking already shows a clear, high-confidence winner, limiting the reranker's blast radius.
3. **Fallback-to-Initial-Ranking Circuit Breaker**: Monitor reranker impact in real time and automatically fall back to the pre-rerank ranking if measured precision drops below a floor for a given traffic segment.

### Metrics
1. **context_precision_before_rerank**: Target: continuously tracked baseline
2. **context_precision_after_rerank**: Target: >= before_rerank; Alert threshold: < before_rerank - 0.1
3. **top1_swap_rate**: Target: < 20%; Alert threshold: monitored jointly with precision delta
4. **domain_segment_degradation_rate**: Target: < 15% of domain-specific queries degraded; Alert threshold: > 25%

### Alerts
1. **Reranker Precision Regression** (P1): Condition - context_precision_after_rerank drops more than 0.1 below the pre-rerank baseline for a query segment. Action: disable the reranker for that segment, fall back to initial ranking, investigate domain fit.
2. **Systematic Correct-Answer Demotion** (P2): Condition - the sampled top-1 swap audit finds correct-but-terse documents repeatedly demoted below verbose-incorrect ones. Action: retrain the reranker with length/fluency debiasing, add adversarial training pairs.
3. **Domain Segment Underperformance** (P2): Condition - domain_segment_degradation_rate exceeds 25% for a specific content type. Action: exclude that segment from reranking or apply a segment-specific reranker model.

## References

- [RAGAS Context Precision](https://docs.ragas.io/en/latest/concepts/metrics/context_precision.html) - Ranking quality metric
- [Cross-Encoder Reranking](https://www.sbert.net/examples/applications/cross-encoder/README.html) - Reranker architecture
- [Pinecone Reranking](https://www.pinecone.io/learn/series/rag/rerankers/) - When rerankers help/hurt
- [ColBERT v2 Analysis](https://arxiv.org/abs/2112.01488) - Domain transfer challenges
