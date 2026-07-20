# Handoff State Loss

## Issue
Task state accumulated by the sending agent — intermediate results, partial progress, resolved variables, in-progress computation — fails to fully transfer to the receiving agent during a handoff. Unlike context incompleteness, where a summary deliberately omits detail, state loss is typically accidental: a serialization step drops fields, a transport mechanism truncates a payload, or the receiving agent initializes its own fresh state instead of loading the transferred one, and the task effectively restarts from a blank slate without anyone intending it to.

**Frequency**: Occasional

**Symptoms**
- Receiving agent's output shows no evidence of work the sending agent had already completed (progress counters reset, prior computed values absent)
- Task duration after a handoff is inconsistent with "resuming" a task and consistent with "starting over"
- Serialization or deserialization errors in logs immediately preceding or during a handoff, sometimes swallowed by a broad exception handler
- Users or downstream systems observing the same question answered or the same step redone that had already been handled before the handoff

## Root Cause
State transfer between agents typically requires serializing an in-memory representation (which may include object references, partial computations, or framework-specific state) into a transport format (JSON, a message queue payload, a database row) and then deserializing it on the receiving end into a compatible in-memory representation. Any asymmetry in this round trip — fields that don't survive serialization, a receiving agent built against a different internal state schema, a transport with a size limit that silently truncates large payloads, or a receiving agent that defaults to initializing new state on any deserialization error instead of failing loudly — causes state to be dropped without an explicit error visible to whoever is monitoring the handoff.

## Example
```
A data-migration agent processes a 50,000-row dataset in batches,
tracking progress state: {rows_processed: 32000, last_row_id: 31999,
validation_errors: [...212 entries...], checkpoint_time: ...}.

At row 32000, the agent hands off to a "migration-finalizer" agent to
complete the remaining batches, serializing its state to a message
queue with a 256KB payload limit. The validation_errors array, after
212 entries, pushes the serialized payload to 280KB. The queue client
silently truncates the payload to fit the limit rather than raising an
error, cutting off the state object mid-field.

The migration-finalizer agent's deserializer, encountering malformed
JSON from the truncation, falls back to its default initialization
path: {rows_processed: 0, last_row_id: null, validation_errors: []}.
It re-processes all 50,000 rows from the beginning, re-writing 32,000
rows that were already correctly migrated, and losing the 212 already-
identified validation errors that a downstream cleanup step needed.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 5-15% of handoffs involving large or complex state payloads experience partial data loss during serialization/transport | Typical range observed in systems handing off substantial in-progress task state |
| Handoff mechanisms with schema-validated deserialization and explicit fallback-on-error handling show markedly fewer silent state resets than those with default-initialize-on-error behavior | Reported range across teams hardening state transfer |
| Transport payload size limits are a disproportionately common root cause of truncation-driven state loss relative to other causes | Estimated from incident classification across handoff-related postmortems |

## Mitigations
1. **Schema-validated state serialization**: Validate serialized state against an explicit schema before transport and after deserialization, and treat any mismatch as a hard failure rather than falling back to default/empty state.
2. **Checkpointing to durable storage instead of inline payloads**: For large or complex state, write a checkpoint to durable storage (database, object store) and hand off a reference/ID rather than embedding the full state in the transport payload, avoiding size-limit truncation entirely.
3. **Explicit fail-loud on deserialization error**: Never let a receiving agent silently substitute default/empty state when deserialization fails; surface it as a task failure requiring investigation.
4. **Round-trip integrity checks**: Compute a checksum or record count on the sending side and verify it against the deserialized state on the receiving side, rejecting the handoff if they don't match.
5. **State transfer load testing**: Test handoff mechanisms with realistically large and complex state payloads (not just small samples) during development, specifically probing for silent truncation or size-limit behavior.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| state_checksum_mismatch_count | Count of handoffs where the post-transfer state checksum doesn't match the pre-transfer checksum | Alert if > 0 |
| deserialization_fallback_count | Count of times a receiving agent's deserializer fell back to default/empty state | Alert if > 0 |
| handoff_payload_size_near_limit | Count of handoff payloads within 10% of the transport's size limit | Alert if > 0 |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| State checksum mismatch | Deserialized state on the receiving side fails a checksum/record-count comparison against the sender's pre-transfer state | High | Halt task, alert on-call, retrieve state from last durable checkpoint if available |
| Payload near transport size limit | A handoff payload approaches the transport mechanism's known size limit | Medium | Switch to reference-based checkpoint handoff before the limit is reached |

## Related Patterns
- [Handoff Context Incompleteness](./handoff-context-incompleteness.md) - a milder, often deliberate version of the same underlying problem: information failing to make it across the handoff boundary
- [Handoff Idempotency Violation](./handoff-idempotency-violation.md) - loss of "already processed" state specifically can cause a retried handoff to be treated as brand new
- [Handoff Rollback Failure](./handoff-rollback-failure.md) - state loss removes the very record a rollback routine would need to cleanly compensate for prior actions
