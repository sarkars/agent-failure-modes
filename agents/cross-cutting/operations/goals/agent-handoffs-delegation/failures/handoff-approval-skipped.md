# Handoff Approval Skipped

## Issue
A workflow is designed so that one agent must obtain sign-off from a human or a designated approval agent before handing a task to the next agent in the chain, but the handoff occurs without the gate being satisfied. This happens most often when the approval step is implemented as a soft convention rather than a hard dependency — the sending agent's code path can reach the handoff call whether or not the approval response was received, correct, or even requested. The receiving agent, having no way to know an approval was expected, proceeds to execute.

**Frequency**: Occasional

**Symptoms**
- Downstream actions (payments, deployments, external communications) occurring with no corresponding approval record
- Approval-agent logs showing a request was sent but no response was ever received, while the workflow log shows the task moved forward anyway
- Audit trails with gaps between "approval requested" and "action taken" events
- Incidents traced back to a race condition where the handoff fired before the approval response arrived, or after an approval timeout that was treated as an implicit yes

## Root Cause
Approval gates are frequently implemented as a side call the sending agent makes and logs, rather than as a blocking precondition enforced by the orchestration layer itself. When the approval call is async — a message sent to a Slack channel, a ticket assigned to a human reviewer, a separate approval microservice — the sending agent's main control flow often doesn't actually wait on a positive result; it fires the request and continues, or it times out and defaults to proceeding rather than defaulting to blocking. Because the gate lives in application logic rather than being enforced structurally (e.g., the receiving agent refusing to act without a signed approval token), any code path, retry, or race condition that bypasses the gate call goes undetected.

## Example
```
A deployment-orchestration agent finishes building a release candidate and
is supposed to request sign-off from a "release-approval" agent before
handing the artifact to the "deploy-agent" for production rollout.

The approval request is sent as a fire-and-forget message: the
deployment-orchestration agent posts to the approval queue and, per its
retry logic, proceeds to hand off to deploy-agent after a 90-second
timeout if no response is received, on the assumption that "the approver
is probably just slow, don't block the pipeline."

The release-approval agent is mid-restart following an unrelated
deployment and never receives the message. 90 seconds later, deploy-agent
receives the handoff with no approval token attached, and its own
validation only checks that a handoff message exists — not that it
carries a valid approval record. The release goes to production without
anyone having reviewed it. The gap is discovered two days later when a
customer reports a regression that would have been caught in the skipped
review.
```

## Statistics
| Finding | Context |
|---------|---------|
| Roughly 10-20% of asynchronous approval gates implemented as fire-and-forget requests fail to block on non-response in production incident samples | Typical range observed across orchestration postmortems |
| Workflows that changed timeout-on-no-response from "proceed" to "block and escalate" saw skipped-approval incidents drop by more than half | Reported range across teams hardening approval gates |
| Median time-to-discovery for a skipped approval is measured in days when no completion audit exists | Estimated from incident reviews of approval-gated pipelines |

## Mitigations
1. **Cryptographic approval tokens**: Require the receiving agent to validate a signed, non-forgeable approval token before acting, rather than trusting that a handoff message implies approval occurred.
2. **Default-deny on timeout**: Configure approval waits to block and escalate to a human on timeout rather than silently proceeding as if approved.
3. **Structural gate enforcement**: Move the approval check out of the sending agent's optional logic and into the receiving agent's or orchestrator's mandatory precondition, so no code path can reach execution without it.
4. **Approval-action correlation audit**: Continuously reconcile "approval granted" events against "downstream action taken" events by task ID, and alert on any action lacking a matching approval.
5. **Idempotent, replay-safe approval requests**: Ensure approval requests survive approver-side restarts or outages by persisting them in a durable queue the approver re-reads on recovery, rather than one-shot messages that are lost if the approver is unavailable.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| unapproved_action_count | Count of downstream actions executed with no matching valid approval token | Alert if > 0 |
| approval_timeout_proceed_rate | Rate at which approval waits time out and the workflow proceeds anyway | Alert if > 1% |
| approval_response_latency | Time between approval request and response | Alert if p95 exceeds configured timeout |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Action without approval token | A gated action executes with no valid, matching approval token in the audit trail | High | Halt the pipeline, page on-call, initiate rollback review |
| Approval gate timeout-proceed | An approval wait times out and the workflow's default-proceed path fires | Medium | Alert the approver channel, flag the task for post-hoc review |

## Related Patterns
- [Handoff Timing Mismatch](./handoff-timing-mismatch.md) - the same async-timing gap that lets an approval be skipped can also cause a handoff to fire before the receiver is ready
- [Handoff Accountability Loss](./handoff-accountability-loss.md) - once an approval is skipped, there is often no clear owner responsible for catching the gap
- [Handoff Rollback Failure](./handoff-rollback-failure.md) - actions taken without approval are frequently the hardest to cleanly roll back once discovered
