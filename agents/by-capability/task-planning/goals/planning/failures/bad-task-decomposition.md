# Bad Task Decomposition

## Issue: Agent splits the task into wrong subtasks, causing missed work.

**Frequency**: Occasional

**Symptoms**
- Subtask list does not cover acceptance criteria.
- [Add more specific symptoms]

**Root Cause**
Agent splits the task into wrong subtasks, causing missed work.

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
1. **Acceptance-Criteria-to-Subtask Traceability Matrix**: Before execution, require every acceptance criterion extracted from the task spec to map to at least one subtask in the decomposition. Generate this mapping as a structured table (criterion_id → subtask_ids) and block plan approval if any criterion has zero mapped subtasks.
2. **Decomposition Critique Pass**: Run a separate critic model/prompt that reviews the proposed subtask list against the original task spec, checking for coverage gaps, overlapping/redundant subtasks, and ambiguous scope boundaries. The critic must explicitly answer "does this decomposition fully cover the spec?" before the plan proceeds to execution.
3. **Template-Based Decomposition for Known Task Types**: For recurring task classes (e.g., "migrate a table," "onboard a customer"), maintain vetted decomposition templates listing the standard required subtasks. The agent's generated plan is diffed against the template, and missing template steps must be justified or added.

### Detection & Response
1. **Coverage Gap Scanner**: At the point the agent proposes a final answer, automatically re-run the criteria-to-subtask matrix check against actual completed work (not just the plan). Any criterion without a corresponding completed subtask blocks finalization and forces a replan cycle.
2. **Post-Hoc Decomposition Audit Sampling**: Sample a percentage of completed tasks weekly and have a reviewer (human or LLM-judge) score decomposition completeness against the original spec, producing a completeness_score used to track drift over time.
3. **Downstream Rework Rate Tracking**: Track how often completed tasks require a follow-up correction because a subtask was missed. Rising rework rate for a given task type is a leading indicator of decomposition quality degradation and should trigger a review of the planner prompt or template.

### Architecture Patterns
1. **Planner-Critic Loop**: Two-stage pipeline where a plan generator produces a structured subtask list `{subtask, maps_to_criterion, dependencies}` and a separate critic stage validates it against the parsed spec before the plan is unlocked for execution.
2. **Spec-Grounded Decomposition Service**: Parse the task spec into a structured criteria list (via schema extraction) first; the decomposition engine consumes this structured list rather than raw free text, so coverage checking is mechanical rather than inferred.
3. **Decomposition Versioning & Diffing**: Persist every subtask list with a version number; when a plan is revised mid-task, diff against the prior version to surface any acceptance-criteria-mapped subtask that was silently dropped.

### Metrics
1. **criteria_coverage_rate_percent**: Target: 100%; Alert threshold: < 95%
2. **decomposition_rework_rate_percent**: Target: < 5%; Alert threshold: > 10%
3. **subtask_missing_from_plan_count**: Target: 0 per task; Alert threshold: > 0
4. **critic_gap_catch_rate_percent**: Target: > 90% of injected gaps caught in eval; Alert threshold: < 75%

### Alerts
1. **Uncovered Acceptance Criterion** (P1 - Critical): Condition - plan approved for execution with an acceptance criterion unmapped to any subtask. Action: Block execution, force replan, notify task owner.
2. **Elevated Rework Rate** (P2 - Warning): Condition - rolling 7-day rework rate for a task type exceeds 10%. Action: Review decomposition template/critic prompt for that task type.
3. **Critic Disagreement Spike** (P3 - Info): Condition - critic flags an unusually high fraction of plans as incomplete in a given period. Action: Investigate planner model/prompt drift before tightening thresholds further.

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
