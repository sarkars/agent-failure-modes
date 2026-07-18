# Webhook Order Not Guaranteed

## Issue
An agent's state-update logic assumes webhook events arrive in the same order the underlying events occurred — processing an "order.updated" after "order.created," a "status.changed" after the prior status.changed it supersedes. Most webhook systems make no such ordering guarantee: events can be delivered out of sequence due to parallel delivery workers, retries of earlier failed deliveries arriving after later successful ones, or multi-region delivery infrastructure. When a stale event arrives after a newer one, the agent overwrites current state with outdated data and has no way to detect that it just went backwards.

**Frequency**: Common

**Symptoms**
- An entity's state periodically "reverts" to an older value with no corresponding action having actually caused that change
- Race-condition-like bugs that are hard to reproduce, correlating with periods of high event volume or vendor-side retry activity
- Two webhook events for the same entity, processed in the order received, produce a final state inconsistent with the entity's actual current state in the source system
- Vendor's webhook documentation doesn't mention ordering guarantees at all, or explicitly states events "may arrive out of order"
- The issue appears more frequently under load or after a delivery retry storm, since retries are exactly the mechanism that reorders events relative to original occurrence time

## Root Cause
Webhook delivery infrastructure is typically built for throughput and reliability, not strict ordering — vendors commonly use parallel delivery workers or queues that don't preserve a single global order, and retries of a failed delivery are requeued independently of newer events, meaning a retried "old" event can arrive after a "new" event that was delivered successfully on the first attempt. An agent that processes webhooks with simple "last write wins" logic (just overwriting local state with whatever the webhook payload says) has no way to distinguish "this event is newer than what I have" from "this event is older," because it isn't checking any ordering signal at all — it's just trusting arrival order.

## Example
```
1. An agent maintains a local cache of order statuses driven by a shipping platform's
   webhooks: "order.created", "order.shipped", "order.delivered". The platform's docs
   note that "delivery order is not guaranteed under high load."
2. An order transitions from "shipped" to "delivered" within the same minute due to a
   same-day local delivery. The platform fires both webhooks nearly simultaneously.
3. The "order.shipped" webhook's first delivery attempt to the agent's receiver times
   out (receiver briefly overloaded) and gets queued for retry; the "order.delivered"
   webhook, fired moments later, is delivered successfully on the first attempt.
4. The agent processes "order.delivered" first, correctly setting local status to
   "delivered". Ninety seconds later, the retried "order.shipped" webhook arrives and
   the agent's simple last-write-wins handler overwrites local status back to "shipped".
5. The customer-facing tracking page now shows "shipped" for an order that has actually
   been delivered, and stays wrong until the next unrelated webhook happens to correct it.
6. Support receives a complaint before anyone notices the underlying webhook-ordering
   issue, since nothing in the agent's logs indicates an error occurred.
```

## Statistics
| Finding | Context |
|---------|---------|
| Out-of-order webhook delivery incidents disproportionately cluster around retry events and high-load periods, consistent with retries being a primary reordering mechanism | Retried deliveries are requeued independently of newer, successfully-delivered events |
| Adding an event-timestamp or sequence-number check before applying webhook state updates has been observed to eliminate the large majority of stale-overwrite incidents | By rejecting/ignoring events older than the currently stored state instead of blindly applying last-write-wins |
| Many vendor webhook systems explicitly disclaim ordering guarantees in their documentation, though this detail is frequently missed during integration because it isn't in the main quickstart or example payloads | Reflects that ordering caveats are often buried in an FAQ or edge-case section |

## Mitigations
1. **Sequence-aware state updates**: Include and check an event timestamp, version number, or monotonically increasing sequence ID in every webhook payload, and reject/ignore updates older than the currently stored state rather than blindly overwriting.
2. **Fetch authoritative state on ambiguous events**: When an event's ordering relative to current state is uncertain, re-fetch the entity's current state directly from the source system's API instead of trusting the webhook payload's implied state.
3. **Idempotent, order-independent event application**: Where possible, design event handlers to apply state transitions in a way that produces the same final result regardless of processing order (e.g., set-based or CRDT-style merges rather than sequential overwrites).
4. **Buffering with reordering window**: For scenarios where strict ordering matters and slight delay is acceptable, buffer events briefly and reorder by timestamp/sequence before applying, rather than processing immediately on arrival.
5. **Explicitly test for out-of-order delivery**: During integration testing, deliberately simulate out-of-order webhook delivery (including simulated retries arriving late) to verify the agent's handling logic doesn't regress state.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `webhook.stale_event_rejected_count` | Count of webhook events rejected/ignored because their sequence/timestamp was older than currently stored state | Track as a leading indicator; alert on sudden spikes suggesting a retry storm |
| `state.reversion_count` | Count of detected cases where an entity's tracked state moved to an earlier logical stage without a corresponding real-world action | Alert on any occurrence for critical entities |
| `webhook.out_of_order_delivery_rate` | Rate of webhook deliveries whose event timestamp precedes the previously processed event's timestamp for the same entity | Alert when rate exceeds 2% of events |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| State reversion detected | `state.reversion_count` > 0 for a critical entity type | High | Investigate for out-of-order webhook delivery; verify sequence-checking logic is active |
| Elevated out-of-order delivery rate | `out_of_order_delivery_rate` exceeds 2% sustained over an hour | Medium | Correlate with vendor-side retry activity or load; confirm ordering-safe handling is in place |

## Related Patterns
- [Webhook Delivery Guarantee Not Enforced](./webhook-delivery-guarantee-not-enforced.md) - a related webhook-reliability assumption gap, delivery guarantee instead of ordering
- [Webhook Retry Exhaustion](./webhook-retry-exhaustion.md) - retries are a primary mechanism that produces the out-of-order delivery described here
- [Undocumented Api Behavior](./undocumented-api-behavior.md) - ordering guarantees (or their absence) are frequently under-documented relative to their operational importance
