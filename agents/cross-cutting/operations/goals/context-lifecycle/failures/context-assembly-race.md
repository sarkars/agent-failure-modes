# Context Assembly Race

## Issue: Race Conditions During Context Assembly Cause Inconsistent State

**Frequency**: Occasional

**Symptoms**
- Missing context elements intermittently
- Duplicate content in context
- Inconsistent behavior across requests
- Context order varies unexpectedly
- Partial updates visible

**Root Cause**
Context assembly often pulls from multiple sources: conversation history, RAG results, tool outputs, memory. If these are assembled concurrently without synchronization, race conditions occur. One request may see incomplete RAG results while another sees duplicates. Async operations without proper coordination cause inconsistent context.

**Example**
```
Context assembly (concurrent):

Thread 1: Fetch conversation history
Thread 2: Fetch RAG results
Thread 3: Fetch user preferences
Thread 4: Assemble final context

Race condition scenario:
  T=0:  Thread 1 starts
  T=5:  Thread 2 starts
  T=10: Thread 4 starts assembly (too early!)
        - History: partially loaded
        - RAG: not started
        - Preferences: missing
  T=15: Thread 2 completes (too late)
  T=20: Thread 3 completes (too late)

Result: Context missing RAG and preferences
        Agent gives poor response
        
Next request: All threads complete
        Agent gives good response
        
Inconsistent behavior!
```

**Contributing Factors**
- Async context fetching without coordination
- No assembly barriers/synchronization
- Timeout handling creates partial state
- Concurrent writes to shared context
- No context validation before use
- Optimistic assembly without checks

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Concurrent assembly | Parallel sources | All included | Missing elements |
| Slow source | One source delayed | Wait or graceful degrade | Race/partial |
| High concurrency | Many simultaneous requests | Consistent | Variable results |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Assembly completeness | 100% | All sources included |
| Assembly consistency | 100% | Same inputs = same context |
| Race condition rate | 0% | Detected races / requests |

---

## Mitigation Strategies

### Prevention
1. **Synchronization barriers**: Wait for all sources
2. **Timeout with fallback**: Degrade gracefully, don't assemble partial
3. **Atomic assembly**: All-or-nothing context building
4. **Validation checks**: Verify completeness before use
5. **Idempotent sources**: Same fetch = same result
6. **Sequential fallback**: If races detected, go sequential

### Architecture Pattern
```python
async def assemble_context():
    # Fetch all sources concurrently
    results = await asyncio.gather(
        fetch_history(),
        fetch_rag(),
        fetch_preferences(),
        return_exceptions=True
    )
    
    # Validate all succeeded
    if any(isinstance(r, Exception) for r in results):
        return fallback_context()
    
    # Assemble atomically
    return Context(
        history=results[0],
        rag=results[1],
        preferences=results[2]
    )
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `assembly.completeness` | <100% |
| `assembly.timeout_rate` | >5% |
| `assembly.consistency_score` | <99% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Incomplete Assembly | Missing sources | P2 |
| Assembly Timeout | Source timeout | P3 |
| Consistency Violation | Same input, different context | P2 |

---

## References

- [Async Coordination Patterns](https://docs.python.org/3/library/asyncio.html)
- [Distributed Systems Coordination](https://martinfowler.com/)
