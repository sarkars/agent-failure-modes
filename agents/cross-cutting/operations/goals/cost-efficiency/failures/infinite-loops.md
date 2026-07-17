# Infinite Loops

## Issue: Agent Gets Stuck in Infinite Retry Loops

**Frequency**: Occasional

**Symptoms**
- Agent repeatedly attempts same action with same or similar inputs
- Token costs spiral without progress toward goal
- No termination condition triggers
- Task never completes or times out after hours/days

**Root Cause**
Iterative refinement and retry logic can enter infinite loops when:
- The underlying failure cannot be resolved by retrying
- Success conditions are impossible to meet
- Agent lacks ability to recognize futile attempts
- No hard limits on iterations or cost

**Example**
```
Iteration 1: Call API, get rate limit error, retry
Iteration 2: Call API, get rate limit error, retry
...
Iteration 10,000: Still retrying

Result: $47,000 in API costs over 11 days (real incident)
```

**Real Incidents**
- $47,000 agent loop over 11 days with no hard stop
- $437 overnight from unchecked agent run
- Development environments running indefinitely

---

## Test Scenario & Reproduction

### Scenario Setup
- Agent configured with retry logic but no hard iteration ceiling and no distinction between retriable and non-retriable errors
- Downstream API enforces a persistent rate limit that the agent's retry cannot resolve
- No real-time cost/budget kill-switch monitoring the running task

### Trigger Mechanism
1. Agent calls the external API and receives a rate-limit error
2. Retry logic re-issues the identical call immediately (or with insufficient backoff) without checking whether the error is terminal for the current window
3. Each retry again hits the same rate limit, and the loop repeats with no upper bound on iteration count or elapsed cost

**Example Reproduction Steps:**
```
1. Configure an agent task that calls a rate-limited external API with standard retry-on-failure logic and no max-iteration cap
2. Trigger a sustained rate-limit condition on the API (e.g., throttle responses to always return 429)
3. Start the agent task and let it enter the retry loop
4. Log iteration count, elapsed time, and cumulative API/token cost at intervals (iteration 1, 10, 100, 1,000, 10,000)
5. Continue the run unattended and measure total elapsed time and cost before any external intervention occurs
6. Compare against the documented real incident: 10,000+ iterations, 11 days, $47,000 in API costs
```

### Expected Failure State
- The agent performs the same retry action with the same input thousands of times with no state change or progress
- Iteration count climbs into the thousands/tens of thousands with no automatic termination
- Cumulative cost grows unbounded over the run's duration (days), eventually reaching the $47,000-scale magnitude documented in the real incident
- No alert or kill-switch fires despite iteration count and elapsed time being orders of magnitude beyond any normal task

---

## Mitigation Strategies

### Prevention
1. **Hard iteration ceiling with forced termination**: Since the $47,000 incident ran to 10,000+ iterations with "no hard stop," enforce a non-negotiable maximum iteration count (e.g., 5-10 retries) that terminates the task regardless of internal agent state, rather than relying on the agent to recognize futility itself. Trade-off: a hard ceiling can cut off tasks that were making slow-but-real progress, so it must pair with a distinguishable "terminated at limit" status rather than silent failure.
2. **Non-retriable error classification**: Because the root cause explicitly includes retrying when "the underlying failure cannot be resolved by retrying" (e.g., a persistent rate-limit or auth failure), classify errors as retriable vs. terminal before entering the retry loop, and fail fast on terminal errors instead of consuming the full iteration budget. Trade-off: misclassifying a genuinely transient error as terminal causes premature task failure.
3. **Real-time cost budget enforcement, not just alerting**: The $47,000 and $437 incidents both involved unchecked spend accumulating before anyone noticed — a budget must actively kill the agent process when a per-task token/cost ceiling is crossed, not merely alert a dashboard someone might check later. Trade-off: hard kill-switches risk terminating legitimate high-cost-but-valuable tasks; pair with a human override path.

### Detection & Response
1. **Iteration-count-vs-baseline monitoring**: Track iteration counts per task type against historical baselines; a task running 100x its typical iteration count (as in the 10,000-iteration incident) should trigger automatic investigation well before it reaches a hard limit.
2. **Identical-action repetition logging**: Log and diff each action's input/output against the immediately preceding one — the example shows the same rate-limit-retry action repeating with no variation, which is a directly detectable signature distinct from legitimate iterative refinement.
3. **Convergence/similarity check between attempts**: Since success conditions can be "impossible to meet," compare successive outputs for semantic similarity; if outputs aren't improving or changing across N iterations, treat this as evidence of futility and escalate rather than continue.

### Architecture Patterns
1. **Circuit breaker with exponential backoff and max-attempt ceiling**: Wrap external calls in a circuit breaker (open after N consecutive failures, half-open probe after backoff) so a persistently failing dependency (like the rate-limited API in the example) stops being hammered after a bounded number of attempts. Deployment consideration: circuit breaker state needs to be shared/coordinated if multiple agent instances hit the same downstream dependency.
2. **Escalation-to-human queue after failure threshold**: Route the task to a human review queue automatically after N consecutive failures rather than looping indefinitely, giving the agent a defined exit path other than "keep trying" or silent abandonment. Deployment consideration: requires on-call/triage capacity sized to the expected escalation volume.
3. **Real-time spend kill switch**: A supervising process (separate from the agent loop itself, so it survives the agent being stuck) tracks cumulative cost/tokens per task and issues a hard-kill signal when the budget is exceeded, directly preventing repeats of the 11-day/$47,000 scenario. Deployment consideration: the kill switch must checkpoint partial results so terminated tasks aren't a total loss.

### Metrics
1. **iterations_per_task_p99**: Target < 20 for standard tasks; Alert if > 100 (well below the 10,000 seen in the real incident).
2. **cost_per_task_p95**: Target < $0.50; Alert if > $10 (catching runaway spend orders of magnitude before the $47,000 incident scale).
3. **max_task_runtime_minutes**: Target < 30 minutes per task; Alert if a task exceeds 120 minutes without completion.
4. **identical_action_repeat_count**: Target 0 exact repeats of the same tool call + input within a task; Alert if any action repeats > 3 times identically.

### Alerts
1. **Runaway-Spend-Kill-Switch** (P1): Condition - cumulative cost for a single task exceeds a hard $10 ceiling (or a configured task-specific budget) before completion. Action: immediately terminate the agent process, checkpoint partial output, and page on-call; do not allow continuation without explicit human approval.
2. **Iteration-Limit-Breach** (P1): Condition - a task exceeds its configured hard iteration ceiling (e.g., 10 retries) without success. Action: force-terminate, log the full retry history, and route to human escalation queue rather than auto-retrying further.
3. **Sustained-Runtime-Without-Progress** (P2): Condition - a task runs longer than 2 hours with no state change or output variation across iterations. Action: flag for manual review; check for a non-retriable error being mistakenly retried.

## References

- [DEV.to: $47,000 Agent Loop](https://dev.to/waxell/the-47000-agent-loop-why-token-budget-alerts-arent-budget-enforcement-389i) - Real incident analysis of an 11-day agent loop with no hard stop
- [Dev Journal: $437 Overnight AI Agent](https://earezki.com/ai-news/2026-04-29-i-let-my-ai-agent-run-overnight-it-cost-437/) - Case study of unchecked overnight agent costs
- [AWS: 3 Agent Failure Modes](https://dev.to/aws/why-ai-agents-fail-3-failure-modes-that-cost-you-tokens-and-time-1flb) - Common failure patterns including infinite loops
