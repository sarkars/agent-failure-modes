# Multi-Agent Coordination

Failures that occur when multiple agents work together, including communication breakdowns, task handoff errors, and consensus failures.

## Failure Patterns

| Pattern | Frequency | Description |
|---------|-----------|-------------|
| [Agent Misalignment](failures/agent-misalignment.md) | Common | Agents pursue conflicting or divergent objectives |
| [Communication Breakdown](failures/communication-breakdown.md) | Common | Information lost or corrupted between agents |
| [Task Handoff Errors](failures/task-handoff-errors.md) | Common | Work lost or duplicated during agent transitions |
| [Consensus Deadlock](failures/consensus-deadlock.md) | Occasional | Multi-agent voting or consensus fails to resolve |
| [Termination Unawareness](failures/termination-unawareness.md) | Common | Agent doesn't know when to stop (12.4% of MAS failures) |
| [Routing Failures](failures/routing-failures.md) | Common | Orchestrator routes task to wrong agent |
| [Orchestrator Bottleneck](failures/orchestrator-bottleneck.md) | Occasional | Central orchestrator becomes system chokepoint |
| [Delegation Depth Explosion](failures/delegation-depth-explosion.md) | Occasional | Agents delegate creating unbounded depth |
| [Parallel Execution Failures](failures/parallel-execution-failures.md) | Common | Parallel agents cause conflicts or inconsistencies |

## Key Statistics

- Multi-agent systems fail at 41-86.7% rates on complex tasks (MAST Taxonomy)
- Inter-agent misalignment accounts for significant portion of MAS failures
- Communication overhead grows O(n^2) with agent count
- 25-35% of tasks routed to suboptimal agent (Routing Research)
- 35% of parallel multi-agent tasks have coordination issues

## Common Causes

1. **Inconsistent objectives**: Agents optimizing for different goals
2. **State synchronization**: Agents have different views of world state
3. **Protocol violations**: Agents don't follow expected communication patterns
4. **Trust assumptions**: Agents incorrectly trust other agents' outputs

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [Microsoft: Taxonomy of Failure Mode in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf)
- [Redis: Why Multi-Agent LLM Systems Fail](https://redis.io/blog/why-multi-agent-llm-systems-fail/)
