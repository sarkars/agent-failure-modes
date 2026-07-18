# Approval Authority Escalation Failure

## Issue
An agent submits an approval request that exceeds the current approver's authority limit (e.g., a spend amount, a data-access scope, or a risk tier above what that role can sign off on). The workflow is supposed to automatically route the request to a higher-authority approver, but the escalation path fails silently — the request sits in the original approver's queue indefinitely, gets auto-approved because the "requires escalation" flag was never checked, or gets auto-rejected because the escalation target couldn't be resolved.

**Frequency**: Common

**Symptoms**
- Approval requests stuck in "pending" for days with no escalation ever triggered
- Requests above a known authority threshold showing as "approved" by someone whose role limit is below the request amount
- Escalation target lookup returning null or a deprovisioned account, with no fallback
- No audit trail entry showing an escalation attempt, only the original submission and a terminal decision
- Agents retrying the same request against the same under-authorized approver instead of routing upward

## Root Cause
Escalation logic is typically implemented as a side lookup (org chart, role table, or delegation-of-authority matrix) that runs at submission time rather than as a continuously enforced invariant. When the authority table is stale, the higher-authority approver is unassigned, or the agent's policy check only validates "is there an approver" rather than "is this the right-tier approver," the system has no mechanism to detect that escalation was required but never happened.

## Example
```
1. A procurement agent submits a $75,000 purchase approval request.
2. The assigned approver, a team lead, has a signing limit of $25,000.
3. The workflow engine is supposed to detect the limit breach and escalate to
   the director tier automatically.
4. The escalation rule references a role-to-approver mapping that was not
   updated after a reorg; the director field resolves to an empty value.
5. The workflow engine treats "no escalation target found" as "no escalation
   needed" rather than raising an error, and leaves the request sitting in
   the team lead's queue.
6. The team lead, unaware the amount exceeds their authority, approves it
   anyway because the UI doesn't surface the limit breach.
7. The purchase executes at $75,000 with only $25,000-tier sign-off on record.
```

## Statistics
| Finding | Context |
|---------|---------|
| Escalation-path failures account for an estimated 15-20% of approval-control audit findings in agentic procurement and access-request systems | Typical range observed in production governance reviews |
| Requests that silently stall without escalation average 3-5x longer time-to-resolution than requests that escalate correctly | Based on workflow latency telemetry patterns |
| A large share of authority-mismatch approvals are only caught retroactively, during periodic audit sampling rather than at execution time | Common in organizations without real-time authority validation |

## Mitigations
1. **Fail-closed on unresolved escalation targets**: If the escalation lookup returns no valid higher-authority approver, block the action and raise an explicit alert rather than defaulting to "no escalation needed."
2. **Authority-tier validation at decision time, not just submission time**: Re-check that the approver who actually clicked "approve" has sufficient authority for the final request amount/scope before executing, not just at routing time.
3. **Surface authority limits in the approver UI**: Show the approver their own signing limit next to the request amount so an under-authorized approval is visually obvious, as a second line of defense.
4. **Periodic reconciliation of the delegation-of-authority table**: Automatically flag role mappings that haven't been validated against current org structure within a defined interval (e.g., 30 days).
5. **Escalation timeout with active paging**: If a request requiring escalation hasn't reached a valid higher-tier approver within a defined SLA, page a fallback approver or governance owner rather than letting it sit silently.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `escalation_resolution_failure_rate` | Share of escalation attempts that fail to resolve a valid higher-authority approver | > 1% of escalation-eligible requests |
| `authority_mismatch_approvals` | Count of approvals executed by an approver below the required authority tier for the request | > 0 per week (should be zero-tolerance) |
| `escalation_pending_age_p95` | 95th-percentile time a request sits waiting for escalation routing | > 4 hours |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Escalation target unresolved | Escalation lookup returns null/empty for a request above an approver's limit | Critical | Block execution, page governance on-call, do not default to auto-approve or auto-route to original approver |
| Stale delegation-of-authority mapping | Role-to-approver table entry unchanged for > 90 days while org roster has changed | Warning | Trigger manual review of the mapping before next escalation event |

## Related Patterns
- [Approval Chain Break](./approval-chain-break.md) - both involve a routing step in a multi-party approval flow silently failing to forward the request
- [Approval Timeout Expiration](./approval-timeout-expiration.md) - escalation failures often manifest as timeouts once the request has no valid recipient
- [Approval Delegation Loop](./approval-delegation-loop.md) - misconfigured delegation mappings can cause loops instead of, or in addition to, escalation dead-ends
