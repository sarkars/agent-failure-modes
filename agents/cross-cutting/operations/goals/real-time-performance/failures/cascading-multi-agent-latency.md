# Cascading Multi-Agent Latency

## Issue: Sequential Agent Calls Create Unacceptable End-to-End Latency

**Frequency**: Common in multi-agent systems

**Symptoms**
- Multi-agent workflows take 10x+ single agent time
- Each agent adds full inference latency
- Orchestration overhead compounds
- Users abandon complex tasks

**Root Cause**
Multi-agent architectures chain multiple LLM calls. Each agent adds inference time, communication overhead, and potential retries. Without parallelization and smart orchestration, latency grows linearly with agent count.

**Example**
```
Research assistant with 4 agents:

Sequential execution:
1. Router agent: 400ms
2. Search agent: 1200ms (includes API calls)
3. Analysis agent: 800ms
4. Writer agent: 1500ms
5. Orchestration overhead: 200ms
Total: 4100ms

User expectation: ~2 seconds
Actual: 4+ seconds

With 2 more review agents: 6+ seconds
Each agent adds ~1s minimum.
```

**Contributing Factors**
- Sequential agent execution
- No agent parallelization
- Heavy orchestration overhead
- Each agent is a full LLM call
- No result caching between agents
- Verbose inter-agent communication

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Agent count scaling | 2, 4, 6 agents | Sub-linear growth | Linear growth |
| Parallel opportunity | Independent agents | Parallel execution | Sequential |
| Orchestration overhead | N agents | < 10% of total | > 25% |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Latency per agent | < 1s | total / agent_count |
| Parallelization rate | > 40% | parallel_time / sequential_time |
| Orchestration overhead | < 15% | orchestration / total |

---

## Mitigation Strategies

### Prevention
1. **Parallel agent execution**: Run independent agents concurrently
2. **Agent result caching**: Cache and reuse agent outputs
3. **Lightweight agents**: Use smaller models for routing/simple tasks
4. **Speculative execution**: Start likely-needed agents early
5. **Streaming between agents**: Pass partial results

### Optimized Orchestration
```python
class LatencyOptimizedOrchestrator:
    def __init__(self):
        self.agent_cache = TTLCache(maxsize=100, ttl=300)
    
    async def execute_workflow(self, task):
        # Phase 1: Route and identify needed agents
        route_start = time.time()
        agents_needed = await self.router.route(task)  # Use fast model
        
        # Phase 2: Group by dependencies
        independent = [a for a in agents_needed if not a.depends_on]
        dependent = [a for a in agents_needed if a.depends_on]
        
        # Phase 3: Execute independent agents in parallel
        results = {}
        parallel_tasks = []
        
        for agent in independent:
            cache_key = agent.cache_key(task)
            if cache_key in self.agent_cache:
                results[agent.name] = self.agent_cache[cache_key]
            else:
                parallel_tasks.append(self.run_agent(agent, task))
        
        parallel_results = await asyncio.gather(*parallel_tasks)
        for agent, result in zip(independent, parallel_results):
            results[agent.name] = result
            self.agent_cache[agent.cache_key(task)] = result
        
        # Phase 4: Execute dependent agents (may also parallelize)
        for agent in dependent:
            deps = {d: results[d] for d in agent.depends_on}
            results[agent.name] = await self.run_agent(agent, task, deps)
        
        return results
    
    async def run_agent(self, agent, task, deps=None):
        # Use appropriate model size for agent type
        if agent.type == "router":
            model = "fast-small"
        elif agent.type == "analysis":
            model = "capable-medium"
        else:
            model = "default"
        
        return await agent.execute(task, deps, model=model)
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `workflow.total_latency` | > 5s |
| `workflow.agents.count` | > 5 |
| `workflow.parallelization` | < 20% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Workflow Too Slow | latency > 10s | P2 |
| Too Many Agents | count > 7 | P3 |
| No Parallelization | parallel = 0% | P3 |

---

## References

- [Multi-Agent Architectures](https://www.anthropic.com/research/building-effective-agents)
- [MAST: Multi-Agent Failures](https://arxiv.org/abs/2503.13657)
