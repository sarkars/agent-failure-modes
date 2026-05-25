# Working Memory Overflow

## Issue: Too Much Information Retrieved for Effective Use

**Frequency**: Common

**Symptoms**
- Agent overwhelmed with context
- Response quality degrades with more memory
- Important memories buried in noise
- "Lost in the middle" effects
- Retrieval returns too much, not best

**Root Cause**
Memory retrieval may return many relevant items, exceeding what the agent can effectively process. Unlike context truncation (which cuts), overflow means too much valid information is provided. The agent's attention is diluted across too many memories, reducing response quality.

**Example**
```
Memory query: "User's preferences"

Retrieved (all relevant, but too many):
1. Color preference: blue
2. Communication style: formal
3. Timezone: PST
4. Language: English
5. Response length: brief
6. Formatting: markdown
7. Technical level: expert
8. Industry: finance
9. Role: manager
10. Previous products used: A, B, C
11. Support history: 15 interactions
12. Feature requests: 8 items
13. ... (50 more memories)

All relevant, but agent can't use 65 memories effectively.

Result:
- Agent mentions some preferences, forgets others
- Inconsistent application of preferences
- Response doesn't reflect full context
```

**Contributing Factors**
- No retrieval limit (top-k)
- Low similarity threshold retrieves too much
- No relevance re-ranking
- All memories treated equally
- No summarization of retrieved memories
- Query too broad

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| High retrieval volume | Broad query | Top-k applied | >20 items |
| Quality vs quantity | Many vs few memories | Few performs better | More = worse |
| Focus test | 50 memories | Key ones used | Important buried |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Retrieval count | <15 | Memories per query |
| Key fact usage | >90% | Critical facts in response |
| Quality vs. volume | Positive correlation | Response quality by memory count |

---

## Mitigation Strategies

### Prevention
1. **Top-k limits**: Cap retrieval at effective amount (5-15)
2. **Re-ranking**: Rank by relevance, take top N
3. **Memory summarization**: Summarize before injection
4. **Query refinement**: Narrow broad queries
5. **Priority filtering**: Only high-priority above threshold
6. **Hierarchical retrieval**: Summary first, details on demand

### Optimal Retrieval
```python
def retrieve_memories(query, max_memories=10):
    # Get candidates
    candidates = memory_store.search(query, limit=50)
    
    # Re-rank by relevance
    ranked = reranker.rank(query, candidates)
    
    # Take top-k
    top_k = ranked[:max_memories]
    
    # Optional: summarize if still too much
    if total_tokens(top_k) > TOKEN_BUDGET:
        return summarize_memories(top_k)
    
    return top_k
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `memory.retrieval_count_p99` | >20 |
| `memory.total_tokens` | >context budget |
| `response.quality_vs_volume` | Negative correlation |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Retrieval Overflow | >25 memories | P3 |
| Context Budget Exceeded | Memories > budget | P2 |
| Quality Degradation | Quality drops with more memory | P2 |

---

## References

- [Lost in the Middle](https://arxiv.org/abs/2307.03172)
- [Retrieval Optimization](https://www.pinecone.io/learn/)
