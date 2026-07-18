# Webhook Retry Exhaustion

## Issue
A tool's webhook delivery fails repeatedly against the agent's receiving endpoint — due to a transient outage, a misconfigured URL, or a deploy-time gap — and the vendor gives up retrying after a fixed number of attempts or a fixed time window. Once that budget is exhausted, the event is dropped permanently with no further attempt and, in many implementations, no notification to the receiver that delivery ultimately failed. The agent never learns the underlying event happened at all, and nothing in its own logs points to the gap since the failure occurred entirely on the vendor's side.

**Frequency**: Common

**Symptoms**
- Specific events are simply missing from downstream processing with no error anywhere in the agent's own logs or metrics
- The gap correlates with a known outage or deployment window on the receiving side that lasted longer than the vendor's total retry window
- Vendor's webhook delivery dashboard (if one exists) shows a "failed" or "exhausted retries" status for specific event IDs that the agent has no record of ever seeing
- Reconciliation against the source system's own data eventually reveals records the agent never processed
- The receiving endpoint's outage was brief (minutes) but still exceeded the vendor's retry window, which is often shorter than teams assume

## Root Cause
Vendors bound webhook retry attempts (both in count and total elapsed time) to prevent an unresponsive receiver from causing unbounded backlog on their own delivery infrastructure — a reasonable constraint from the vendor's perspective, but one that creates a hard cutoff after which an event is permanently and silently lost from the receiver's point of view. Retry windows are often shorter than teams assume (commonly minutes to a few hours, not days), so even a moderately brief receiver-side outage — a deploy, a database failover, a brief scaling event — can outlast the retry budget. Because the failure is entirely vendor-side after that point, the agent's own monitoring (which only observes what reaches it) has structurally no way to detect the loss without an independent check against the vendor or source system.

## Example
```
1. A CI/CD platform's webhook notifies an agent of build-completion events, used to
   trigger automated deployment. The platform retries failed webhook deliveries up to
   5 times over a 30-minute window before giving up permanently, with no further
   notification.
2. The agent's webhook receiver experiences a database connection pool exhaustion
   incident lasting 45 minutes, during which it returns 503 for all incoming requests.
3. Three build-completion webhooks fired during that window; each exhausts its 5 retry
   attempts within the platform's 30-minute window, well before the 45-minute outage
   resolves, and are marked permanently failed on the platform's side.
4. The agent's own incident retrospective for the database issue focuses on the pool
   exhaustion itself and doesn't surface the dropped webhooks, since nothing in the
   agent's logs shows a build-completion event was ever expected.
5. Two days later, engineers notice three recent builds were never auto-deployed and
   have to manually trigger deployment after realizing the webhooks were lost, not
   just delayed.
```

## Statistics
| Finding | Context |
|---------|---------|
| Vendor webhook retry windows commonly range from a few minutes to a few hours, shorter than many receiver-side outage/deploy windows teams plan around | Consistent with vendors optimizing retry budgets for their own infrastructure load, not receiver-side recovery time |
| Incidents combining a receiver-side outage with silent webhook retry exhaustion often go undetected for days, versus minutes-to-hours for incidents with active reconciliation monitoring | Because there's no direct error signal at the point of permanent loss |
| Vendors that expose a delivery-status/dead-letter API for failed webhooks are used by only a minority of integrating teams in practice, despite being the most direct way to detect exhausted deliveries | Reflects that this capability is often undiscovered or unused during initial integration |

## Mitigations
1. **Query the vendor's delivery-status or dead-letter API if one exists**: Many webhook providers expose an endpoint listing failed/exhausted deliveries; poll it periodically to catch drops that never reached the receiver.
2. **Keep receiver-side outages shorter than the vendor's retry window**: Know the vendor's specific retry count and total time window, and ensure deploy strategies, failover times, and incident response targets stay comfortably under it.
3. **Independent reconciliation against the source system**: Run a periodic job that queries the vendor's underlying data (build list, order list, etc.) directly and diffs against what the agent actually processed, catching exhausted-retry drops regardless of whether a dead-letter API exists.
4. **High-availability webhook receiver with fast health recovery**: Architect the receiver to fail over or recover quickly (seconds, not tens of minutes) from common failure modes like connection pool exhaustion, directly reducing the window in which retries can be exhausted.
5. **Alert on receiver-side downtime duration relative to known retry windows**: When the receiver experiences downtime, explicitly calculate whether that downtime exceeded any dependent vendor's retry window, and trigger a reconciliation check proactively rather than waiting for a report of missing data.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `receiver.downtime_duration_vs_retry_window` | Ratio of an observed receiver outage duration to the vendor's documented retry window | Alert when ratio exceeds 0.7 (outage approaching the vendor's exhaustion point) |
| `vendor.exhausted_delivery_count` | Count of webhook deliveries reported as permanently failed by the vendor's delivery-status API, where available | Alert on any nonzero count |
| `reconciliation.missing_event_count` | Count of events present in the source system but absent from the agent's processed log, from periodic reconciliation | Alert on any nonzero count |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Receiver outage approaching vendor retry-exhaustion window | `downtime_duration_vs_retry_window` exceeds 0.7 during an active incident | High | Trigger proactive reconciliation check immediately after recovery, don't wait for a scheduled run |
| Vendor reports exhausted deliveries | `exhausted_delivery_count` > 0 | High | Manually process the specific event IDs reported as failed, backfill from source system |

## Related Patterns
- [Webhook Delivery Guarantee Not Enforced](./webhook-delivery-guarantee-not-enforced.md) - retry exhaustion is the specific terminal mechanism by which a best-effort delivery guarantee ultimately fails
- [Webhook Order Not Guaranteed](./webhook-order-not-guaranteed.md) - retries are also a primary cause of out-of-order delivery when they arrive after a subsequent event
- [Sla Availability Not Met](../../tool-sla-quality-limits/failures/sla-availability-not-met.md) - receiver-side or vendor-side downtime exceeding assumptions is often the trigger event for retry exhaustion
