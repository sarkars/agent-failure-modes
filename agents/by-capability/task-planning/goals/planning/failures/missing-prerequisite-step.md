# Missing Prerequisite Step

## Issue: Agent skips required validation, lookup, permission, or confirmation.

**Frequency**: Common

**Symptoms**
- Action happens before prerequisite evidence exists.
- [Add more specific symptoms]

**Root Cause**
Agent skips required validation, lookup, permission, or confirmation.

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
1. **Precondition Schema per Tool**: Every tool/action definition declares a `required_preconditions` list (e.g., `permission_check`, `balance_lookup`, `user_confirmation`). The tool-execution layer refuses to invoke the underlying API unless each precondition has a satisfying evidence record in the current session, making the check mechanical rather than dependent on the agent remembering to do it.
2. **Evidence-Gated Tool Calling**: Require the agent to attach a reference (a prior tool-call result ID or document ID) that satisfies each declared precondition when it proposes an action. Calls lacking valid evidence references are rejected by the executor before reaching the underlying system, not just flagged after the fact.
3. **Prerequisite Checklist Injection**: For action types identified in a risk taxonomy as commonly missing prerequisites (payments, deletions, permission-gated reads), auto-inject an explicit "prerequisites" step into the plan template so the agent cannot propose the action without the antecedent steps already appearing earlier in the plan.

### Detection & Response
1. **Precondition Violation Scanner**: Middleware wraps every tool call and checks the evidence log for the immediately preceding precondition-satisfying calls; a missing entry blocks the call and logs a violation event with the tool name and missing precondition type.
2. **Trace Replay Auditing**: Periodically replay sampled execution traces offline against the current precondition schema to catch violations that evaded live enforcement (e.g., due to a schema gap for a newly added tool).
3. **Outcome-Based Signal**: Correlate downstream failures (permission errors, invalid-state errors, customer complaints) with sessions where a precondition was skipped, to prioritize which precondition gaps matter most.

### Architecture Patterns
1. **Precondition Middleware / Policy Engine**: Sits between the agent and the tool executor, evaluating a rules table keyed by tool name against the session's evidence store before allowing any call through.
2. **State Store for Evidence**: A shared session state records completed lookups/validations with timestamps and result references, so precondition checks are O(1) lookups rather than re-derived each time.
3. **Fail-Closed Tool Gateway**: Default behavior on ambiguous or missing precondition metadata is to block the call and request the missing evidence, not to allow the call through.

### Metrics
1. **precondition_violation_rate_percent**: Target: 0%; Alert threshold: > 0.5% of tool calls
2. **actions_with_missing_evidence_count**: Target: 0 per day; Alert threshold: > 0
3. **mean_time_to_violation_detection_seconds**: Target: < 1s (live blocking); Alert threshold: > 5s
4. **false_precondition_block_rate_percent**: Target: < 2%; Alert threshold: > 5%

### Alerts
1. **Precondition Bypass Detected** (P1 - Critical): Condition - a tool call executed without satisfying a declared required precondition. Action: Halt the session, roll back if the action was destructive, alert the on-call engineer.
2. **Repeated Skips by Same Agent Config** (P2 - Warning): Condition - 3+ precondition violations from the same agent/prompt version within 24 hours. Action: Review the planner prompt or tool schema for that config; consider disabling the affected tool until fixed.
3. **High False-Block Rate** (P3 - Info): Condition - false_precondition_block_rate exceeds 5%, indicating overly strict schema. Action: Review and tune precondition definitions to reduce unnecessary friction.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | High |

---

## References

- [Tool-Augmented-LLM-Testing](https://homes.cs.washington.edu/~rjust/publ/tallm_testing_ast_2025.pdf)
- Note: Failures in tool-augmented LLM systems and testing implications.
