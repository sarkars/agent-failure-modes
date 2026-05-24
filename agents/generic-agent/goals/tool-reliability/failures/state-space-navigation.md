# State-Space Navigation Failure

## Issue: Agent Fails to Discover Required Information

**Frequency**: Common

**Symptoms**
- Agent completes task with incomplete information
- Required data exists but agent didn't find it
- Agent makes decisions based on partial state
- Task fails due to missing context

**Root Cause**
Agent fails to navigate the environment to retrieve all necessary data required to complete the task. The agent doesn't explore enough of the state space, missing critical information that exists but requires additional tool calls to discover.

**Example**
```
Task: "Find the cheapest flight from NYC to LA for tomorrow"

Environment state:
- Direct flights: $450 (American), $380 (Delta)
- Connecting flights: $290 (United via Denver)

Agent behavior:
1. Calls search_direct_flights("NYC", "LA")
2. Gets: American $450, Delta $380
3. Returns: "Delta at $380 is cheapest"

Missed: Agent never called search_connecting_flights()
        Actual cheapest: United $290

Result: Incorrect answer due to incomplete exploration
```

**Key Statistics**
From Aegis study of 142 failed agent traces:
- Exploration failures are a major category of agent-environment interaction failures
- State-space navigation failures occur when agents prematurely conclude exploration

**Contributing Factors**
- Agent assumes current results are exhaustive
- Tool descriptions don't indicate additional data sources
- Large state spaces with many exploration paths
- Lack of environment observability

**Mitigation Strategies**
1. **Environment lookahead**: Show agent preview of available data
2. **Completeness signals**: Indicate when more data exists
3. **Exploration prompts**: Encourage exhaustive search
4. **Tool bundling**: Group related discovery tools
5. **State space hints**: Indicate unexplored regions

**Detection**
- Task results missing obvious relevant data
- Tool call patterns showing incomplete exploration
- Comparison of agent path vs. ideal exploration path
- User corrections indicating missed information

## References

- [Aegis: Agent-Environment Failures](https://arxiv.org/abs/2508.19504) - State-space navigation as exploration failure mode
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Task verification failures
- [AWS: 3 Agent Failure Modes](https://dev.to/aws/why-ai-agents-fail-3-failure-modes-that-cost-you-tokens-and-time-1flb) - Incomplete exploration patterns
