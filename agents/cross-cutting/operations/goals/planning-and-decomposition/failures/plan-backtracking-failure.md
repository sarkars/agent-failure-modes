# Plan Backtracking Failure

## Issue
When a branch of a plan fails or turns out to be a dead end, the agent needs to cleanly undo whatever partial side effects that branch caused and return to a known-good state before trying an alternative. Many agents lack this capability: they either can't identify which prior actions need to be reversed, leave partial side effects in place while proceeding down a new branch, or attempt an undo that itself only partially succeeds, leaving the system in a state that matches neither the old branch nor the new one.

**Frequency**: Common

**Symptoms**
- Partial side effects (a resource created, a record updated, a message sent) left behind from an abandoned plan branch
- The agent proceeding with an alternative approach while an earlier failed approach's effects are still active
- State left inconsistent — some fields updated per the old branch, others per the new one — after a backtrack
- No explicit "undo" or "rollback" step visible in the execution trace when a branch is abandoned
- Retried tasks that fail differently the second time because the first attempt's partial state wasn't cleaned up

## Root Cause
Backtracking requires the agent to know, for every action it takes, whether and how that action can be reversed — but most agent tool interfaces expose only a "do" operation, not a matching "undo," and even when an undo exists, the agent's plan representation rarely tracks which actions are reversible versus destructive. Without a structured record of what's been done and how to reverse each one, an agent that decides a branch has failed can only proceed forward from where it is, either ignoring the stale side effects or attempting an ad hoc cleanup that's improvised rather than paired to the specific actions taken. This is compounded when actions are irreversible (an email sent, a payment initiated) — true backtracking is impossible there, but agents often don't distinguish reversible from irreversible actions up front, so they don't know which branches are safe to explore speculatively at all.

## Example
```
A project-setup agent is asked to provision a new client workspace,
tries Configuration A first (a shared team structure), finds partway
through that the client's plan tier doesn't support it, and switches to
Configuration B (an isolated structure) instead.

Configuration A steps taken before the failure was detected:
  1. Created team "client-acme" (succeeded)
  2. Created 3 shared channels under that team (succeeded)
  3. Invited 5 users to the shared channels (succeeded)
  4. Attempted to enable cross-project shared billing (FAILED -- not
     supported on the client's Starter tier)

The agent detects the failure at step 4 and decides to switch to
Configuration B, which creates a separate isolated workspace per project.
It has no record marking steps 1-3 as "belonging to the abandoned
Configuration A branch, should be undone." It proceeds directly into
Configuration B's steps without reversing anything.

Result: the client ends up with both the abandoned shared team
"client-acme" (with 3 channels and 5 invited users still active) AND the
new isolated Configuration B workspace, doubling their user invites and
confusing the client about which workspace to actually use -- discovered
only when the client asks support why they got two invitation emails.
```

## Statistics
| Finding | Context |
|---------|---------|
| Abandoned-branch side effects are estimated to persist uncleaned in a meaningful share of multi-step agent executions that switch strategies mid-task | Typical range observed in agent execution trace reviews |
| Tool integrations exposing an explicit inverse/undo operation are reported to be a minority of all tool integrations in typical agent toolkits, leaving most actions effectively non-backtrackable by default | Estimated from surveys of common agent tool-calling frameworks |
| Adding explicit action-reversibility tagging and automatic rollback on branch abandonment is reported to substantially reduce leftover side-effect incidents | Reported range across teams that added structured undo tracking |

## Mitigations
1. **Reversibility tagging per action**: Have the planner classify every action as reversible (with a known undo operation), irreversible, or unknown before executing it, and use this to decide whether a branch can be safely abandoned versus committed to.
2. **Transactional action logging**: Maintain an explicit log of every side-effecting action taken within a branch, paired with its inverse operation where one exists, so abandoning the branch can trigger an automatic, ordered rollback.
3. **Checkpoint-and-restore for exploratory branches**: For tasks involving genuine uncertainty about which approach will work, snapshot state before beginning a speculative branch and support restoring to that snapshot cleanly if the branch is abandoned.
4. **Escalate before irreversible-branch abandonment**: When a branch contains irreversible actions and needs to be abandoned, surface this to a human rather than silently proceeding to an alternative that will leave the irreversible effects stranded.
5. **Post-backtrack state verification**: After a rollback or branch switch, explicitly verify the resulting state matches expectations (no orphaned resources, no half-applied changes) rather than assuming the rollback succeeded.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| orphaned_side_effect_count | Resources or records created by an abandoned plan branch that were never cleaned up | Alert if > 0 |
| rollback_failure_rate | Fraction of attempted rollbacks that don't fully restore the pre-branch state | Alert if > 5% |
| branch_switch_without_cleanup_rate | Fraction of branch abandonments with no corresponding cleanup action in the execution trace | Alert if > 10% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Branch abandoned with unreversed side effects | Agent switches strategy mid-task while a prior branch's actions remain uncleaned | High | Page on-call, manually audit and clean up orphaned resources |
| Irreversible action stranded by abandoned branch | An irreversible action (message sent, payment made) is part of a branch the agent abandoned | High | Immediate human review, may require external correction (refund, follow-up message) |

## Related Patterns
- [Contingency Plan Missing](./contingency-plan-missing.md) - a plan without a defined fallback is also unlikely to have a defined rollback for the path it's abandoning
- [Plan Adaptability Failure](./plan-adaptability-failure.md) - adapting a plan to new information often requires exactly the backtracking capability this pattern describes
- [Plan Dependency Cycle](./plan-dependency-cycle.md) - both concern the structural integrity of a plan's step relationships, one during execution failure and one before execution even begins
