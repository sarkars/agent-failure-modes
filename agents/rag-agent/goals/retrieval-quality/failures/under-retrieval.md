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

**Mitigation Strategies**
1. **Lower thresholds with re-ranking**: Retrieve more, filter after
2. **Increase top-K for complex queries**: More docs for multi-faceted questions
3. **Multi-query retrieval**: Generate multiple query variants
4. **Recursive retrieval**: Use initial results to find more
5. **Knowledge graph augmentation**: Follow entity relationships
6. **Query decomposition**: Break complex queries into sub-queries

**Detection**
- Track "no information found" responses
- Monitor answer completeness scores
- Analyze queries with high hallucination rates
- Compare retrieved docs to known relevant docs
