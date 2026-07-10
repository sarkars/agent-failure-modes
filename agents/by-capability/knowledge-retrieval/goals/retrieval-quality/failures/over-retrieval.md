# Over-Retrieval

## Issue: Too Many Documents Retrieved, Mostly Irrelevant

**Frequency**: Common

**Symptoms**
- Context window filled with marginally relevant content
- Relevant documents buried among irrelevant ones
- Model confused by conflicting information
- Latency increases from processing excess documents

**Root Cause**
- Retrieval threshold too low
- Top-K too high for query type
- Similar but irrelevant documents in corpus
- Broad queries matching many documents

**Example**
```
Query: "What is the refund policy?"

Retrieved (top 10):
1. Refund Policy document (relevant) ✓
2. Return Shipping Guide (somewhat relevant)
3. Customer FAQ - refunds section (relevant) ✓
4. 2019 Refund Policy (outdated)
5. Refund Request Form Template
6. Blog post mentioning refunds
7. Employee refund expense policy (wrong context)
8. Competitor comparison mentioning refunds
9. Legal terms with refund clause
10. Marketing email about "refund your time"

Result: 2 relevant docs buried in 8 irrelevant/distracting ones
```

## Mitigation Strategies

### Prevention
1. **Query-Adaptive Top-K**: Set retrieval count dynamically based on query specificity — narrow factual queries get k=3-5, broad exploratory queries get k=10+ — instead of a single fixed k that over-retrieves for simple queries like the refund policy example.
2. **Similarity-Threshold Gating**: Enforce a minimum similarity cutoff, not just a fixed count, so borderline matches like "Blog post mentioning refunds" are excluded even when they'd otherwise fill out a fixed top-k slot.
3. **Near-Duplicate and Off-Context Suppression**: Deduplicate and filter documents with high lexical overlap but different context (e.g., "Employee refund expense policy" vs. "Customer Refund Policy") using metadata/category checks before they enter the candidate set. Trade-off: requires reliable category metadata to distinguish context, not just topic.

### Detection & Response
1. **Context-Utilization Tracking**: Measure what fraction of retrieved content is actually referenced in the generated answer; a low utilization ratio signals over-retrieval is padding context with unused, irrelevant material.
2. **Retrieval-Volume vs. Answer-Quality Correlation**: Track whether increasing retrieved-document count correlates with degraded answer accuracy from conflicting information, and use this to calibrate top-k defaults per query type.
3. **Diversity/Redundancy Scoring**: Compute pairwise similarity within the retrieved set; alert when a high fraction of top-k results are near-duplicates rather than covering distinct relevant angles.

### Architecture Patterns
1. **Maximal Marginal Relevance (MMR) Re-Ranking**: After initial retrieval, re-rank to balance relevance against diversity, actively penalizing redundant near-duplicate results so limited context slots aren't consumed by variations of the same document.
2. **Two-Stage Recall-Then-Precision Funnel**: Retrieve a wide candidate set cheaply (recall-oriented), then apply a cross-encoder or relevance classifier to cut down to a precision-focused final k before passing to the LLM.
3. **Query-Type Routing**: Classify queries (narrow factual vs. broad exploratory) and route each type to a distinct retrieval configuration (different k, threshold, index) instead of a one-size-fits-all pipeline.

### Metrics
1. **context_utilization_rate**: Target: > 60%; Alert threshold: < 40%
2. **retrieved_set_avg_similarity_score**: Target: > 0.75; Alert threshold: < 0.6
3. **near_duplicate_rate_in_topk**: Target: < 15%; Alert threshold: > 30%
4. **avg_retrieved_doc_count_per_query**: Target: within configured range per query type; Alert threshold: unexplained upward drift

### Alerts
1. **Context Dilution** (P2): Condition - context_utilization_rate drops below 40% for a query category over 7 days. Action: reduce top-k or raise the similarity threshold for that category, review query classifier routing.
2. **Redundant Retrieval Spike** (P3): Condition - near_duplicate_rate_in_topk exceeds 30%. Action: enable/tune MMR re-ranking, review the corpus for duplicate content needing consolidation.
3. **Low-Relevance Floor Breach** (P2): Condition - retrieved_set_avg_similarity_score falls below 0.6. Action: raise the similarity threshold, audit whether the threshold configuration regressed.

## References

- [Mindee: RAG Hallucinations Explained](https://www.mindee.com/blog/rag-hallucinations-explained) - Over-retrieval problems
- [FloTorch: 2026 RAG Performance Landscape](https://www.flotorch.ai/blogs/the-2026-rag-performance-landscape-what-every-enterprise-leader-needs-to-know) - Retrieval optimization
