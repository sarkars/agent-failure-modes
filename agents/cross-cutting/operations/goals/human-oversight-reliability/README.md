# Human-in-the-Loop Failures in AI Agents: Missing Approvals, Stale Approvals, and Queue Overflow

**Human oversight fails when approvals are missing, the wrong person approves, a stale approval is reused, or the approval step itself breaks down.** These eight patterns cover human-in-the-loop reliability for agents that take consequential actions.

## Key Takeaways

- Gates can be missing entirely, or present but pointed at the wrong approver.
- An approval is only valid for the context it was given in; reusing it for changed context is a failure.
- The approval path needs fallbacks: queue overflow, unavailable approvers, and timeouts each cause their own failures.
- Human corrections also need to feed back into later agent decisions.

## Patterns

| Pattern | What goes wrong |
|---|---|
| [Approval Queue Overflow](failures/approval-queue-overflow.md) | Too Many Pending Approvals Cause Delays or Dropped Requests |
| [AI Agent Approval Timeout Mishandling](failures/approval-timeout-mishandling.md) | The automatic approval review times out while evaluating the requested approval, and the agent then does the wrong thing — auto-approving without real review, or… |
| [Authority Mismatch](failures/authority-mismatch.md) | Wrong Person Approves Action |
| [Escalation Not Triggered](failures/escalation-not-triggered.md) | Agent Fails to Escalate to Human When Required |
| [Feedback Not Incorporated](failures/feedback-not-incorporated.md) | Human Corrections Ignored in Subsequent Agent Decisions |
| [Human Unavailability](failures/human-unavailability.md) | No Fallback When Required Approver Is Unavailable |
| [Missing Approval Gates](failures/missing-approval-gates.md) | Workflow Lacks Required Approval Step for High-Risk Action |
| [Stale Approval Reuse](failures/stale-approval-reuse.md) | Agent Uses Old Approval for New or Changed Context |

**Total: 8 patterns**

## How These Patterns Group

- **Gates and authority:** Missing Approval Gates, Authority Mismatch, Escalation Not Triggered
- **Approval validity:** Stale Approval Reuse, AI Agent Approval Timeout Mishandling
- **Capacity and availability:** Approval Queue Overflow, Human Unavailability
- **Learning from humans:** Feedback Not Incorporated

## When This Matters

- The agent can move money, change records, or send external messages
- Approvers are few and queues can back up
- Policies require a named person to sign off

## Frequently Asked Questions

### When should an AI agent escalate to a human?

See escalation not triggered for what goes wrong when it does not.

### What happens when no approver is available?

See human unavailability and approval timeout mishandling.

### Can an old approval cover a new action?

No. See stale approval reuse.

## Related

- [All operations goals](../)
- [Operations overview](../../)
