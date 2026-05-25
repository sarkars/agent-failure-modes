# Context Priority Inversion

## Issue: Low-Priority Content Displaces High-Priority Content

**Frequency**: Common

**Symptoms**
- Verbose tool outputs consume context
- Irrelevant RAG results included
- Important instructions at risk
- Recent low-value content kept over old high-value
- System prompt gets squeezed

**Root Cause**
Context assembly often doesn't consider content priority. A 5,000-token tool output is included fully while critical instructions get truncated. Without priority-based assembly and truncation, context fills with low-value content, displacing what matters most.

**Example**
```
Context budget: 8K tokens

Priorities should be:
1. System prompt (critical)
2. User preferences (high)  
3. Current query (high)
4. Relevant context (medium)
5. Tool outputs (low)

Actual assembly (no priority):
- System prompt: 1K tokens
- Tool output (full JSON dump): 6K tokens
- Current query: 500 tokens
- [NO ROOM] User preferences: truncated
- [NO ROOM] Relevant history: truncated

Result: 75% of context is verbose tool output
        Critical preferences lost
```

**Contributing Factors**
- No content prioritization
- Tools return verbose output
- RAG returns full documents
- FIFO assembly without scoring
- No content compression
- Fixed allocation per content type

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Priority preservation | High + low priority content | High preserved | High truncated |
| Tool output handling | Large tool response | Summarized | Full dump |
| System prompt safety | Near capacity | System prompt intact | Truncated |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| High-priority retention | 100% | Critical content present |
| Context efficiency | >70% | Useful tokens / total |
| System prompt integrity | 100% | Full prompt included |

---

## Mitigation Strategies

### Prevention
1. **Priority tiers**: Define strict priority levels
2. **Reserved budgets**: Guarantee space for critical content
3. **Tool output limits**: Cap/summarize tool responses
4. **RAG filtering**: Only include relevant chunks
5. **Dynamic allocation**: Adjust based on content value
6. **Compression by tier**: Compress low-priority first

### Priority Framework
```
Tier 1 (Protected): System prompt, safety rules
Tier 2 (Reserved): User preferences, key facts
Tier 3 (Allocated): Current query, recent turns
Tier 4 (Best effort): Tool outputs, RAG context
Tier 5 (Compressed): History, verbose content
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `context.tier1_coverage` | <100% |
| `context.low_priority_ratio` | >60% |
| `tool_output.size_p99` | >2K tokens |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| System Prompt Truncated | Tier 1 incomplete | P1 |
| Priority Inversion | Tier 4 > Tier 2 | P2 |
| Tool Output Bloat | Single output >4K | P3 |

---

## References

- [LangChain: Context Management](https://python.langchain.com/docs/modules/memory/)
- [Context Window Optimization](https://www.pinecone.io/learn/)
