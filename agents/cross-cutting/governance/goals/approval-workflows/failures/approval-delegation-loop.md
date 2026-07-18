# Approval Delegation Loop

## Issue
An approver who is unavailable delegates their approval authority to another approver, who in turn delegates back to the original approver (or to a third party who delegates further, forming a longer cycle). The delegation graph has no cycle detection, so the request bounces indefinitely between the delegated parties, or the workflow engine detects the loop only after it has already re-notified the same approvers dozens of times.

**Frequency**: Occasional

**Symptoms**
- The same approvers receiving repeated notifications for the same request in a short window
- Delegation chain logs showing A -> B -> A or A -> B -> C -> A patterns
- Requests that never reach a terminal approved/rejected state despite active delegation activity
- Out-of-office delegation rules set by two approvers pointing at each other simultaneously
- Agents or notification systems rate-limited or flagged as spammy due to repeated delegation notifications for the same request

## Root Cause
Delegation is usually implemented as a simple "if I'm unavailable, forward to X" rule configured independently by each approver, with no central validation that the resulting graph is acyclic. Because each delegation rule is set in isolation (often via a self-service out-of-office setting), no single point in the system has visibility into the full delegation chain until a request actually traverses it, and even then, most implementations don't track chain history to detect a repeat visit.

## Example
```
1. Approver A goes on leave and sets an out-of-office delegation to
   Approver B.
2. Approver B, unaware A has delegated to them specifically for this period,
   is also about to be out and has a standing delegation rule pointing back
   to A (set months earlier for a different circumstance and never removed).
3. A financial approval request arrives for A, is auto-forwarded to B per
   A's delegation rule.
4. B's own delegation rule immediately forwards it back to A.
5. The workflow engine treats each forward as a fresh routing decision and
   has no memory of the request having already visited A, so it forwards
   back to B again.
6. The request cycles between A and B every few minutes for two days,
   generating a stream of notifications neither actually reads, until the
   requester escalates manually outside the system.
```

## Statistics
| Finding | Context |
|---------|---------|
| Delegation chains longer than two hops carry a meaningfully elevated risk of cycles, since each additional hop is configured independently by a different person | Typical pattern in self-service delegation systems |
| A large share of delegation loops trace back to stale delegation rules left active well past their original intended time window | Common finding in access-review audits of delegation configurations |
| Loop detection, where implemented, catches the majority of cases only after multiple redundant traversals rather than on the first cycle | Reflects reactive rather than preventive cycle detection in most systems |

## Mitigations
1. **Cycle detection before forwarding**: Before forwarding a delegated request, check whether the target approver already appears earlier in that request's delegation path; if so, block the forward and escalate rather than looping.
2. **Delegation chain length limits**: Cap the number of delegation hops a single request can traverse (e.g., 2) and route to a fallback approver or governance owner once the cap is hit.
3. **Centralized delegation registry with expiry**: Require delegation rules to be set with a mandatory expiration date and store them in a single registry that can be validated for cycles across all approvers, rather than as independent per-user out-of-office settings.
4. **Delegation rule conflict check at creation time**: When an approver sets a delegation rule, check whether the target has an active delegation rule pointing back (directly or transitively) and warn or block at configuration time instead of at request time.
5. **Automatic stale-delegation cleanup**: Periodically flag and deactivate delegation rules whose configured time window has passed but were never removed.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `delegation_hop_count_p95` | 95th-percentile number of delegation hops a request traverses before reaching a terminal decision | > 3 hops |
| `delegation_cycle_detected_count` | Number of requests where a cycle was detected in the delegation path | > 0 per week |
| `repeat_notification_rate` | Rate at which the same approver receives more than 2 notifications for the same request | > 1% of requests |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Delegation cycle detected | A request's delegation path revisits an approver already in that path | Critical | Halt forwarding, route to fallback approver or governance owner, notify all approvers in the cycle |
| Delegation chain exceeds hop limit | Request traverses more than the configured maximum delegation hops | Warning | Route to fallback approver, flag chain for manual review of stale rules |

## Related Patterns
- [Approval Chain Break](./approval-chain-break.md) - both are structural failures in how a request moves between approvers, one by stalling and one by looping
- [Approval Authority Escalation Failure](./approval-authority-escalation-failure.md) - misconfigured routing tables cause both escalation dead-ends and delegation loops
- [Approval Timeout Expiration](./approval-timeout-expiration.md) - loops that are never detected eventually manifest as timeouts once someone notices the request never resolved
