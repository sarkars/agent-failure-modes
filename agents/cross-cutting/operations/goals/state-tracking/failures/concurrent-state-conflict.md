# Concurrent State Conflict

## Issue: Multiple agents/users modify same object without coordination.

**Frequency**: Common

**Symptoms**
- Race conditions; conflicting updates.
- [Add more specific symptoms]

**Root Cause**
Multiple agents/users modify same object without coordination.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- [List factors that make this failure more likely]

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| [Test name] | [Input] | [Expected output] | [What indicates failure] |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |

## Test Scenario & Reproduction

### Scenario Setup
- Deploy two agent instances handling support tickets from the same queue, both able to update a shared `ticket` object's status field, with no version token or optimistic concurrency control on writes
- No pessimistic lock is acquired before the read-modify-write sequence on ticket status
- No conflict-resolution service exists to reconcile simultaneous updates

### Trigger Mechanism
1. Agent A reads ticket #500's current status ("open") and begins processing a "assign to specialist" update
2. Before Agent A's write completes, Agent B independently reads the same ticket's status ("open") and begins processing a "close as duplicate" update
3. Both agents write their updates without checking whether the object changed since their read
4. Whichever write lands last silently overwrites the other, with no conflict detected or logged

### Example Reproduction Steps
```
1. Agent A: read ticket #500 -> {status: "open", version: 1}
2. Agent B: read ticket #500 -> {status: "open", version: 1}
   (both reads happen within the same short window)
3. Agent A: write {status: "assigned_to_specialist"} -- no version
   check, succeeds
4. Agent B: write {status: "closed_duplicate"} -- no version check,
   succeeds, silently overwrites Agent A's assignment
5. Query final ticket #500 state -> {status: "closed_duplicate"},
   with no record that the specialist assignment ever happened
6. Run the lost-update reconciliation scan against ticket #500's
   mutation history -> confirms Agent A's write was overwritten
   without going through conflict resolution
```

### Expected Failure State
Ticket #500 ends up in the "closed_duplicate" state with the specialist assignment silently lost, because neither agent's write checked whether the object had changed since its read, and no lock or version mismatch ever surfaced the conflict. A correctly defended system requires each write to include the version read (optimistic concurrency control), so Agent B's write is rejected with a 409 conflict once Agent A's update has already advanced the version, forcing Agent B to re-read and reconcile instead of silently overwriting.

## Mitigation Strategies

### Prevention
1. **Optimistic Concurrency Control with Version Tokens**: Every mutable object carries a version number or ETag. Writes must include the version they read; the store rejects (409 conflict) any write whose version doesn't match current state, forcing the writer (agent or human) to re-read and reconcile instead of silently clobbering a concurrent change.
2. **Scoped Pessimistic Locks for Critical Sections**: For operations that cannot tolerate a reconcile-and-retry pattern (e.g., inventory decrement, ticket assignment), acquire a short-lived, narrowly-scoped lock on the specific object before the read-modify-write sequence, and release it immediately after commit, minimizing contention while eliminating the race window.
3. **Idempotency Keys on Agent-Initiated Writes**: Each agent write action carries a unique idempotency key tied to the triggering task/turn, so retries after a detected conflict don't double-apply the same change, and concurrent agents attempting the same logical operation collapse to a single effect.

### Detection & Response
1. **Conflict/Rejection Rate Monitoring**: Track the rate of version-mismatch rejections and lock-acquisition failures per object type. A sudden spike indicates either a hot object under heavy concurrent load or a bug causing an agent to loop retries without proper backoff.
2. **Lost-Update Reconciliation Scan**: Periodically compare object state against its full mutation history to detect updates that were silently overwritten by a later concurrent write without going through conflict resolution (a signal that some write path is bypassing the version check).
3. **Stuck Lock Detection**: Monitor for locks held past an expected max duration (indicating a crashed or hung agent process) and auto-release with an alert, preventing a single failed agent from deadlocking all other writers to that object.

### Architecture Patterns
1. **Versioned Object Store with Conflict Response**: The data layer returns both the current object and its version on read, requires the version on write, and returns a structured conflict response (current state + attempted state) on mismatch so the caller can build a merge/retry strategy instead of failing opaquely.
2. **Conflict Resolution Service**: A dedicated component receives conflict events, applies domain-specific merge rules where safe (e.g., additive counters, disjoint field updates) and routes to human/agent re-decision where merges aren't safe (e.g., conflicting status transitions).
3. **Distributed Lock Manager with TTL**: A lock service (e.g., backed by a consensus store) issues time-boxed leases for critical-section locks, auto-expiring them if the holder crashes, and exposes lock-wait metrics for contention monitoring.

### Metrics
1. **write_conflict_rate_percent**: Target: < 2% of writes to shared objects; Alert threshold: > 8%
2. **lost_update_incidents_per_week**: Target: 0; Alert threshold: > 0
3. **stuck_lock_count**: Target: 0 active beyond TTL; Alert threshold: > 0
4. **mean_conflict_resolution_latency_ms**: Target: < 500ms; Alert threshold: > 3000ms

### Alerts
1. **Lost Update Detected** (P1 - Critical): Condition - reconciliation scan finds a committed write that was silently overwritten without conflict resolution. Action: Immediate incident, restore correct state from mutation history, audit the write path that bypassed version checking.
2. **High Contention on Shared Object** (P2 - Warning): Condition - write_conflict_rate_percent exceeds 8% for a specific object class over 1h. Action: Investigate for a hot-object bottleneck, consider finer-grained locking or object partitioning.
3. **Stuck Lock Blocking Writers** (P2 - Warning): Condition - a lock is held past its TTL with pending waiters. Action: Auto-release lock, alert on-call to investigate the crashed/hung holder, verify no partial write was left in an inconsistent state.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | High |

---

## References

- [CSA-Agentic-Profile](https://labs.cloudsecurityalliance.org/agentic/agentic-nist-ai-rmf-profile-v1/)
- Note: Agentic AI governance profile built around NIST RMF.
