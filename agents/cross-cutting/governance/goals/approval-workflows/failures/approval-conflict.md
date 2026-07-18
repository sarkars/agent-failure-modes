# Approval Conflict

## Issue
An action requires sign-off from two or more independent approvers, and they issue conflicting decisions — one approves, another rejects. The approval system has no defined resolution rule for this case, so the agent falls back to undefined behavior: proceeding because "at least one approval" was recorded, blocking because "any rejection" wins, or simply acting on whichever decision was recorded last (last-write-wins), none of which reflects an actual governance policy.

**Frequency**: Occasional

**Symptoms**
- Audit logs showing one "approve" and one "reject" for the same request with the action still executed
- Approvers surprised to learn their rejection was overridden by a later approval from someone else
- Inconsistent outcomes for structurally identical conflicts depending on which approver responded first or last
- No UI or workflow state that ever surfaces "conflicting decision" as its own status
- Agents proceeding on partial quorum (e.g., 1 of 2 required approvers) without a defined quorum rule

## Root Cause
Multi-approver workflows are often built assuming approvers will agree, so the decision-aggregation logic only handles "all approved" and "any rejected" as trivial cases and lacks an explicit rule for genuine disagreement, or worse, aggregates decisions with a simple database update where the last write simply overwrites the field holding "current decision," destroying the record of the earlier conflicting vote.

## Example
```
1. A data-access request requires sign-off from both the requester's manager
   and the data owner, evaluated independently.
2. The manager approves the request at 10:02 AM.
3. The data owner, reviewing separately, rejects the request at 10:15 AM
   citing sensitivity concerns.
4. The approval record is a single "status" field per request; the data
   owner's rejection simply overwrites the manager's approval.
5. Because the final recorded status happens to be "rejected," the agent
   blocks the action -- but if the data owner had responded first and the
   manager second, the final status would have been "approved" and the
   action would have proceeded, purely due to response ordering.
6. Neither approver is notified that their decision conflicted with the
   other's, and no one reviews the disagreement itself.
```

## Statistics
| Finding | Context |
|---------|---------|
| Multi-approver requests see genuine disagreement between approvers in roughly 3-8% of cases in access-control and spend-approval workflows | Typical range observed in dual-control governance systems |
| A majority of systems without an explicit conflict-resolution rule default to some form of last-write-wins behavior by construction of their data model | Common in systems using a single mutable "status" field per request |
| Conflicting-decision incidents are disproportionately represented in post-incident reviews relative to their frequency, because the outcome is unpredictable rather than merely delayed | Consistent with governance audit patterns |

## Mitigations
1. **Explicit conflict state as a first-class outcome**: Model "approve" and "reject" per-approver as independent, preserved records, and define a distinct "conflicting decision" status that blocks execution until resolved -- do not let one decision silently overwrite another.
2. **Defined resolution policy, not ordering**: Establish and encode an explicit rule for conflicts (e.g., any rejection blocks regardless of approval count, or conflicts escalate to a designated tie-breaker) rather than letting outcome depend on response timing.
3. **Immediate conflict notification**: When a conflict is detected, notify all approvers involved and a governance owner immediately, rather than letting the action proceed or stall silently.
4. **Quorum and unanimity rules defined per action type**: Specify up front whether an action requires unanimous approval, majority, or any single rejection to block, and enforce that rule mechanically rather than through ad hoc status fields.
5. **Immutable per-approver decision log**: Store every approver's decision as an append-only record tied to their identity and timestamp, so conflicts are always reconstructable and auditable, independent of the current aggregate status.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `approval_conflict_rate` | Share of multi-approver requests with at least one dissenting decision | > 2% of multi-approver requests |
| `conflict_resolution_latency_p95` | Time from conflict detection to a defined resolution | > 24 hours |
| `order_dependent_outcome_count` | Requests where the final action outcome would differ had approver response order been reversed | > 0 (should be zero once resolution policy is enforced) |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Conflicting decisions detected | Two or more required approvers return different decisions on the same request | Critical | Block execution immediately, notify all approvers and governance owner, route to defined tie-breaker |
| Action executed on partial quorum | Action proceeds with fewer than the required number of recorded decisions | Critical | Halt and reverse if possible, audit the quorum-check logic |

## Related Patterns
- [Approval Chain Break](./approval-chain-break.md) - both involve multi-party approval state that isn't tracked as a coherent whole
- [Approval Authority Escalation Failure](./approval-authority-escalation-failure.md) - unresolved conflicts should escalate the same way authority mismatches should
- [Approval Delegation Loop](./approval-delegation-loop.md) - both arise from approval logic that wasn't designed for the non-happy-path case
