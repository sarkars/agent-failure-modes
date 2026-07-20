# Handoff Accountability Loss

## Issue
An agent completes its portion of a multi-agent workflow and hands the remaining work to another agent, but no entity is ever explicitly marked as the owner of the outstanding task after the transfer. Both the sending agent and the receiving agent treat the handoff itself as the completion event, rather than the downstream task being resolved. The task sits in the receiving agent's queue, an inbox, or a shared work-item store with no active owner tracking it to completion, and it silently stalls.

**Frequency**: Common

**Symptoms**
- Tasks marked "handed off" or "delegated" in logs but never marked "completed" or "failed"
- Users or downstream systems asking "who is working on this?" with no agent able to answer
- Work items sitting untouched for hours or days past their expected completion window with no alert fired
- Post-incident review shows every individual agent behaved correctly according to its own local definition of "done"

## Root Cause
Most multi-agent systems define "done" locally: the sending agent's success criterion is "I successfully transmitted the task," not "the task was completed." Ownership is treated as implicit — whichever agent currently holds the task is assumed to own it — but nothing enforces that assumption once the task crosses an agent boundary. If the receiving agent is busy, misconfigured, or simply never polls its queue, there is no mechanism that notices the task has no active owner, because no component's job is to track ownership across the full lifecycle rather than within a single agent's execution.

## Example
```
A customer-support triage agent classifies an incoming billing dispute as
"requires refund approval" and hands it to a finance-approval agent via a
shared task queue, logging: "Handoff complete: ticket #48213 assigned to
finance-approval-agent."

The triage agent considers its job done and moves to the next ticket.

The finance-approval agent's queue poller is configured to only pick up
tasks tagged "priority=high", but ticket #48213 was tagged "priority=normal"
by the triage agent's default settings. The finance-approval agent never
sees it.

No component owns "verify ticket #48213 reached a resolved state." The
ticket sits in the shared queue for 11 days until the customer emails a
human support lead directly, asking why their refund never arrived.
Retroactive log review shows every individual agent's own logs report
success — the triage agent successfully handed off, and the finance
agent's logs show no error, because it never touched the ticket at all.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 15-25% of tasks in unmonitored multi-agent handoff chains stall without an active owner for longer than the workflow's expected SLA | Typical range observed in production multi-agent pipelines lacking explicit ownership tracking |
| Teams that add explicit ownership-transfer confirmation report a 60-80% reduction in "silently stalled" tasks | Reported range across teams retrofitting accountability tracking |
| Median time-to-detection for an unowned stalled task without active monitoring is measured in days, not minutes | Estimated from incident postmortems involving queue-based agent handoffs |

## Mitigations
1. **Explicit ownership acknowledgment**: Require the receiving agent to emit an explicit "ownership accepted" event before the sending agent is allowed to consider the handoff complete; treat the absence of acknowledgment within a timeout as a handoff failure.
2. **End-to-end task lifecycle tracking**: Track each task's state through a lifecycle owned by the workflow orchestrator, not by any individual agent, so "handed off" is a transient state rather than a terminal one.
3. **Ownership TTL and escalation**: Attach a time-to-live to every ownership assignment; if the owning agent hasn't produced a status update or completion signal before the TTL expires, automatically escalate to a human or reassign to a fallback agent.
4. **Single source of truth for open tasks**: Maintain a queryable registry of all tasks with a non-terminal state and their current owner, and periodically reconcile it against agent activity logs to surface orphaned tasks.
5. **Handoff completion is not task completion**: Instrument agents to distinguish "I transmitted the task" metrics from "the task reached a terminal state" metrics, and alert when the two diverge for the same task ID.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| unowned_task_duration_seconds | Time a task has spent with no agent actively acknowledging ownership | Alert if > 4x expected task SLA |
| handoff_to_acknowledgment_gap | Time between a handoff event and the receiving agent's ownership acknowledgment | Alert if > 15 minutes with no acknowledgment |
| stalled_task_count | Count of tasks in non-terminal state with no owner activity in the last N hours | Alert if > 0 for high-priority queues |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Orphaned task detected | A task has a non-terminal state and no agent has acknowledged ownership within the configured TTL | High | Escalate to on-call, reassign to fallback agent, notify workflow owner |
| Handoff/completion metric divergence | handoff_count for a task ID has no corresponding completion_count within the expected window | Medium | Audit the receiving agent's queue configuration and filters |

## Related Patterns
- [Handoff Context Incompleteness](./handoff-context-incompleteness.md) - a related failure where the receiving agent does take ownership but lacks the information to act on it correctly
- [Handoff Timing Mismatch](./handoff-timing-mismatch.md) - one specific mechanism by which a receiving agent never picks up ownership, contributing to accountability loss
- [Handoff Rollback Failure](./handoff-rollback-failure.md) - accountability loss often surfaces only when a rollback is attempted and no owner can be found to authorize or perform it
