# Token Explosion

## Issue: Exponential Token Usage Growth

**Frequency**: Common

**Symptoms**
- Token usage grows exponentially across conversation turns
- Context window fills rapidly
- Costs far exceed estimates
- Agent becomes slower as context grows

**Root Cause**
Several patterns cause token counts to explode:
- Accumulating full conversation history without summarization
- Including verbose tool outputs in context
- Repeatedly passing large documents
- Multi-agent handoffs duplicating context
- Chain-of-thought reasoning generating excessive tokens

**Example**
```
Turn 1: 1,000 tokens
Turn 2: 2,500 tokens (includes turn 1)
Turn 3: 5,000 tokens (includes turns 1-2)
Turn 4: 10,000 tokens
Turn 5: Context window exceeded

Result: Quadratic growth instead of linear
```

**Mitigation Strategies**
1. **Context summarization**: Compress history periodically
2. **Selective context**: Only include relevant prior turns
3. **Tool output truncation**: Summarize or trim large outputs
4. **Reference by ID**: Don't repeat full documents, reference them
5. **Token budgets per turn**: Limit input/output tokens
6. **Sliding window**: Keep only recent N turns in context

**Detection**
- Track tokens per turn over conversation
- Alert on growth rate exceeding threshold
- Monitor context utilization percentage
- Compare actual vs. expected token usage

---

## References

- [LeanOps: Agents Burn 50x More Tokens](https://leanopstech.com/blog/agentic-ai-cost-runaway-token-budget-2026/) - Analysis of token consumption patterns in agentic AI
- [AWS: 3 Agent Failure Modes](https://dev.to/aws/why-ai-agents-fail-3-failure-modes-that-cost-you-tokens-and-time-1flb) - Common failure patterns including token explosion
