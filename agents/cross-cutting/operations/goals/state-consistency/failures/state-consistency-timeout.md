# State Consistency Timeout

## Issue
An agent that must confirm its local or cached view of state matches an authoritative source — a sync check against a database, a quorum read, a reconciliation call to another service — issues that check, the check exceeds its timeout, and the agent proceeds with the action anyway using whatever state it already had. The timeout is treated as a soft failure ("couldn't verify, continue") rather than a hard stop, so the agent acts on state that may already be stale or wrong.

**Frequency**: Occasional

**Symptoms**
- Actions complete successfully against stale state shortly after a logged consistency-check timeout
- Timeout and fallback-to-cached-state events cluster during periods of downstream service latency or load
- Post-incident review finds the authoritative state had already changed at the moment the timed-out check would have caught it
- No distinction in logs between "consistency confirmed" and "consistency check timed out, proceeded anyway" — both paths lead to the same downstream action
- Retrying the consistency check manually after the fact reveals a different state than what the agent acted on

## Root Cause
Consistency checks are usually implemented as a bounded-latency call so that a single slow dependency can't stall the whole agent pipeline indefinitely. But the timeout value and the fallback behavior are chosen for availability, not correctness: engineers set a short timeout to keep the pipeline responsive, and on timeout the code path is written to "fail open" (proceed with best-known state) rather than "fail closed" (abort or escalate), because fail-closed was seen as worse for uptime during design. This treats a consistency check that didn't complete as equivalent to one that passed, when in fact a timeout means the system deliberately has no information about current state — the exact condition the check existed to rule out.

## Example
```
An inventory-reservation agent checks stock consistency against the
warehouse system before confirming an order, with a 2-second timeout
on the consistency call and a fallback of "use last-cached count."

14:32:01  Agent has cached stock count for SKU-8842: 3 units (cached
          90 seconds ago)
14:32:01  Agent issues consistency check to warehouse system to confirm
          3 units is still accurate
14:32:03  Warehouse system is under load from a concurrent stock sync
          job; consistency check times out at 2.0s with no response
14:32:03  Agent logs "consistency check timeout, proceeding with cached
          state" and confirms the order using the cached count of 3
14:32:04  Warehouse system's actual current count (had it responded)
          was 0 - the last 3 units were reserved by two other orders
          in the preceding 60 seconds

Result: the agent confirms an order for stock that doesn't exist. The
customer receives an order confirmation email, and the discrepancy is
only caught during nightly reconciliation, requiring a manual
cancellation and apology email.
```

## Statistics
| Finding | Context |
|---------|---------|
| 10-25% of consistency-check timeouts occur during the same load spike that is actively changing the state being checked | Typical range observed in production agent telemetry |
| Fail-open timeout handling is estimated to convert 1 in 20-50 timeouts into a downstream correctness incident | Estimated from post-incident review samples |
| Switching high-risk consistency checks to fail-closed reduces stale-state action incidents by roughly 70-90% at the cost of some added latency/abort rate | Reported range across teams that changed timeout-handling policy |

## Mitigations
1. **Fail-closed for high-stakes actions**: For actions with material cost of being wrong (financial commitments, inventory reservation, irreversible sends), treat a consistency-check timeout as a hard abort or escalation, not a green light to proceed on cached state.
2. **Distinguish confirmed-consistent from unknown**: Track and expose three states — confirmed fresh, confirmed stale, and unknown (timed out) — rather than collapsing "timed out" into the same code path as "passed."
3. **Adaptive timeout with backoff-and-retry**: Instead of a single short timeout that immediately falls back, retry the consistency check with a slightly longer window once before giving up, since transient load spikes often clear within a second or two.
4. **Staleness-bounded cache**: Attach a hard TTL to any cached state used as a fallback, and refuse to act on cache older than that TTL even if the fresh check times out, rather than using arbitrarily old data.
5. **Post-action reconciliation with compensating action**: Where fail-closed isn't feasible, run an immediate post-action consistency check and trigger an automatic compensating transaction (cancellation, correction) the moment true state is confirmed to differ from what was acted on.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| consistency_check_timeout_rate | Fraction of consistency checks that exceed their timeout | Alert if > 2% |
| fail_open_action_count | Count of downstream actions taken after a consistency-check timeout (fail-open path) | Alert if > 0 for high-stakes action types |
| post_action_state_mismatch_rate | Fraction of fail-open actions where a subsequent reconciliation check finds the acted-on state was wrong | Alert if > 5% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| High-stakes action on unconfirmed state | A financial, inventory, or irreversible action proceeds after a consistency-check timeout | High | Page on-call, trigger immediate reconciliation, hold or reverse the action if mismatch found |
| Timeout rate spike | consistency_check_timeout_rate exceeds threshold for 5+ minutes | Medium | Investigate downstream service load, consider temporarily switching affected action types to fail-closed |

## Related Patterns
- [State Replication Lag](./state-replication-lag.md) - a related cause of the staleness a consistency check is designed to detect
- [Concurrent State Modification](./concurrent-state-modification.md) - the underlying race that a timed-out consistency check often fails to catch
- [State Machine Violation](./state-machine-violation.md) - acting on stale state from a timed-out check can itself produce an invalid state transition
