# Deadlock in Multi-Agent

## Issue
Two or more agents each hold a resource that another agent in the group needs, and each is waiting for the resource held by the next, forming a closed cycle of dependencies where no agent can proceed. Unlike a simple timeout or a single stuck agent, deadlock is a stable state — none of the agents involved will ever make progress on their own, because each is correctly waiting for something that will never be released, since the releaser is itself waiting.

**Frequency**: Occasional

**Symptoms**
- A set of agents that all show as "waiting" or "in progress" indefinitely, with no individual error or crash
- CPU/API usage for the stuck agents drops to near-zero while they remain "active" in orchestration dashboards
- Resource lock tables showing a cycle: Agent A holds lock 1 and waits on lock 2; Agent B holds lock 2 and waits on lock 1
- Tasks that were progressing normally suddenly stall completely with no throughput, requiring manual intervention to clear
- The same subset of agents recurring in stalls, correlated with a specific pair or set of shared resources

## Root Cause
Deadlock arises when agents acquire multiple shared resources without a consistent, system-wide ordering, and hold one resource while waiting for another. If Agent A's workflow acquires resource 1 then tries to acquire resource 2, while Agent B's workflow (running concurrently) acquires resource 2 then tries to acquire resource 1, the two acquisition orders can interleave into a cycle: A holds 1 and wants 2, B holds 2 and wants 1. Because neither agent is designed to detect this cycle or to release a resource it already holds while waiting, both simply block forever. This is the classic circular-wait condition from operating-systems theory, but it appears more easily in multi-agent systems because agent workflows are often composed dynamically (e.g. by an LLM planning which resources to acquire in what order) rather than written with a fixed, reviewed lock-ordering discipline.

## Example
```
A collaborative document-editing system has two agents that both need to
lock two shared sections of a document to perform cross-referencing edits.

Section-Sync Agent (processing doc changes top-down):
  1. Acquires lock on Section A (references)
  2. Attempts to acquire lock on Section B (appendix) to update a
     cross-reference -- blocks, because Section B is locked.

Appendix-Update Agent (processing doc changes bottom-up, running
concurrently on the same document):
  1. Acquires lock on Section B (appendix)
  2. Attempts to acquire lock on Section A (references) to update a
     citation -- blocks, because Section A is locked.

Both agents now hold one lock and wait on the other. Neither has any
mechanism to detect the cycle or back off. The document remains in a
"processing" state indefinitely. Twenty minutes later, a user trying to
open the document for editing is told it is "locked by another process"
and the on-call engineer has to manually kill both agent processes and
release the locks before edits can resume.
```

## Statistics
| Finding | Context |
|---------|---------|
| Deadlock incidents are less frequent than simple resource contention but tend to require manual intervention, unlike self-resolving contention | Typical qualitative finding across reported multi-agent operational reviews |
| Systems without consistent lock ordering are estimated to encounter deadlock in roughly 1 in several thousand to tens of thousands of concurrent multi-resource operations, rising sharply as the number of concurrently held resources per agent increases | Estimated from instrumented lock-acquisition logs |
| Adding timeout-based deadlock detection and automatic rollback reduces mean-time-to-recovery from deadlock by an estimated 90%+ compared to manual intervention | Reported range across teams that added automated detection |

## Mitigations
1. **Global lock ordering**: Require all agents to acquire multiple shared resources in a single, system-wide consistent order (e.g. always by resource ID ascending), which mathematically eliminates circular-wait conditions.
2. **Timeout-based deadlock detection and rollback**: Have each resource acquisition carry a timeout; when it fires, release any locks already held by that agent and retry the whole operation after a randomized delay, breaking the cycle.
3. **Wait-for graph monitoring**: Run a background process that periodically builds the current "agent waits for resource held by agent" graph and detects cycles directly, killing or rolling back one participant to break a detected cycle.
4. **Single-resource-at-a-time acquisition**: Where possible, redesign workflows so agents never need to hold more than one shared lock simultaneously, eliminating the precondition for deadlock entirely.
5. **Avoid dynamically-planned lock acquisition order**: When an LLM-driven planner decides what to lock and in what sequence, constrain it with a fixed acquisition-order policy rather than letting it choose resource order freely per task.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| agent_wait_duration_p99 | 99th percentile time an agent spends waiting to acquire a shared resource | Alert if > 5x expected task duration |
| detected_wait_cycles | Count of circular-wait cycles found by periodic wait-for graph analysis | Alert if > 0 |
| stalled_agent_count | Number of agents in "in progress" state with zero resource activity for an extended period | Alert if > 0 for more than 2 min |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Deadlock cycle detected | Wait-for graph analysis finds a closed cycle among active agents | High | Page on-call, auto-rollback and release locks for one cycle participant |
| Stalled agents with zero throughput | Multiple agents show "active" status but no resource or task progress for N minutes | High | Investigate for deadlock, manually inspect lock state |

## Related Patterns
- [Agent Priority Inversion](./agent-priority-inversion.md) - both involve resource holds blocking other agents, though inversion is priority-order-only and deadlock is a circular, unresolvable wait
- [Livelock in Multi-Agent](./livelock-in-multi-agent.md) - the "unstuck but never progressing" counterpart to deadlock's "fully stuck" state, often caused by naive deadlock-avoidance logic
- [Agent Resource Contention](./agent-resource-contention.md) - deadlock is the pathological extreme of unmanaged resource contention between agents
