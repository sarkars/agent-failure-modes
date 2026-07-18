# Record Ownership Not Validated

## Issue
Before executing a write, update, or delete via a tool, the agent doesn't verify that the current user is actually the owner of, or otherwise authorized to modify, the specific record being targeted. The write succeeds because the tool checks that the agent/user has general permission to call the "update" endpoint, but never re-confirms that the particular record ID supplied belongs to that user — turning a routine "update my profile" or "cancel my order" request into a capability to modify anyone's record, simply by supplying a different ID.

**Frequency**: Common

**Symptoms**
- Update or delete calls succeed against records the requesting user doesn't own, with no rejection
- The agent can be prompted (accidentally or adversarially) to modify a record by ID without the tool re-validating ownership at write time
- Read paths correctly enforce ownership but the corresponding write paths on the same record type don't, because they were implemented separately and the ownership check wasn't carried over
- Post-incident review finds a write occurred against a record whose owner never interacted with the agent session that made the change
- Audit trail shows a write attributed to an agent/session with no corresponding ownership verification step in the logs

## Root Cause
Write-path implementations often trust that the agent, having already established some general authorization to use the tool, will supply a legitimate record ID because that's the "normal" usage pattern — so the ownership check that exists on the read path (if any) is either skipped on the write path or assumed to have already happened earlier in the conversation. This assumption breaks down whenever the record ID is attacker- or user-suppliable, comes from an untrusted intermediate step (like a prior tool result that wasn't itself scoped), or is inferred by the agent from conversational context that doesn't actually establish ownership.

## Example
```
A customer-facing agent lets users cancel their own orders via a
`cancel_order(order_id)` tool. The tool's authorization check confirms
the calling session belongs to an authenticated customer, then executes
the cancellation against whatever `order_id` is passed, without
checking that the order's `customer_id` matches the session's customer.

A user, chatting with the agent, mentions an order number they saw
referenced by a friend ("hey can you check on order 88213 for me, my
roommate ordered it under my address"). The agent, trying to be
helpful and interpreting "cancel it since it's a duplicate" from later
in the conversation, calls `cancel_order(88213)`. The tool executes the
cancellation immediately, because it only validated that *a* customer
was authenticated, not that *this* customer owns order 88213 — canceling
a stranger's order based on an ID that surfaced in casual conversation.
```

## Statistics
| Finding | Context |
|---------|---------|
| Missing ownership validation on write/update endpoints is a frequently cited subclass of broken object-level authorization findings, distinct from and often more severe than the equivalent read-path gap | Common in API security assessments |
| Write-path ownership checks are less consistently implemented than read-path checks across audited systems, since read endpoints are more frequently the target of manual security testing | Typical asymmetry found in access-control reviews |
| Agent-mediated write actions are disproportionately represented in "unauthorized modification" incidents compared to direct API misuse, because the record ID reaching the write call is often inferred from conversational or upstream tool-result context rather than supplied by a validated UI control | Emerging pattern specific to agentic tool-calling architectures |

## Mitigations
1. **Ownership check as a mandatory pre-write gate**: Require every write/update/delete tool call to independently verify the target record's ownership against the authenticated requester immediately before executing, with no code path that bypasses this check based on upstream trust.
2. **Reject IDs sourced from untrusted context**: Distinguish between record IDs the agent obtained through its own authorized lookup (already ownership-scoped) versus IDs supplied by the user or inferred from conversation, and require the latter to pass an explicit ownership re-check before any write.
3. **Confirmation step for writes on externally-sourced IDs**: When a write target's ID didn't originate from the agent's own scoped read, require an explicit confirmation step that surfaces the record's key identifying details back to the user before executing, so a mismatch is caught before the action completes.
4. **Symmetric read/write authorization libraries**: Implement ownership checks once in a shared authorization library used by both read and write paths for a given record type, so a check present on reads is guaranteed to also apply to writes.
5. **Write-action audit logging with ownership proof**: Log the ownership verification result (not just the write outcome) for every write action, so any write executed without a matching, logged ownership check is immediately identifiable in an audit.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `unvalidated_write_count` | Count of write/update/delete actions executed without a logged ownership verification | Alert threshold: > 0 (any occurrence) |
| `cross_owner_write_count` | Count of writes where the record's owner doesn't match the authenticated requester | Alert threshold: > 0 (any occurrence) |
| `externally_sourced_id_write_rate` | Share of write actions targeting a record ID that didn't originate from the agent's own scoped lookup | Alert threshold: track and require confirmation gating above a defined baseline |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Unauthorized Write Executed | A write action's logged ownership check fails or is absent, but the write still executed | P1 | Revert the write if possible, notify the affected record owner, patch the missing gate |
| Cross-Owner Write Detected | A completed write's target record ownership doesn't match the requester | P1 | Immediate incident response, notify security and the affected user |

## Related Patterns
- [Record-Level Access Not Enforced](./record-level-access-not-enforced.md) - the read-path counterpart to this write-path failure
- [Account-Level Data Scope](./account-level-data-scope.md) - a related failure where the wrong tenant, rather than the wrong record owner, is targeted
- [Access Control Inheritance Wrong](./access-control-inheritance-wrong.md) - writes executed on inherited-but-unvalidated scope can produce this same unauthorized-modification outcome
