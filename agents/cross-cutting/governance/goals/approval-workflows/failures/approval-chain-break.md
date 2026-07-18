# Approval Chain Break

## Issue
A multi-step approval chain (for example, manager approves, then finance reviews, then compliance signs off) breaks partway through because one link in the chain fails to forward the request to the next stage. The agent or workflow engine has already recorded the completed steps as "approved," creating the appearance of forward progress, but the request never actually reaches the remaining approvers and simply goes cold in an intermediate state.

**Frequency**: Common

**Symptoms**
- A request shows "manager approved" but no record of ever reaching the finance queue
- Requesters follow up weeks later assuming the request is "in finance" when it never left the manager's system
- No single owner exists for the handoff between stages, so no one notices the gap
- Chain state stored inconsistently across systems (e.g., manager approval in an HR tool, finance review in a separate ticketing system) with no shared correlation ID
- Agents that re-trigger the whole chain from stage one when asked to "check status," masking that the chain was broken rather than slow

## Root Cause
Approval chains are frequently implemented as a sequence of independent point-to-point handoffs rather than as a single state machine with an authoritative status. Each stage's system only knows "did I receive a request" and "did I complete my review" — nothing owns the transition between stages. When the handoff mechanism (a webhook, a queue message, a scheduled job) fails without raising an error, the chain has no way to detect that a completed stage never triggered the next one.

## Example
```
1. An agent submits a $40,000 contract for approval, requiring
   manager -> finance -> compliance sign-off in sequence.
2. The manager approves within the HR approval tool.
3. Approval of the manager stage is supposed to fire a webhook that creates
   a corresponding review ticket in the finance system.
4. The webhook call fails due to a transient network error; the finance
   system never creates a ticket, and the webhook has no retry or
   dead-letter handling.
5. The HR tool marks the manager stage "complete" regardless of whether the
   downstream ticket was created successfully.
6. Three weeks pass. No one in finance has a queue item for the contract.
7. The requester, seeing "manager approved" in the HR tool, assumes the
   contract is progressing and proceeds to reference it as approved in
   external communications, even though finance and compliance have never
   seen it.
```

## Statistics
| Finding | Context |
|---------|---------|
| Cross-system approval handoffs (chains spanning more than one tool) fail to complete at a notably higher rate than single-system chains, often cited in the 5-10% range | Typical range reported in workflow-automation postmortems |
| Median time-to-discovery for a broken chain is measured in weeks, not days, when discovery depends on a human noticing rather than automated detection | Common in organizations without chain-level status tracking |
| A majority of broken-chain incidents involve a webhook, queue, or scheduled-job handoff rather than a failure within a single stage's own logic | Consistent pattern across integration-heavy approval systems |

## Mitigations
1. **Single authoritative chain-state record**: Maintain one system of record for the overall chain status (not started / stage N pending / stage N complete / chain complete) that all stages read from and write to, rather than inferring status by querying each stage's system independently.
2. **Idempotent, retried handoffs with dead-letter alerting**: Make inter-stage handoffs (webhooks, queue messages) retry automatically on failure, and alert a human when a handoff exhausts retries instead of failing silently.
3. **Heartbeat / staleness detection per stage**: If a chain has been sitting in a "pending at stage N" state longer than that stage's expected SLA, raise an alert rather than waiting for a stakeholder to notice.
4. **Correlation ID across all systems in the chain**: Require every system involved in the chain to log against a shared request ID so a chain's full path can be reconstructed and audited across tool boundaries.
5. **Explicit "chain complete" gate before execution**: Do not allow the agent to treat the action as approved until the chain-state record shows every required stage complete — never infer overall approval from the most recent stage alone.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `chain_handoff_failure_rate` | Share of inter-stage handoffs that fail to create the downstream review item | > 0.5% of handoffs |
| `chain_stage_stall_age_p95` | 95th-percentile time a chain sits at a single stage without progressing | > SLA for that stage (e.g., 48h for finance review) |
| `orphaned_chain_count` | Number of chains with a completed stage but no corresponding downstream record | > 0 (should trend to zero) |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Handoff dead-lettered | Inter-stage webhook/queue message exhausts retries | Critical | Page workflow owner, manually create downstream review item, backfill correlation ID |
| Chain stalled past SLA | No stage-status change for longer than that stage's defined SLA | Warning | Notify chain owner and current-stage approver to confirm receipt |

## Related Patterns
- [Approval Authority Escalation Failure](./approval-authority-escalation-failure.md) - both are routing failures within a multi-party approval process
- [Approval Timeout Expiration](./approval-timeout-expiration.md) - a broken chain often presents as a timeout at whichever stage the handoff failed to reach
- [Approval Conflict](./approval-conflict.md) - both stem from the absence of a single authoritative status for a multi-approver decision
