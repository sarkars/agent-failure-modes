# Recovery Ordering Violation

## Issue
During recovery, logged operations are replayed in an order that violates the causal dependencies between them — an operation that logically depended on an earlier one is applied before it, or two operations that must be applied in a specific relative order are applied out of sequence — producing a state that no valid execution of the original system could ever have reached. This is distinct from recovery-data-corruption (which is about a single operation being malformed or partially applied): here every individual operation replays correctly in isolation, but the sequence is wrong.

**Frequency**: Occasional

**Symptoms**
- Post-recovery state fails business-logic invariants that depend on temporal/causal ordering (e.g. a "cancel" applied before the "create" it was meant to cancel)
- Recovered state includes effects that reference an entity or precondition that, in the wrong order, doesn't exist yet
- The individual replayed operations are each valid and well-formed, so standard schema/checksum validation passes even though the aggregate result is wrong
- Symptoms appear only for entities that had multiple related operations logged close together in time, especially across parallel log streams or partitions

## Root Cause
Ordering violations typically arise when recovery replays multiple independent log streams, shards, or partitions and merges them using an ordering key that doesn't actually preserve causal order — wall-clock timestamps from different hosts with clock skew, log sequence numbers that reset per-partition, or parallelized replay for speed that processes entries out of their original relative order to maximize throughput. Causal dependencies between operations (operation B logically depends on operation A having already happened) are usually implicit in the application logic rather than explicitly encoded in the log format, so a generic replay mechanism has no way to know it needs to preserve the A-before-B relationship unless the log entries are already in a single, globally-ordered stream — which is often not how logs are sharded for write-throughput reasons.

## Example
```
Setup: A ride-hailing dispatch agent logs two kinds of events to
per-region shards for write scalability: "driver_assigned" and
"driver_reassigned". A single trip can have both events if the first
driver cancels and a new one is assigned. Recovery replays each
region's shard in parallel to reduce total recovery time.

14:00:00.100 - Trip #7734: driver_assigned(driver=D-102) logged to
               shard-3.
14:00:00.850 - Trip #7734: driver D-102 cancels; 
               driver_reassigned(driver=D-118) logged to shard-3 as
               well (same shard, correctly ordered within it).
14:00:01.200 - A THIRD event, driver_reassigned(driver=D-118, 
               eta_update), is logged to shard-7 (a different shard,
               because ETA updates are routed to a separate
               high-throughput shard for load-balancing reasons) with a
               timestamp that, due to 400ms of clock skew between the
               two shard-writing hosts, appears to be 14:00:00.700 —
               EARLIER than the shard-3 reassignment event it actually
               depended on.

14:15:00 - System crashes. Recovery begins, replaying shard-3 and
           shard-7 in parallel and merging by logged timestamp to
           reconstruct global order.

14:15:05 - Because of the clock skew, the merge applies the shard-7
           ETA update (nominally 14:00:00.700) BEFORE the shard-3
           driver_reassigned event (14:00:00.850) that it causally
           depended on. The recovered state shows an ETA update
           referencing driver D-118 attached to trip #7734 while the
           trip's driver field still shows D-102 (the reassignment
           hadn't "happened" yet in replay order), producing an
           internally contradictory trip record that confuses both the
           rider-facing app and the driver-facing app.
```

## Statistics
| Finding | Context |
|---------|---------|
| Cross-shard or cross-partition replay ordered by wall-clock timestamp is a common root cause of ordering violations when any inter-shard clock skew exists | Estimated from postmortem analysis of multi-shard recovery incidents |
| Ordering violations are typically discovered through business-invariant failures rather than technical errors, since each replayed operation is individually well-formed | Typical range observed in ordering-violation incident detection |
| Adopting a single global logical clock (e.g. vector clocks or a centralized sequencer) for cross-shard causal ordering is reported to eliminate the large majority of these violations | Reported range across teams migrating from wall-clock to logical-clock ordering |

## Mitigations
1. **Logical clocks instead of wall-clock timestamps for cross-shard ordering**: Use vector clocks, Lamport timestamps, or a centralized monotonic sequencer to establish causal order across shards, rather than relying on host wall-clock timestamps that are subject to skew.
2. **Explicit causal dependency encoding**: Where an operation depends on a prior one, encode that dependency explicitly in the log entry (e.g. "depends on event ID X") so replay can enforce the dependency regardless of merge ordering heuristics.
3. **Single-writer or single-stream ordering for causally-related entities**: Route all events for a given causally-linked entity (e.g. all events for one trip) through the same shard/log stream, so within-entity ordering is trivially preserved even if cross-entity ordering uses a weaker guarantee.
4. **Sequential (not parallel) replay for entities with cross-shard history**: When an entity's history spans multiple shards, fall back to sequential, dependency-aware replay for that entity specifically, even if the bulk of recovery is parallelized for speed.
5. **Post-recovery invariant checks targeting ordering-sensitive fields**: Run automated checks for known ordering-dependent invariants (e.g. "reassignment must exist before any subsequent ETA update referencing the new driver") as a standard post-recovery validation step.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| cross_shard_clock_skew | Measured timestamp skew between hosts writing to different log shards | Alert if > defined tolerance (e.g. 50ms) |
| post_recovery_invariant_violation_count | Count of business-logic ordering invariants violated in recovered state | Alert if > 0 |
| causal_dependency_reorder_count | Count of detected cases where a dependent operation was replayed before its dependency | Alert if > 0 |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Ordering invariant violated post-recovery | Automated post-recovery check finds an entity with operations applied in violation of known causal rules | High | Quarantine affected entities, re-run replay with sequential dependency-aware ordering for those entities |
| Excessive cross-shard clock skew | cross_shard_clock_skew exceeds tolerance | Medium | Investigate NTP sync on affected hosts, consider moving affected event types to logical-clock ordering |

## Related Patterns
- [Recovery Data Corruption](./recovery-data-corruption.md) - a related replay-correctness failure, this pattern preserves individual entry integrity but breaks their sequence
- [Recovery Divergence](./recovery-divergence.md) - misordered replay is one specific mechanism that can produce a recovered state divergent from true pre-failure state
- [Cascade Divergent Recovery](./cascade-divergent-recovery.md) - ordering violations across components compound into the broader cross-component divergence problem
