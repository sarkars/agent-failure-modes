# Wrong Target Action

## Issue: Agent acts on wrong account, order, file, or user.

**Frequency**: Rare but Catastrophic

**Symptoms**
- Entity mismatch between request and tool call.
- Agent resolves a name or partial identifier ("John Doe", "order 123") to the wrong record among several similarly-named matches.
- Action executed against a cached or stale target ID that no longer corresponds to the resource the user meant.

**Root Cause**
Agent acts on wrong account, order, file, or user.

**Example**
```
Customer says "cancel my order from yesterday." The account has two orders placed the
previous day. The agent picks the first one returned by the order-lookup API — a $12
accessory order — and cancels it, when the customer meant the $340 order that shipped
early by mistake. No disambiguation step confirmed which order the customer meant before
the cancel action executed.
```

**Contributing Factors**
- Target resolved from partial or ambiguous identifiers (name, "yesterday's order") without disambiguation when multiple matches exist.
- Agent passes raw IDs between tool calls without re-displaying a human-readable summary for confirmation.
- Race condition where the target resource changes between when it was identified and when the action executes.
- Tool responses return bare IDs rather than rich, disambiguating object details (status, amount, date).

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Multiple matching targets | Lookup returns 2+ resources matching the user's description | Agent surfaces the candidates and confirms which one before acting | Agent silently acts on the first/most-recent match |
| Target confirmation binding | Agent confirms a target, then executes the action | Executed target matches the confirmed target exactly | Executed target differs from the one confirmed (race condition or ID mix-up) |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| wrong_target_action_attempts_per_day | 0 | Count actions where confirmed_target_id doesn't match executed_target_id |

---

## Mitigation Strategies

### Prevention
1. **Target Confirmation with Semantic Summary**: Before executing action, display semantic summary of target resource (e.g., 'Refund $500 for Customer: John Doe (ID: CUST-123), Order: #12345-ABC'). Require explicit agent confirmation of target identity. Bind confirmed target to action request.
2. **Typed Object Representations**: Use rich object representations (not just IDs) for action targets. Display disambiguating information (e.g., if multiple customers named 'John Doe', show email, phone, account balance to enable user to differentiate). Use type checking to verify object is correct type.
3. **Target Validation Rules per Action**: Define validation rules per action type. Example: 'refund action must target an order_id with status=completed AND order_amount_in_range AND within_refund_window'. Enforce before execution.

### Detection & Response
1. **Target Confirmation Mismatch Detection**: Compare target object confirmed by agent/user with actual target of execution. Alert if mismatch detected (confirmed_target_id ≠ executed_target_id). Potential target mix-up.
2. **Context-Specific Target Anomaly Detection**: Flag actions targeting unusual resources. Example: agent refunding orders from unusual customers (high-value orders, VIP customers), deleting resources of unusual type/age. Correlate with user.
3. **Bulk Action Target Validation**: For batch operations (multi-target), validate each target's appropriateness. Sample-check targets (e.g., audit 10% of target set). Flag anomalies (unusual resource mix, unexpected quantity).

### Architecture Patterns
1. **Target Confirmation Middleware**: All actions route through confirmation layer. Display rich target summary with key disambiguating fields. Persist confirmed_target_id with action for later verification. Fail if confirmation not provided.
2. **Semantic Target Validation**: Before execution, re-verify target still matches original confirmation summary. Alert if target was modified between confirmation and execution (race condition detection).
3. **Audit Trail with Target Binding**: Log action with: confirmed_target (user-acknowledged), executed_target (actual target), delta (if mismatch). Enables incident investigation if wrong-target occurred.

### Metrics
1. **wrong_target_action_attempts_per_day**: Target: 0; Any wrong-target is critical
2. **target_confirmation_mismatch_rate_percent**: Target: < 0.01%; Alert threshold: > 0.05%; Track: mismatches, agents, targets
3. **target_confirmation_accuracy_rate_percent**: Target: 99.9%; Measure confirmations that match actual execution
4. **target_validation_failure_rate_percent**: Target: < 0.1%; Measure validation rule catches
5. **bulk_action_target_anomaly_detection_rate_percent**: Target: > 95%; Detect unusual target mixes

### Alerts
1. **Target Confirmation Mismatch Detected** (P1 - Critical): Condition - confirmed_target ≠ executed_target. Action: Immediately block action execution, audit investigation, attempted rollback, stakeholder notification.
2. **Target Validation Failure** (P2 - Warning): Condition - target fails validation rules for action type. Action: Block action, notify agent with failure reason, require manual override with justification.
3. **Bulk Action Target Anomaly** (P1 - Critical): Condition - batch operation targets unusual resources (e.g., 95% of targets older than 1-year threshold). Action: Auto-pause operation, require manual review and confirmation, audit sample of targets.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| target_confirmation_mismatch_rate_percent | > 0.05% |
| wrong_target_action_attempts_per_day | > 0 |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Target Confirmation Mismatch Detected | Confirmed target does not match the actually executed target | Critical |
| Bulk Action Target Anomaly | Batch operation targets an unusual resource mix relative to baseline | Critical |

---

## References

- [Tool-Augmented-LLM-Testing](https://homes.cs.washington.edu/~rjust/publ/tallm_testing_ast_2025.pdf)
- Note: Failures in tool-augmented LLM systems and testing implications.
