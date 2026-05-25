# Memory Retrieval Failures

## Issue: Relevant Memories Not Retrieved When Needed

**Frequency**: Common

**Symptoms**
- Agent doesn't recall previous conversations
- Relevant context not included
- User must repeat information
- Agent behaves inconsistently across sessions
- Important preferences forgotten

**Root Cause**
Long-term memory systems use embedding-based retrieval to find relevant past context. If the query doesn't semantically match stored memories, relevant information isn't retrieved. Poor embeddings, wrong similarity thresholds, or missing metadata filters cause retrieval failures.

**Example**
```
Memory store contains:
- "User prefers dark mode" (stored 3 days ago)
- "User's timezone is PST" (stored 1 week ago)
- "User allergic to peanuts" (stored 1 month ago)

Query: "What display settings should I use?"

Embedding similarity search:
- "dark mode" ↔ "display settings": 0.72 (below threshold)
- "timezone" ↔ "display settings": 0.45 
- "allergic" ↔ "display settings": 0.30

Threshold: 0.75

Result: No memories retrieved
Agent: "I don't have your display preferences saved."

Expected: Recall dark mode preference
```

**Contributing Factors**
- Embedding model mismatch
- Similarity threshold too high
- No metadata filtering (recency, type)
- Query reformulation not attempted
- Memory not indexed properly
- No fallback retrieval strategies

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Direct recall | Query matches memory | Memory retrieved | Not found |
| Semantic match | Paraphrased query | Memory retrieved | Not found |
| Cross-session | Multi-session context | Relevant recalled | Forgotten |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Retrieval recall | >90% | Relevant found / relevant exist |
| Retrieval precision | >80% | Relevant / retrieved |
| User repeat rate | <10% | Times user repeats info |

---

## Mitigation Strategies

### Prevention
1. **Query expansion**: Try multiple query formulations
2. **Hybrid retrieval**: Combine semantic + keyword search
3. **Dynamic thresholds**: Adjust based on query type
4. **Metadata filters**: Filter by recency, type, importance
5. **Retrieval validation**: Check if retrieval seems complete
6. **Explicit memory prompts**: "Remember when we discussed..."

### Architecture Pattern
```
Query → [Query Expansion] → [Semantic Search]
              ↓                    ↓
        [Keyword Search]    [Combine Results]
              ↓                    ↓
        [Metadata Filter] → [Ranked Results]
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `memory.retrieval_empty` | >20% |
| `memory.user_repeat_rate` | >15% |
| `memory.relevance_score` | <0.7 |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| High Miss Rate | >30% empty retrievals | P2 |
| User Frustration | >3 repeats in session | P2 |
| Low Relevance | Mean score <0.6 | P3 |

---

## References

- [Dense Retrieval](https://arxiv.org/abs/2004.04906)
- [Hybrid Search](https://www.pinecone.io/learn/hybrid-search-intro/)
