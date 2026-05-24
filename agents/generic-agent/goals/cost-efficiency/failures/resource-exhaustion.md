# Resource Exhaustion

## Issue: Agent Exceeds Allocated Resources Before Completion

**Frequency**: Common

**Symptoms**
- Task terminates due to turn limit
- Token budget exceeded mid-task
- Timeout before completion
- Incomplete results due to resource caps

**Root Cause**
Agent fails due to exceeding allocated maximum number of turns or tokens before task completion. This occurs when agents take inefficient paths through tasks, make unnecessary tool calls, or face complex tasks that genuinely require more resources than allocated.

**Example**
```
Task: "Summarize all customer complaints from last month"

Resource limits: 50 turns, 100K tokens

Agent trace:
Turn 1-5:   Get customer list (works)
Turn 6-30:  Fetch each complaint individually (inefficient)
Turn 31-45: Start summarizing first batch
Turn 46-50: Continue summarizing...
Turn 50:    [TERMINATED - Turn limit reached]

Result: Only 60% of complaints processed
        Summary is incomplete
        Task marked as failed
```

**Resource Exhaustion Types**
- **Turn exhaustion**: Exceeds maximum interaction turns
- **Token exhaustion**: Exceeds context or generation limits
- **Time exhaustion**: Exceeds wall-clock timeout
- **API exhaustion**: Exceeds rate limits or quotas
- **Compute exhaustion**: Exceeds compute budget

**Key Statistics**
From Aegis study: Resource exhaustion is a distinct failure category, accounting for failures where agents run out of allocated resources before completing tasks.
- $47,000 spent on single 11-day agent loop (DEV.to incident)
- $437 overnight from unchecked agent run

**Contributing Factors**
- Inefficient tool call patterns
- Verbose reasoning consuming tokens
- Retry loops eating resources
- Complex tasks with many steps
- No progress toward completion

**Mitigation Strategies**
1. **Speculative actions**: Bundle related tool calls to reduce turns
2. **Token budgeting**: Track and report remaining budget
3. **Efficiency guidance**: Suggest efficient paths through tasks
4. **Early termination**: Stop before exhaustion with partial results
5. **Progress checkpoints**: Save progress for resumption
6. **Resource-aware planning**: Plan tasks within resource constraints

**Detection**
- Tasks terminated at resource limits
- Increasing resource usage without progress
- Incomplete results from resource-limited runs
- Pattern of exhaustion on similar tasks

## References

- [Aegis: Agent-Environment Failures](https://arxiv.org/abs/2508.19504) - Resource exhaustion as distinct failure category
- [DEV.to: $47,000 Agent Loop](https://dev.to/waxell/the-47000-agent-loop-why-token-budget-alerts-arent-budget-enforcement-389i) - Real resource exhaustion incident
- [LeanOps: Agents Burn 50x More Tokens](https://leanopstech.com/blog/agentic-ai-cost-runaway-token-budget-2026/) - Token efficiency analysis
