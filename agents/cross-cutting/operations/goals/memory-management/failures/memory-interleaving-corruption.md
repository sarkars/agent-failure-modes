# Memory Interleaving Corruption

## Issue
When two writes to the same memory record happen concurrently and the storage layer performs a non-atomic read-modify-write cycle (read current value, apply an update in application code, write the result back), the two writes can interleave: both read the same starting state, both compute an update based on that stale starting state, and the second write to complete overwrites the first — or worse, a field-level race produces a record that mixes fragments of both updates, a state that neither writer ever intended and that doesn't correspond to either update applied cleanly. Unlike a full corrupted record from a crashed write, this is a "successfully" completed write that is nonetheless wrong because of the race.

**Frequency**: Occasional

**Symptoms**
- A memory record reflects neither of two concurrent updates cleanly, but some inconsistent blend of both
- An update that was applied is later found to have been silently overwritten by a concurrent, unrelated update to the same record
- Record fields are individually valid but mutually inconsistent (e.g. a status field from one update paired with a timestamp from another)
- Bug is intermittent and reproduces only under concurrent load, not in single-threaded testing
- No error or exception is raised anywhere in the write path — both writes report success

## Root Cause
A classic read-modify-write race: two concurrent processes (two agent instances, or an agent and a background job) each read a record's current state, compute a locally-correct update based on that state in application memory, and write the result back — without a lock, compare-and-set, or transaction wrapping the whole read-modify-write sequence. If both reads happen before either write, both updates are computed from the same stale base state; whichever write lands last "wins" and silently discards the other's intended change. If the storage layer additionally allows field-level or partial writes without an aggregate lock, the two writes can genuinely interleave at the storage level, producing a record with some fields from update A and some from update B — a combination that was never valid from either writer's perspective.

## Example
```
Memory record for a user's task list, keyed by user_id, stored as
a single JSON blob:
  { "tasks": ["draft proposal", "call client"], "version": 4 }

Agent A (processing a new task request) at t=0:
  reads record (version 4, 2 tasks)
  computes: tasks = tasks + ["draft proposal", "call client",
            "review contract"]

Agent B (processing a task completion) at t=0.1 (before A writes):
  reads record (version 4, 2 tasks)
  computes: tasks = ["call client"]  (removes "draft proposal"
            as completed)

Agent A writes at t=0.5: { "tasks": [..., "review contract"],
                            "version": 5 }
Agent B writes at t=0.6, overwriting A's write since there's no
compare-and-set: { "tasks": ["call client"], "version": 5 }

Final stored state: "review contract" (added by A) is silently
lost, and the version number gives no indication a conflicting
write happened — it looks like a clean sequential update to
version 5, but is actually the second of two racing writes
clobbering the first.
```

## Statistics
| Finding | Context |
|---------|---------|
| Read-modify-write races on shared records without compare-and-set typically produce lost-update incidents proportional to concurrent-writer count and update frequency | Typical pattern for unsynchronized concurrent access to mutable records |
| Systems relying on "last write wins" without versioning show a measurable rate of silently discarded updates under concurrent multi-agent load in stress testing | Reported range across teams load-testing multi-agent write paths |
| Adding optimistic concurrency control (compare-and-set on a version field) eliminates the large majority of observed lost-update incidents in comparative testing | Estimated from before/after adoption of optimistic locking |

## Mitigations
1. **Optimistic concurrency control**: Require writes to include the version they read and reject (forcing a retry with a fresh read) if the stored version has since changed, rather than blindly overwriting.
2. **Atomic field-level operations**: Where possible, express updates as atomic operations (append-to-list, increment, compare-and-swap on a specific field) supported natively by the store, rather than read-full-record/modify-in-app/write-full-record.
3. **Record-level locking for hot entities**: For records under frequent concurrent access, use a short-lived lock around the read-modify-write sequence to serialize conflicting updates.
4. **Retry-on-conflict logic**: Have writers detect a failed compare-and-set and automatically retry by re-reading the current state and reapplying their intended change, rather than treating the conflict as a hard error.
5. **Write audit logging**: Log every write with its base version and resulting version so lost-update incidents can be detected retroactively by scanning for version gaps or writes that silently reverted a prior writer's change.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| lost_update_rate | Rate of detected writes whose intended change was subsequently overwritten by a concurrent write with no merge | Alert if > 0.1% of concurrent writes |
| compare_and_set_conflict_rate | Rate at which optimistic-concurrency writes are rejected due to version mismatch | Alert if sustained > 5% (indicates high contention) |
| interleaved_field_anomaly_count | Records detected with mutually inconsistent field combinations suggesting a partial interleaved write | Alert if > 0 |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Lost update detected | A write is found to have silently discarded a concurrent writer's change | High | Reconcile record manually, review whether affected write path lacks optimistic concurrency control |
| High write contention | compare_and_set_conflict_rate spikes for a specific record/entity type | Medium | Consider record-level locking or splitting the hot entity into finer-grained records |

## Related Patterns
- [Memory Corruption Detection Failure](./memory-corruption-detection-failure.md) - both leave a record in a state neither writer intended, though this pattern is caused specifically by concurrent write races rather than partial/failed writes
- [Memory Inconsistency Between Agents](./memory-inconsistency-between-agents.md) - a read-side version of the same underlying concurrency problem, where divergent reads rather than colliding writes cause the inconsistency
- [Memory Priority Inversion](./memory-priority-inversion.md) - concurrency control mechanisms (locks) intended to prevent interleaving can themselves introduce priority inversion under contention
