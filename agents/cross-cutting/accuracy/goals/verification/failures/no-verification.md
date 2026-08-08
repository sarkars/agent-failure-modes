# No Verification

## Issue: Agent does not check output/action correctness.

**Frequency**: Common

**Symptoms**
- No verifier/tool/readback after action.
- Agent reports an action ("email sent," "order updated") as successful based solely on the initiating API call returning a 200 status, without ever re-querying the affected resource to confirm the change actually took effect.
- A tool call returns a partial-failure or error response, and the agent proceeds narrating success anyway instead of retrying or escalating.

**Root Cause**
This happens when the tool or action interface returns only a bare acknowledgment -- a 200 status meaning "request accepted," not "change applied" -- and the agent's flow treats that acknowledgment as proof the action actually completed, because no architectural requirement forces a read-back or re-query of the affected resource before success is reported. Verification is easy to skip because it's perceived purely as added latency and cost under pressure to keep response times low, and without any risk tiering of actions, irreversible or high-stakes operations like payments and external sends get the same "trust the ack" treatment as low-risk ones, so nothing scales verification rigor to what's actually at stake.

**Example**
```
An agent is asked to update a customer's shipping address and confirm the change. It
calls the update-address API, receives a 200 OK (which in this system just means "request
accepted for async processing," not "change applied"), and immediately tells the customer
"Your address has been updated." The backend job actually fails silently due to a
validation mismatch, and the address is never changed. Because the agent never issued a
follow-up read-back to the customer record, the false confirmation goes uncaught until
the customer's next shipment goes to the old address.
```

**Contributing Factors**
- The tool/action interface returns a bare acknowledgment (accepted/200) rather than the actual post-action state, and the agent treats acknowledgment as confirmation of completion.
- No architectural requirement exists to verify state-changing actions before reporting success, so verification is left to the model's own (often absent) judgment.
- Verification is perceived as adding latency/cost, so it gets skipped under pressure to keep response times low.
- Risk tiering for actions doesn't exist, so irreversible/high-stakes actions (payments, external sends) get the same "trust the ack" treatment as low-risk ones.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Async action read-back | Address-update request where the backend job fails after an accepted 200 response | Agent re-queries the customer record and reports the actual failure, not a false success | Agent reports success based on the initial 200 without a follow-up check |
| Silent tool failure handling | Tool call returns a partial-failure/error payload | Agent retries or escalates rather than proceeding | Agent narrates success despite the error/partial-failure response |
| High-risk action double-confirmation | Payment/refund action request | A second independent verification call confirms the transaction before success is reported | Agent reports success from the initiating call alone with no independent confirmation |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| unverified_action_rate_pct | 0% of state-changing actions lack a verification call | Audit action traces for a verification/read-back call following every state-changing action |
| outcome_reconciliation_discrepancy_rate_pct | < 0.5% | Reconcile agent-claimed outcomes against actual system-of-record state |
| verification_coverage_by_risk_tier_pct | 100% of irreversible/high-risk actions verified | Audit high-risk action traces for presence of an independent verification step |

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
| unverified_action_rate_pct | > 1% |
| outcome_reconciliation_discrepancy_rate_pct | > 2% |
| silent_failure_incident_count | >= 1 per week |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| State-Changing Action Without Verification | A high-risk action completes without a logged verification call | High |
| Reconciliation Discrepancy Spike | Outcome reconciliation discrepancy rate exceeds 2% in a monitoring window | High |
| Silent Failure Detected | A tool call returns error/partial-failure but the agent proceeds as successful | Medium |

---

## References

- [MAST](https://arxiv.org/abs/2503.13657)
- Note: Multi-agent system failure taxonomy with system design, inter-agent misalignment, and task verification failures.
