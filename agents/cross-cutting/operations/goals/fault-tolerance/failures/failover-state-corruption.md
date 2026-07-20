# Failover State Corruption

## Issue
During the process of transferring state to a failover instance — replicating in-memory session data, migrating an in-progress agent execution context, transferring a partially-written data structure — the state itself becomes corrupted in transit, so the standby comes up with internally inconsistent or malformed data rather than a clean (if slightly stale) copy. This differs from failover-data-loss (specific writes missing entirely) and failover-correctness-failure (standby running stale-but-internally-consistent code/config): here the transferred state is actively broken — partial objects, torn records, mismatched cross-references — because the transfer mechanism itself was not atomic or crash-safe.

**Frequency**: Rare

**Symptoms**
- The standby comes up and passes basic health checks, but specific requests crash with deserialization errors, null-reference exceptions, or constraint violations referencing transferred state
- Data structures on the standby show internal inconsistency (e.g. a record's foreign key points to an entity that doesn't exist, or a multi-field object has some fields from an old version and some from a new one)
- Corruption is intermittent and tied to which records happened to be mid-write on the primary at the exact moment of transfer, rather than affecting all data uniformly
- Restarting the standby process sometimes "fixes" the symptom temporarily if it reloads from a clean snapshot, masking the underlying transfer defect

## Root Cause
State transfer mechanisms that are not designed to be atomic with respect to the primary's in-memory or on-disk write operations can capture a record mid-mutation — for example, streaming a serialized copy of an in-progress agent conversation state while a separate thread is still appending to it, or copying a multi-field session object field-by-field instead of as a single atomic snapshot. If the primary fails (or the transfer mechanism itself has a bug) at the exact moment a record is only partially copied, the standby ends up with a torn, half-written version of that record rather than either the fully-old or fully-new version. This is distinct from ordinary replication lag (which produces staleness, a consistent past state) — corruption produces a state that never validly existed on the primary at any single point in time.

## Example
```
Setup: A long-running customer-support agent maintains in-memory
conversation state (message history, extracted entities, current task
plan) that is periodically snapshotted to a standby via a background
serializer for warm-standby failover.

10:05:00.000 - Primary's serializer begins snapshotting session
               #af31c9's state: it serializes message_history first,
               then entities, then current_task_plan as three separate
               writes to the transfer buffer (not a single atomic
               snapshot).

10:05:00.012 - Concurrently, the agent's main loop processes a new user
               message for session #af31c9, appending to message_history
               and updating current_task_plan (removing a completed
               subtask) as part of normal operation.

10:05:00.015 - The serializer's write of current_task_plan captures the
               UPDATED (post-message) version, but its earlier write of
               message_history had already captured the PRE-message
               version. The standby now has message_history that does
               not include the user's latest message, but
               current_task_plan that reflects a subtask as completed
               based on that message.

10:05:03.000 - Primary crashes. Standby is promoted with session
               #af31c9 in this torn state.

10:05:05.000 - The agent, now running on the standby, tries to explain
               to the user why a subtask is marked complete, but has no
               record in message_history of the message that completed
               it, and produces an incoherent response referencing
               information it cannot find, then throws a null-reference
               exception trying to look up a message ID that the task
               plan references but message_history doesn't contain.
```

## Statistics
| Finding | Context |
|---------|---------|
| Non-atomic multi-field state transfer is a common root cause identified in post-failover data-integrity incidents | Estimated from postmortem categorization of failover corruption cases |
| Corruption incidents affect only records that were mid-mutation at transfer time, typically a small fraction of total transferred state per incident | Typical range observed in transfer-timing-dependent corruption |
| Moving to atomic/copy-on-write snapshotting for state transfer is reported to eliminate the vast majority of torn-state corruption incidents | Reported range across teams that redesigned transfer mechanisms |

## Mitigations
1. **Atomic snapshot transfer**: Use copy-on-write, versioned immutable snapshots, or a single-write serialization of the entire state object rather than field-by-field or multi-step transfer, so any captured snapshot is guaranteed internally consistent.
2. **Checksums and structural validation on the standby**: Validate transferred state against a checksum or schema/referential-integrity check before marking the standby ready to serve traffic, rejecting and re-fetching any record that fails validation.
3. **Write-ahead log replication instead of live-object snapshotting**: Replicate the same durable, ordered log of mutations the primary itself uses to persist state, rather than snapshotting live in-memory objects, so the standby reconstructs state the same way the primary would after its own restart.
4. **Quiesce-and-transfer for planned failovers**: For planned (non-emergency) failovers, briefly pause writes to the record being transferred so the snapshot is guaranteed atomic, accepting a small latency cost in exchange for correctness.
5. **Post-promotion integrity sweep**: Run an automated referential-integrity and schema-validation pass across all transferred state immediately after promotion, quarantining any records that fail validation for manual review instead of serving them.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| post_failover_deserialization_error_rate | Rate of deserialization/validation errors on transferred state after a failover event | Alert if > 0% on critical state |
| torn_record_count | Count of records failing referential-integrity or checksum validation after transfer | Alert if > 0 |
| state_transfer_atomicity_coverage | Share of state-transfer paths verified to use atomic snapshot mechanisms | Alert if < 100% for critical state types |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Torn state detected post-failover | Post-promotion integrity sweep finds any record failing validation | High | Quarantine affected records, fall back to last-known-good snapshot if available, alert data-integrity on-call |
| Deserialization error spike after promotion | post_failover_deserialization_error_rate rises above 0 following a failover | High | Treat as active incident distinct from the original outage; investigate transfer mechanism atomicity |

## Related Patterns
- [Failover Data Loss](./failover-data-loss.md) - both involve state damage during failover, one is loss of specific writes, this is corruption of transferred state structure
- [Recovery Data Corruption](./recovery-data-corruption.md) - the equivalent mechanism during recovery/replay rather than during live failover transfer
- [Failover Correctness Failure](./failover-correctness-failure.md) - both produce a standby that serves wrong results, one via stale-but-consistent state, this via internally torn state
