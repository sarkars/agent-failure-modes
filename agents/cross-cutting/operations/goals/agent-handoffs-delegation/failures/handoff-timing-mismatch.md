# Handoff Timing Mismatch

## Issue
A task is handed off before the receiving agent is actually ready to accept it (it's still initializing, mid-way through another task, or hasn't started polling its queue yet), or after the receiving agent's window to act on it has already closed (a deadline passed, a session expired, an external resource is no longer available). In both directions, the handoff is transmitted successfully at the protocol level but arrives at the wrong moment for the receiver to do anything useful with it.

**Frequency**: Common

**Symptoms**
- Handoff messages sent to a receiving agent that isn't actively listening yet, resulting in the message being missed or requiring a separate recovery mechanism to be picked up later
- Tasks handed off with a deadline or validity window that has already elapsed by the time the receiving agent processes them
- Receiving agent logs showing it discarded or rejected a task as "expired" or "stale" despite the sender believing the handoff succeeded
- Race conditions where handoff success depends on which of two independently-scheduled agents happens to act first

## Root Cause
Handoffs between independently operating agents rarely have a shared, synchronized notion of "the receiver is ready now." The sending agent typically fires a handoff as soon as its own work is done, based on its own internal completion signal, with no guarantee about the receiving agent's readiness state at that instant — the receiver might be cold-starting, still processing a prior task, or not yet subscribed to the channel the handoff arrives on. Symmetrically, time-bound tasks (an approval that's only valid for 10 minutes, a price quote that expires) are handed off without the sender accounting for queueing delay, receiver processing time, or clock skew between systems, so a task that was "on time" when sent can be stale by the time it's actually read.

## Example
```
A price-quoting agent generates a shipping quote valid for 5 minutes
(carrier API rate volatility) and hands it off to a checkout-agent to
present to the customer and finalize the order if accepted.

The handoff goes through a message queue with no delivery time
guarantee. Under normal load, delivery is near-instant; during a
traffic spike, queue backlog adds an 8-minute delay before
checkout-agent actually reads the message.

checkout-agent receives the quote, presents it to the customer, and
by the time the customer clicks "confirm" 90 seconds later, the quote
is now 9.5 minutes old -- already expired per the 5-minute validity
window the price-quoting agent set, but checkout-agent has no
mechanism to check the quote's age against its validity window before
presenting it. The order proceeds at a shipping rate the carrier API
no longer honors, and the discrepancy is only caught when the
fulfillment agent's carrier-rate reconciliation flags a mismatch after
the order is already placed.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 5-10% of time-bound handoffs in queue-based multi-agent systems experience delivery delay exceeding the task's validity window during peak load | Typical range observed in queue-backed handoff systems |
| Adding explicit expiry checks at the point of use (not just at handoff time) eliminates the large majority of stale-task incidents | Reported range across teams adding receiver-side freshness validation |
| Cold-start-related missed handoffs are disproportionately common in autoscaled agent deployments compared to statically provisioned ones | Estimated from incident data across autoscaled multi-agent pipelines |

## Mitigations
1. **Receiver-side freshness validation**: Require the receiving agent to check a task's timestamp and validity window against the current time at the point of use (not just at receipt), and re-fetch or reject if stale.
2. **Readiness acknowledgment before handoff**: Have the sending agent confirm the receiving agent is actively ready (via a heartbeat or readiness probe) before transmitting time-sensitive handoffs, rather than assuming readiness.
3. **Time-to-live enforcement at the transport layer**: Configure message queues or transport mechanisms with a TTL matching the task's validity window, so expired messages are dropped or rerouted rather than delivered late and silently acted on.
4. **Deadline-aware retry and re-derivation**: For tasks with tight validity windows, build the receiving agent to re-derive time-sensitive values (like re-fetching a live quote) rather than trusting a value that may have aged during transit.
5. **Warm-start guarantees for receiving agents**: For latency-sensitive handoff chains, ensure the receiving agent maintains a minimum warm capacity rather than relying purely on cold-start autoscaling, reducing the odds a handoff arrives before the receiver can act.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| handoff_to_processing_latency | Time between a handoff being sent and the receiving agent beginning to process it | Alert if p95 exceeds the tightest task validity window in use |
| stale_task_rejection_rate | Rate of tasks rejected or discarded by receiving agents as expired | Alert if > 2% |
| receiver_cold_start_miss_count | Count of handoffs sent while the intended receiving agent instance was not yet ready | Alert if > 0 |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Time-sensitive task processed near/past expiry | A task with a validity window is acted on with less than a configured safety margin remaining, or after expiry | High | Halt the action, re-derive fresh data, notify the workflow owner |
| Handoff latency spike | handoff_to_processing_latency exceeds the alert threshold for a sustained period | Medium | Investigate queue backlog or receiver capacity, scale up if needed |

## Related Patterns
- [Handoff Approval Skipped](./handoff-approval-skipped.md) - the same async timing gap that causes stale-task delivery can also cause an approval wait to be bypassed via timeout
- [Handoff Idempotency Violation](./handoff-idempotency-violation.md) - timing-driven retries are a primary source of the duplicate handoffs that trigger idempotency violations
- [Handoff Circular Dependency](./handoff-circular-dependency.md) - timing mismatches and circular routing are both cases where locally reasonable handoff logic produces a globally broken outcome
