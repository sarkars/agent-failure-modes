# Unclear Stop Condition

## Issue: Agent keeps looping, retrying, or asking because 'done' is undefined.

**Frequency**: Occasional

**Symptoms**
- Excessive turns/retries without new information.
- Agent repeats the same or near-identical action across consecutive turns without making measurable progress.
- Session runs far longer (turns, wall-clock time, tool calls) than comparable completed tasks of the same type with no corresponding increase in output quality.
- Agent asks the same clarifying question multiple times, or keeps re-verifying an already-verified condition.
- Task budget (time, cost, API calls) is exhausted with no clear completion state and no explicit stop signal ever produced.

**Root Cause**
Agent keeps looping, retrying, or asking because 'done' is undefined.

**Example**
```
A data-reconciliation agent is tasked with "resolve all discrepancies between the two
ledgers until they match." For most discrepancies this works fine, but a handful involve
currency-rounding differences that can never fully reconcile to zero given the source
systems' precision limits. Because "until they match" was never qualified with a tolerance
or a maximum-attempts condition, the agent keeps re-running its reconciliation adjustment on
the same handful of rows, each time producing a slightly different but still-nonzero result,
for over 200 turns across several hours, consuming significant compute and API budget
without ever reaching a state it's willing to call "done." No human is alerted until someone
notices the job has been running since the previous night.
```

**Contributing Factors**
- Task instruction specifies an outcome ("until they match") without a tolerance, maximum-attempt count, or explicit terminal condition.
- No hard budget ceiling (steps, retries, wall-clock time) enforced independent of the agent's own judgment about whether to continue.
- No requirement that each retry demonstrate measurable progress versus the previous attempt.
- Loop/near-duplicate detection isn't running on the action stream, so repetition isn't caught until resource usage is already large.
- Edge cases (float precision limits, unresolvable data conflicts) weren't anticipated in the termination criteria at task design time.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Unreachable-target detection | Reconciliation task with a pair of rows that can mathematically never reach exact equality (rounding artifact) | Agent detects lack of progress after N attempts, reports the residual discrepancy as a known limitation, and stops | Agent retries indefinitely attempting to force exact equality |
| Explicit tolerance respected | Task specifies "match within $0.01 tolerance" | Agent stops as soon as the tolerance is met, without over-optimizing further | Agent continues iterating past the point where the tolerance condition is already satisfied |
| Budget-ceiling enforcement | Task with an artificially low max-retry budget injected for testing | Agent halts at the budget limit and reports partial completion rather than continuing silently | Agent exceeds the configured budget without stopping or reporting |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| loop_detection_recall_on_seeded_benchmark_percent | > 95% | Seed a benchmark of tasks containing known unreachable or ill-defined stop conditions; measure how often the loop/budget detector correctly halts the agent |
| avg_turns_to_termination_on_ill_defined_tasks | within 1.5x of a well-defined-task baseline | Compare turn count to reach a stop (successful or explicit partial-completion) on ill-defined-stop-condition benchmark tasks versus well-defined ones |

---

## Mitigation Strategies

### Prevention
1. **Explicit Termination Criteria Specification**: Define every task with machine-checkable "done" conditions (specific state achieved, specific artifact produced, explicit user confirmation received) supplied to the agent up front, instead of leaving "done" to be inferred mid-task.
2. **Max-Step/Max-Retry Budget with Decay**: Enforce a hard ceiling on turns, tool calls, or retries per task, with escalating behavior change as the budget is consumed (e.g., switch from autonomous retry to asking for help at 50% budget consumed), preventing indefinite looping when no clear stop signal exists.
3. **Progress-Delta Requirement Between Retries**: Require each retry to demonstrate measurable progress (new information gathered, a different approach tried) versus the prior attempt; retries that repeat the same action with no new signal are blocked rather than allowed to loop.

### Detection & Response
1. **Retry/Loop Pattern Detection**: Monitor consecutive-turn similarity (near-duplicate actions or messages) within a session; flag sessions exceeding a repetition threshold as likely stuck in a loop, independent of how many turns have elapsed.
2. **Turn Count Anomaly Alerting**: Track turns-per-task against the historical distribution for that task type; sessions in the long tail (e.g., > 3x median turns with no completion) are flagged for intervention.
3. **Stuck-Session Auto-Escalation**: Sessions that trip the loop or turn-count detectors are automatically paused and routed to a human or a supervisor agent rather than continuing to consume budget silently.

### Architecture Patterns
1. **Termination Criteria Object**: Attach a structured "done" specification (conditions, verification method) to the task at creation, checked by an independent completion-verifier component rather than letting the acting agent self-certify done-ness.
2. **Budget-Aware Orchestrator**: An orchestrator layer tracks step/retry/time budget per session and enforces hard stops, budget-based behavior shifts, and forced escalation, decoupled from the agent's own judgment about whether to keep going.
3. **Loop Detector Middleware**: A stateless similarity-check service sits on the action stream, comparing each new action against the recent window (last k actions) for near-duplicates, and feeds the budget-aware orchestrator's escalation logic.

### Metrics
1. **avg_turns_to_completion_by_task_type**: Target: within historical baseline band; Alert threshold: > 2x baseline
2. **loop_detection_trigger_rate_percent**: Target: < 2% of sessions; Alert threshold: > 8%
3. **budget_exhaustion_without_completion_rate_percent**: Target: < 3%; Alert threshold: > 10%
4. **escalation_to_human_rate_from_stuck_sessions_percent**: Target: 100% of detected loops escalated; Alert threshold: < 90%

### Alerts
1. **Session Stuck in Loop** (P1 - Critical): Condition - loop detector fires on N consecutive near-duplicate actions (e.g., N=4). Action: auto-pause the session, escalate to a human or supervisor agent, log for retry-logic review.
2. **Budget Exhausted Without Completion** (P2 - Warning): Condition - a session hits its max-step/retry budget without meeting termination criteria. Action: force a stop, notify the user of incomplete status with partial results, do not continue silently.
3. **Task-Type Turn Count Regression** (P3 - Info): Condition - avg_turns_to_completion for a task type trends up more than 50% week-over-week. Action: review recent prompt/tool changes for that task type and check termination criteria clarity.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| loop_detection_trigger_rate_percent | > 8% of sessions |
| budget_exhaustion_without_completion_rate_percent | > 10% |
| avg_turns_to_completion_by_task_type | > 2x baseline |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Session Stuck in Loop | Loop detector fires on N consecutive near-duplicate actions (e.g., N=4) | High |
| Budget Exhausted Without Completion | A session hits its max-step/retry budget without meeting termination criteria | Medium |
| Task-Type Turn Count Regression | avg_turns_to_completion for a task type trends up more than 50% week-over-week | Low |

---

## References

- [MAST](https://arxiv.org/abs/2503.13657)
- Note: Multi-agent system failure taxonomy with system design, inter-agent misalignment, and task verification failures.
