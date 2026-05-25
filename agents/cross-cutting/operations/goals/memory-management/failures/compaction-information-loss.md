# Compaction Information Loss

## Issue: Memory Compaction Removes Critical Information

**Frequency**: Common

**Symptoms**
- Old but important information disappears
- Agent forgets established patterns
- Long-term context degrades over time
- Critical historical decisions lost
- User relationships not maintained

**Root Cause**
Memory systems compact old data to manage storage and retrieval costs. Compaction strategies may remove information based on age, access frequency, or size - without considering importance. Critical information that isn't accessed frequently may be compacted away.

**Example**
```
Memory compaction policy:
- Remove memories >30 days old
- Keep only top 1000 memories by access frequency

User's stored memories:
- Daily: "Prefers brief responses" (accessed daily)
- Critical: "Has peanut allergy" (stored 45 days ago, rarely accessed)
- Critical: "VIP customer, escalate issues" (stored 60 days ago)

After compaction:
✓ "Prefers brief responses" (kept - frequent access)
✗ "Has peanut allergy" (removed - old, rarely accessed)
✗ "VIP customer" (removed - old)

Later:
User: "What should I avoid eating?"
Agent: "I don't have dietary information for you."

User: "I have a complaint"
Agent: [Normal handling, not escalated]

Failures due to compacted critical information
```

**Contributing Factors**
- Age-only compaction policies
- No importance scoring
- Access frequency bias
- No critical fact protection
- Aggressive compaction ratios
- No validation before compaction

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Critical retention | Critical old memory | Preserved | Compacted |
| Age handling | Memories of various ages | Important kept | Age-biased removal |
| Post-compaction query | Query old facts | Retrieved | Not found |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Critical retention | 100% | Critical facts after compaction |
| Information fidelity | >95% | Useful info retained |
| Compaction recall | >90% | Can recall compacted-era info |

---

## Mitigation Strategies

### Prevention
1. **Importance scoring**: Protect high-importance memories
2. **Protected categories**: Never compact safety/critical info
3. **Validation before compaction**: Check what's being removed
4. **Hierarchical compaction**: Summarize instead of delete
5. **Access decay**: Gradual importance decay, not cliff
6. **User-tagged important**: Let users mark critical memories

### Compaction Policy
```
Priority levels:
  P0 (Never compact): Safety info, allergies, VIP status
  P1 (Summarize only): Key preferences, patterns
  P2 (Age-based): Transactional history
  P3 (Aggressive): Ephemeral context

Compaction:
  P3: Delete after 7 days
  P2: Summarize after 30 days
  P1: Archive after 90 days (still searchable)
  P0: Never remove
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `compaction.critical_removed` | >0 |
| `compaction.size_reduction` | >50% |
| `memory.post_compact_recall` | <90% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Critical Memory Removed | P0 memory compacted | P1 |
| High Information Loss | >30% removed | P2 |
| Recall Degradation | <80% post-compaction | P2 |

---

## References

- [Memory Management in AI](https://arxiv.org/abs/2312.08901)
- [Long-term Memory Systems](https://www.pinecone.io/learn/)
