# Unclear Stop Condition

## Issue: Agent keeps looping, retrying, or asking because 'done' is undefined.

**Frequency**: Occasional

**Symptoms**
- Excessive turns/retries without new information.
- [Add more specific symptoms]

**Root Cause**
Agent keeps looping, retrying, or asking because 'done' is undefined.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- [List factors that make this failure more likely]

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| [Test name] | [Input] | [Expected output] | [What indicates failure] |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |

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
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Medium |

---

## References

- [MAST](https://arxiv.org/abs/2503.13657)
- Note: Multi-agent system failure taxonomy with system design, inter-agent misalignment, and task verification failures.
