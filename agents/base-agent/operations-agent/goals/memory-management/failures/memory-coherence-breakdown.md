# Memory Coherence Breakdown

## Issue: Retrieved Memories Contradict Each Other

**Frequency**: Common

**Symptoms**
- Agent states contradictory facts
- Different sessions have conflicting information
- User receives inconsistent responses
- Agent acknowledges contradictions but can't resolve
- Memory contains multiple versions of truth

**Root Cause**
Over time, memory accumulates conflicting information: corrections, updates, different contexts. Without coherence management, retrieval may return contradictory memories. The agent then produces confused responses or arbitrarily picks one version.

**Example**
```
Memories retrieved:
- "User's favorite color is blue" (2024-01)
- "User said they hate blue" (2024-06)
- "User prefers blue for work, red for personal" (2024-08)

Query: "What color should I use?"

Without coherence management:
Agent: "You like blue... but also hate blue... 
        but prefer blue for work..."
User: Confused and frustrated

With coherence management:
Agent: "For work contexts, you've said you prefer blue.
        For personal use, you prefer red. Which context
        is this for?"
```

**Contributing Factors**
- No conflict detection
- All versions stored without reconciliation
- No source/context tracking
- Updates append instead of replace
- No truth arbitration logic
- Missing provenance metadata

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Conflict detection | Contradictory memories | Detected | Unnoticed |
| Resolution | Conflicting facts | Coherent response | Contradiction stated |
| Update handling | Old + new info | Latest used | Both conflated |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Contradiction rate | <5% | Contradictions / retrievals |
| Coherence score | >90% | User-rated consistency |
| Resolution rate | >95% | Conflicts resolved correctly |

---

## Mitigation Strategies

### Prevention
1. **Conflict detection**: Identify contradictory memories
2. **Source tracking**: Record where each fact came from
3. **Version management**: Updates replace, not append
4. **Context tagging**: Tag facts with applicable context
5. **Resolution logic**: Rules for which version wins
6. **User confirmation**: Ask user to resolve conflicts

### Coherence Framework
```
On retrieval:
1. Fetch candidate memories
2. Detect conflicts (semantic similarity + contradiction)
3. Resolve conflicts:
   - Same context: Use most recent
   - Different contexts: Keep both, tag context
   - Uncertain: Ask user
4. Return coherent set
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `memory.conflict_rate` | >10% |
| `memory.unresolved_conflicts` | >0 |
| `user.confusion_signals` | >5% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| High Conflict Rate | >20% contradictions | P2 |
| Unresolved Conflict | Contradiction in response | P2 |
| User Confusion | Reports inconsistency | P2 |

---

## References

- [Knowledge Base Consistency](https://arxiv.org/abs/2010.12688)
- [Belief Revision in AI](https://plato.stanford.edu/entries/logic-belief-revision/)
