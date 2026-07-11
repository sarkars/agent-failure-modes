# Infinite Loops

## Issue: Infinite Loops in Iterative Refinement

**Frequency**: Occasional

**Symptoms**
- Agent repeatedly retries failed extraction
- Token costs spiral without progress
- No termination condition triggered

**Root Cause**
Iterative refinement loops designed to improve accuracy can enter infinite loops when the underlying failure cannot be resolved by retrying.

**Example**
```
Iteration 1: Extract total, validation fails (expected $X, got $Y)
Iteration 2: Re-extract with different prompt, same wrong result
Iteration 3-100: Repeat forever

Result: $47,000 in token costs for 11-day loop (real incident)
```

**Key Statistics**
- One production incident: $47,000 agent loop over 11 days with no hard stop
- Another incident: $437 overnight from unchecked agent run

## Mitigation Strategies

### Prevention
1. **Hard iteration caps enforced outside the LLM loop**: Set a maximum retry count (e.g., 3-5 attempts) enforced by the orchestrating code, not by asking the LLM to "know when to stop" — the loop-continuation decision must never be delegated to the same model that's failing to converge. Trade-off: a hard cap can prematurely stop a genuinely-improving multi-step refinement; tune the cap per task type using historical convergence data.
2. **Per-task token/cost budgets with automatic kill switches**: Allocate a token or dollar budget per document/task before execution starts, and have the orchestrator hard-kill the process (not just alert) when the budget is exceeded, rather than relying on a human to notice a runaway cost. Trade-off: requires accurate upfront budget estimation; too-tight a budget will kill legitimate long-running tasks.
3. **Progress-delta requirement between iterations**: Require each retry to demonstrate measurable improvement (e.g., validation error count decreasing, confidence score increasing) versus the previous attempt; if two consecutive iterations produce no improvement, terminate rather than continuing to retry the same failing approach.

### Detection & Response
1. **Real-time spend velocity monitoring**: Track token/cost spend rate per task in near-real-time (not just end-of-run totals), and alert when a single task's spend rate exceeds what a bounded task should ever need — this is what catches multi-day runaway loops before they reach five figures in cost.
2. **Output similarity/convergence detection**: Compare each iteration's output to the previous iteration's; if outputs are near-identical or cycling between the same few states without progress, flag as a stuck loop rather than a productive retry sequence.
3. **Escalation after N unresolved failures**: After a fixed, small number of failed attempts, automatically route the task to a human reviewer with the full retry history, rather than letting the agent continue attempting the same fix indefinitely.

### Architecture Patterns
1. **Circuit breaker pattern**: Wrap the retry loop in a circuit breaker that trips (halts further attempts) after a failure threshold is crossed within a time window, requiring explicit reset (human or upstream system) before the task can retry again.
2. **Budget-as-first-class-resource orchestration**: Treat token/cost budget as a resource the orchestrator allocates and tracks per task the same way it would track memory or file handles — the task simply cannot execute another LLM call once its budget is exhausted, independent of any application-level logic.
3. **Bounded self-refinement with external judge**: Instead of letting the agent decide when its own output is "good enough," use a separate, cheap, deterministic validator to judge convergence and gate whether another iteration is even attempted.

### Metrics
1. **max_iterations_hit_rate**: Target: < 5% of tasks hit the hard iteration cap; Alert if > 15% (signals cap is too low or underlying failure is systemic)
2. **cost_per_task_p99**: Target: define per task type baseline; Alert if p99 exceeds 5x the median cost per task
3. **stuck_loop_detection_rate**: Target: track as baseline; Alert if detection rate rises > 3x week-over-week
4. **time_to_kill_switch_trigger**: Target: runaway task killed within 5 minutes of budget breach; Alert if any task exceeds budget by more than 20% before being killed

### Alerts
1. **Cost Velocity Anomaly** (P1): Condition - a single task's spend rate exceeds 10x the median task's spend rate over a 10-minute window. Action: Kill the task immediately, page on-call, review the task's retry history before allowing any re-run.
2. **Iteration Cap Saturation** (P2): Condition - more than 15% of tasks in a given document type are hitting the hard iteration cap. Action: Investigate whether the underlying extraction approach is systemically failing for that document type rather than raising the cap.
3. **Kill Switch Delay** (P1): Condition - a task exceeds its allocated budget by more than 20% before the kill switch triggers. Action: Treat as an incident — audit the kill switch implementation for the execution path that allowed overrun.

## References

- [DEV.to: $47,000 Agent Loop](https://dev.to/waxell/the-47000-agent-loop-why-token-budget-alerts-arent-budget-enforcement-389i) - 11-day infinite loop incident
- [Dev Journal: $437 Overnight AI Agent](https://earezki.com/ai-news/2026-04-29-i-let-my-ai-agent-run-overnight-it-cost-437/) - Unchecked overnight run
- [AWS: 3 Agent Failure Modes](https://dev.to/aws/why-ai-agents-fail-3-failure-modes-that-cost-you-tokens-and-time-1flb) - Loop detection
