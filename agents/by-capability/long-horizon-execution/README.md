# Long-Horizon Planning & Execution

Failures in multi-step, multi-turn autonomous workflows where compounding errors accumulate over hours or days.

## Goals

| Goal | Description | Patterns |
|------|-------------|----------|
| [World State Divergence](goals/world-state-divergence/) | Agent's model of world diverges from reality | In progress |
| [Goal Memory Loss](goals/goal-memory-loss/) | Original objective forgotten mid-workflow | In progress |
| [Cascading Errors](goals/cascading-errors/) | Small errors amplify exponentially through steps | In progress |

**Status**: ~30 patterns planned

## Key Challenges

1. **Reality Divergence**: Assumptions made at step 1 violated by step 50
2. **Context Truncation**: Original goal drops from context over long conversations
3. **Error Amplification**: Hallucination in step 2 corrupts all downstream steps
4. **Resource Exhaustion**: Token budgets, API quotas, loop termination
5. **Cross-Agent Desynchronization**: Multiple agents pursuing conflicting assumptions
