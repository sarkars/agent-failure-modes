# Failover Data Loss

## Issue
When failover to a standby is triggered, writes that were in flight to the primary at the moment of failure — accepted by the client as successful, or in the process of being processed — never make it to the standby and are permanently lost. This is distinct from replication lag causing the standby to be generally behind (recovery-point-objective-miss is the measurement of that gap); this pattern is about the specific in-flight requests that were being processed at the exact instant of the failure, which fall into a gap between "already acknowledged to the client" and "durably replicated to the standby."

**Frequency**: Occasional

**Symptoms**
- Clients report a write succeeded (received a 200/ack) but the data is absent after failover
- The count of lost records correlates tightly with the replication lag window at the moment of failure, not with the overall outage duration
- Idempotency-key or dedup logs show requests that were accepted but never appear in the post-failover primary's data
- Users or downstream agents retry a "failed" operation that actually succeeded on the old primary, creating duplicates once the retry lands on the new primary

## Root Cause
Most replication setups acknowledge a write to the client as soon as the primary durably persists it locally, then asynchronously ships it to the standby — this is done for latency reasons, since waiting for synchronous replication to the standby before acknowledging would slow down every write. The gap between "primary persisted and acknowledged" and "standby received and applied" is the replication lag window, typically milliseconds to a few seconds. If the primary fails inside that window, any writes that were acknowledged to the client but not yet shipped to the standby are gone the moment failover promotes the standby, because the standby genuinely never received them — there is nothing to recover, since the only copy was on the now-dead primary.

## Example
```
Setup: OrderLedger uses primary-standby async replication with typical
replication lag of 80-150ms. Writes are acknowledged to callers as soon
as the primary's local WAL fsync completes, before shipping to standby.

14:55:00.000 - Client submits order #91204, primary durably persists it
               locally and returns "200 OK, order confirmed" to the
               client at 14:55:00.040 (40ms).

14:55:00.060 - Primary begins shipping the WAL segment containing order
               #91204 to the standby asynchronously.

14:55:00.090 - Primary's host crashes (kernel panic) before the WAL
               segment finishes transmitting. The standby never receives
               order #91204.

14:55:03.000 - Health checks detect primary failure after 3 missed
               heartbeats; automated failover promotes the standby.
               Failover completes in 2.8s, within the defined RTO.

14:55:05.000 - The client, having received a confirmed "200 OK" for
               order #91204 at 14:55:00.040, proceeds to reference that
               order in a follow-up API call (add a shipping label).
               The new primary has never heard of order #91204 and
               returns "order not found." Order #91204 and roughly 40
               other writes accepted in the same ~90ms window before the
               crash are permanently lost, despite each having been
               acknowledged as successful to its caller.
```

## Statistics
| Finding | Context |
|---------|---------|
| Async-replicated systems typically lose all writes acknowledged within the replication lag window at the moment of primary failure — commonly tens to a few hundred milliseconds of writes | Typical range for standard async primary-standby replication |
| Synchronous or semi-synchronous replication (waiting for standby ack before confirming to client) eliminates in-flight data loss but adds measurable write latency | Reported tradeoff across teams evaluating replication modes |
| A large share of "successful write, data missing after failover" support tickets trace to this exact acknowledgment/replication gap rather than a broader outage | Estimated from post-failover incident review |

## Mitigations
1. **Synchronous or semi-synchronous replication for critical writes**: For write paths where data loss is unacceptable, require acknowledgment from the standby (or a quorum) before confirming success to the client, accepting the added latency as the cost of durability.
2. **Client-side write receipts with reconciliation**: Have clients hold a durable local record of writes they believe succeeded, and run a post-failover reconciliation pass that re-submits any writes the new primary doesn't have.
3. **Shrink the replication lag window**: Reduce batching intervals and use lower-latency replication transport so the exposure window during any given failure is minimized, even if full synchronous replication isn't feasible everywhere.
4. **Idempotency keys on all writes**: Require every write to carry a client-generated idempotency key so that reconciliation or client retries after failover can safely re-submit without creating duplicates.
5. **Explicit data-loss window reporting post-failover**: After every failover event, automatically compute and report the maximum possible data-loss window (based on measured replication lag at time of failure) so affected writes can be identified and reconciled rather than discovered via customer complaints.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| replication_lag_at_failover | Measured replication lag at the moment failover was triggered | Alert if > defined RPO for the affected data class |
| acknowledged_writes_missing_post_failover | Count of writes with a client-visible success receipt that are absent from the post-failover primary | Alert if > 0 for critical write paths |
| write_ack_to_replication_gap | Time between write acknowledgment to client and successful replication to standby | Alert if p99 > 200ms on critical paths |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Data loss window detected post-failover | replication_lag_at_failover > 0 for a critical write path following a failover event | High | Trigger reconciliation job, notify affected clients, quantify lost record count |
| Missing acknowledged write confirmed | A specific acknowledged write is confirmed absent from new primary | High | Escalate to data-integrity incident, attempt reconciliation from client-side receipts or logs |

## Related Patterns
- [Failover State Corruption](./failover-state-corruption.md) - both involve state loss/damage during transfer to standby, one is loss of specific in-flight writes, the other is corruption of transferred state
- [Recovery Point Objective Miss](./recovery-point-objective-miss.md) - measures the general data-loss window an organization tolerates; failover data loss is the concrete incident-level instance of exceeding it
- [Failover Delay Too Long](./failover-delay-too-long.md) - a longer failover delay generally widens the exposure window in which in-flight data loss can occur
