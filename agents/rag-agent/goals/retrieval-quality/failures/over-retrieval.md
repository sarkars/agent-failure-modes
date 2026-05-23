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

**Mitigation Strategies**
1. **Dynamic top-K**: Adjust based on query specificity
2. **Relevance thresholds**: Set minimum similarity scores
3. **Re-ranking**: Use cross-encoder to re-score results
4. **Diversity filtering**: Remove near-duplicates
5. **Query classification**: Route to appropriate retrieval strategy
6. **Maximal Marginal Relevance (MMR)**: Balance relevance and diversity

**Detection**
- Track context utilization (how much retrieved content is used)
- Monitor retrieval-to-answer ratio
- Analyze diversity of retrieved documents
- User feedback on answer quality vs. retrieval volume
