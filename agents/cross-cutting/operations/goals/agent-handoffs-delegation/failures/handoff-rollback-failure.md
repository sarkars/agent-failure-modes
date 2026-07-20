# Handoff Rollback Failure

## Issue
After a task is handed off, the receiving agent fails partway through execution, and the workflow attempts to roll back to the pre-handoff state — but the rollback cannot be cleanly performed. This happens because the receiving agent has already taken irreversible or partially-irreversible actions (sent a message, committed a write, called an external API with a side effect), and no compensating action exists, or the sending agent no longer has the context or authority to undo what the receiver did.

**Frequency**: Occasional

**Symptoms**
- A failed task leaves behind partial side effects (a record created but not linked, a notification sent but the underlying action never completed) that persist after the "failure" is logged
- Rollback logic exists for the sending agent's own actions but has no visibility into or control over actions the receiving agent took independently
- Manual intervention required to reconcile state after a handoff failure, rather than an automated rollback completing
- Incident reviews finding that a "rolled back" task actually left residual state that a person had to clean up by hand

## Root Cause
Rollback across an agent boundary requires either that all actions taken be reversible by design (compensating transactions) or that the rollback mechanism have full visibility and authority over every side effect the receiving agent performed. Neither is guaranteed by default: a receiving agent's actions are often opaque to the sender beyond "task succeeded" or "task failed," and even where a compensating action theoretically exists (cancel an order, revoke a grant), the receiving agent might not implement it, or the sending agent might not know it needs to invoke it because the two agents were never designed with a shared rollback protocol. The failure is structural — rollback was treated as "undo the handoff," when what's actually needed is "undo every side effect performed after the handoff," which is a much larger and harder-to-guarantee scope.

## Example
```
An HR-onboarding agent hands off "provision new-hire accounts for
Priya Shah" to a provisioning agent, which sequentially: creates an
email account, adds her to the company directory, sends a welcome
email with a temporary password, and requests a laptop from IT asset
management.

The laptop request step fails (IT asset management API returns "out of
stock, cannot fulfill"). The provisioning agent reports task failure
back to the onboarding agent, which triggers a rollback.

The rollback logic deletes the email account and directory entry it
knows the provisioning agent created (inferred from the task
definition), but has no record of the welcome email having already
been sent, and no compensating action ("recall email," "invalidate
temp password") was ever implemented. Priya receives a welcome email
with login credentials for an account that no longer exists by the
time she tries to use it, and calls IT confused about why her new
account was deleted before her first day.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 15-30% of handoff failures that trigger a rollback leave at least one residual side effect uncleaned | Typical range observed in multi-step provisioning and fulfillment workflows |
| Workflows using saga-pattern compensating transactions for every step report substantially fewer residual-state incidents than those relying on generic "undo" logic | Reported range across teams adopting explicit compensation design |
| Median manual cleanup time for a failed rollback with residual state is measured in tens of minutes to hours depending on how many downstream systems were touched | Estimated from incident postmortems involving multi-system provisioning failures |

## Mitigations
1. **Saga pattern with explicit compensating actions**: Design each step of a multi-step handoff chain with a corresponding, tested compensating action (e.g., "send welcome email" pairs with "send account-deactivated notice"), not a generic rollback that assumes reversibility.
2. **Side-effect ledger per task**: Have every agent in a handoff chain append every side-effecting action it takes to a shared, task-scoped ledger, so a rollback routine has full visibility into what actually happened, not just what the task definition assumed would happen.
3. **Irreversible-action gating**: Flag genuinely irreversible actions (sending external communications, financial transactions) and require them to occur only after all reversible steps in the chain have succeeded, minimizing the rollback surface.
4. **Rollback dry-run and verification**: After executing a rollback, verify against the side-effect ledger that every logged action has a corresponding compensating action recorded, and alert if any are missing.
5. **Human-in-the-loop for partial-failure states**: When an automated rollback cannot fully compensate for a receiving agent's actions, route the task to a human with the full side-effect ledger attached rather than reporting silent or partial rollback success.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| residual_side_effect_count | Count of logged side effects from a failed task with no corresponding compensating action recorded post-rollback | Alert if > 0 |
| rollback_completion_rate | Share of triggered rollbacks that successfully compensate for every recorded side effect | Alert if < 100% |
| irreversible_action_before_completion_rate | Rate of tasks where an irreversible action occurred before all reversible steps succeeded | Alert if > 0% for gated workflows |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Incomplete rollback detected | A rollback completes but the side-effect ledger shows uncompensated actions remaining | High | Page on-call, route to human for manual reconciliation, halt further automated rollback attempts on similar tasks |
| Irreversible action taken pre-failure | An irreversible action (send, charge, external notify) occurred in a task that subsequently failed and required rollback | Medium | Flag for manual review, assess customer/user-facing impact |

## Related Patterns
- [Handoff Idempotency Violation](./handoff-idempotency-violation.md) - both involve side effects that are hard to cleanly reverse, one from duplication and one from partial failure
- [Handoff Accountability Loss](./handoff-accountability-loss.md) - a failed rollback that leaves residual state often has no clear owner responsible for the cleanup
- [Handoff State Loss](./handoff-state-loss.md) - without a preserved side-effect ledger, the state needed to perform a correct rollback is often the first thing lost
