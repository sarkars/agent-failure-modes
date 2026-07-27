# What Are the Most Common Multi-Agent Coordination Failures in AI Systems?

**Multi-agent AI systems fail to coordinate because the system-design layer — who owns which decision, how messages are validated at handoffs, and how disagreement gets resolved — is left implicit, so agents fall back on ad hoc behavior that breaks silently under real workloads.** All 15 coordination patterns here trace back to the same taxonomy (MAST — Cemri et al., arXiv:2503.13657) of multi-agent system failures spanning specification gaps, inter-agent misalignment, and task-verification weaknesses. The shared consequence is that a multi-agent pipeline can pass every single-agent test and still fail once agents actually have to coordinate.

## Key Takeaways

- 15 distinct coordination failure patterns are documented here, all citing the MAST taxonomy as their reference framework for multi-agent system failure.
- 9 of the 15 patterns are rated "Common," 5 are "Occasional," and 1 (Cascading Error) is rated "Rare but Catastrophic" — coordination failures are frequent, not edge cases.
- Every pattern shares the same three-part mitigation architecture: handoff schema validation with type checking, distributed consensus checkpoints at agent-to-agent transitions, and a saga pattern with compensating actions for error isolation.
- The patterns split into three mechanism clusters: authority/role design gaps (3 patterns), communication and handoff breakdowns (7 patterns), and verification/convergence failures (5 patterns).

## Scope

- **Authority & Role Design** — [Authority Confusion](failures/authority-confusion.md), [Role Ambiguity](failures/role-ambiguity.md), [Coordinator Failure](failures/coordinator-failure.md). Authority Confusion, Role Ambiguity, and Coordinator Failure share a root cause at the specification layer: the system was never told which agent's output wins, who owns which responsibility, or how a manager agent should assign and synthesize subtasks.
- **Communication & Handoff Breakdown** — [Communication Loss](failures/communication-loss.md), [Message Misinterpretation](failures/message-misinterpretation.md), [Task Handoff Failure](failures/task-handoff-failure.md), [Contradictory Outputs](failures/contradictory-outputs.md), [Duplicate Work](failures/duplicate-work.md), [Worker Tunnel Vision](failures/worker-tunnel-vision.md), [Emergent Behavior](failures/emergent-behavior.md). The seven patterns above describe information or intent that fails to survive the boundary between agents — dropped context, misread output, unresolved conflict, redundant effort, or local optimization that undermines the global task.
- **Verification & Convergence Failure** — [Consensus Illusion](failures/consensus-illusion.md), [Premature Consensus](failures/premature-consensus.md), [Infinite Debate](failures/infinite-debate.md), [Verifier-Agent Weakness](failures/verifier-agent-weakness.md), [Cascading Error](failures/cascading-error.md). The five verification-and-convergence patterns describe a multi-agent system's mechanisms for reaching or checking a conclusion breaking down — agents converge for the wrong reasons, never converge at all, or a verifier fails to catch what it was built to catch.

## When Coordination Matters

