# Tool Call Latency Accumulation

## Issue: Sequential Tool Calls Create Unacceptable Total Latency

**Frequency**: Common

**Symptoms**
- Simple queries fast, complex queries extremely slow
- Latency scales linearly with tool call count
- Users abandon multi-step workflows
- Timeouts on agentic tasks

**Root Cause**
Each tool call adds latency (network, processing, response parsing). Sequential tool calls accumulate, turning a 500ms operation into a 10+ second workflow. No parallelization or optimization.

**Example**
```
Query: "What's the weather in NYC and book me a flight there"

Sequential execution:
1. Parse intent: 200ms
2. Weather API call: 800ms
3. LLM processes weather: 500ms
4. Flight search API: 1200ms
5. LLM processes flights: 600ms
6. Booking API: 900ms
7. Final response: 300ms
Total: 4.5 seconds

With parallelization:
1. Parse intent: 200ms
2. Weather + Flight search (parallel): 1200ms
3. LLM processes both: 700ms
4. Booking: 900ms
5. Response: 300ms
Total: 3.3 seconds (27% faster)
```

**Contributing Factors**
- No tool call parallelization
- Synchronous API calls
- No caching of repeated calls
- Chatty tool interfaces
- No timeout budgets per tool

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Multi-tool query | 3+ tool calls needed | < 5s total | > 10s |
| Parallel opportunity | Independent tools | Parallel execution | Sequential |
| Repeated tool call | Same API twice | Cache hit | Duplicate call |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Latency per tool call | < 500ms | Individual tool timing |
| Tool parallelization rate | > 50% | parallel / total possible |
| Total tool overhead | < 50% of response time | tool_time / total_time |

---

## Mitigation Strategies

### Prevention
1. **Parallelize independent tools**: Call non-dependent tools concurrently
2. **Tool result caching**: Cache recent results
3. **Batched tool calls**: Combine multiple calls where possible
4. **Timeout budgets**: Allocate time per tool, fail fast
5. **Prefetching**: Anticipate likely tool needs

### Parallel Execution
```python
async def execute_tools_optimized(tool_calls):
    # Group into dependency levels
    independent = [t for t in tool_calls if not t.depends_on]
    dependent = [t for t in tool_calls if t.depends_on]
    
    # Execute independent tools in parallel
    results = await asyncio.gather(*[
        execute_with_timeout(t, timeout=2.0)
        for t in independent
    ])
    
    # Then execute dependent tools
    for tool in dependent:
        results.append(await execute_with_timeout(tool, timeout=2.0))
    
    return results
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `tool.calls.per_request` | > 5 |
| `tool.total_latency` | > 3s |
| `tool.parallelization.rate` | < 30% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Tool Chain Too Long | calls > 7 | P3 |
| Tool Latency Excessive | total > 5s | P2 |
| No Parallelization | parallel_rate = 0% | P3 |

---

## References

- [Agentic Tool Optimization](https://www.anthropic.com/research/building-effective-agents)
- [Async Tool Patterns](https://langchain.readthedocs.io/en/latest/modules/agents/async_agents.html)
