# Bad Task Decomposition

## Issue: Agent splits the task into wrong subtasks, causing missed work.

**Frequency**: Occasional

**Symptoms**
- Subtask list does not cover acceptance criteria.
- Subtasks overlap or duplicate effort while a required step (e.g., compliance sign-off) never appears as its own line item.
- Agent marks the parent task complete after finishing only the subtasks it generated, even though the original request listed additional deliverables.
- A single subtask silently bundles two distinct systems or owners (e.g., "update ERP and notify finance"), so only one half actually executes.
- Plan granularity is inconsistent: trivial steps get their own subtask while a critical multi-part step is folded into one line.

**Root Cause**
Agent splits the task into wrong subtasks, causing missed work.

**Example**
```
A procurement automation agent is asked to "onboard new vendor Acme Fasteners: create the vendor record, verify the W-9 and insurance certificate, set payment terms, and notify the requesting department." The agent decomposes this into two subtasks — "create vendor record in ERP" and "notify requesting department" — because its decomposition prompt folded document verification and payment-terms configuration into an implicit part of "create vendor record" that the ERP-creation tool call never actually performs. The vendor record gets created with default net-30 terms and no compliance documents on file, the notification goes out, and the missing insurance certificate isn't discovered until a vendor-risk audit three months later.
```

**Contributing Factors**
- Task spec is written as flowing prose rather than an itemized list, making it easy for decomposition to fold multiple requirements into one subtask.
- No acceptance-criteria extraction step runs before decomposition, so there is nothing to check the subtask list against.
- Decomposition prompt biases toward the tools/APIs the agent has readily available rather than the full scope of the request.
- Single-pass decomposition with no critic or review step before execution begins.
- Task spans multiple systems or owners (ERP, compliance, accounts payable) and no template forces one subtask per system.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Multi-system coverage | "Onboard vendor X: create record, verify compliance docs, set terms, notify dept" | 4 subtasks, one per system/action, each traceable to a request clause | Fewer than 4 subtasks, or a subtask silently bundling two distinct actions |
| Compliance step omission | Vendor onboarding request with explicit W-9/insurance verification requirement | Subtask list includes an explicit "verify compliance documents" step with its own completion evidence | Compliance verification absent from the subtask list or folded into another subtask with no separate evidence |
| Granularity consistency | Task spec with 5 explicit deliverables of comparable complexity | 5 subtasks of comparable scope, none absorbing 2+ deliverables | One subtask covers multiple deliverables while others remain single-item |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| decomposition_criteria_coverage_percent | 100% | Automated diff of the acceptance-criteria list against the subtask-to-criterion mapping in the eval harness |
| avg_subtasks_per_deliverable | 1.0-1.3 | Count of generated subtasks divided by count of explicit deliverables in the test spec, averaged across the eval set |

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
| criteria_coverage_rate_percent | < 95% |
| decomposition_rework_rate_percent | > 10% |
| avg_time_to_discover_missed_subtask_days | > 7 days |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| **Vendor Onboarded Without Compliance Subtask** | Vendor record created with no corresponding "compliance verification complete" evidence logged in the same task | Medium |
| **Decomposition Coverage Below Threshold** | criteria_coverage_rate_percent drops below 95% over a rolling 7-day window | Medium |
| **Repeated Rework on Same Task Template** | decomposition_rework_rate_percent exceeds 10% for a specific task template over 7 days | Low |

---

## References

- [MAST](https://arxiv.org/abs/2503.13657)
- Note: Multi-agent system failure taxonomy with system design, inter-agent misalignment, and task verification failures.
