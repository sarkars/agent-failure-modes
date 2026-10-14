# AI Agent Cost Efficiency Failures: Token Waste, Retry Storms, and Model Overuse

**Cost efficiency failures are the ways an AI agent spends more tokens and API calls than the task needs: processing items one at a time, caching badly, calling expensive models for easy work, or retrying and looping without progress.** The 15 patterns here cover execution-level waste.

## Key Takeaways

- Waste shows up in four places: how many calls are made, how big each call is, which model is used, and how often calls repeat.
- Retries can multiply cost: a single request with exponential backoff that re-invokes the model gets billed again each time.
- Cost cuts can hurt quality, so one pattern covers that trade-off directly.
- For planning, caching, and architecture-level waste, see [cost optimization](../cost-optimization/).

## Patterns

| Pattern | What goes wrong |
|---|---|
| [Batch Optimization Failures](failures/batch-optimization-failures.md) | Processing Items Individually When Batching Would Be More Efficient |
| [Caching Failures](failures/caching-failures.md) | Redundant LLM Calls for Identical or Similar Requests |
| [Context Stuffing](failures/context-stuffing.md) | Overloading Context with Irrelevant Information |
| [Cost-Quality Tradeoff](failures/cost-quality-tradeoff.md) | Cost Optimization Degrades Agent Quality |
| [Expensive Model Cascade](failures/expensive-model-cascade.md) | Agent Escalates to More Expensive Models for Tasks That Don't Require Them |
| [Infinite Loops](failures/infinite-loops.md) | Agent Gets Stuck in Infinite Retry Loops |
| [Model Selection Waste](failures/model-selection-waste.md) | Using Expensive Models When Cheaper Alternatives Suffice |
| [Resource Exhaustion](failures/resource-exhaustion.md) | Agent Exceeds Allocated Resources Before Completion |
| [Retry Amplification of Costs](failures/retry-amplification-of-costs.md) | Exponential Retry Logic Multiplies Costs Beyond Original Request |
| [Retry Storms](failures/retry-storms.md) | Aggressive Retries Multiply Costs |
| [Step Repetition](failures/step-repetition.md) | Agent Repeats Same Steps Without Progress |
| [Token Budget Overflow Attack](failures/token-budget-overflow-attack.md) | Attacker Intentionally Triggers High-Token Operations to Exhaust Cost Budget |
| [Token Explosion](failures/token-explosion.md) | Exponential Token Usage Growth |
| [Unnecessary Tool Calls](failures/unnecessary-tool-calls.md) | Agent Calls Tools When Not Needed |
| [Verbose Reasoning](failures/verbose-reasoning.md) | Excessive Chain-of-Thought Output |

**Total: 15 patterns**

## How These Patterns Group

- **Wasted calls:** Batch Optimization Failures, Caching Failures, Unnecessary Tool Calls, Step Repetition, Infinite Loops, Retry Storms, Retry Amplification of Costs
- **Oversized calls:** Context Stuffing, Token Explosion, Verbose Reasoning
- **Wrong model or budget:** Expensive Model Cascade, Model Selection Waste, Cost-Quality Tradeoff, Resource Exhaustion, Token Budget Overflow Attack

## When This Matters

- The agent calls paid APIs without a per-request or per-user budget
- Traffic is growing and cost per task matters
- The same task runs at high volume

## Frequently Asked Questions

### Why is my AI agent so expensive to run?

Common causes: model selection waste, token explosion, and retry storms. Check which one matches your cost breakdown first.

### How do I stop an agent from looping and burning tokens?

See infinite loops and step repetition. Both need limits on turns and repeated steps.

### Does cutting cost hurt quality?

It can. See cost-quality tradeoff.

### What is the difference between cost efficiency and cost tracking?

This goal is about spending less. [Cost tracking](../cost-tracking/) is about measuring and enforcing budgets.

## Related

- [All operations goals](../)
- [Operations overview](../../)
