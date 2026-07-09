# Over-Planning

## Issue: Agent spends excessive time planning instead of acting.

**Frequency**: Rare

**Symptoms**
- Many plan turns; no execution progress.
- [Add more specific symptoms]

**Root Cause**
Agent spends excessive time planning instead of acting.

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
1. **Step/Turn Budget for Planning Phase**: Cap the number of planning turns (e.g., 3-5) before the orchestrator forces a transition to execution with the best plan available so far, preventing indefinite re-planning loops.
2. **Plan Complexity Cap**: Bound subtask count/nesting depth relative to the task's complexity score; when a plan exceeds the cap, the agent is required to simplify or merge subtasks rather than continue elaborating.
3. **Diminishing-Returns Detector**: Compare successive plan revisions; if the diff between consecutive planning turns falls below a materiality threshold (no new information incorporated), force a transition to execution instead of allowing further refinement turns.

### Detection & Response
1. **Planning Turn Counter/Timer**: Track elapsed turns and wall-clock time spent in the planning phase per session; sessions exceeding the budget are flagged and force-transitioned.
2. **Zero-Progress Session Detector**: Identify sessions with many planning turns but zero executed tool calls, which is the direct symptom of over-planning, and auto-escalate or force execution.
3. **Plan Churn Analysis**: Measure how much each plan revision actually changes (subtasks added/removed/reordered) without new information being introduced; high churn with low information gain indicates unproductive re-planning.

### Architecture Patterns
1. **Planning Budget Enforcer**: Orchestrator-level middleware that tracks planning turns/time per session and interrupts the planning loop once the budget is exhausted, handing control to the executor.
2. **Time-Boxed Plan-Execute Loop**: On planning timeout, escalate to a simpler heuristic planner (e.g., execute the first N subtasks of the current best plan) rather than continuing open-ended deliberation.
3. **Plan Diff Service**: Tracks revision-to-revision deltas of the plan artifact, feeding the diminishing-returns detector and providing an audit trail of why planning continued or stopped.

### Metrics
1. **planning_turns_before_first_action**: Target: <= 3; Alert threshold: > 6
2. **planning_time_to_action_ratio**: Target: < 0.3; Alert threshold: > 0.6
3. **plan_churn_rate_percent**: Target: < 20% per revision; Alert threshold: > 50% with no new info
4. **timeout_forced_execution_rate_percent**: Target: < 10% of sessions; Alert threshold: > 25%

### Alerts
1. **Planning Budget Exceeded** (P2 - Warning): Condition - session exceeds configured planning turn/time budget. Action: Force transition to execution with current best plan, log for review.
2. **Zero Execution Progress** (P2 - Warning): Condition - 5+ planning turns with zero tool executions. Action: Auto-escalate to simpler planner or human review.
3. **Excessive Plan Churn** (P3 - Info): Condition - plan_churn_rate stays high across multiple sessions for a task type. Action: Review planner prompt for indecisiveness patterns.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Low |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
