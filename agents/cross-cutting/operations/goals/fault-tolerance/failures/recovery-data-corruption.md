# Recovery Data Corruption

## Issue
The process of recovering a system after a failure — replaying a write-ahead log, re-running a batch job from a checkpoint, restoring from a snapshot combined with incremental logs — itself introduces data corruption, rather than faithfully restoring the pre-failure state. A partial write during log replay, a crash that interrupts the recovery process itself mid-way, or an off-by-one in checkpoint/log-offset alignment can leave the recovered system with malformed or partially-applied data. This is specifically about the recovery mechanism damaging data, as opposed to recovery simply being slow (recovery-time-objective-miss) or replaying events out of causal order (recovery-ordering-violation).

**Frequency**: Rare

**Symptoms**
- Data integrity checks (checksums, referential integrity, schema validation) fail specifically on records touched during a recent recovery event, and only those records
- The recovery process itself crashes or is interrupted partway through replay, and is restarted without first verifying whether partially-applied changes need to be rolled back
- Corrupted records show partial application of a single logical operation — e.g. one field of a multi-field update applied, others not
- The corruption is only discovered by a downstream consumer or a later integrity audit, well after the recovery was marked "successful"

## Root Cause
Recovery mechanisms replay a sequence of operations (log entries, transactions, batch steps) against a base state, and this replay is only safe if each operation is either applied in full or not at all (atomicity) and if the replay process can itself be safely interrupted and resumed without re-applying or partially applying an entry twice. When the recovery/replay code doesn't treat each entry as an atomic unit — for example, applying a multi-field update field-by-field rather than as a single transaction, or writing progress checkpoints at a granularity coarser than the atomic unit of replay — an interruption during recovery (a crash, an OOM kill, a manual abort) can leave a partially-applied entry on disk. Because recovery is itself the failure-handling path, there's often less test coverage and less operational rigor around it than around the primary write path, so this failure mode is discovered less often in testing and more often in production.

## Example
```
Setup: InventoryService recovers from a crash by replaying its
write-ahead log from the last durable checkpoint. Each log entry
represents a stock adjustment with two fields: quantity_delta and
reason_code, written as two separate disk writes for historical reasons
rather than one atomic write.

11:00:00 - InventoryService crashes mid-operation. Last durable
           checkpoint is at log offset 88,402.

11:00:05 - Recovery process starts, begins replaying log entries from
           offset 88,402 onward. Entry 88,415 represents a stock
           adjustment: quantity_delta=-50, reason_code="damaged_goods".

11:00:05.200 - Recovery writes quantity_delta=-50 to the live inventory
               record for SKU-4471.

11:00:05.210 - The recovery process itself is OOM-killed by the host
               (unrelated memory pressure from another process on the
               same node) before writing reason_code.

11:00:20 - Orchestrator restarts the recovery process. It reads the
           last recovery checkpoint, which was only updated after FULL
           entries (not sub-fields) — so it correctly identifies entry
           88,415 as not-yet-checkpointed and re-applies it.

11:00:20.500 - The re-applied entry executes quantity_delta=-50 AGAIN
               (since the recovery logic doesn't know the first write
               partially succeeded), resulting in SKU-4471's inventory
               count being reduced by 100 instead of 50, while
               reason_code is now correctly recorded — but for the
               wrong total.

Two weeks later, a warehouse reconciliation audit flags SKU-4471 as
50 units short with no matching adjustment reason, eventually traced
back to this partial-write-then-reapply sequence during recovery.
```

## Statistics
| Finding | Context |
|---------|---------|
| A meaningful share of post-recovery data-integrity incidents trace to non-atomic multi-step writes within a single logical recovery operation | Estimated from postmortem analysis of recovery-related corruption |
| Corruption from interrupted recovery is disproportionately rare compared to other cascade/recovery patterns but disproportionately costly to detect and repair | Typical range observed given delayed detection via periodic audits |
| Making recovery replay operations atomic and idempotent is reported to eliminate nearly all partial-write corruption on retried recovery | Reported range across teams that redesigned replay to be transactional |

## Mitigations
1. **Atomic replay of each logical operation**: Ensure every log entry or checkpoint step is applied as a single atomic write (e.g. a database transaction) rather than as multiple separate writes, so a mid-replay interruption cannot leave a partially-applied entry.
2. **Idempotent recovery operations**: Design each replayable operation to be safely re-appliable (e.g. absolute-value sets or dedup-keyed deltas rather than raw increment/decrement) so that recovery restarting and re-processing an already-partially-applied entry cannot double-apply it.
3. **Fine-grained, atomic-unit-aligned checkpointing**: Write recovery progress checkpoints at the same granularity as the atomic unit of replay (never coarser), so a restarted recovery process can precisely determine what was and wasn't fully applied.
4. **Post-recovery integrity verification as a mandatory gate**: Run an automated checksum/referential-integrity pass over all records touched during recovery before declaring recovery complete or resuming normal traffic.
5. **Recovery-path test coverage equal to the primary write path**: Include interrupted-recovery scenarios (kill the recovery process mid-replay, verify no corruption) in the same test suite rigor applied to the primary write path, not as an afterthought.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| post_recovery_integrity_check_failures | Count of records failing checksum/referential-integrity validation after a recovery event | Alert if > 0 |
| recovery_process_interruption_count | Number of times the recovery process itself crashed or was killed mid-replay | Alert if > 0 |
| double_applied_entry_count | Count of log entries detected as applied more than once during recovery | Alert if > 0 |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Post-recovery integrity failure | Any record fails integrity check immediately following a recovery event | High | Quarantine affected records, halt dependent processing, run full audit of records touched during recovery |
| Recovery process interrupted mid-replay | recovery_process_interruption_count > 0 | High | Do not resume automatically without verifying atomicity of the last applied entry |

## Related Patterns
- [Recovery Ordering Violation](./recovery-ordering-violation.md) - a related replay-correctness failure, one is about corrupting individual entries, the other about applying correct entries in the wrong sequence
- [Recovery Partial Failure](./recovery-partial-failure.md) - both involve incomplete recovery, but this pattern is about corruption within a component, that pattern is about some components recovering and others not
- [Failover State Corruption](./failover-state-corruption.md) - the equivalent corruption mechanism occurring during live state transfer rather than log replay
