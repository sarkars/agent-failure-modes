# Redundancy Coordination Failure

## Issue
A system runs multiple redundant instances of the same agent, worker, or failover component deliberately, for availability — but the instances have no coordination mechanism (a lock, a lease, a consensus protocol) governing who acts when, so two or more of them independently decide they are the one responsible for a given task and both act on it. This produces either duplicate execution of a side-effecting action (two remediation scripts both restart the same service, two agent replicas both send the same customer notification) or an outright split-brain, where two instances each believe themselves to be the sole active primary and take conflicting, contradictory actions on the same shared resource at the same time.

**Frequency**: Occasional

**Symptoms**
- The same side-effecting action (a notification, a remediation step, a database write) fires twice within a short window, each instance's logs showing it acted with no awareness the other also acted
- Two component instances each report themselves as "active" or "primary" simultaneously, discoverable only by cross-referencing both instances' own status rather than from any single source of truth
- A remediation or failover action taken by one redundant instance is undone or conflicted with by another instance's own, differently-timed remediation attempt on the same resource
- Redundancy was added specifically to improve availability, but the failure mode observed is a correctness/consistency incident rather than an outage — the system is more available and less correct at the same time
- Incident review finds no lock, lease, or leader-election mechanism between the redundant instances; each instance's decision logic assumes it is the only one active

## Root Cause
Redundancy for availability and coordination for correctness are two separate concerns that are easy to conflate: running multiple instances of a component protects against any single instance failing, but it does nothing on its own to ensure only one instance acts at a time — that requires an explicit coordination protocol (a distributed lock, a lease with a timeout, a consensus-based leader election, an idempotency mechanism at the point of action) layered on top of the redundancy. When a system is designed with redundant instances but the coordination layer is assumed rather than built — because "we have replicas" is treated as sufficient without asking "and how do they agree on who acts" — every redundant instance runs its own independent decision loop, and under normal conditions this may go unnoticed if timing rarely causes overlap. It surfaces specifically when multiple instances observe the same trigger condition close together in time (a shared health-check failure, a shared queue item), each independently concludes it should act, and no protocol exists to let only one of them win.

## Example
```
A platform runs two replicas of an on-call remediation agent for
availability, each independently subscribed to the same infrastructure
health-check feed, with no leader election or distributed lock between
them - the team's reasoning at design time was "if one replica goes
down, the other keeps handling remediation," without a corresponding
answer to "what happens when both are up at once."

A shared database connection pool reports exhaustion. Both remediation
agent replicas receive the same alert within the same second and each,
running its own independent decision loop, concludes the fix is to
restart the affected service to clear the pool.

Replica A issues a restart command at 03:14:02.100. Replica B, unaware
of Replica A's action, issues its own restart command at 03:14:02.340 -
before the first restart has even completed. The service, mid-restart
from the first command, receives a second restart signal and enters a
crash-loop, because the underlying orchestrator wasn't designed to
handle two overlapping restart requests for the same instance.

The db connection pool incident, which a single, correctly-scoped
restart would have resolved in under a minute, instead becomes a
10-minute outage caused entirely by the two redundant remediation
agents fighting each other, with neither aware the other existed.
```

## Statistics
| Finding | Context |
|---|---|
| A meaningful share of duplicate-action incidents in systems with redundant automated remediation trace back to a missing coordination protocol rather than a bug in either instance's individual logic | Estimated from postmortems of multi-replica automation incidents |
| Systems adding an explicit lease or lock before allowing an automated action report a substantial reduction in duplicate/conflicting remediation events | Reported range across teams introducing coordination after a prior incident |
| Split-brain-style incidents in redundant agent deployments are more likely during shared, correlated trigger events (a common health-check failure) than during independent, staggered triggers | Typical pattern observed where simultaneous observation of the same signal is the primary precondition |

## Mitigations
1. **Require a lease or lock before any side-effecting action, not just before claiming leadership**: Have every redundant instance acquire a short-lived, renewable lease scoped to the specific resource or task before acting, so simultaneous triggers resolve to exactly one actor even without a persistent leader role.
2. **Make side-effecting actions idempotent at the point of execution**: Design the downstream action itself (restart, notification, write) to be safely repeatable — a restart command that no-ops if a restart is already in progress, a notification keyed to dedupe on a request ID — so a coordination gap degrades to a harmless no-op instead of a conflicting double-action.
3. **Treat "redundant instances" and "coordinated instances" as separate design requirements**: When adding replicas for availability, explicitly design and test the coordination protocol between them as its own requirement, rather than treating redundancy as automatically implying safe concurrent operation.
4. **Centralize the decision, distribute only the execution**: Where feasible, route the "should we act" decision through a single coordinating point (even if backed by redundant infrastructure) so multiple redundant workers only ever execute a dispatched action rather than each independently deciding to act.
5. **Log and alert on concurrent claims of the same task/resource**: Instrument redundant instances to detect and flag when two of them attempt to act on the same resource within a short window, surfacing coordination gaps in testing and staging before they cause a production incident.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| duplicate_action_rate | Rate of the same side-effecting action being executed more than once for the same trigger/resource within a short window | Alert on any nonzero rate for critical remediation actions |
| concurrent_active_instance_count | Number of redundant instances simultaneously believing themselves active/primary for the same resource | Alert if greater than 1 |
| lease_acquisition_contention_rate | Rate at which multiple instances attempt to acquire the same lease/lock concurrently | Track as a leading indicator even when contention resolves correctly |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Duplicate action detected | duplicate_action_rate nonzero for a side-effecting remediation or notification action | High | Halt further automated action on the affected resource, reconcile any conflicting state, add/fix the coordination lease |
| Multiple instances claim active status | concurrent_active_instance_count > 1 for a component expected to have a single active instance | Critical | Force one instance into standby, investigate the coordination mechanism's failure |

## Related Patterns
- [Cascade Divergent Recovery](./cascade-divergent-recovery.md) - divergent recovery is multiple components independently recovering to inconsistent end states after one shared fault; this pattern is redundant instances acting without coordination during normal or fault-triggered operation, a distinct mechanism (missing coordination protocol vs. independent recovery paths) even though both produce cross-component inconsistency
- [Leader Election Failure](../../multi-agent-orchestration/failures/leader-election-failure.md) - a failed or absent leader-election mechanism is one specific way this pattern's coordination gap can arise; this pattern also covers coordination failures with no leader concept at all (lease-based or lock-based coordination between peer redundant instances)
- [Byzantine Agent Failure](../../multi-agent-orchestration/failures/byzantine-agent-failure.md) - byzantine failure is about one agent producing actively adversarial-looking output that others can't detect; this pattern's instances are all behaving correctly and honestly, they simply lack a protocol to avoid acting redundantly
