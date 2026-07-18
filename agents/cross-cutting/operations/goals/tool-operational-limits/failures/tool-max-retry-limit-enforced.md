# Tool Max Retry Limit Enforced

## Issue
Some tools track retry attempts server-side per operation (keyed by an idempotency key, request ID, or resource ID) and permanently block further retries once a maximum attempt count is reached within a window — for example, a payment gateway that hard-fails an idempotency key after 5 attempts, refusing all further retries regardless of the reason for prior failures. An agent's own retry counter, especially one held in process memory or reset on deploy/restart, frequently loses sync with this server-side count, so the agent believes it has budget for more attempts and keeps retrying into a wall that will never open, wasting time and obscuring the real failure behind a misleading "max retries exceeded" or generic error each time.

**Frequency**: Occasional

**Symptoms**
- Retry attempts that continue well past what the agent's own logs show as its retry budget, because a process restart reset the agent's local counter while the server's counter persisted
- A specific, permanent-sounding error (e.g., "idempotency key permanently locked" or "maximum attempts exceeded for this operation") that the agent's generic retry-eligibility check doesn't recognize as terminal
- Operations that can never succeed again under the same key/ID, requiring a new idempotency key or resource identifier to proceed, which the agent's retry logic doesn't know to generate
- Retry loops that appear to run indefinitely (or until an external timeout) against an operation the server has already permanently rejected
- Discrepancy between the agent's internal retry-count metric and the actual number of attempts the server has recorded for the same operation, visible only by cross-referencing agent logs against server-side audit logs

## Root Cause
Server-side retry tracking exists to prevent an operation (particularly one with side effects, like a payment or a write with an idempotency guarantee) from being retried indefinitely, since unlimited retries against a persistently-failing operation waste resources and can indicate a client bug rather than transient failure. Agents typically implement their own retry-count tracking in process memory or in a local per-call scope, which does not survive process restarts, deploys, or horizontal scaling (a retry issued by a different worker instance than the one that made earlier attempts has no visibility into those prior attempts). When the agent's local counter and the server's counter diverge — almost always with the agent's counter under-counting relative to the server's true count — the agent believes it still has retries available long after the server has permanently closed the door on that specific operation/key, and its generic error handling doesn't distinguish "temporarily rejected, retry later" from "permanently blocked, need a new key."

## Example
```
An agent processes payment retries for failed subscription charges. It
uses an idempotency key derived from `{customer_id}_{billing_period}` and
tracks retry attempts in an in-memory counter within its current process,
capped locally at 3 attempts per charge. The payment gateway also tracks
attempts against that same idempotency key server-side, hard-capping at
5 attempts, after which the key is permanently locked and returns
`{"error": "idempotency_key_locked", "attempts": 5, "max_attempts": 5}`
for any further use of that key, even for what would otherwise be a
retriable transient failure. The agent's worker process crashes and
restarts after 2 failed attempts (in-memory counter resets to 0). The
new process instance retries 3 more times (attempts 3, 4, 5 server-side),
hitting the server's 5-attempt cap. It then crashes and restarts again;
the new instance's local counter is again 0, so it attempts a 6th
server-side retry against the now-permanently-locked key, receiving
`idempotency_key_locked` — which its error handler classifies as a
generic retriable 4xx and retries two more times identically, before
finally surfacing an unhelpful "payment failed" error with no mention
that the key needs to be regenerated to make any further progress.
```

## Statistics
| Finding | Context |
|---------|---------|
| Idempotency-key-based retry caps in payment and messaging APIs are commonly set in the 3-10 attempt range within the key's TTL window | Common in payment gateway and transactional messaging API designs |
| In-memory or process-local retry counters are a common implementation choice that does not survive process restarts, a frequent source of agent/server retry-count divergence | Typical of stateless or auto-scaled agent worker architectures |
| Server-side "permanently locked" or "max attempts exceeded" errors are frequently misclassified by generic retry-eligibility logic as ordinary retriable errors, since the error's HTTP status class often overlaps with transient error codes | Based on typical generic HTTP-status-based retry classification |

## Mitigations
1. **Persist retry counters outside process memory, keyed to the same identifier the server uses**: Store attempt counts in a durable store (database row, distributed cache) keyed by the same idempotency key or request ID the server tracks against, so counters survive restarts and are shared across worker instances.
2. **Parse and honor terminal-failure signals distinctly from transient ones**: Recognize server responses that indicate a permanent block (explicit "locked"/"max attempts exceeded" errors, or a documented attempt count reaching the known max) and route these to a non-retriable failure path rather than the generic retry loop.
3. **Generate a new idempotency key/identifier when a terminal block is confirmed and a genuine retry is still desired**: If server-side attempts are exhausted for a key but the underlying operation should still be attempted again (e.g., after fixing an upstream data issue), deliberately mint a new key rather than reusing the locked one.
4. **Reconcile local and server-side attempt counts periodically**: Where the API exposes an attempts-remaining or attempts-used field in responses, use it to correct the agent's local counter rather than trusting local state exclusively.
5. **Cap total attempts conservatively below the known server-side max**: Configure the agent's own retry ceiling with margin below the server's documented max attempts, so counter drift from a restart doesn't push the combined attempt count past the server's hard limit before the agent's own logic would have stopped anyway.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `retry.local_counter_vs_server_reported_attempts_delta` | Difference between the agent's local retry count and the server's reported attempt count for the same key | Alert if delta != 0 |
| `retry.terminal_block_misclassified_as_retriable_count` | Count of retries issued against an operation that had already received a terminal/locked error | Alert if > 0 |
| `retry.process_restart_mid_retry_sequence_count` | Count of process restarts occurring while a retry sequence for a given key is in progress | Track as a leading indicator of counter-drift risk |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Server-side max retries permanently exceeded | Terminal "locked"/"max attempts" error received | High | Halt retries for that key immediately, mint new idempotency key if operation must be re-attempted |
| Retry-counter divergence detected | Local retry count differs from server-reported attempt count for the same operation | Medium | Migrate retry-count storage to a durable, server-key-aligned store |

## Related Patterns
- [Backoff Envelope Violation](./backoff-envelope-violation.md) - incorrect retry timing that can accelerate reaching a server-side max-retry wall
- [Batch Total Operations Limit](./batch-total-operations-limit.md) - another server-tracked rolling counter independent of client-side state that agents commonly fail to mirror
- [Request Timeout No Graceful Handling](./request-timeout-no-graceful-handling.md) - timeouts are a common trigger for the retry sequences that then run into a server-side max-retry block
