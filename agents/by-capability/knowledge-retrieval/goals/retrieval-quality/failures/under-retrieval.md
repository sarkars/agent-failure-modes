# Under-Retrieval

## Issue: Relevant Documents Not Retrieved

**Frequency**: Common

**Symptoms**
- Agent says "I don't have information about that" incorrectly
- Answers incomplete when more information exists
- User must ask multiple follow-ups to get full picture
- Hallucination fills gaps that retrieval should fill

**Root Cause**
- Retrieval threshold too high
- Top-K too low
- Relevant documents poorly indexed
- Query doesn't match document embedding

**Example**
```
Query: "What are the system requirements?"

Knowledge base contains:
- Hardware Requirements document
- Software Dependencies guide  
- Installation Prerequisites
- Compatibility Matrix

Retrieved (top 3, threshold 0.8):
1. Hardware Requirements (score: 0.82) ✓

Not retrieved:
- Software Dependencies (score: 0.76)
- Installation Prerequisites (score: 0.71)
- Compatibility Matrix (score: 0.69)

Result: User only gets hardware info, misses software requirements
```

## Mitigation Strategies

### Prevention
1. **Recall-First Retrieval With Post-Filtering**: Lower the initial similarity threshold substantially to prioritize recall, then apply a reranker or relevance classifier as a second pass, rather than using a single high threshold that silently drops true positives just below the cutoff — like "Software Dependencies" at 0.76 being excluded by a 0.8 threshold in the example.
2. **Multi-Faceted Query Decomposition**: Detect when a query implies multiple sub-topics (e.g., "system requirements" spanning hardware, software, and installation) and decompose into sub-queries retrieved independently, then merge, instead of relying on a single top-k pull to capture every facet.
3. **Adaptive Top-K by Query Breadth**: Increase retrieved-document count for queries classified as broad/multi-faceted rather than applying a uniform top-3, since complex queries need proportionally more context to avoid gaps that get filled by hallucination.

### Detection & Response
1. **"No Information Found" False-Negative Tracking**: Flag every case where the agent reports missing information, then verify offline whether the knowledge base actually contained relevant content that was simply not retrieved; a high false-negative rate indicates threshold/top-k miscalibration.
2. **Answer Completeness Scoring Against Known Facets**: For domains with enumerable sub-topics like system requirements, score whether the answer covered all expected facets and trace incomplete answers back to specific documents that scored just below the retrieval cutoff.
3. **Hallucination-Rate Correlation With Retrieval Gaps**: Correlate flagged hallucinations with cases of low retrieved-document count or near-threshold exclusions, confirming that hallucination is filling gaps under-retrieval created.

### Architecture Patterns
1. **Recursive/Iterative Retrieval**: Use initial retrieval results to generate follow-up retrieval queries (entities or sub-topics mentioned in the first pass), progressively pulling in related documents the original query alone wouldn't surface.
2. **Knowledge Graph Augmentation**: Follow explicit entity/topic relationships (e.g., "Hardware Requirements" linked to "Software Dependencies" as siblings under "System Requirements") to pull in related documents even when their embedding similarity to the original query falls below threshold.
3. **Query Decomposition With Parallel Sub-Retrieval**: Break multi-faceted queries into independent sub-queries, retrieve for each in parallel, and merge/deduplicate results, ensuring lower-similarity facets like "Compatibility Matrix" at 0.69 still get a dedicated retrieval pass instead of competing against stronger matches in a single pooled top-k.

### Metrics
1. **no_info_found_false_negative_rate**: Target: < 5%; Alert threshold: > 10%
2. **facet_coverage_completeness_percent**: Target: > 90% for known multi-facet query types; Alert threshold: < 75%
3. **near_threshold_exclusion_rate**: Target: < 10% of relevant docs excluded within 0.1 of threshold; Alert threshold: > 20%
4. **hallucination_rate_on_low_retrieval_count**: Target: < 5%; Alert threshold: > 15%

### Alerts
1. **Recall Failure Spike** (P1): Condition - no_info_found_false_negative_rate exceeds 10% for a query category. Action: lower the similarity threshold or raise top-k for that category, add a reranking pass to compensate.
2. **Facet Coverage Gap** (P2): Condition - facet_coverage_completeness_percent falls below 75% for known multi-facet topics (e.g., system requirements). Action: enable query decomposition for that topic, review related-document linking.
3. **Hallucination-Driven-by-Gap Correlation** (P1): Condition - hallucination_rate_on_low_retrieval_count exceeds 15%. Action: treat as a retrieval defect, not a generation defect; prioritize threshold/top-k tuning over prompt changes.

## References

- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - Missing context leads to hallucination
- [RAGAS Fails 83% of Time](https://medium.com/data-science-collective/air-canada-lost-a-lawsuit-because-their-rag-hallucinated-yours-will-too-b92b6b9a4d39) - Retrieval failures