- A pipeline assigns different subtasks to different agents (a manager/worker split, a pipeline of specialist agents, or a debate/critique loop) and no single agent has visibility into the whole task
- A multi-agent trace fails in production despite every individual agent passing its own isolated test — the classic signature of an interaction-level rather than component-level failure
- A system relies on agent agreement (consensus, voting, a verifier's sign-off) as its correctness signal, and needs to know whether that signal can be trusted

## Cross-Pattern Insight

All 15 coordination patterns point to the same underlying gap: multi-agent systems are usually built by getting each agent to work, then wiring the agents together, with no equivalent investment in the wiring itself. The documented mitigation is consistent across every pattern regardless of cluster: validate handoffs against an explicit schema before forwarding, checkpoint world-model state at agent-to-agent transitions so divergence is caught early rather than discovered downstream, and structure the workflow as a saga with compensating actions so a single agent's error doesn't corrupt global state. None of the documented mitigations are agent-capability fixes — the mitigations are coordination-layer infrastructure that has to exist independently of how good any individual agent is.

## Frequently Asked Questions

### What's the difference between coordination failures and error propagation in multi-agent systems?
Coordination failures cover the breadth of ways agents fail to work together — authority, roles, communication, consensus. [Error Propagation](../error-propagation/) covers one specific mechanism in depth: how a single upstream error compounds exponentially through a sequential pipeline, with measured amplification factors. Cascading Error in coordination is the same conceptual failure at stub depth; Error Propagation's pattern documents it with worked examples and statistics.

### How can multi-agent systems fail even when every individual agent passes its own tests?
Because the failure lives in the interaction, not in any single agent — see [Emergent Behavior](failures/emergent-behavior.md). Agents that behave correctly in isolation can still produce a broken system when their outputs, timing, or assumptions interact in ways no single-agent test exercises.

### Can a stronger verifier or judge agent fix consensus-illusion and premature-consensus failures?
Not by itself. [Verifier-Agent Weakness](failures/verifier-agent-weakness.md) documents that a judge agent can fail to catch worker-agent errors for the same reason the workers made the errors — shared blind spots, insufficient independence, or no access to ground truth the workers lacked. A verifier adds value only when it has a genuinely independent check, not just another model instance reviewing the same evidence.

### Is authority confusion the same problem as role ambiguity?
They're related but distinct. [Role Ambiguity](failures/role-ambiguity.md) is about agents not knowing who is responsible for which subtask (leading to duplicate or missing work). [Authority Confusion](failures/authority-confusion.md) is about agents each producing an output and the system having no rule for which one wins when they conflict. A system can have clear roles but still lack authority rules, or vice versa.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Authority Confusion](failures/authority-confusion.md) | System has no rule for which agent's output wins when outputs conflict |
| [Cascading Error](failures/cascading-error.md) | An early agent's error propagates and is amplified by every downstream agent in the pipeline |
| [Communication Loss](failures/communication-loss.md) | Key information present in one agent's trace never reaches another agent that needs it |
| [Consensus Illusion](failures/consensus-illusion.md) | Agents agree because they share the same flawed context or bias, not because the answer is correct |
| [Contradictory Outputs](failures/contradictory-outputs.md) | Agents produce conflicting recommendations and no arbitration mechanism exists |
| [Coordinator Failure](failures/coordinator-failure.md) | A manager agent assigns subtasks poorly or fails to synthesize worker outputs into a coherent result |
| [Duplicate Work](failures/duplicate-work.md) | Multiple agents independently solve the same subtask, wasting effort or producing conflicting versions |
| [Emergent Behavior](failures/emergent-behavior.md) | Agent interaction produces a failure mode not observed when any agent is tested in isolation |
| [Infinite Debate](failures/infinite-debate.md) | Agents critique and revise each other's output endlessly without a termination condition |
| [Message Misinterpretation](failures/message-misinterpretation.md) | One agent misreads another agent's output, and downstream action contradicts the upstream result |
| [Premature Consensus](failures/premature-consensus.md) | Agents converge on an answer before the evidence needed to support that answer has actually been checked |
| [Role Ambiguity](failures/role-ambiguity.md) | Agents don't know who owns which responsibility, causing duplicate or missing work |
| [Task Handoff Failure](failures/task-handoff-failure.md) | One agent passes incomplete or incorrect state to the next agent in the workflow |
| [Verifier-Agent Weakness](failures/verifier-agent-weakness.md) | A judge/verifier agent approves a trace that a worker agent got wrong |
| [Worker Tunnel Vision](failures/worker-tunnel-vision.md) | A specialized agent optimizes its own local subtask goal at the expense of overall task success |

**Total: 15 patterns**

## Related Goals

- [Error Propagation](../error-propagation/) — the sequential-amplification mechanism behind coordination's Cascading Error pattern, documented in full depth with measured amplification factors
- [Handoff Reliability](../handoff-reliability/) — a specific, narrower failure of the handoff mechanism coordination's Task Handoff Failure and Communication Loss patterns describe more broadly
- [Reasoning Quality](../reasoning-quality/) — why agreement among agents (the signal coordination's Consensus Illusion and Premature Consensus patterns question) doesn't guarantee correctness
