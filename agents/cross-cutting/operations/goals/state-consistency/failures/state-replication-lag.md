# State Replication Lag

## Issue
An agent writes state to a primary store and then, moments later, reads it back from a replica (a read-replica database, a cache, a secondary region) that hasn't yet caught up with the write. The agent proceeds as though the read reflects current reality, making a decision based on data that is seconds or minutes out of date relative to what it itself just wrote or what another writer has since changed.

**Frequency**: Common

**Symptoms**
- An agent's own write appears to be "missing" when it immediately reads it back, despite the write having succeeded
- Decisions made shortly after a write don't reflect that write, but the same query minutes later does
- Behavior is intermittent and correlates with replica lag metrics, not with any deterministic input
- Read-after-write consistency bugs are far more common under load, when replication lag is naturally higher
- Different agent instances querying different replicas see different "current" states for the same entity at the same moment

## Root Cause
Read replicas and caches exist specifically to scale read throughput and reduce load on the primary, and the mechanism that makes this possible — asynchronous replication — inherently means there is a window, often milliseconds but sometimes much longer under load or network partition, during which the replica's view of the world is stale relative to the primary. Agent code that reads state to inform a decision frequently defaults to the cheaper/faster read path (a replica or cache) without distinguishing between reads that can tolerate staleness and reads that require read-your-own-writes or strong consistency, because that distinction requires the agent's author to reason explicitly about consistency guarantees rather than treating "read the data" as a single undifferentiated operation.

## Example
```
An order-processing agent writes a payment-confirmation status to the
primary database, then immediately queries a read-replica (used for
all normal reads to keep primary load low) to fetch the full order
record before generating a confirmation email.

t=0.00s  Agent writes: order #77213 status = "paid" to primary DB
t=0.05s  Agent queries read-replica for order #77213 to build the
         confirmation email
t=0.05s  Replica is 300ms behind primary due to a burst of write
         traffic from a flash sale; replica still shows status =
         "pending"
t=0.06s  Agent's logic branches on status: sees "pending", concludes
         the payment write must have failed, and re-triggers the
         payment-processing flow instead of sending a confirmation

Result: the customer's card is charged a second time by the
re-triggered payment flow, because the agent treated a stale replica
read as ground truth about whether its own prior write had succeeded.
The duplicate charge is only caught when the customer disputes it with
their bank three days later.
```

## Statistics
| Finding | Context |
|---------|---------|
| Typical async replication lag under normal load is in the tens-of-milliseconds range, but can extend to seconds or longer under write bursts | Typical range observed in production database deployments |
| Read-after-write consistency bugs are estimated to be 3-6x more frequent during traffic spikes than during steady-state load | Estimated from incident data correlated with load metrics |
| Routing read-your-own-writes queries to the primary (or a session-consistent replica) eliminates the large majority of these incidents at a modest primary-load cost | Reported range across teams that added consistency-aware read routing |

## Mitigations
1. **Read-your-own-writes routing**: For any read that immediately follows a write by the same agent and depends on seeing that write, route the read to the primary or a replica with session/causal consistency guarantees rather than an arbitrary replica.
2. **Pass state forward instead of re-reading**: Where possible, have the write operation return the confirmed state directly, and use that returned value for subsequent logic in the same flow instead of issuing a separate read that might hit a lagging replica.
3. **Bounded staleness checks**: For reads that do go to a replica, check the replica's replication lag/lsn against a threshold and fall back to the primary if the replica is further behind than the operation can tolerate.
4. **Idempotency keys on write-triggering actions**: Guard actions like "re-trigger payment" with an idempotency key tied to the original transaction, so even if stale-read logic incorrectly concludes a retry is needed, the downstream system rejects the duplicate.
5. **Lag-aware alerting separate from correctness alerting**: Monitor replication lag directly and alert when it exceeds levels known to cause read-after-write violations, rather than only discovering lag through downstream correctness incidents.

## Related Patterns
- [State Consistency Timeout](./state-consistency-timeout.md) - a related staleness problem where the check meant to catch lag itself fails to complete in time
- [Concurrent State Modification](./concurrent-state-modification.md) - both involve an agent acting on a view of state that a concurrent process has already changed
- [State Machine Violation](./state-machine-violation.md) - acting on a lagging replica's stale status field can trigger a transition that violates the state machine given the true, current state

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| replica_lag_ms | Measured replication delay between primary and replica used for agent reads | Alert if > 500ms sustained |
| read_after_write_mismatch_rate | Fraction of immediate post-write reads that don't reflect the write | Alert if > 0.5% |
| duplicate_action_from_stale_read_count | Count of actions (retries, re-triggers) traced to a stale-read-driven decision | Alert if > 0 |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Replica lag exceeds tolerance | replica_lag_ms exceeds threshold for reads flagged as consistency-sensitive | High | Page on-call, route affected read paths to primary, investigate replication bottleneck |
| Stale-read-triggered duplicate action | An action with side effects (payment, send, mutation) is traced to a decision made on stale replica data | High | Halt further automated retries, reconcile the duplicate action, review read-routing for that flow |
