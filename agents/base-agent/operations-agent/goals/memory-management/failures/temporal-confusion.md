# Temporal Confusion

## Issue: Agent Confuses When Events Occurred

**Frequency**: Common

**Symptoms**
- Agent reports wrong timeframes
- Recent events described as old
- Historical events treated as current
- "Last time" refers to wrong session
- Temporal ordering incorrect

**Root Cause**
Memory systems often store content without robust timestamps or temporal context. When retrieved, the agent may not know when something occurred. "You mentioned this before" could be yesterday or 6 months ago. Without temporal metadata, the agent conflates past and present.

**Example**
```
Memory contains:
- "User complained about slow performance" (January 2025)
- "User upgraded to premium plan" (March 2025)
- "User praised new feature" (June 2025)

User query (July 2025): "How has my experience been?"

Agent (without temporal context):
"You've had performance issues and praised our new feature."

Agent (with temporal context):
"You initially had performance concerns in January,
upgraded to premium in March, and recently praised
our new feature in June. Your experience has improved
over time."

Without temporal context:
- No sense of progression
- Can't identify trends
- May reference resolved issues as current
```

**Contributing Factors**
- Missing timestamps in memory
- No temporal reasoning in retrieval
- All memories treated as equally current
- No "as of" context in responses
- Relative time references not resolved
- No temporal ordering in retrieval

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Recency detection | "What did I say recently?" | Recent items | Old items |
| Temporal ordering | Multi-event query | Correct order | Wrong sequence |
| Resolved issues | Past problem | Marked as past | Treated as current |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Temporal accuracy | >95% | Correct time references |
| Ordering accuracy | 100% | Events in right sequence |
| Recency precision | >90% | "Recent" = actually recent |

---

## Mitigation Strategies

### Prevention
1. **Timestamp all memories**: Record creation time
2. **Temporal metadata**: Include "as of", "valid until"
3. **Temporal retrieval**: Filter by time relevance
4. **Explicit time context**: Include dates in responses
5. **Temporal resolution**: Convert "last week" to dates
6. **State tracking**: Mark issues as resolved/current

### Memory Schema
```json
{
  "content": "User complained about performance",
  "created_at": "2025-01-15T10:30:00Z",
  "valid_until": "2025-03-01T00:00:00Z",
  "status": "resolved",
  "resolution": "Upgraded to premium",
  "temporal_tags": ["past_issue", "resolved"]
}
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `memory.temporal_coverage` | <90% |
| `memory.ordering_errors` | >0 |
| `memory.stale_as_current` | >0 |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Temporal Confusion | Past treated as present | P2 |
| Missing Timestamps | >10% without timestamp | P3 |
| Ordering Error | Events in wrong sequence | P2 |

---

## References

- [Temporal Reasoning in NLP](https://arxiv.org/abs/2010.12753)
- [Time-Aware Memory](https://arxiv.org/abs/2312.08901)
