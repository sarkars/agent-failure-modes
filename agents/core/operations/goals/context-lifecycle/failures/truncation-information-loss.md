# Truncation Information Loss

## Issue: Critical Information Lost When Context is Truncated

**Frequency**: Very Common

**Symptoms**
- Agent forgets earlier conversation context
- Important instructions get cut off
- References to truncated content fail
- Response quality degrades in long conversations
- Agent contradicts earlier statements

**Root Cause**
When context exceeds the window limit, truncation removes content - typically from the beginning (oldest first). If critical information (user preferences, key facts, early instructions) is in truncated portions, the agent loses access to it. Simple FIFO truncation doesn't consider information importance.

**Example**
```
Context window: 8K tokens
Conversation reaches: 12K tokens

Truncation (FIFO - first in, first out):
  [TRUNCATED] User: "Always respond in Spanish"
  [TRUNCATED] User: "My account number is 12345"
  [KEPT] ... recent messages ...
  [KEPT] User: "What's my account number?"

Agent: "I don't have your account number. 
        Could you provide it?"  (in English)

Two failures:
1. Forgot account number (truncated)
2. Forgot language preference (truncated)
```

**Contributing Factors**
- Simple FIFO truncation
- No importance weighting
- No summary of truncated content
- Large system prompts leaving less room
- No semantic deduplication
- Truncation at arbitrary boundaries

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Key fact retention | Fact at start, query at end | Fact recalled | Information lost |
| Instruction persistence | Early instruction | Still followed | Ignored |
| Multi-reference | Reference across window | Consistent | Contradiction |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Key fact retention | >95% | Recall after truncation |
| Instruction compliance | 100% | Early instructions followed |
| Consistency score | >90% | Cross-turn consistency |

---

## Mitigation Strategies

### Prevention
1. **Importance scoring**: Weight content by relevance
2. **Summarization**: Summarize truncated content
3. **Key extraction**: Extract and preserve key facts
4. **Sliding window with summary**: Keep summary of old content
5. **Semantic deduplication**: Remove redundant content first
6. **Protected sections**: Never truncate critical instructions

### Architecture Pattern
```
[System Prompt - PROTECTED]
[Key Facts Summary - PROTECTED]
[Summarized History - Compressible]
[Recent Context - Full detail]
[Current Turn - Full detail]
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `truncation.frequency` | Track trend |
| `truncation.key_fact_loss` | >0 |
| `consistency.cross_turn` | <90% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Critical Truncation | System prompt affected | P1 |
| High Truncation Rate | >50% of sessions | P3 |
| Consistency Drop | <80% cross-turn | P2 |

---

## References

- [Lost in the Middle](https://arxiv.org/abs/2307.03172)
- [LongLLMLingua](https://arxiv.org/abs/2310.06839)
