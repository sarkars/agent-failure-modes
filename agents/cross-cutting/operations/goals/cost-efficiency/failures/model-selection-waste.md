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

## Mitigation Strategies

### Prevention
1. **Complexity-scored model routing**: Since the root cause is defaulting all requests to the most capable model absent a task-complexity classifier, score each incoming query (e.g., "What's your return policy?" vs. "Help me decide between products") and route the 60% Simple / 30% Medium tier to GPT-4o-mini/Claude Haiku class models, reserving frontier models for the 10% Complex tier as in the example's routing table. Trade-off: the complexity scorer itself must run on every request, adding a small fixed cost/latency that eats into savings if not kept lightweight.
2. **Cascade with escalation instead of static tiering**: Rather than a one-shot classify-then-route decision, start every query on the cheap model and escalate to the expensive model only when the cheap model's response confidence is low or it explicitly signals inability, reducing misrouting risk versus a purely upfront classifier. Trade-off: cascades add latency for escalated queries (two calls instead of one) and require the cheap model to reliably signal low confidence.
3. **Per-query-type cost visibility at design time**: Since "No cost visibility per query type" is a named contributing factor, require new agent features to declare expected query-type distribution and per-tier cost projections before launch, similar to the $5,000-vs-$635 comparison in the example, so routing is designed in rather than retrofitted after overspend is discovered.

### Detection & Response
1. **Cost-distribution-by-query-type audit**: Regularly break down spend by classified query type (simple/medium/complex) and compare against the expected 60/30/10 style distribution; a disproportionate share of spend concentrated in "simple" queries hitting expensive models indicates the router isn't functioning.
2. **No-value-add detection on expensive-model responses**: Sample expensive-model responses to simple/medium queries and compare quality against what the cheap-model tier would have produced; per the research, quality impact should be unmeasurable for simple/medium queries, so any measurable degradation from downgrading is a signal to keep that query type on the expensive tier, not evidence routing is broken.
3. **Model-selection decision audit trail**: Log the routing decision (which model, why) per request so patterns of unnecessary frontier-model usage — e.g., "What time is it?" going to a $15/million-token model — can be traced back to a specific classifier failure or missing routing rule.

### Architecture Patterns
1. **Model router/classifier service**: A lightweight, low-latency classifier (rule-based or a small model) sits in front of the LLM call and assigns each query to a cost tier, implementing the "Model routing" and "Complexity scoring" strategies as a dedicated service rather than ad hoc per-feature logic. Deployment consideration: the router needs its own accuracy monitoring — a misrouting router silently reintroduces the exact waste it's meant to prevent.
2. **Cascade / fallback chain**: Chain cheap-to-expensive models (Haiku → Sonnet → Opus, or GPT-4o-mini → GPT-4o) where each tier only escalates on explicit low-confidence signal, giving graceful quality preservation for the 10% Complex tier without paying frontier prices for the 90% that don't need it. Deployment consideration: requires the cheap model to expose or infer a reliable confidence signal, which not all model APIs provide natively.
3. **Cost-per-query-type dashboard**: Real-time dashboard breaking down spend and volume by classified query tier (mirroring the Cost Comparison table), making the $4,365/month overspend pattern visible before it accumulates for months. Deployment consideration: requires consistent query-type tagging at the logging layer, which must be maintained as new query types are introduced.

### Metrics
1. **pct_simple_queries_on_expensive_model**: Target < 5%; Alert if > 20% (signals routing/classifier failure on the largest query segment).
2. **cost_per_query_blended**: Target < $0.001 (per the $635/1M-query routed example); Alert if > $0.003 (approaching the unrouted $5,000/1M baseline).
3. **model_tier_distribution_accuracy**: Target within ±10 percentage points of expected 60/30/10 simple/medium/complex split; Alert if simple-tier queries routed to frontier model exceed 15% of simple-tier volume.
4. **monthly_overspend_vs_routed_baseline**: Target < 10% above the intelligently-routed cost estimate; Alert if > 50% above baseline (approaching unrouted-cost territory).

### Alerts
1. **Router-Bypass-Spike** (P2): Condition - pct_simple_queries_on_expensive_model exceeds 20% over a rolling 24h window. Action: check for a router service outage or misconfiguration causing fallback to the default (expensive) model, and confirm the classifier is receiving traffic.
2. **Overspend-Vs-Baseline** (P3): Condition - monthly cost trends more than 50% above the routed-cost baseline projection for two consecutive weeks. Action: audit cost distribution by query type and cross-check against the routing decision log for systematic misclassification.

## References

- [OpenAI: Model Pricing](https://openai.com/api/pricing/) - Current model costs
- [Anthropic: Claude Pricing](https://www.anthropic.com/pricing) - Claude model tiers
- [LeanOps: Agents Burn 50x More Tokens](https://leanopstech.com/blog/agentic-ai-cost-runaway-token-budget-2026) - Cost analysis
- [MindStudio: Token Budget Management](https://www.mindstudio.ai/blog/ai-agent-token-budget-management-claude-code) - Cost optimization
- [Portal26: Agentic Token Controls](https://siliconangle.com/2026/04/23/portal26-launches-agentic-token-controls-cap-runaway-ai-agent-spend/) - Cost control tools
