# Wrong Success Criteria

## Issue: Agent reports success when the real-world task outcome is not complete.

**Frequency**: Common

**Symptoms**
- Tool success but downstream status unchanged.
- [Add more specific symptoms]

**Root Cause**
Agent reports success when the real-world task outcome is not complete.

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
1. **Outcome Verification Step Required Before Success Report**: Success can only be declared after an independent check against the system-of-record confirms the real-world state changed as intended (e.g., order status = shipped in the fulfillment DB), never from the tool call's own return code alone.
2. **Success Criteria Defined at Task Creation, Not Inferred**: Each task specifies the verifiable end-state (specific field/value/downstream status) up front; the agent's definition of "done" is constrained to match this spec rather than defaulting to "the tool call didn't error."
3. **Separation of Action Execution and Completion Certification**: The component that performs the action is architecturally distinct from the component that certifies success, so a single agent can't both act and self-report completion without an independent confirmation step in between.

### Detection & Response
1. **Tool-Success vs. Downstream-State Reconciliation**: An asynchronous job re-checks the actual downstream system state some time after every "success"-reported action and flags mismatches where the tool reported success but the real state didn't change.
2. **False-Success Rate Tracking by Action Type**: Aggregate reconciliation mismatches by tool/action type to identify systematically unreliable success signals, such as a flaky downstream webhook that silently no-ops.
3. **User-Reported Non-Completion Mining**: Monitor follow-up user messages indicating the task wasn't actually done despite an agent success message ("it still shows pending"), and correlate against the original tool-call response to close gaps in the verification logic.

### Architecture Patterns
1. **Completion Verifier Service**: An independent service polls or subscribes to the actual system-of-record for the expected end-state and only marks a task complete when verified, decoupled from the action-executing agent's self-report.
2. **Idempotent Status Reconciliation Job**: A scheduled job compares agent-reported completions against source-of-truth state over a trailing window, producing a discrepancy report used both for alerting and for retraining success-detection heuristics.
3. **Two-Phase Completion Protocol**: Action execution first emits a "pending verification" status; only after the verifier confirms the downstream state does the task transition to "complete," preventing premature success reporting to the user.

### Metrics
1. **tool_success_to_verified_outcome_match_rate_percent**: Target: > 98%; Alert threshold: < 90%
2. **false_success_report_rate_percent**: Target: < 1%; Alert threshold: > 5%
3. **verification_latency_p95**: Target: within defined SLA (e.g., < 2 min); Alert threshold: exceeded
4. **user_reported_non_completion_rate_percent**: Target: < 2%; Alert threshold: > 6%

### Alerts
1. **Confirmed False Success Report** (P1 - Critical): Condition - reconciliation job finds a task marked complete where downstream state shows no change after the verification window. Action: reopen the task, notify the user, re-attempt the action or escalate.
2. **Systemic Tool Unreliability Detected** (P2 - Warning): Condition - false_success_report_rate for a specific action/tool exceeds threshold for 3+ consecutive days. Action: investigate tool/webhook reliability, add stronger verification for that action type.
3. **Verification Latency Breach** (P3 - Info): Condition - verification_latency_p95 exceeds its SLA. Action: investigate verifier service performance and downstream system responsiveness.

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
