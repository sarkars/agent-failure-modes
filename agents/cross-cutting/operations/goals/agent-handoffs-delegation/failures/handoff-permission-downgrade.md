# Handoff Permission Downgrade

## Issue
The sending agent hands off a task assuming the receiving agent has sufficient permissions to complete it, but the receiving agent actually operates under a narrower permission set — a different service account, a scoped API token, or a role with fewer grants. Rather than failing loudly, the task often degrades silently: the receiving agent's tool calls are denied or return partial results, and it either produces an incomplete output without flagging the gap or falls back to a lower-quality path that masks the permission problem entirely.

**Frequency**: Occasional

**Symptoms**
- Receiving agent completes a task but with missing data, skipped steps, or a degraded output, with no explicit error surfaced
- Permission-denied or 403-class errors appearing in the receiving agent's logs that don't propagate up as task failures
- Receiving agent silently substitutes a fallback method (e.g., estimating a value instead of fetching it) when a permissioned call fails
- Discrepancy between what the sending agent's task description assumes is possible and what the receiving agent's credentials actually allow

## Root Cause
Permission scopes are typically set up per-agent based on that agent's normal responsibilities, not per-task. When Agent A hands a task to Agent B, A's description of the task ("pull the customer's full account history and update their tier") implicitly assumes whatever permissions A itself would need, but A has no visibility into B's actual credential scope and no mechanism to verify B can perform every step before handing it off. If B's tool-calling code treats a permission denial as a recoverable error — logging it and moving on with partial data — rather than as a hard failure that must propagate, the downgrade becomes invisible to everyone except someone who reads B's raw logs.

## Example
```
An account-review agent (running with an admin-scoped service account)
hands off "compile a full billing and support history for account
#8823 and prepare a renewal recommendation" to a report-generation
agent, which runs under a read-only, customer-facing scoped token that
excludes internal support-ticket data for compliance reasons.

The report-generation agent successfully pulls billing history but its
call to the internal support-ticket API returns 403 Forbidden. Its
error-handling path catches the exception, logs "ticket data
unavailable, continuing," and proceeds to generate a renewal
recommendation using only billing data.

The resulting report recommends renewal at the current tier, omitting
that the account has 6 open critical support tickets -- information
that would have changed the recommendation. The gap is only noticed
when a human account manager, reviewing the report before sending it
to the customer, happens to already know about the open tickets.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 10-15% of multi-agent handoffs between agents with different credential scopes involve at least one silently-degraded permission call | Typical range observed in systems with heterogeneous per-agent service accounts |
| Making permission denials hard-fail rather than soft-fail eliminates the majority of silently degraded outputs traced to this cause | Reported range across teams hardening error handling on scoped tool calls |
| Cross-agent permission mismatches are disproportionately common when agents are added to a workflow incrementally without a shared permission audit | Estimated from postmortems on incrementally assembled multi-agent pipelines |

## Mitigations
1. **Permission manifest attached to handoff**: Require the sending agent to declare which permissions/scopes the task needs, and have the receiving agent verify it holds all of them before starting, refusing the handoff otherwise.
2. **Hard-fail on permission denial**: Treat permission-denied responses from tool calls as task-level failures that halt and escalate, not as recoverable errors to log and continue past.
3. **Explicit degraded-output flagging**: If a receiving agent must proceed with partial data due to scope limits, require it to mark the output as degraded and enumerate what was skipped, rather than presenting a partial result as complete.
4. **Pre-handoff capability check**: Before handing off, have the sending agent (or orchestrator) query the receiving agent's effective permission scope and compare it against the task's requirements, rejecting the handoff upfront if there's a known gap.
5. **Periodic cross-agent permission audit**: Regularly compare the permission scopes of agents that hand tasks to each other against the task types they're expected to fulfill, to catch drift as scopes or task definitions change over time.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| silent_permission_denial_count | Count of permission-denied tool responses that did not result in a propagated task failure | Alert if > 0 |
| degraded_output_without_flag_rate | Rate of outputs produced with incomplete data but no degraded-output marker | Alert if > 0% |
| cross_agent_scope_gap_count | Count of task types where the receiving agent's permission scope doesn't cover the sending agent's assumed requirements | Alert if > 0 |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Unflagged degraded output | A task completes using fallback/partial data after a permission denial, with no degraded-output flag set | High | Recall or hold the output, notify the requester, review the affected task manually |
| Permission scope gap detected | Pre-handoff capability check finds the receiving agent lacks a required scope | Medium | Block handoff, route to an agent with sufficient permissions or escalate to a human |

## Related Patterns
- [Handoff Context Incompleteness](./handoff-context-incompleteness.md) - both result in a receiving agent producing output on incomplete information, though from different root mechanisms
- [Handoff Protocol Version Mismatch](./handoff-protocol-version-mismatch.md) - schema mismatches can similarly cause silent partial failures that resemble a permission downgrade
- [Handoff Accountability Loss](./handoff-accountability-loss.md) - a silently degraded output from a permission downgrade is more likely to go unnoticed when no one is tracking the task to a verified completion
