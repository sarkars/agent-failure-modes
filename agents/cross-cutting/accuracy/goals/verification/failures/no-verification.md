# No Verification

## Issue: Agent does not check output/action correctness.

**Frequency**: Common

**Symptoms**
- No verifier/tool/readback after action.
- [Add more specific symptoms]

**Root Cause**
Agent does not check output/action correctness.

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
1. **Mandatory Post-Action Verification Step**: For every state-changing action (write, send, purchase, update), require an explicit verification call (read-back the record, check the API response status, re-query the affected resource) before the agent reports success, scaled to task risk.
2. **Verification-by-Design in Tool Interfaces**: Design tool/action interfaces so the action's own response includes a verifiable confirmation (e.g., return the updated record, not just an ack) that the agent's flow is required to check before proceeding, rather than trusting a bare success flag.
3. **Risk-Tiered Verification Policy**: Classify actions by consequence (reversible/informational vs. irreversible/financial) and mandate verification depth accordingly — e.g., irreversible financial actions require a second independent confirmation call, not just the initiating tool's response.

### Detection & Response
1. **Unverified Action Audit**: Log every state-changing action and whether a verification step ran afterward; flag and alert on any action reported as successful without a corresponding verification call in the trace.
2. **Post-Hoc Outcome Reconciliation**: Periodically reconcile the agent's claimed outcomes against the actual system-of-record state (did the "sent" email actually send, did the "updated" record actually update); track discrepancy rate.
3. **Silent Failure Pattern Detection**: Monitor for tool calls that return errors or partial failures but are followed by the agent proceeding as if successful (no retry, no escalation), a strong signal that verification logic is missing or broken.

### Architecture Patterns
1. **Verify-Then-Report Action Wrapper**: Every action-executing tool call is wrapped so the agent's success message can only be generated after a verification sub-call confirms the expected state change occurred; failure to verify routes to retry or escalation instead of a success report.
2. **Idempotent Action + Confirmation Ledger**: State-changing actions are logged to an append-only ledger with pending/verified/failed status, and downstream steps only proceed once an action is marked verified, giving an auditable trail distinct from the agent's own narration.
3. **Independent Verification Service**: For high-risk actions, verification is performed by a service separate from the one that executed the action (different code path/credentials), avoiding the case where a single buggy integration both performs and "confirms" the same broken action.

### Metrics
1. **unverified_action_rate_pct**: Target: 0% of state-changing actions lack a verification call; Alert threshold: > 1%
2. **outcome_reconciliation_discrepancy_rate_pct**: Target: < 0.5%; Alert threshold: > 2%
3. **silent_failure_incident_count**: Target: 0 per week; Alert threshold: >= 1
4. **verification_coverage_by_risk_tier_pct**: Target: 100% of irreversible/high-risk actions verified; Alert threshold: < 100%

### Alerts
1. **State-Changing Action Without Verification** (P1 - Critical): Condition - a high-risk action (payment, irreversible write, external communication) completes without a logged verification call. Action: Halt further automation for that flow, manual reconciliation, patch the missing verification gate before re-enabling.
2. **Reconciliation Discrepancy Spike** (P1 - Critical): Condition - outcome reconciliation discrepancy rate exceeds 2% in a monitoring window. Action: Incident response, audit affected records, notify impacted users if needed.
3. **Silent Failure Detected** (P2 - Warning): Condition - a tool call returns error/partial-failure but the agent proceeds as successful. Action: Investigate error-handling logic, add regression case, review recent tool-integration changes.

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

- [MAST](https://arxiv.org/abs/2503.13657)
- Note: Multi-agent system failure taxonomy with system design, inter-agent misalignment, and task verification failures.
