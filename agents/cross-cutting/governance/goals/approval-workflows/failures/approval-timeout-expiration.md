# Approval Timeout Expiration

## Issue
An approval request times out because no approver responds within the configured window, and the agent's downstream behavior on timeout is either undefined or set to fail-open: the action proceeds automatically as if approved, or the requester and approvers are never clearly told that the timeout occurred and what happened as a result. Either way, a control that was supposed to require an affirmative human decision ends up producing an outcome no human actually made.

**Frequency**: Very Common

**Symptoms**
- Actions executing with an approval record showing "timed out" rather than "approved"
- Requesters unsure whether their request was approved, rejected, or simply never actioned
- Approvers unaware a request they never saw or acted on has already resulted in an executed action
- Timeout duration configured without regard to the actual criticality or risk of the action (a $500 expense and a production database migration sharing the same timeout window)
- No escalation or re-notification before the timeout fires, so approvers had no second chance to respond

## Root Cause
Timeout handling is often added late in workflow design, as a way to prevent requests from blocking indefinitely, without a corresponding decision about what should happen when the timeout is hit. Defaulting to fail-open ("proceed if unanswered") is operationally convenient because it keeps agent throughput high and avoids the appearance of the system being "stuck," but it silently converts an approval gate into a no-op under load or during approver unavailability, and this default is frequently chosen without an explicit risk assessment per action type.

## Example
```
1. An agent requests approval to rotate a production API credential, with a
   4-hour approval timeout inherited from a generic workflow template not
   specifically reviewed for this action type.
2. The designated approver is in a full day of back-to-back meetings and
   does not see the notification.
3. No reminder or escalation fires before the timeout window closes.
4. At the 4-hour mark, the workflow's default timeout behavior -- proceed if
   no rejection was received -- causes the agent to rotate the credential
   automatically.
5. The rotation breaks an integration that depended on the old credential,
   which the approver would have flagged as a known dependency had they
   actually reviewed the request.
6. The incident retrospective finds the approval record shows "timed out,
   proceeded by default," which no one had configured deliberately for this
   action type.
```

## Statistics
| Finding | Context |
|---------|---------|
| A substantial share of automated workflow templates default to fail-open on approval timeout unless explicitly configured otherwise | Common default in workflow-engine tooling |
| Timeout-driven executions are disproportionately involved in approval-related incident postmortems relative to their share of total approval volume | Consistent with fail-open being a higher-risk path than an explicit human decision |
| Requests that receive at least one reminder notification before the timeout window closes are answered by a human at a markedly higher rate than those without a reminder | Typical effect of reminder/escalation nudges in approval systems |

## Mitigations
1. **Fail-closed by default**: Configure approval timeouts to block the action (not proceed) unless a specific, risk-assessed exception explicitly justifies fail-open behavior for that action type.
2. **Risk-tiered timeout windows**: Set timeout duration based on the risk/criticality of the action rather than a single generic default across all workflows; high-risk actions should have shorter windows and more aggressive escalation, not the same window as low-risk ones.
3. **Pre-timeout reminders and escalation**: Send at least one reminder before the timeout window closes, and escalate to a backup approver or governance owner rather than letting the window lapse with no human ever having seen the request.
4. **Explicit timeout-outcome notification**: When a timeout occurs, clearly notify the requester, the original approver, and (for fail-open cases) a governance owner of exactly what happened and why, rather than leaving the timeout outcome buried in a status field.
5. **Timeout behavior as a reviewable policy setting**: Make the fail-open/fail-closed choice per action type a documented, periodically reviewed policy decision, not an unexamined default inherited from a workflow template.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `timeout_fail_open_rate` | Share of timed-out approvals that proceeded automatically rather than blocking | > 5% of timeouts for high-risk action types |
| `unreminded_timeout_rate` | Share of timeouts that occurred without any prior reminder notification | > 10% of timeouts |
| `timeout_to_incident_correlation` | Count of production incidents traceable to an action that executed via timeout rather than explicit approval | > 0 per quarter (target: zero for high-risk actions) |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| High-risk action proceeding via timeout | A fail-open timeout is about to trigger execution for an action above a defined risk threshold | Critical | Auto-escalate to backup approver, delay execution, notify governance owner before proceeding |
| Timeout with no prior reminder | Approval window closes without any reminder having been sent | Warning | Review reminder configuration for that workflow, treat outcome as lower-confidence for audit purposes |

## Related Patterns
- [Approval Chain Break](./approval-chain-break.md) - a broken chain often surfaces first as an unexplained timeout
- [Approval Authority Escalation Failure](./approval-authority-escalation-failure.md) - both involve a request stalling with no effective human decision reached in time
- [Approval Waiver Abuse](./approval-waiver-abuse.md) - fail-open timeout behavior and waiver abuse both let actions proceed without a genuine approval decision
