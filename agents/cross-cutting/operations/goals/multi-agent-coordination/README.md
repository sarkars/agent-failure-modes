# Multi-Agent Coordination Failures: Handoff Errors, Routing Mistakes, and Delegation Loops

**Multi-agent coordination failures happen when agents working together lose information, pursue conflicting goals, get routed wrong, or never agree when to stop.** Ten patterns cover communication, delegation, routing, and termination.

## Key Takeaways

- Handoffs can lose or duplicate work, and messages between agents can be lost or corrupted.
- Ambiguous role specifications make agents interpret their jobs differently.
- Central orchestrators become chokepoints, and delegation can grow without a depth limit.
- Agents need a clear signal for when to stop and how to resolve disagreement.

## Patterns

| Pattern | What goes wrong |
|---|---|
| [Agent Misalignment](failures/agent-misalignment.md) | Agents Pursue Conflicting Objectives |
| [Communication Breakdown](failures/communication-breakdown.md) | Information Lost or Corrupted Between Agents |
| [Consensus Deadlock](failures/consensus-deadlock.md) | Multi-Agent Voting or Agreement Fails to Resolve |
| [Delegation Depth Explosion](failures/delegation-depth-explosion.md) | Agents Delegate to Sub-Agents Creating Unbounded Depth |
| [Orchestrator Bottleneck](failures/orchestrator-bottleneck.md) | Central Orchestrator Becomes System Chokepoint |
| [Parallel Execution Failures](failures/parallel-execution-failures.md) | Agents Operating in Parallel Cause Conflicts or Inconsistencies |
| [Routing Failures](failures/routing-failures.md) | Orchestrator Routes Task to Wrong Agent |
| [Specification Ambiguity Causing Multi-Agent Role Misalignment](failures/specification-ambiguity-causing-misalignment.md) | Ambiguous Blueprint Specifications Cause Agents to Interpret Roles Differently |
| [Task Handoff Errors](failures/task-handoff-errors.md) | Work Lost or Duplicated During Agent Transitions |
| [Termination Condition Unawareness](failures/termination-unawareness.md) | Agent Doesn't Know When to Stop |

**Total: 10 patterns**

## How These Patterns Group

- **Roles and goals:** Agent Misalignment, Specification Ambiguity Causing Multi-Agent Role Misalignment
- **Communication and handoffs:** Communication Breakdown, Task Handoff Errors, Routing Failures
- **Structure and scale:** Orchestrator Bottleneck, Delegation Depth Explosion, Parallel Execution Failures
- **Agreement and stopping:** Consensus Deadlock, Termination Condition Unawareness

## When This Matters

- More than one agent works on the same task
- An orchestrator routes work to specialists
- Agents delegate to other agents

## Frequently Asked Questions

### Why do my agents lose information when passing work to each other?

See task handoff errors and communication breakdown.

### How do I stop agents from delegating endlessly?

See delegation depth explosion.

### Why does the wrong agent get my task?

See routing failures.

### How do agents know when to stop?

See termination unawareness.

## Related

- [All operations goals](../)
- [Operations overview](../../)
