# Model Selection Waste

## Issue: Using Expensive Models When Cheaper Alternatives Suffice

**Frequency**: Very Common

**Symptoms**
- All requests routed to most capable (expensive) model
- Simple tasks use frontier models
- No model tiering based on task complexity
- Cost increases without quality improvement
- Latency higher than necessary for simple tasks

**Root Cause**
Organizations default to using the most capable model for all requests, either due to lack of routing logic, fear of quality degradation, or inability to classify task complexity. A simple "What time is it?" query gets processed by a $15/million token model when a $0.25/million token model would suffice. Without model routing, costs scale linearly with usage regardless of task requirements.

**Example**
```
Scenario: Customer support agent handling mixed queries

Query distribution (1M queries/month):
  Simple (FAQ, status): 60% - "What's your return policy?"
  Medium (lookup, calc): 30% - "Calculate shipping for order #123"
  Complex (reasoning): 10% - "Help me decide between products"

Without model routing:
  All queries → GPT-4o ($5/1M input)
  Monthly cost: $5,000

With intelligent routing:
  Simple → GPT-4o-mini ($0.15/1M)   = $90
  Medium → GPT-4o-mini ($0.15/1M)   = $45
  Complex → GPT-4o ($5/1M)          = $500
  Monthly cost: $635

Waste: $4,365/month (87% overspend)

Quality impact: None measurable
  - Simple queries: Same accuracy
  - Medium queries: Same accuracy  
  - Complex queries: Appropriate model used
```

**Key Statistics**
From Cost Analysis Research (2026):
- 70-80% of agent queries can be handled by smaller models
- Model routing reduces costs by 60-90% with <2% quality loss
- Only 15% of organizations implement model tiering
- Average overspend from no routing: $0.003-0.01 per query
- Frontier model costs 20-100x more than capable alternatives

**Cost Comparison (2026)**
| Model | Input/1M | Output/1M | Best For |
|-------|----------|-----------|----------|
| GPT-4o | $5.00 | $15.00 | Complex reasoning |
| Claude Opus | $15.00 | $75.00 | Nuanced analysis |
| GPT-4o-mini | $0.15 | $0.60 | Most tasks |
| Claude Haiku | $0.25 | $1.25 | Simple tasks |

**Contributing Factors**
- "One model fits all" architecture
- No task complexity classifier
- Fear of quality degradation
- Lack of A/B testing infrastructure
- No cost visibility per query type

**Mitigation Strategies**
1. **Model routing**: Classify tasks and route to appropriate model
2. **Complexity scoring**: Score query complexity before model selection
3. **Cascade approach**: Start with cheap model, escalate if needed
4. **A/B testing**: Validate quality on cheaper models
5. **Cost dashboards**: Track cost per query type
6. **Quality gates**: Define minimum quality thresholds per task type

**Detection**
- Compare cost distribution across query types
- Measure quality difference between model tiers
- Track queries where expensive model adds no value
- Monitor cost per successful completion
- Audit model selection decisions

## References

- [OpenAI: Model Pricing](https://openai.com/api/pricing/) - Current model costs
- [Anthropic: Claude Pricing](https://www.anthropic.com/pricing) - Claude model tiers
- [LeanOps: Agents Burn 50x More Tokens](https://leanopstech.com/blog/agentic-ai-cost-runaway-token-budget-2026) - Cost analysis
- [MindStudio: Token Budget Management](https://www.mindstudio.ai/blog/ai-agent-token-budget-management-claude-code) - Cost optimization
- [Portal26: Agentic Token Controls](https://siliconangle.com/2026/04/23/portal26-launches-agentic-token-controls-cap-runaway-ai-agent-spend/) - Cost control tools
