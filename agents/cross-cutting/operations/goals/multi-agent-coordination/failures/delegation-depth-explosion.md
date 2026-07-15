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

## Mitigation Strategies

### Prevention
1. **Hard depth budget passed through the call chain**: The Tokyo weather example shows a simple lookup passed through 5 layers (L0-L4) purely because each agent's default behavior is "delegate" rather than "check if I can just do this." Attach a decrementing depth budget (e.g., start at 3) to the task at L0, and require any agent receiving budget=0 to execute directly or fail rather than delegate further — this caps the chain before it reaches L4-level absurdity. Trade-off: a hard cap can force a genuinely complex task to be handled by an under-equipped agent if the budget is set too low.
2. **Complexity-gated delegation instead of default-delegate**: "What's the weather in Tokyo?" is a single API call, yet every layer chose to delegate rather than execute — the stats confirm average production depth should be 2-3 levels, not 5. Require each agent to score task complexity (e.g., "does this need one tool call or multiple reasoning steps?") before delegating, and force direct execution for single-tool-call tasks like weather lookups. Trade-off: complexity scoring itself costs an LLM call and can be wrong, occasionally delegating something that should have been direct or vice versa.
3. **Circular-delegation guard via visited-agent set**: The "worse case" in the example — Agent A delegates to B, B delegates back to A — causes a hang/crash with no depth limit needed to trigger it. Attach a visited-agent-ID list to the task context and reject any delegation that would re-enter an agent already in the chain. Trade-off: requires every agent in the system to honor and propagate the visited-list faithfully; a non-compliant agent reintroduces the loop risk.

### Detection & Response
1. **Per-level latency accumulation tracking**: Since each delegation level in the example adds ~500ms (400-800ms per the stats) and the chain compounds to 5x direct latency, instrument each hop to log cumulative latency and flag any task exceeding 2x the direct-execution baseline latency for its task type.
2. **Token/cost multiplier monitor**: The example shows 8x token cost ($0.016 vs $0.002) purely from delegation overhead with zero added value (same answer, just re-narrated at each level). Track the ratio of total tokens consumed across the chain vs. tokens the final tool call itself required, and flag ratios above a threshold (e.g., >3x) as excessive delegation overhead.
3. **Context fidelity decay check**: The stats note 10-20% fidelity drop per level as "72°F, Sunny" gets re-narrated (L4→L3→L2→L1→L0). Sample final output against the ground-truth tool result and flag semantic drift (paraphrase divergence) beyond a threshold as a sign the chain is too deep for the content it's carrying.

### Architecture Patterns
1. **Supervisor with bounded delegation depth**: A single supervisor (L0) holds the depth budget and a registry of available direct-execution tools (like the weather API), so it can call the tool itself instead of delegating to a Research Agent that delegates to a Data Gathering Agent, etc. Deployment consideration: requires the supervisor to maintain an up-to-date tool/capability registry, or it will fall back to delegation anyway.
2. **Flat tool-calling instead of nested agent-to-agent delegation**: For tasks like the weather lookup that resolve to one API call, replace the L1-L4 agent hierarchy with direct tool access from L0 — i.e., treat "weather API" as a callable tool, not a sub-agent to delegate to. Deployment consideration: blurs the architectural line between "agent" and "tool," requiring clear guidelines on when a capability should be a tool vs. a full agent.
3. **Delegation ledger with loop detection**: Maintain an explicit, task-scoped ledger recording every delegation hop (who delegated to whom, at what depth) that is checked before each new delegation for depth-budget and cycle violations — directly preventing the "Agent A delegates to Agent B, Agent B delegates to Agent A" infinite loop. Deployment consideration: the ledger must be passed reliably through every hop; losing it mid-chain reopens the loop risk.

### Metrics
1. **avg_delegation_depth**: Target 2-3 levels (per observed production baseline); Alert if p95 exceeds 4 levels for any task category.
2. **delegation_overhead_ratio**: Target < 2x tokens/latency vs. direct execution baseline; Alert if > 5x (matching the example's 8x/5x blowup pattern).
3. **circular_delegation_rate**: Target 0% of tasks hitting a repeated agent ID in the delegation chain; Alert on any occurrence (P1, since this causes hangs per the 8% hang-rate stat).
4. **context_fidelity_at_final_hop**: Target > 90% semantic similarity between final output and ground-truth tool result; Alert if < 80%.

### Alerts
1. **Circular Delegation Detected** (P1): Condition - a delegation chain re-enters an agent ID already present in the visited-agent list. Action: immediately abort the chain, return an error to the originating caller, and log the full chain for debugging (matches the "system hangs or crashes" failure mode in the example).
2. **Depth Budget Exhausted** (P2): Condition - a task's delegation depth budget reaches 0 without task completion. Action: force the current agent to execute directly with available tools or return a "cannot complete without further delegation" response rather than silently continuing.
3. **Excessive Overhead Ratio** (P3): Condition - delegation_overhead_ratio for a completed task exceeds 5x the direct-execution baseline. Action: log for delegation-policy review; if recurring for the same task pattern, add a complexity-threshold rule to route that pattern to direct execution.

## References

- [MAST Taxonomy](https://arxiv.org/abs/2503.13657) - Multi-agent coordination failures
- [Augment Code: Multi-Agent Failures](https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them) - Delegation patterns
- [DEV.to: $47,000 Agent Loop](https://dev.to/waxell/the-47000-agent-loop-why-token-budget-alerts-arent-budget-enforcement-389i) - Runaway agents
- [Microsoft: Failure Modes in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Agent coordination
- [LeanOps: Token Cost Analysis](https://leanopstech.com/blog/agentic-ai-cost-runaway-token-budget-2026) - Cost patterns
