# Agent Handoff Race Condition

## Issue
When one agent hands off a task to another (e.g. a triage agent passing a ticket to a specialist agent), both agents briefly believe they may be responsible for the same unit of work. If the handoff isn't atomic — the sender marks the task "handed off" in one write and the receiver marks it "claimed" in a separate write — a narrow window opens where either both agents act on the task simultaneously, or neither does because each assumes the other has it. The failure is timing-dependent and often invisible in single-agent testing, only surfacing under concurrent load.

**Frequency**: Common

**Symptoms**
- Duplicate actions taken on the same task (two agents both reply to a customer, both submit the same order)
- Orphaned tasks that sit untouched because each agent's state shows the other as owner
- Handoff logs showing overlapping timestamps between "sent" and "received" events with no clear winner
- Intermittent failures that only reproduce under load or with multiple concurrent handoffs, never in isolated testing
- Downstream systems receiving conflicting or duplicate writes traced back to the same originating task ID

## Root Cause
Handoff between agents is usually implemented as two separate operations — the sending agent updates its own state to "delegated" and, independently, the receiving agent updates shared state to "claimed" — rather than as a single atomic transaction with a compare-and-swap or distributed lock. Between those two writes there is a window where the task's ownership is ambiguous: a message queue redelivery, a retry after a timeout, or a second receiver polling the same queue can all observe the pre-handoff state and act on it. Because most orchestration frameworks treat "agent A finished its turn" and "agent B started its turn" as independent events rather than a single transition guarded by a lock, the race is structural, not incidental.

## Example
```
A support orchestration system routes escalated tickets from a Triage
Agent to a Billing Agent via a shared task queue.

T+0.00s: Triage Agent decides ticket #4471 needs Billing Agent and writes
         status = "handed_off_to_billing" to the ticket record.
T+0.02s: Triage Agent's handoff message is published to the queue.
T+0.03s: A network blip delays the queue acknowledgment; the orchestrator's
         retry logic re-publishes the same handoff message.
T+0.05s: Billing Agent instance #1 picks up the first copy of the message
         and begins drafting a refund.
T+0.06s: Billing Agent instance #2 (auto-scaled to handle queue depth)
         picks up the redelivered copy of the same message and also
         begins drafting a refund, because the ticket's "claimed_by" field
         was never set atomically before both instances read it.
T+0.40s: Both instances independently call the refund API. The customer
         is refunded twice ($89.50 x 2) before a reconciliation job
         catches the duplicate three hours later.
```

## Statistics
| Finding | Context |
|---------|---------|
| Handoff race conditions account for an estimated 10-20% of duplicate-action incidents in queue-based multi-agent systems | Typical range observed in production orchestration postmortems |
| Systems using non-atomic "read state, then write state" handoffs see race-triggered duplicates roughly 1-3 times per 10,000 handoffs under normal load, rising sharply under retry storms | Estimated from instrumented handoff logs |
| Moving to compare-and-swap or single-writer claim semantics reduces duplicate/orphaned handoffs by 90%+ in reported migrations | Reported range across teams that added atomic claim checks |

## Mitigations
1. **Atomic claim with compare-and-swap**: Require the receiving agent to claim a task via a single atomic operation (e.g. `UPDATE task SET owner = B WHERE owner IS NULL`) so only one claimant can ever succeed, regardless of message redelivery.
2. **Idempotency keys on handoff messages**: Tag every handoff with a unique, stable ID and have receiving agents check-and-record that ID before acting, so a redelivered message is recognized and dropped rather than reprocessed.
3. **Single-writer ownership field**: Model task ownership as one authoritative field with a strict state machine (unassigned -> claimed -> in_progress -> done) enforced by the datastore, not by convention between agents.
4. **Explicit handoff acknowledgment protocol**: Require the receiver to send a synchronous or awaited acknowledgment back to the sender before the sender considers the handoff complete, closing the ambiguous window rather than assuming success.
5. **Reconciliation sweep for orphaned/duplicated tasks**: Run a periodic job that detects tasks with no owner past a timeout, or tasks acted on by more than one agent ID, and alerts or auto-corrects before downstream effects compound.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| duplicate_task_claim_rate | Fraction of handoffs where two or more agents recorded a claim on the same task ID | Alert if > 0.1% |
| orphaned_handoff_count | Tasks marked "handed off" with no receiver claim after N seconds | Alert if > 5 per hour |
| handoff_ack_latency_p99 | Time between sender's handoff write and receiver's acknowledgment | Alert if p99 > 2s |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Duplicate downstream action detected | Two agent instances both completed a terminal action (refund, send, submit) for the same task ID | High | Page on-call, halt affected task queue, initiate reconciliation |
| Orphaned task backlog growing | orphaned_handoff_count exceeds threshold for 3 consecutive intervals | Medium | Trigger reconciliation sweep, check queue redelivery settings |

## Related Patterns
- [Agent State Divergence](./agent-state-divergence.md) - handoff races are a specific, transaction-boundary case of the broader state-sync problem
- [Deadlock in Multi-Agent](./deadlock-in-multi-agent.md) - both stem from missing or incorrect coordination primitives around shared task ownership
- [Byzantine Agent Failure](./byzantine-agent-failure.md) - both involve one agent needing to tolerate or resolve conflicting claims from another
