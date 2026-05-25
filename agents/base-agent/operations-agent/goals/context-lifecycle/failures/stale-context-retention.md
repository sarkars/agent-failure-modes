# Stale Context Retention

## Issue: Outdated Information Kept While Current Information Discarded

**Frequency**: Common

**Symptoms**
- Agent references outdated information
- Recent corrections ignored
- Old versions of facts used
- Updates don't take effect
- Agent contradicts recent statements

**Root Cause**
Context management may retain old information while discarding newer updates. If a user corrects information or provides updates, FIFO truncation keeps the old (incorrect) version longer. Without staleness tracking, the agent uses outdated context.

**Example**
```
Turn 1: User: "My address is 123 Main St"
        Agent: "Got it, 123 Main St"

Turn 15: User: "Actually, I moved. New address is 456 Oak Ave"
         Agent: "Updated to 456 Oak Ave"

Turn 40 (context near limit, FIFO truncation):
  [TRUNCATED] Turn 15: Address update to 456 Oak Ave
  [KEPT] Turn 1: Address is 123 Main St
  
Turn 41: User: "Send the package to my address"
         Agent: "Sending to 123 Main St"
         
Failure: Old address used, recent update truncated
```

**Contributing Factors**
- No timestamp-based prioritization
- Updates don't invalidate old versions
- FIFO keeps first mention, not latest
- No semantic deduplication
- No fact versioning
- Corrections not specially handled

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Fact update | Update value, query later | New value | Old value |
| Correction handling | Correct mistake | Correction used | Mistake repeated |
| Version conflict | Multiple versions exist | Latest used | Old used |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Update retention | 100% | Updates survive truncation |
| Fact freshness | Latest | Most recent version used |
| Correction compliance | 100% | Corrections applied |

---

## Mitigation Strategies

### Prevention
1. **Fact versioning**: Track versions of key facts
2. **Update precedence**: Updates replace, not append
3. **Semantic dedup**: Remove old versions of same fact
4. **Recency weighting**: Prioritize recent over old
5. **Explicit correction handling**: Mark and prioritize corrections
6. **Key-value memory**: Structured fact storage with updates

### Architecture Pattern
```
Facts memory:
{
  "user.address": {
    "value": "456 Oak Ave",
    "updated": "turn 15",
    "previous": ["123 Main St"]
  }
}

On truncation: Keep latest value, discard history
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `fact.version_conflicts` | >0 |
| `update.retention_rate` | <100% |
| `correction.applied_rate` | <100% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Stale Fact Used | Old version in response | P2 |
| Update Lost | Recent update truncated | P2 |
| Correction Ignored | Correction not applied | P2 |

---

## References

- [Memory in LLM Agents](https://arxiv.org/abs/2312.08901)
- [LangChain: Conversation Memory](https://python.langchain.com/docs/modules/memory/)
