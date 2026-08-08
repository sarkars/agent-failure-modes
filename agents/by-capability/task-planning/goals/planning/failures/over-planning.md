# Over-Planning

## Issue: Agent spends excessive time planning instead of acting.

**Frequency**: Rare

**Symptoms**
- Many plan turns; no execution progress.
- Agent repeatedly regenerates the outline for a report or workflow without ever calling a search/data tool to fill it in.
- Successive planning turns reorder or rename the same subtasks with no new information incorporated.
- Agent poses clarifying sub-questions it could resolve with a tool call, but keeps deliberating instead of calling the tool.
- Session times out or hits a turn/cost budget while still in the planning phase, with zero completed deliverable sections.

**Root Cause**
Nothing enforces a turn or time budget on the planning phase, so for a genuinely open-ended task with no crisp definition of "done planning," refinement has no natural stopping point and can continue indefinitely. The agent's self-critique loop tends to reward producing a more polished-looking plan over making the transition to execution, and without a diminishing-returns check comparing successive plan revisions for actual new information, reordering the same subtasks looks like productive iteration rather than the stall it actually is. Because planning and execution aren't architecturally separated into distinct phases with an enforced handoff, there is no structural moment that forces the agent to stop refining and start gathering the information the plan was supposed to be organizing in the first place.

**Example**
```
A research agent is asked to "produce a competitive analysis of three SaaS vendors for the procurement team." Instead of researching the first vendor after an initial outline, the agent spends 14 turns iterating on the report structure — adding a subsection, then merging it back, then splitting the pricing comparison into two different framings, then reconsidering the audience and revising the outline again. No search or data-gathering tool is called during this entire span. By the time a human notices no actual vendor data has been retrieved, half the allotted session budget is gone and the report is still an empty outline.
```

**Contributing Factors**
- No turn or time budget is enforced on the planning phase, so refinement can continue indefinitely.
- Task is genuinely open-ended ("produce an analysis") with no crisp definition of "done planning," inviting endless elaboration.
- Agent's self-critique loop rewards producing a more polished-looking plan over transitioning to execution.
- No diminishing-returns check compares successive plan revisions for actual new information.
- Planning and execution are not architecturally separated, so there is no natural handoff point forcing a transition.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Planning turn budget enforcement | "Produce a competitive analysis of 3 SaaS vendors" | Agent transitions to research/execution within 3-5 planning turns | Agent exceeds 6+ planning turns with zero tool calls made |
| Diminishing-returns detection | Plan revised 3 times with no new information introduced between revisions | Orchestrator forces transition to execution after the 2nd no-new-info revision | Agent continues revising the same plan indefinitely without new information |
| Genuinely complex task allowance | Task requiring coordination across 8 interdependent systems | Agent is allowed a proportionally larger but still capped planning budget | Agent is force-transitioned before a genuinely necessary planning step completes, causing execution errors |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| planning_turns_before_first_tool_call | <= 3 | Count reasoning/plan-revision turns preceding the first search/data tool call in the eval trace |
| plan_revision_information_gain_rate_percent | > 50% of revisions introduce new information | LLM-judge or diff-based comparison of consecutive plan revisions for materially new content |

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
| planning_turns_before_first_action | > 6 |
| planning_time_to_action_ratio | > 0.6 |
| timeout_forced_execution_rate_percent | > 25% of sessions |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| **Planning Budget Exceeded** | Session exceeds the configured planning turn/time budget with no tool call made | Low |
| **Zero-Progress Session** | 5+ planning turns logged with zero tool executions | Medium |
| **Session Timeout During Planning** | Session hits its overall time/cost budget while still in the planning phase, producing no deliverable | Medium |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
