# Recovery Divergence

## Issue
A single instance that recovers from a failure — restarting after a crash, restoring from a snapshot, resuming from a checkpoint — ends up in a state that differs from what its pre-failure state actually was, even though the recovery process completes without error and reports success. This is the single-instance version of the problem (as opposed to cascade-divergent-recovery, which is about multiple components recovering into mutually inconsistent states relative to each other): here, the concern is purely whether the one recovered instance matches its own prior true state, regardless of what any other component believes.

**Frequency**: Occasional

**Symptoms**
- The recovered instance's data or in-memory state does not match what it was known to be immediately before the failure, based on external records (logs, audit trails, user reports)
- Recovery completes without any error and passes health checks, but downstream behavior changes subtly after the restart (different recommendations, different computed values, missing recent context)
- Users or clients notice "the agent forgot" something it clearly knew moments before the crash
- A gap exists between the instance's last durable checkpoint and the actual moment of failure, and whatever happened in that gap is simply absent post-recovery rather than reconciled

## Root Cause
Recovery mechanisms restore an instance to its last durable checkpoint, not to its actual pre-failure state — anything that happened between the checkpoint and the failure (in-memory state that hadn't yet been persisted, a request that was being processed but not yet committed, a cache entry populated from an external call that isn't itself replayed) is simply gone, and the recovered instance has no way to know it's missing anything, because from its own internal perspective it looks perfectly consistent. Divergence becomes especially likely for agentic systems that maintain rich in-memory conversational or planning state which is checkpointed only periodically or on a coarse interval, so a crash between checkpoints can silently erase a meaningful amount of recent context, reasoning, or partially-completed multi-step work that the agent (and any external observer) has no record ever happened.

## Example
```
09:00:00 - A research agent begins a 12-step investigation task,
           maintaining its plan, intermediate findings, and tool-call
           history in memory. It checkpoints its full state to durable
           storage every 5 minutes.

09:04:30 - Last checkpoint before the incident: agent has completed
           steps 1-6 and recorded findings from 6 tool calls.

09:04:31 - 09:06:50 - Agent continues working in memory: completes
           steps 7-9, makes 3 more tool calls (including one that costs
           $4.50 and takes 90 seconds), and revises its plan to skip
           step 10 based on a finding from step 8.

09:06:51 - Host crashes (out-of-memory kill from an unrelated process).

09:07:10 - Orchestrator restarts the agent, which loads its last
           checkpoint from 09:04:30 — state reflecting only steps 1-6.

09:07:11 - The recovered agent, with no record of ever reaching step 7,
           resumes execution from step 7 as if for the first time. It
           re-runs the $4.50 tool call from before (redundant cost), and
           because it never made the revision to skip step 10, it goes
           on to execute step 10 anyway — a step whose output actively
           contradicts a step-8 finding that existed only in the lost
           in-memory state.

09:15:00 - The final report presented to the user contains an internal
           contradiction between two sections, traceable to the agent
           "forgetting" its own mid-task revision due to checkpoint gap
           recovery divergence.
```

## Statistics
| Finding | Context |
|---------|---------|
| Checkpoint-interval gaps of several minutes are common in long-running agent workflows, and any work in that window is lost on crash-recovery | Typical range observed in periodic (non-continuous) checkpointing designs |
| Recovery divergence incidents in agentic systems are more likely to be self-consistent (masking themselves) than in stateless transactional systems, so detection rates are lower | Estimated from comparison of agent vs. transactional recovery incident reports |
| Shortening checkpoint intervals or moving to continuous/event-sourced checkpointing is reported to substantially reduce the average amount of unrecoverable in-flight state | Reported range across teams that reduced checkpoint intervals |

## Mitigations
1. **Finer-grained or continuous checkpointing**: Reduce the checkpoint interval, or move to event-sourced/write-ahead logging of state changes as they happen rather than periodic full-state snapshots, to shrink the window of unrecoverable in-flight work.
2. **External record cross-verification on recovery**: Have the recovered instance compare its restored state against external, independently-durable records (an audit log, a tool-call ledger) to detect and flag gaps rather than silently resuming as if nothing happened.
3. **Explicit "recovered from gap" signaling**: When an instance restores from a checkpoint known to predate the failure by more than a defined threshold, surface this explicitly (to users, to downstream consumers, or to a supervising process) rather than resuming silently as if state is complete.
4. **In-flight work journaling separate from state checkpoints**: Maintain a lightweight, low-latency journal of in-progress work (distinct from the heavier periodic state checkpoint) that can be replayed on recovery to reconstruct recent context even if the full state snapshot is stale.
5. **Post-recovery consistency self-check**: Have the recovered instance run a sanity pass over its own restored state, checking for known-fragile properties (plan consistency, no orphaned partial steps) before resuming normal operation.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| checkpoint_to_failure_gap | Time between last durable checkpoint and detected failure | Alert if > defined threshold for the workload |
| post_recovery_redundant_action_count | Count of actions re-executed after recovery that had already completed before the failure | Alert if > 0 for costly/side-effecting actions |
| post_recovery_consistency_check_failures | Count of internal consistency violations detected in restored state | Alert if > 0 |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Large checkpoint gap on recovery | checkpoint_to_failure_gap exceeds threshold for a recovered instance | Medium | Flag recovered session as potentially incomplete, notify downstream consumers or users |
| Redundant costly action re-executed | A recovered instance repeats a side-effecting or costly action already completed pre-failure | High | Add idempotency guard, investigate checkpoint granularity |

## Related Patterns
- [Cascade Divergent Recovery](./cascade-divergent-recovery.md) - the multi-component version of this same underlying gap-between-checkpoint-and-failure mechanism
- [Recovery Ordering Violation](./recovery-ordering-violation.md) - both concern the recovered state not matching pre-failure reality, one via lost work, the other via misordered replay
- [Recovery Point Objective Miss](./recovery-point-objective-miss.md) - the checkpoint-to-failure gap that causes divergence is exactly the quantity RPO is meant to bound
