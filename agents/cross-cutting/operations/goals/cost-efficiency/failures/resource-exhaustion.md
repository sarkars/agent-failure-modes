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

## Mitigation Strategies

### Prevention
1. **Bundled/batched tool calls instead of per-item turns**: The trace in the example shows turns 6-30 spent "fetch each complaint individually," burning more than half the 50-turn budget on fetch alone; bundle related fetches into fewer calls (e.g., a bulk-fetch API or parallel tool calls within one turn) so turn budget is preserved for the actual summarization work. Trade-off: bundling requires the underlying API to support multi-item requests, which isn't always available.
2. **Resource-aware upfront planning**: Before execution, estimate the turn/token cost of the task's natural steps (list → fetch → summarize) against the allocated budget (50 turns, 100K tokens) and choose an execution strategy that fits — e.g., if 100+ items exist, batch-fetch or paginate-and-summarize incrementally rather than one turn per item. Trade-off: planning overhead itself consumes a turn or two, and estimates can be wrong for tasks with unknown item counts.
3. **Budget-remaining awareness threaded into agent context**: Since the agent in the example proceeded obliviously until hard termination at turn 50, surface remaining turn/token budget to the agent's reasoning at each step so it can adapt strategy (e.g., switch to a coarser summary) before hitting the wall rather than being cut off mid-task. Trade-off: constantly recomputing and injecting budget state adds a small token overhead per turn.

### Detection & Response
1. **Turns-consumed-per-phase tracking**: Break down turn consumption by task phase (list, fetch, summarize) as in the example trace; a phase like "fetch" consuming 50%+ of budget (25 of 50 turns) before any summarization begins is a leading indicator the task will exhaust before completion.
2. **Progress-per-turn ratio**: Track a completion-percentage delta per turn; the example shows only 60% of complaints processed by termination — a declining or flat progress-per-turn ratio partway through a task should trigger a strategy change (e.g., switch to batch fetch) before the hard limit is hit.
3. **Exhaustion pattern recurrence by task template**: Log which task types/templates repeatedly hit resource limits (per "Pattern of exhaustion on similar tasks"); recurring exhaustion on the same task shape (e.g., "summarize all X from last month") indicates the allocated budget or default execution strategy is structurally undersized for that task class.

### Architecture Patterns
1. **Speculative/parallel tool-call batching**: Issue multiple independent tool calls within a single turn (e.g., fetch all complaint IDs' details in one parallelized batch) instead of one tool call per turn, directly addressing the turns 6-30 inefficiency in the example. Deployment consideration: requires the agent framework to support multi-call turns and the backend to handle concurrent requests without rate-limit collisions.
2. **Progress checkpointing with resumable state**: Persist partial results (e.g., complaints summarized so far) at intervals so a task that hits turn/token limits can resume from the checkpoint in a follow-up run rather than losing all progress and being "marked as failed," as happened in the example. Deployment consideration: requires a state store and resumption logic that reconstructs agent context accurately from the checkpoint.
3. **Early-termination-with-partial-results path**: Instead of a hard cutoff at turn 50 that discards the task as failed, define a graceful degradation path that returns whatever partial summary exists (e.g., the 60% processed) with an explicit "partial" flag, rather than silent or total failure. Deployment consideration: downstream consumers must be able to handle and clearly surface partial results distinctly from complete ones.

### Metrics
1. **turns_consumed_pct_at_completion**: Target < 80% of allocated turn budget used for successful task completions; Alert if median approaches 100% (signals budgets are systematically undersized).
2. **task_completion_rate_within_budget**: Target > 90% of tasks completing before hitting resource limits; Alert if < 70% for a given task template.
3. **progress_pct_per_turn**: Target a roughly linear or front-loaded progress curve; Alert if progress-per-turn in the back half of a task drops below 50% of the front-half rate (signals inefficient phase like per-item fetching).
4. **partial_result_rate**: Target < 10% of tasks terminating with partial (vs. complete) results; Alert if > 25% for any recurring task type.

### Alerts
1. **Turn-Budget-Exhaustion-Recurring** (P2): Condition - the same task template (e.g., "summarize all complaints from period X") hits its turn/token limit in 3+ consecutive runs. Action: review the execution trace for inefficient per-item tool-call patterns (as in turns 6-30) and introduce batching or increase the allocated budget.
2. **Fetch-Phase-Overrun** (P3): Condition - a single task phase (fetch, search, etc.) consumes more than 50% of total turn budget before the primary task action begins. Action: flag for review of whether bundled/parallel tool calls could compress that phase.

## References

- [Aegis: Agent-Environment Failures](https://arxiv.org/abs/2508.19504) - Resource exhaustion as distinct failure category
- [DEV.to: $47,000 Agent Loop](https://dev.to/waxell/the-47000-agent-loop-why-token-budget-alerts-arent-budget-enforcement-389i) - Real resource exhaustion incident
- [LeanOps: Agents Burn 50x More Tokens](https://leanopstech.com/blog/agentic-ai-cost-runaway-token-budget-2026/) - Token efficiency analysis
