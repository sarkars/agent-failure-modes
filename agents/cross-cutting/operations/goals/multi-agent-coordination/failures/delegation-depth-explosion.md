# Delegation Depth Explosion

## Issue: Agents Delegate to Sub-Agents Creating Unbounded Depth

**Frequency**: Occasional

**Symptoms**
- Task passes through many agent layers
- Context diluted at each delegation level
- Latency compounds with each delegation
- Token costs multiply per delegation
- Original intent lost in delegation chain

**Root Cause**
Agents that can spawn or delegate to other agents may create deep delegation chains. Each level adds latency, token overhead, and potential for context loss. A simple task that could be handled directly gets delegated through 5+ layers, each agent adding its overhead. Without depth limits, delegation can spiral into unbounded recursion.

**Example**
```
Scenario: Research agent with delegation capability

User query: "What's the weather in Tokyo?"

Agent delegation chain:
  L0: Main Agent
      "I'll delegate this to my research agent"
      
  L1: Research Agent  
      "I'll delegate this to my data gathering agent"
      
  L2: Data Gathering Agent
      "I'll delegate this to my API specialist agent"
      
  L3: API Specialist Agent
      "I'll delegate this to my weather API agent"
      
  L4: Weather API Agent
      Finally calls weather API
      Returns: "72°F, Sunny"
      
  L4→L3: "The weather API reports 72°F, Sunny in Tokyo"
  L3→L2: "My API specialist found it's 72°F and Sunny"
  L2→L1: "Data gathering confirms 72°F, Sunny weather"
  L1→L0: "Research indicates Tokyo is 72°F and Sunny"
  L0→User: "Based on my research, Tokyo is 72°F and Sunny"

Cost analysis:
  Direct call: 1 API call + 1 LLM call
  With delegation: 1 API call + 10 LLM calls (2 per level)
  
  Latency: 5x (each level adds ~500ms)
  Tokens: 8x (context passed up and down)
  Cost: $0.002 vs $0.016

Worse case: Infinite delegation
  Agent A delegates to Agent B
  Agent B delegates to Agent A
  System hangs or crashes
```

**Key Statistics**
From Delegation Research (2026):
- Average delegation depth in production: 2-3 levels
- Each delegation level adds 400-800ms latency
- Token overhead per level: 150-300 tokens
- Delegation loops cause 8% of agent hangs
- Context fidelity drops 10-20% per level

**Delegation Problems**
| Problem | Cause | Impact |
|---------|-------|--------|
| Deep chains | No depth limit | High latency/cost |
| Circular delegation | A→B→A | Infinite loop |
| Context loss | Summarization at each level | Wrong output |
| Over-delegation | Simple tasks delegated | Waste |
| Accountability loss | "Who did what?" unclear | Debug difficulty |

**Contributing Factors**
- No delegation depth limits
- Agents optimized to delegate
- No task complexity assessment
- Missing delegation tracking
- No direct execution preference
- Recursive agent architectures

**Mitigation Strategies**
1. **Depth limits**: Hard cap on delegation depth (e.g., max 3)
2. **Complexity threshold**: Only delegate complex tasks
3. **Direct execution bias**: Prefer handling directly when capable
4. **Delegation tracking**: Track full delegation chain
5. **Loop detection**: Prevent circular delegation
6. **Cost-aware delegation**: Consider overhead before delegating

**Detection**
- Monitor delegation depth per task
- Track latency vs. delegation depth
- Alert on circular delegation patterns
- Compare direct vs. delegated execution costs
- Audit delegation decisions

## References

- [MAST Taxonomy](https://arxiv.org/abs/2503.13657) - Multi-agent coordination failures
- [Augment Code: Multi-Agent Failures](https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them) - Delegation patterns
- [DEV.to: $47,000 Agent Loop](https://dev.to/waxell/the-47000-agent-loop-why-token-budget-alerts-arent-budget-enforcement-389i) - Runaway agents
- [Microsoft: Failure Modes in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Agent coordination
- [LeanOps: Token Cost Analysis](https://leanopstech.com/blog/agentic-ai-cost-runaway-token-budget-2026) - Cost patterns
