# Integration Data Consistency

## Issue
Two integrated systems each maintain their own copy of what should be shared state — a CRM's "customer status" and a billing system's "account status," or an inventory system's stock count and an order system's reserved-stock count — and updates to one side don't reliably propagate to the other, whether due to a failed sync, a race condition between concurrent writes, or a missing update hook on one integration path. The agent, reading from whichever system it happens to query, acts on a view of "the" state that the other system would flatly contradict.

**Frequency**: Very Common

**Symptoms**
- The same entity shows a different status, value, or state depending on which integrated system is queried
- A sync/reconciliation job exists specifically to detect and fix these discrepancies, and its queue of unresolved conflicts grows rather than staying near zero
- An agent action based on one system's state (approve a refund because billing shows "active") is later found to conflict with the other system's state (CRM shows the account was already cancelled)
- Root-cause analysis of a consistency incident finds a specific update path (a manual admin action, a webhook that silently failed, a batch job that skipped a record) that never triggered the sync
- Consistency issues cluster around specific update paths (bulk imports, admin overrides) that bypass the normal, sync-aware code path

## Root Cause
Keeping two independently-owned systems' data consistent requires every single write path on both sides to reliably trigger a corresponding update on the other side, and any path that doesn't — a manual database edit, an admin tool that writes directly rather than through the integration's API, a webhook delivery that silently fails without retry, a batch import that predates the sync integration — creates a permanent, undetected divergence unless there's a separate reconciliation process actively looking for it. Without either a single source of truth that the other system merely mirrors (rather than two systems each capable of independent writes) or a robust two-phase/transactional update mechanism, "eventually consistent" in practice means "consistent only for the write paths someone remembered to wire up," and every unwired path is a latent inconsistency waiting to be read by an agent that assumes the two systems agree.

## Example
```
A subscription-management agent checks a billing system to determine if a
customer's account is active before granting access to a premium feature.
The billing system and the CRM system are integrated: cancelling a
subscription in the CRM is supposed to trigger a webhook that updates the
billing system's status to "cancelled."

A support agent, working a complex refund case, cancels the customer's
subscription directly in the CRM's admin panel rather than through the
standard cancellation flow, because the standard flow doesn't support the
specific partial-refund scenario they're handling. The admin panel writes
directly to the CRM database and does not fire the webhook that the
standard cancellation flow triggers -- a gap that exists because the admin
panel was built by a different team, years after the webhook integration,
and was never updated to include it.

The billing system's status remains "active." Two weeks later, the
subscription-management agent checks billing status (still "active"),
grants the customer continued access to the premium feature, and the
customer -- who believes and was told their subscription was cancelled --
is confused to still have access, while also potentially still being
billed if a similar gap exists on the billing side, prompting a dispute
that support has to manually untangle by comparing both systems by hand.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 15-25% of two-system data consistency incidents trace back to an administrative or manual write path that bypasses the standard sync integration | Typical range observed in reconciliation incident reviews |
| Systems relying on webhook-based sync without delivery guarantees (retries, dead-letter handling) report an estimated 1-3% webhook delivery failure rate, each producing a lasting inconsistency until reconciled | Estimated from webhook reliability studies |
| Regular automated reconciliation jobs that compare both systems' state and alert on divergence catch an estimated 90%+ of consistency drift before it affects a customer-facing decision | Reported range across teams running scheduled reconciliation |

## Mitigations
1. **Single source of truth with mirrored reads**: Where feasible, designate one system as authoritative for a given piece of shared state and have the other system only display a cached/mirrored copy, rather than allowing both systems independent write authority.
2. **Reliable, retried webhook/event delivery**: Ensure every sync-triggering event uses at-least-once delivery with retries and dead-letter handling, rather than a fire-and-forget webhook call that silently fails.
3. **Closing manual/admin write-path gaps**: Audit every write path to shared state (including admin tools, bulk imports, and one-off scripts) and ensure each one either goes through the standard sync-aware API or explicitly triggers the same sync event, rather than writing directly to a system's database.
4. **Scheduled reconciliation with alerting**: Run a recurring job that compares both systems' state for shared entities and flags divergence, treating unresolved reconciliation conflicts as an actionable queue rather than a passive report.
5. **Consistency-aware agent decision logic**: For high-stakes decisions (granting access, approving a refund), have the agent check both systems and require agreement (or explicitly flag disagreement for human review) rather than trusting a single system's state as ground truth.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| cross_system_state_divergence_count | Count of entities where two integrated systems disagree on shared state, per reconciliation run | Alert if > 0 and growing |
| unresolved_reconciliation_queue_depth | Number of detected inconsistencies awaiting resolution | Alert if backlog grows rather than trending toward zero |
| sync_event_delivery_failure_rate | Rate of failed webhook/event deliveries meant to keep systems in sync | Alert if > 0.5% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Growing unresolved divergence queue | Reconciliation job's unresolved conflict count increases over consecutive runs | High | Investigate which write path is causing new divergence, prioritize fixing the sync gap |
| Agent decision made on disagreeing state | An agent action proceeds despite the two source systems disagreeing on the relevant entity's state | High | Halt automated decision, route to human review, log both systems' conflicting values |

## Related Patterns
- [Integration Error Handling Mismatch](./integration-error-handling-mismatch.md) - silent webhook/event delivery failures, a common cause of consistency drift, are a specific instance of mismatched error signaling between systems
- [Data Lineage Loss](./data-lineage-loss.md) - without lineage, it's hard to determine which system's value is more recent or authoritative when reconciling a divergence
- [Integration Order Dependency](./integration-order-dependency.md) - consistency issues can also arise when sync operations that must happen in a specific order are triggered out of sequence
