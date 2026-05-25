# Context Size Latency Impact

## Issue: Large Context Windows Cause Quadratic Latency Growth

**Frequency**: Common

**Symptoms**
- Latency increases dramatically with conversation length
- Long documents have disproportionately slow processing
- Multi-turn conversations degrade over time
- Memory-heavy tasks timeout

**Root Cause**
Transformer attention is O(n²) in context length. Doubling context quadruples compute. Systems that blindly include full history or large documents see non-linear latency growth.

**Example**
```
Context size vs latency (same model):

1K tokens:   200ms
4K tokens:   450ms   (2.25x for 4x context)
16K tokens:  1800ms  (4x for 4x context)
64K tokens:  12000ms (6.7x for 4x context)

Real scenario - customer service chat:
Turn 1 (1K context): 300ms
Turn 5 (5K context): 800ms
Turn 10 (10K context): 2.1s
Turn 20 (20K context): 6.5s ← User frustrated

Without context management, every turn gets slower.
```

**Contributing Factors**
- No context pruning or summarization
- Full history included every turn
- Large documents loaded entirely
- No streaming for long contexts
- Wrong model for context size

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Context scaling | 1K, 4K, 16K, 64K | Sub-quadratic | Quadratic or worse |
| Long conversation | 20 turns | Stable latency | Linear growth |
| Document processing | 50K doc | Chunked efficiently | Single-pass timeout |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Latency/context slope | < 1.5x per 2x context | Regression analysis |
| Max context before timeout | Documented | Binary search |
| Context efficiency | > 80% relevant | relevant_tokens / total |

---

## Mitigation Strategies

### Prevention
1. **Context pruning**: Remove irrelevant history
2. **Summarization**: Compress old context
3. **Sliding window**: Only recent N turns
4. **Chunked processing**: Process documents in pieces
5. **Model selection**: Use models efficient for context size

### Context Management
```python
class ContextManager:
    def __init__(self, max_tokens=8000, summary_threshold=4000):
        self.max_tokens = max_tokens
        self.summary_threshold = summary_threshold
    
    def prepare_context(self, messages, documents):
        context = []
        token_count = 0
        
        # Always include system prompt
        context.append(messages[0])
        token_count += count_tokens(messages[0])
        
        # Recent messages (most important)
        recent = messages[-5:]
        for msg in recent:
            token_count += count_tokens(msg)
        
        # Summarize older messages if needed
        older = messages[1:-5]
        if older and token_count + count_tokens(older) > self.summary_threshold:
            summary = self.summarize(older)
            context.append({"role": "system", "content": f"Previous conversation summary: {summary}"})
        else:
            context.extend(older)
        
        context.extend(recent)
        
        # Chunk documents if too large
        for doc in documents:
            if count_tokens(doc) > 2000:
                relevant_chunk = self.extract_relevant(doc, messages[-1])
                context.append(relevant_chunk)
            else:
                context.append(doc)
        
        return context
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `context.tokens.p95` | > 80% of limit |
| `latency.per_token` | > 0.5ms |
| `context.efficiency` | < 50% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Context Near Limit | tokens > 90% max | P3 |
| Latency Scaling Bad | slope > 2x per 2x | P2 |
| Context Bloat | efficiency < 30% | P3 |

---

## References

- [Efficient Transformers Survey](https://arxiv.org/abs/2009.06732)
- [Context Compression](https://arxiv.org/abs/2310.06839)
