# Cascade Divergent Recovery

## Issue
After a cascading failure hits several components, each component recovers independently — resuming from its own local checkpoint, cache, or retry queue — without coordinating with the others on what the "true" post-incident state should be. The result is that components which were consistent before the cascade come back online in mutually inconsistent or conflicting states: one service thinks an order is confirmed, another thinks it was cancelled, and a third has no record of it at all. This is distinct from a single component failing to recover correctly; the problem is specifically that multiple components recover to different, incompatible versions of the truth.

**Frequency**: Occasional

**Symptoms**
- Post-incident reconciliation jobs report a spike in cross-service state mismatches (e.g. order exists in Service A but not Service B)
- Different services report different "last known good" timestamps for the same logical entity
- Customer-visible inconsistencies appear (an item shows as shipped in one view and pending in another) shortly after an incident is marked resolved
- Automated reconciliation or dedup logic that normally runs quietly starts generating a burst of conflict-resolution actions right after recovery
- No single component's health checks fail post-recovery, yet end-to-end business metrics remain wrong

## Root Cause
When multiple components fail together during a cascade, each one typically has its own recovery path — replaying its own write-ahead log, restoring from its own last snapshot, or re-processing its own queue — and each of these recovery paths runs on an independent clock with no shared "recovery epoch" or barrier. If Service A recovers from a checkpoint 30 seconds before the cascade started while Service B recovers from a checkpoint 90 seconds before, the two services silently disagree about what happened during that 60-second gap. Without a coordinated recovery protocol (a shared recovery point, a reconciliation pass across all recovered components before traffic resumes, or an authoritative source of truth that others reconcile against), each component's locally-correct recovery becomes globally incorrect.

## Example
```
11:00:00 - Cascade begins: message broker outage disrupts OrderService,
           InventoryService, and ShippingService simultaneously.

11:00:00-11:12:00 - Each service queues writes locally and buffers them
           for replay once the broker is back.

11:12:00 - Broker restored. Each service independently begins replaying
           its buffered writes.

11:12:05 - OrderService replays its buffer cleanly, including an order
           cancellation for order #55219 that was queued at 11:04:30.

11:12:20 - InventoryService's replay logic hits a transient error at
           11:04:30 in its own buffer and, per its local retry policy,
           skips the failed entry and continues — silently dropping the
           inventory-release event tied to order #55219's cancellation.

11:12:40 - ShippingService, which restores from a snapshot taken at
           11:03:00 rather than replaying a buffer, has no knowledge of
           order #55219 being created OR cancelled, and later receives a
           stale "ship order #55219" instruction from a queued job that
           predates the cancellation.

11:20:00 - Order #55219 is now: cancelled in OrderService, still reserved
           in InventoryService, and shipped by ShippingService. A refund
           and a shipment go out for the same cancelled order.
```

## Statistics
| Finding | Context |
|---------|---------|
| 15-25% of multi-component cascades produce at least one cross-service state mismatch detectable by reconciliation jobs | Typical range observed in distributed systems without coordinated recovery |
| Divergent-recovery incidents take 2-3x longer to fully resolve than the original outage, because reconciliation happens after the incident is marked "closed" | Estimated from post-incident reconciliation timelines |
| Systems using a shared recovery barrier or authoritative reconciliation source reduce post-cascade state mismatches by roughly 60-70% | Reported range across teams adopting coordinated recovery protocols |

## Mitigations
1. **Shared recovery epoch/barrier**: Define a single, cluster-wide recovery point (e.g. "all components resume from event offset X") that every recovering component must honor, instead of each recovering independently from its own local checkpoint.
2. **Hold traffic until reconciliation passes**: Keep the system in a degraded/read-only mode after a multi-component cascade until an automated reconciliation pass confirms cross-service consistency, rather than resuming full traffic as soon as each component reports healthy.
3. **Authoritative source of truth for reconciliation**: Designate one system (often the system of record, e.g. the order ledger) as authoritative during post-cascade reconciliation, and have all other components reconcile their state against it rather than trusting their own replay.
4. **Idempotent, order-independent replay**: Design event replay to be idempotent and order-tolerant where possible, so differences in exactly which events each component replays don't produce divergent end states.
5. **Post-recovery consistency audit as a release gate**: Require an automated cross-service consistency check to pass before declaring an incident resolved, not just individual component health checks.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| cross_service_state_mismatch_rate | Rate of entities with conflicting state across services, measured by reconciliation jobs | Alert if > baseline within 1 hour of an incident |
| recovery_checkpoint_skew | Time difference between the recovery checkpoints chosen by different components in the same cascade | Alert if > 30 seconds skew |
| post_incident_reconciliation_action_count | Number of automated conflict-resolution actions triggered in the hour following incident resolution | Alert if > 3x normal baseline |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Post-cascade reconciliation spike | Reconciliation job conflict rate exceeds 3x baseline within 1 hour of a multi-component incident closing | High | Reopen incident, freeze affected write paths, run full reconciliation before resuming |
| Recovery checkpoint skew detected | Two or more components in the same cascade recover from checkpoints more than 30s apart | Medium | Delay traffic resumption until checkpoints are aligned or reconciled |

## Related Patterns
- [Recovery Divergence](./recovery-divergence.md) - the single-instance version of this problem; this pattern is the multi-component, cross-service form of the same divergence mechanism
- [Recovery Ordering Violation](./recovery-ordering-violation.md) - out-of-order replay within one component is one of the mechanisms that produces cross-component divergence
- [Redundancy Coordination Failure](./redundancy-coordination-failure.md) - both stem from a missing coordination protocol between independently-acting components during recovery
