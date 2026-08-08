# Wrong Success Criteria

## Issue: Agent reports success when the real-world task outcome is not complete.

**Frequency**: Common

**Symptoms**
- Tool success but downstream status unchanged.
- Agent reports a task as complete based on a tool call returning HTTP 200/no error, while the downstream system-of-record shows the real-world state unchanged.
- Customer-facing status (e.g., "order shipped") is communicated before the actual fulfillment event has occurred.
- Discrepancy between agent-reported completion and verified outcome is only discovered when the customer complains or asks for a status update.
- Same action/tool type produces false-success reports repeatedly, suggesting a systematically unreliable success signal rather than isolated flukes.

**Root Cause**
The agent infers success from the immediate return code of the tool it called rather than from the actual state of the downstream system of record, treating what is really an asynchronous, decoupled process — request accepted versus outcome achieved — as if the two happened synchronously. No independent verification step sits between "action requested" and "success reported to the user," and because the same agent both performs the action and certifies its own completion, there's no separation of duties that would catch a false positive. When the downstream step then fails silently, as an out-of-stock warehouse system might, that failure never propagates back as an error the agent would see, so it reports completion with total confidence for a task that never actually finished.

**Example**
```
An order-fulfillment agent calls the warehouse management system's "create shipment" API for
a customer order, receives a 200 OK response, and immediately messages the customer that
"your order has shipped" and updates the order status to Shipped. In reality, the warehouse
system's 200 response only confirms the shipment request was queued, not that a physical
shipment occurred -- the actual pick-pack-ship process runs asynchronously and, in this
case, fails silently because the item is out of stock at that warehouse location. The
agent's success criteria was "API call returned success," not "package is physically in a
carrier's hands," so it reported completion three days before anyone discovers the order
never actually shipped, when the customer contacts support asking where their package is.
```

**Contributing Factors**
- Success is inferred from the immediate tool-call return code rather than from the actual downstream system-of-record state.
- The action-triggering step and the state-confirming step are asynchronous/decoupled, but the agent treats them as synchronous.
- No independent verification step exists between "action requested" and "success reported to user."
- The agent's role bundles both executing the action and self-certifying its completion, with no separation of duties.
- Downstream failures (out-of-stock, carrier rejection) fail silently rather than propagating an error the agent would see.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Async completion verification | Shipment API returns 200 (queued) but warehouse fulfillment ultimately fails (out of stock) | Agent withholds "shipped" status/customer messaging until the warehouse system confirms actual pick-pack-ship completion | Agent reports "shipped" immediately off the API's 200 response |
| Silent downstream failure | Downstream system fails the actual fulfillment step without raising an error to the calling API | Reconciliation check catches the mismatch between reported and verified state within the SLA window | Mismatch goes undetected until the customer complains |
| True success confirmation | Shipment genuinely completes and the warehouse system confirms | Agent reports "shipped" only after verified confirmation, with no unnecessary delay beyond the verification SLA | Agent either reports too early (false positive) or delays reporting well past actual completion (false negative) |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| tool_success_verified_outcome_match_rate_on_benchmark_percent | > 98% | Run a benchmark of fulfillment scenarios including seeded async-failure cases; compare the agent's reported completion against the verified warehouse/carrier state |
| false_success_rate_on_seeded_failure_cases_percent | < 2% | On seeded cases where the downstream action is engineered to fail after an API 200, measure how often the agent still reports success |

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
| tool_success_to_verified_outcome_match_rate_percent | < 90% |
| false_success_report_rate_percent | > 5% |
| verification_latency_p95 | Exceeds SLA (e.g., > 2 min) |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Confirmed False Success Report | Reconciliation job finds a task marked complete where downstream state shows no change after the verification window | High |
| Systemic Tool Unreliability Detected | false_success_report_rate for a specific action/tool exceeds threshold for 3+ consecutive days | Medium |
| Verification Latency Breach | verification_latency_p95 exceeds its SLA | Low |

---

## References

- [Tool-Augmented-LLM-Testing](https://homes.cs.washington.edu/~rjust/publ/tallm_testing_ast_2025.pdf)
- Note: Failures in tool-augmented LLM systems and testing implications.
