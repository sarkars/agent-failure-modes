# AI Agent Creates Duplicate Orders, Charges, or Tickets: Causes and Fixes

## Issue: The agent retries a write-type tool call after a timeout or ambiguous error and ends up creating duplicate tickets, emails, orders, or charges.

**Frequency**: Rare but Catastrophic

**Symptoms**
- Multiple equivalent writes appear in the same trace.
- Customer receives 2+ identical order confirmations, charge receipts, or support tickets for a single request.
- Retry after a timeout or tool-call error re-executes the original write instead of checking whether it already succeeded.

This shows up commonly in agents built on tool-calling protocols like MCP, where a tool call's outcome can go unconfirmed after a timeout and the agent has no built-in way to tell "unknown" apart from "failed."

**Root Cause**
Write-type tool calls carry no idempotency key, so a retry is indistinguishable at the receiving system from a brand-new request — there is nothing in the request itself that says "this is the same logical operation as the one five seconds ago." The agent compounds this by treating an ambiguous outcome (a timeout, a dropped response) as "definitely failed" rather than "unknown," so it retries by default instead of first checking whether the original call actually succeeded server-side. With no shared lock across parallel execution paths (retry logic racing a user-triggered re-ask, for instance), two logically identical writes can commit independently with no mechanism at any layer positioned to recognize they're the same request.

**Example**
```
Agent calls create_charge(customer_id=C-882, amount=49.00) but the tool times out before
returning a response. The agent interprets the timeout as a failure and retries the same
call. Both calls actually succeeded server-side (the first response was just lost in
transit), so the customer is charged $98.00 across two separate charge records with no
idempotency key to link them.
```

**Contributing Factors**
- No idempotency key attached to write-type tool calls, so retries are indistinguishable from new requests.
- Agent treats a tool-call timeout or ambiguous error as "definitely failed" rather than "unknown outcome."
- Multi-turn conversations where the user restates a request the agent already fulfilled earlier in the session.
- Parallel tool-call execution paths (e.g., retry logic plus a user-triggered re-ask) racing against each other with no shared lock.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Timeout-then-retry | Tool call succeeds server-side but response is dropped, agent retries | Second call returns cached result via idempotency key, no second charge/ticket created | Two distinct resource IDs created for one logical request |
| Repeated user request same session | User re-asks for the same refund/order two turns later | Agent recognizes prior completed action and confirms status instead of re-executing | Agent silently executes the action again |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| duplicate_action_attempts_per_hour | < 0.1 | Count actions sharing (agent_id, action_type, target_id, params) signature within 24h window |

---

Fixing this means attaching idempotency keys to write calls so a retry is recognized as the same request instead of a new one.

## Mitigation Strategies

### Prevention
1. **Idempotency Keys with Deduplication Cache**: Require agent to include unique idempotency key with each action. Backend maintains time-windowed cache (24-hour TTL) mapping (agent_id, action_type, target_id, idempotency_key) → result. On duplicate key detection, return cached result instead of re-executing action.
2. **State Transition Guards**: Before executing action, check current state of target resource. Reject action if it would create invalid state transition. Example: refuse to cancel already-canceled order, refuse to approve already-approved transfer. Implement state machine validation at action entry.
3. **Action Deduplication Cache with Signature Matching**: Maintain 24-hour cache of (agent_id, action_type, target_id, normalized_params) signatures. Log cache hits. Return idempotent result on duplicate signature detection.

### Detection & Response
1. **Duplicate Action Detection via Signature Tracking**: Track action signatures in 24-hour rolling window. Flag when identical signature appears 2+ times. Alert on potential duplicate attempts. Log: original action time, duplicate attempt time, outcomes.
2. **State Integrity Checks Post-Execution**: Monitor resource state changes after each action. Alert if state exhibits impossible transitions (e.g., order total increases despite no new line items, account balance changes without recorded transaction). Compare actual delta to expected delta.
3. **Audit Trail Divergence Monitoring**: Compare intended action (from agent logs) with actual system state delta (from audit logs). Alert if gap detected. Example: intended 1 transfer but 2 transfers in audit trail = duplicate execution detected.

### Architecture Patterns
1. **Idempotency Middleware at Action Handler Entry**: All action handlers implement idempotency check as first step. Use Redis/cache layer with key = (agent_id, idempotency_key, action_type), value = {status, result}. TTL = 24 hours. Return cached result for duplicates.
2. **Event Sourcing for State Reconstruction**: Store all state changes as immutable events with idempotency keys attached. Replay event log detects duplicate event application. Use event store to reconstruct state, detect duplicates via event ID deduplication.
3. **Saga Pattern with Compensation Transactions**: For multi-step actions, use saga pattern. Each step emits event with idempotency key. On duplicate step detection, skip re-execution. Implement compensating transactions to roll back already-executed steps if needed.

### Metrics
1. **duplicate_action_attempts_per_hour**: Target: < 0.1; Alert threshold: > 0.5; Track: agent_id, action_type, timestamp
2. **idempotency_key_hit_rate_percent**: Target: 0.1% (indicates 99.9% single-execution); Low rate = system working correctly
3. **action_deduplication_latency_p99_ms**: Target: < 20ms; Ensure dedup doesn't add latency
4. **resource_state_integrity_violations_per_day**: Target: 0; Count state transition violations
5. **duplicate_action_recovery_success_rate_percent**: Target: 100%; Track successful idempotent resolutions

### Alerts
1. **Duplicate Action Detected** (P2 - Warning): Condition - same (agent, action_type, target, params) within 1-hour window. Action: Block duplicate, log idempotency cache hit, notify agent operator with evidence, investigate root cause of retry.
2. **State Integrity Violation** (P1 - Critical): Condition - resource state doesn't match expected delta from action. Example: order total changed unexpectedly. Action: Immediate audit log review, potential compensation transaction attempt, stakeholder notification.
3. **High Duplication Rate Spike** (P1 - Critical): Condition - duplicate_action_attempts_per_hour > 1 for 5+ consecutive hours. Action: Agent behavior investigation, retry logic audit, potential agent suspension pending review.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| duplicate_action_attempts_per_hour | > 0.5 |
| resource_state_integrity_violations_per_day | > 0 |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Duplicate Action Detected | Same (agent, action_type, target, params) signature within 1-hour window | Critical |
| State Integrity Violation | Resource state delta doesn't match the single intended action | Critical |

---

## References

- [OWASP-LLM-Top10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- Note: LLM application risks including prompt injection, insecure output handling, supply chain, sensitive information disclosure, excessive agency.
