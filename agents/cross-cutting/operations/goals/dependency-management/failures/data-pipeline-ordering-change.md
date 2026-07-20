# Data Pipeline Ordering Change

## Issue
An agent's processing logic implicitly assumes events arrive in the order they occurred (a "created" event before an "updated" event, a payment "authorized" before a "captured"), but a pipeline change — adding parallel processing, repartitioning a queue by a different key, introducing retries, or migrating to a different message broker — reorders events in transit. The agent applies updates in the new arrival order, producing state that reflects an event sequence that never actually happened.

**Frequency**: Occasional

**Symptoms**
- Entity state shows impossible transitions (an order "shipped" before it was "paid," a user "deactivated" then "created")
- Out-of-order application of updates causes a later event to be silently overwritten by an earlier one that arrives after it
- Bugs appear only under load or after a pipeline scaling/repartitioning change, not in low-volume testing where near-in-order delivery is more likely
- Downstream aggregates or state machines enter states with no valid incoming transition, requiring manual reconciliation
- Reprocessing the same event log with a different consumer parallelism setting produces different final state

## Root Cause
Ordering guarantees are a property of the specific transport and partitioning scheme (e.g., strict order within a single partition of a single topic), not an inherent property of "a pipeline." When a pipeline is scaled out (adding consumer parallelism), repartitioned (changing the partition key so related events land on different partitions), or routed through a component that doesn't preserve order (a load-balanced HTTP fan-out, a retry queue that redelivers independently), the ordering guarantee the original logic was built against silently disappears. Because most application code updates state field-by-field or record-by-record without checking an event's own sequence number or timestamp against the current state's, it has no way to detect that an "earlier" event just arrived after a "later" one.

## Example
```
An inventory agent consumes a Kafka topic "inventory-events" partitioned by
warehouse_id, applying each event (restock, sale, adjustment) in order to
update a running stock count per SKU. Because all events for a given
warehouse land on the same partition, order is preserved and the logic
(naively applying "new_count = old_count + delta") works correctly.

The team scales the pipeline for Black Friday by repartitioning the topic by
sku_id instead of warehouse_id, to better parallelize processing for
high-volume SKUs. This is intended purely as a throughput optimization.

For SKU "TSHIRT-BLU-M", a sale event (delta=-3) from warehouse A and a
restock event (delta=+50) from warehouse B, which actually occurred in that
order, now get processed by two different consumer instances and can be
applied out of order due to differing consumer lag. When the restock is
applied before the sale is fully committed, a race condition causes the
sale's delta to be applied against a stale base count, undercounting stock
by 3 units. Across thousands of SKUs during the sale, this produces
enough drift that the site shows "in stock" for items that are actually
sold out.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 20-30% of event-driven pipeline incidents following a repartitioning or scaling change involve an ordering assumption that was previously implicit and undocumented | Typical range observed in scaling-related incident reviews |
| Adding explicit event sequence numbers with out-of-order detection catches an estimated 90%+ of ordering violations that would otherwise silently corrupt state | Reported range across teams using sequence-checked consumers |
| Ordering-related bugs are disproportionately reported during peak-load periods, when parallelism and retry rates are highest | Estimated from incident timing analysis |

## Mitigations
1. **Explicit sequence numbers and version checks**: Attach a monotonically increasing sequence number or version to each entity's events, and have consumers reject or reorder-buffer any event whose sequence number is not strictly greater than the entity's current applied version.
2. **Partition-key stability review**: Treat any change to a topic's partition key as a breaking change requiring explicit review of every consumer's ordering assumptions, not just a throughput tuning knob.
3. **Idempotent, commutative state updates where possible**: Design state transitions (e.g., using last-write-wins with a timestamp comparison, or CRDTs) so that out-of-order application converges to the same correct result regardless of arrival order.
4. **Ordering assumption documentation**: Explicitly document, in the consumer code and its interface contract, which ordering guarantees it depends on and from which specific transport/partitioning scheme they derive.
5. **Out-of-order event alerting**: Instrument consumers to detect and count events arriving with an out-of-order sequence number or timestamp relative to already-applied state, surfacing violations even when the application logic tolerates them.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| out_of_order_event_rate | Rate of events arriving with a sequence number/timestamp earlier than the entity's current applied state | Alert if > 0.1% of events |
| invalid_state_transition_count | Count of entities observed in a state with no valid incoming transition from their prior state | Alert if > 0 for state machines with strict transition rules |
| reprocessing_result_divergence | Difference in final state when replaying the same event log with different consumer parallelism | Alert if any divergence detected in reprocessing tests |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Partition key changed on live topic | A topic's partition key configuration changes | High | Require sign-off from all consumer owners before deploy, review ordering assumptions |
| Out-of-order event spike | out_of_order_event_rate exceeds threshold | Medium | Investigate consumer lag imbalance, check for recent scaling/repartitioning changes |

## Related Patterns
- [Data Pipeline Replay Idempotency](./data-pipeline-replay-idempotency.md) - both concern event delivery guarantees consumers implicitly rely on; ordering and idempotency are frequently violated together
- [Data Pipeline Backpressure Unhandled](./data-pipeline-backpressure-unhandled.md) - scaling changes made to relieve backpressure are a common trigger for the repartitioning that breaks ordering
- [Data Pipeline Latency](./data-pipeline-latency.md) - uneven consumer lag across partitions, a latency phenomenon, is the direct mechanism by which repartitioning produces out-of-order application
