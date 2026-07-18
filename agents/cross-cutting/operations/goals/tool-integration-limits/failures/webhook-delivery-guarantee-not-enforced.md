# Webhook Delivery Guarantee Not Enforced

## Issue
An agent's architecture assumes a tool's webhook events are delivered reliably — exactly once, or at least once with guaranteed eventual delivery — when the tool's actual delivery model is best-effort with no guarantee at all. Under transient failures on either the vendor's or the agent's side (a brief outage, a deploy causing a 502 on the receiving endpoint, a network blip), the event is simply dropped rather than retried, and the agent never learns the underlying event happened, leading to silently missing state with no error to trigger investigation.

**Frequency**: Common

**Symptoms**
- Downstream state is missing records that should have been created by a webhook-triggered process, with no corresponding error logged anywhere
- The gap is only discovered via a periodic reconciliation against the source system, if one exists at all
- The receiving endpoint's brief downtime or a deploy window correlates with missing events, but no alert fired at the time
- Vendor's webhook documentation, on close reading, describes delivery as "best-effort" or specifies a limited retry count, not a durable guarantee
- The same event type is sometimes received twice (duplicate) and sometimes not at all (dropped), consistent with an unreliable at-most-effort delivery model rather than a bug in event generation

## Root Cause
Many webhook systems are implemented as a simple HTTP POST fired at the moment an event occurs, with only a limited number of retries (or none) if the receiving endpoint doesn't return a success status quickly. Vendors vary widely in what guarantee they actually provide — some offer durable at-least-once delivery with persistent retry queues, others fire-and-forget with minimal or no retry — and this distinction is often buried in documentation rather than prominently stated. Agent architectures built assuming "the event will always eventually arrive" have no compensating mechanism (polling, periodic reconciliation, explicit acknowledgment tracking) to catch the case where it doesn't, so a dropped event simply produces silence rather than a detectable failure.

## Example
```
1. An agent processes new-order webhooks from an e-commerce platform to trigger
   fulfillment, warehouse allocation, and customer notification. The platform's webhook
   docs describe delivery as "we attempt delivery up to 3 times over 5 minutes" with
   no guarantee beyond that window.
2. The agent's webhook receiver is deployed behind a load balancer; during a rolling
   deployment, a 90-second window exists where roughly 15% of incoming requests receive
   a 502 as old instances drain and new ones aren't yet ready.
3. Six order-created webhooks arrive during that 90-second window; the platform's 3
   retry attempts for each are exhausted (spread across the 5-minute window) before
   the deployment fully stabilizes, since the deployment itself takes longer than 5
   minutes end-to-end including a canary period.
4. All 6 orders are never fulfilled, since the agent has no other mechanism (polling,
   reconciliation) to discover orders it never received a webhook for.
5. Three days later, customers contact support asking why their orders never shipped;
   investigation eventually finds the gap correlates with the deployment window, but
   by then the missed fulfillment SLA has already caused customer-facing harm.
```

## Statistics
| Finding | Context |
|---------|---------|
| Webhook drop rates during receiver-side deploys or brief outages are commonly observed in the low single-digit percentage range of total events during the affected window, but can spike much higher during longer incidents | Consistent with limited-retry-window delivery models common across vendors |
| Systems that rely solely on webhooks with no reconciliation mechanism take substantially longer to detect missing events, often measured in days, compared to systems with a daily reconciliation job, measured in hours | Because webhook-only architectures have no independent detection signal |
| Adding a periodic reconciliation/backfill job against the source system's list/query API has been observed to close the large majority of the gap left by best-effort webhook delivery | By providing an independent, guaranteed-eventually-consistent detection path |

## Mitigations
1. **Confirm the vendor's actual delivery guarantee before building on it**: Read the vendor's webhook documentation specifically for delivery guarantee language (best-effort vs. at-least-once vs. exactly-once) and design the architecture around the documented reality, not an assumption.
2. **Periodic reconciliation against the source of truth**: Run a scheduled job that queries the vendor's list/search API for events in a recent time window and diffs against what the agent actually processed, catching drops that webhooks alone missed.
3. **High-availability, fast-responding webhook receivers**: Ensure the receiving endpoint responds with a success status quickly and remains available during deploys (e.g., via zero-downtime deployment patterns) to maximize the chance of catching the vendor's limited retry attempts.
4. **Idempotent processing with durable acknowledgment tracking**: Track which event IDs have been successfully processed in durable storage, so reconciliation can identify gaps precisely and safely reprocess without duplicating effects.
5. **Alert on reconciliation-discovered gaps, not just webhook errors**: Since dropped webhooks by definition produce no direct error signal, the alerting must come from the reconciliation process detecting a mismatch, not from webhook-receiver-side monitoring alone.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `webhook.receiver_non_2xx_rate` | Rate of non-success responses returned by the webhook receiver, a leading indicator of potential drops | Alert above 1% over any 5-minute window |
| `reconciliation.missing_event_count` | Count of events found in the source system's API but not in the agent's processed-event log, from the periodic reconciliation job | Alert on any nonzero count |
| `webhook.deploy_window_error_correlation` | Correlation between receiver error rate and deployment windows | Track and alert if deploys reliably produce elevated error rates |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Reconciliation detects missing events | `missing_event_count` > 0 after a scheduled reconciliation run | High | Backfill missing events via source API, investigate the receiver-side gap that caused the drop |
| Receiver errors spike during deploy | `receiver_non_2xx_rate` exceeds threshold during a known deployment window | Medium | Review deployment process for zero-downtime gaps; treat as a leading indicator of dropped webhooks |

## Related Patterns
- [Webhook Retry Exhaustion](./webhook-retry-exhaustion.md) - the specific mechanism (retries running out) by which delivery guarantees fail to be enforced
- [Webhook Order Not Guaranteed](./webhook-order-not-guaranteed.md) - a related but distinct assumption gap about webhooks, ordering instead of delivery
- [Sla Availability Not Met](../../tool-sla-quality-limits/failures/sla-availability-not-met.md) - receiver-side or vendor-side availability gaps are frequently the proximate cause of dropped webhook deliveries
