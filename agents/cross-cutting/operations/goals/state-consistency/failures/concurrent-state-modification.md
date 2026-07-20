# Concurrent State Modification

## Issue
Two or more agent instances (or an agent and a background job) read the same piece of shared state — a task queue entry, a customer record, a conversation memory slot — modify their own in-memory copy, and write it back without any locking or optimistic-concurrency check. Whichever write lands last silently overwrites the other, so one agent's update disappears without either agent, or the user, ever being told a conflict occurred.

**Frequency**: Common

**Symptoms**
- A field that was updated by one agent run reverts to an earlier value shortly after, with no error logged
- Two agents working the "same" ticket/record each believe they applied their change successfully
- Audit logs show two writes to the same record within milliseconds, with the second silently discarding the first's fields
- Counters (retry counts, inventory levels, budget balances) drift below or above the value that sequential accounting would predict
- Bug reports are hard to reproduce because the failure depends on the exact interleaving of two concurrent runs

## Root Cause
Most agent frameworks treat "read state, decide, write state" as three separate calls rather than one atomic operation, because the decision step (an LLM call) can take seconds and holding a database lock across a multi-second LLM round trip is avoided for performance and deadlock-risk reasons. That leaves a window between read and write during which another writer can also read the pre-update value, make its own decision, and write — a classic read-modify-write race. Without optimistic locking (a version/etag check on write) or pessimistic locking (a held lock for the whole cycle), the last writer wins and simply clobbers whatever the other writer produced, with no conflict signal raised to either side.

## Example
```
Two instances of a support-ticket triage agent poll the same queue every 10
seconds because a scaling event briefly ran two replicas.

t=0.00s  Agent A reads ticket #4521: {status: "open", assignee: null,
         priority: "normal"}
t=0.02s  Agent B reads ticket #4521: {status: "open", assignee: null,
         priority: "normal"}   (same pre-image, no lock taken)
t=1.40s  Agent A's LLM call finishes: decides to set
         {assignee: "agent-A", priority: "high", status: "in_progress"}
         and writes it.
t=1.55s  Agent B's LLM call finishes independently: decides to set
         {assignee: "agent-B", status: "in_progress"} (priority untouched
         in B's local copy, still "normal")
         and writes it, overwriting A's write.

Result: ticket #4521 ends up assigned to agent-B with priority "normal",
silently discarding agent-A's "high" priority escalation. Neither agent
logs an error. The escalation is only noticed four hours later when an
SLA breach alert fires on a ticket that should have been fast-tracked.
```

## Statistics
| Finding | Context |
|---------|---------|
| 5-15% of duplicate-worker incidents in agent queue systems result in a silently lost field update rather than a visible duplicate-processing error | Typical range observed in production agent telemetry |
| Adding optimistic-locking version checks reduces silent-overwrite incidents by an estimated 80-95% | Reported range across teams instrumenting write-conflict detection |
| Race windows of 0.5-3 seconds (matching typical LLM call latency) account for the large majority of observed concurrent-write collisions | Estimated from workflows with concurrency logging enabled |

## Mitigations
1. **Optimistic concurrency control**: Attach a version number or etag to every read; require writes to include the version they read and reject (with a retriable conflict error) if it no longer matches, rather than blindly overwriting.
2. **Compare-and-swap on critical fields**: For fields written by multiple agents (status, assignee), use atomic compare-and-swap or database-level conditional updates instead of full-record overwrites, so unrelated fields written by another agent aren't clobbered.
3. **Single-writer ownership per record**: Route all writes for a given entity through one owning process or a per-key queue/lock, so concurrent agent instances never race on the same record even if they both read it.
4. **Field-level merge instead of full overwrite**: Write only the fields the agent actually changed (a patch) rather than the full record snapshot it read, so a concurrent writer's untouched fields survive.
5. **Idempotency and dedup keys upstream**: Prevent the duplicate-reader scenario in the first place by ensuring queue/poll systems hand a given item to only one worker at a time (visibility timeouts, leases) instead of relying on downstream locking to paper over duplicate delivery.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| write_conflict_rate | Fraction of writes rejected or detected as overwriting a newer version | Alert if > 0.5% of writes |
| lost_update_count | Count of fields reverted to a stale value shortly after being set (detected via version diffing) | Alert if > 0 in a given window |
| concurrent_reader_overlap | Count of records read by two+ agent instances within the same decision window before either writes | Alert if sustained > baseline |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Silent overwrite detected | Version-diff job finds a write that reverted a field set by a more recent prior write | High | Page on-call, replay the lost update from audit log, investigate duplicate-worker cause |
| Conflict rate spike | write_conflict_rate exceeds threshold for 3+ consecutive windows | Medium | Check for scaling events producing duplicate workers, verify queue visibility-timeout configuration |

## Related Patterns
- [State Machine Violation](./state-machine-violation.md) - concurrent writers can also drive a record through an invalid transition sequence, not just lose field values
- [State Replication Lag](./state-replication-lag.md) - a related timing failure where the read side, not the write side, sees stale state
- [State Consistency Timeout](./state-consistency-timeout.md) - describes what happens when the safeguards meant to catch this race (a consistency check) themselves fail to complete
