# Idempotency Failure

## Issue: Agent repeats a write action and creates duplicates.

**Frequency**: Rare but Catastrophic

**Symptoms**
- Duplicate tickets/emails/charges/events.
- Same idempotency key reused across genuinely different payloads, or omitted entirely on a retry, defeating deduplication.

**Root Cause**
The tool wrapper retries automatically on timeout without ever checking whether the original call already succeeded server-side, and because the tool's API surface exposes no idempotency-key mechanism, the agent has no way to signal "this is the same action" even if it wanted to. That gap is compounded by session state that doesn't persist which write actions were already attempted across a multi-turn conversation or a crash/restart, so a retry after a dropped connection looks to the system exactly like a brand-new, independent request.

**Example**
```
A support agent calls create_ticket() for a customer complaint. The HTTP
response times out client-side after 10s, but the server had already
committed the write. The agent's retry logic re-issues create_ticket()
with the same payload and no idempotency key, producing two open tickets
for the same complaint and two separate agent replies to the customer.
```

**Contributing Factors**
- Tool wrapper retries automatically on timeout without checking whether the original call already succeeded server-side.
- No idempotency key support exposed in the tool's API surface, so the agent has no mechanism to signal "this is the same action."
- Agent's session state doesn't persist which write actions were already attempted across a multi-turn conversation or after a crash/restart.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Timeout-then-retry duplicate | Simulate a create-ticket call that times out client-side after the server already committed the write | Agent detects the existing ticket via idempotency key or pre-write check and does not create a second one | A second ticket/charge/event appears for the same source event |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| duplicate_write_rate | < 0.1% of write actions | Reconcile write-tool call logs against created objects in the target system over a rolling 24h window |

---

## Mitigation Strategies

### Prevention
1. **Idempotency Key Injection**: Every write-tool call carries a client-generated idempotency key (deterministic hash of action + target + payload + conversation turn) that the downstream API/gateway deduplicates against a TTL-bound key store; retries or agent re-invocations with the same key return the cached result instead of executing again.
2. **Pre-Write State Check**: Before issuing a create/charge/send action, the agent queries current state (e.g., "does an open ticket already exist for this issue?") and only proceeds if the desired end-state doesn't already exist; the check-then-act sequence is wrapped in a short-lived lock to avoid races between check and write.
3. **Single-Fire Action Registry**: The tool-calling loop maintains a per-conversation ledger of write actions already attempted (action type + target + payload hash); the orchestrator blocks re-submission of an identical write within the same session/task unless explicitly confirmed by the user or a new upstream event justifies it.

### Detection & Response
1. **Duplicate Write Fingerprint Matching**: A background job hashes all completed write actions (type, target, payload) over a rolling window and flags near-duplicate writes to the same target within a short time delta; matches above a similarity threshold are surfaced for review.
2. **Downstream Duplicate-Object Scan**: A periodic reconciliation job queries the target system (ticketing, billing, calendar) for objects with matching subject/amount/recipient created within minutes of each other and cross-references them to the same agent session, surfacing suspected duplicates before they compound.
3. **Retry-Without-Key Audit**: Logs are scanned for write-tool calls lacking an idempotency key or reusing a key across different payloads; both patterns indicate the idempotency mechanism was bypassed and trigger an audit ticket.

### Architecture Patterns
1. **Idempotency Middleware Layer**: A shared gateway sits in front of all write-capable tools, requires an idempotency key header on every mutating call, persists key-to-response mappings in a fast store (Redis) with TTL matching business retry windows, and replays the stored response for repeat keys instead of re-executing.
2. **Outbox/Exactly-Once Dispatch**: The agent writes intended actions to an outbox table within the same transaction as its planning step; a separate dispatcher reads the outbox and calls the external API exactly once per row, marking rows complete only after a confirmed success response, decoupling "decided to act" from "executed."
3. **Compensating Action Framework**: Every write tool registers a matching "undo" or "merge" operation (cancel duplicate ticket, void duplicate charge) so that when duplicates are detected downstream, an automated or human-triggered compensation can collapse them without manual data surgery.

### Metrics
1. **duplicate_write_rate_percent**: Target: < 0.1%; Alert threshold: > 0.5% of write actions in a day
2. **idempotency_key_coverage_percent**: Target: 100% of write-tool calls carry a valid key; Alert threshold: < 99%
3. **key_reuse_conflict_count**: Target: 0; Alert threshold: > 0 (same key, different payload)
4. **duplicate_object_reconciliation_backlog**: Target: < 5 open items; Alert threshold: > 20 open items

### Alerts
1. **Duplicate Write Detected** (P1 - Critical): Condition - reconciliation job finds 2+ objects with matching target/payload created by the same agent session within 5 minutes. Action: Auto-flag for compensating action, halt further writes to that target until reviewed.
2. **Idempotency Key Missing** (P2 - Warning): Condition - a write-tool call executed without an idempotency key. Action: Block the call at the middleware layer, log incident, require key before retry.
3. **Elevated Duplicate Rate** (P3 - Info): Condition - duplicate_write_rate_percent exceeds target for 3 consecutive days. Action: Review recent tool/prompt changes for regressions in retry or state-check logic.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| duplicate_write_rate_percent | > 0.5% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Duplicate Write Detected | Reconciliation job finds 2+ objects with matching target/payload from the same session within 5 minutes | Critical |

---

## References

- [OWASP-LLM-Top10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- Note: LLM application risks including prompt injection, insecure output handling, supply chain, sensitive information disclosure, excessive agency.
