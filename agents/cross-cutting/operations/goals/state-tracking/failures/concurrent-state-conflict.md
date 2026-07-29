# Concurrent State Conflict

## Issue: Multiple agents/users modify same object without coordination.

**Frequency**: Common

**Symptoms**
- Race conditions; conflicting updates.
- Last write silently wins with no conflict ever detected or logged, erasing an earlier valid update.
- Mutation history shows an object's field flipping between two agents' intended values with no reconciliation event recorded in between.
- Conflicts appear only intermittently, concentrated on whichever write path lacks a version check or lock.
- Object ends in a state that neither concurrent writer actually intended (e.g., a ticket closed as duplicate after being assigned).

**Root Cause**
Multiple agents/users modify same object without coordination.

**Example**
```
Two order-fulfillment agents both pull from the same warehouse queue.
Agent A reads order #781 (status: "pending", qty_reserved: 0) and
begins reserving 5 units of SKU-221.
Agent B reads the same order a moment later, also sees qty_reserved: 0,
and begins reserving 5 units of a substitute SKU because the primary
is low-stock.
Both writes succeed since neither checks whether qty_reserved changed
since its read. The order ends up with two overlapping reservations
against different SKUs, and the warehouse over-picks inventory that
was never actually needed twice.
No 409 conflict, lock timeout, or reconciliation alert ever fires,
so the double-reservation is only caught days later during a stock
count.
```

**Contributing Factors**
- No optimistic concurrency control (version tokens/ETags) on the shared object's write path, so a stale read is never rejected at write time.
- Multiple agent instances (or agent + human) act on the same queue or record with no shared locking service coordinating access.
- Write operations are implemented as read-modify-write rather than an atomic compare-and-swap, widening the race window.
- High-frequency access concentrated on a small set of "hot" shared objects (a single queue, a popular ticket, a shared counter) increases collision likelihood.
- No conflict-resolution service exists, so even when a conflict is technically detectable, there is no defined merge or escalation path to act on it.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Concurrent status update race | Two simulated agents read the same ticket (status="open", version=1) within 50ms, then each writes a different status without re-checking | Second write is rejected with a 409 version conflict; final ticket state reflects a deliberate reconciliation, not a race | Second write succeeds unconditionally and silently overwrites the first agent's update |
| Stuck lock auto-release | Simulate an agent process crashing mid-transaction while holding a critical-section lock on a shared inventory object | Lock is auto-released after its TTL, allowing a waiting writer to proceed | Lock remains held past TTL, blocking all other writers with no auto-release or alert |
| High-concurrency hot object | 20 concurrent simulated writers issue read-modify-write against the same shared counter with no version checks | Writes serialize correctly with zero lost updates; final counter equals the sum of all increments | Final counter undercounts writes, indicating one or more concurrent updates were silently dropped |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| version_check_enforcement_rate_percent | 100% of writes to shared objects include a version token | Scan eval-harness write logs for writes missing the version/ETag field |
| simulated_conflict_detection_rate_percent | >= 99% of injected concurrent-write pairs are caught as conflicts | Run a paired-write test harness that issues deliberately racing writes and measure the 409-rejection rate |
| lost_update_rate_in_harness_percent | 0% of simulated concurrent write pairs result in a silently overwritten update | Compare final object state against the full simulated write log after each test run |

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
| write_conflict_rate_percent | > 8% |
| lost_update_incidents_per_week | > 0 |
| stuck_lock_count | > 0 |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Lost Update Detected | Reconciliation scan finds a committed write that was silently overwritten without conflict resolution | Critical |
| High Contention on Shared Object | write_conflict_rate_percent exceeds 8% for a specific object class over 1h | Warning |
| Stuck Lock Blocking Writers | A lock is held past its TTL with pending waiters | Warning |

---

## References

- [CSA-Agentic-Profile](https://labs.cloudsecurityalliance.org/agentic/agentic-nist-ai-rmf-profile-v1/)
- Note: Agentic AI governance profile built around NIST RMF.
