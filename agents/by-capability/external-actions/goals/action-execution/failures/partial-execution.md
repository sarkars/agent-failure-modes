# Partial Execution

## Issue: Agent completes only some steps but reports full success.

**Frequency**: Common

**Symptoms**
- Subtask status incomplete vs final status success.
- [Add more specific symptoms]

**Root Cause**
Agent completes only some steps but reports full success.

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
1. **Atomic Action Batches with Explicit Checkpoints**: Decompose multi-step actions into atomic subtasks with explicit completion checkpoints. Each subtask must complete fully before proceeding to next. On subtask failure, halt entire batch and enter recovery mode (don't proceed with remaining steps).
2. **Subtask Completion Verification**: Before declaring multi-step action complete, query completion status of all required subtasks. Flag incomplete subtasks explicitly. Return partial_success status if any step fails (not full success).
3. **All-or-Nothing Execution Semantics**: Implement transactional semantics for action sequences. All steps must complete successfully for action to commit. If any step fails, rollback all completed steps and return to pre-action state (or execute compensating transactions).

### Detection & Response
1. **Incomplete Action Detection**: Track action start time, expected completion time per action type, actual completion time. Alert if action not completed within SLA. Example: 'Multi-step refund should complete within 2 hours'.
2. **State Consistency Checks Post-Execution**: After action completes, verify all affected resources reached expected state. Example: after order cancellation, verify order status=cancelled, inventory restored, refund processed. Flag missing steps as partial failure.
3. **Audit Log Gap Detection**: Compare action execution log with resource state changes. Alert if expected state changes (per action plan) are missing from audit trail. Indicates partial execution.

### Architecture Patterns
1. **Workflow Orchestration Engine**: Use workflow platform (Temporal, Airflow, Step Functions) to manage multi-step actions with built-in retry, compensation, and state tracking. Each step emits completion event before proceeding.
2. **Compensation Transaction Pattern**: For each action step, define compensating action to undo changes if downstream steps fail. On failure, execute compensation chain in reverse order to restore pre-action state.
3. **State Machine Validation**: Model action lifecycle as finite state machine. All state transitions must be valid (defined in state machine). Enforce at execution layer. Prevent invalid transitions that could indicate partial execution.

### Metrics
1. **multi_step_action_completion_rate_percent**: Target: 100%; Alert threshold: < 98%; Track: all steps completed
2. **partial_execution_attempts_per_day**: Target: 0; Any partial execution is critical
3. **action_step_failure_rate_percent**: Target: < 0.1%; Low failure rate indicates reliable execution
4. **incomplete_action_recovery_time_minutes_p95**: Target: < 30; Recovery should be fast
5. **compensation_transaction_success_rate_percent**: Target: 100%; Rollbacks must complete successfully

### Alerts
1. **Partial Action Execution Detected** (P1 - Critical): Condition - multi-step action stopped before all steps completed. Action: Trigger recovery workflow automatically, notify admin with step-by-step status, log for analysis.
2. **Action Completion Timeout** (P2 - Warning): Condition - action in progress for > SLA duration (e.g., > 2 hours). Action: Send retry notification, escalate if timeout exceeds max duration, potential auto-compensation.
3. **Inconsistent Final State Post-Action** (P1 - Critical): Condition - resource state doesn't match expected final state. Example: refund action completes but customer doesn't receive funds. Action: Immediate audit log review, compensation attempt, stakeholder notification.

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
