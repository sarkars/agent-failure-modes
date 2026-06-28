# Market-Impact Blindness in Trading Execution

## Issue: Agent Sizes and Times Orders Without Accounting for Its Own Price Impact, Especially Across Correlated Positions or Repeated Trades

**Frequency**: Common

**Symptoms**
- Agent executes the full recommended trade size at once, moving the market against itself before completing the order
- Repeated rebalancing trades in the same direction (e.g., across many client accounts) compound into a visible, exploitable footprint
- No coordination between multiple concurrent orders in correlated instruments, causing self-inflicted adverse price moves
- Agent's "optimal execution" plan treats market impact as a fixed cost rather than a function of its own trading pace

**Root Cause**
Execution agents are frequently optimized per-order, in isolation, without visibility into the aggregate flow the platform is generating across many accounts or correlated instruments simultaneously. When the same signal triggers trades across thousands of accounts (e.g., a model-driven rebalance), the agent has no mechanism to recognize that its own aggregate footprint is the dominant driver of adverse price movement.

**Example**
```
Scenario: Robo-advisor platform triggers a model-driven sector rotation across 50,000 accounts simultaneously
Each account's order: Small individually (sizing looks negligible)
Aggregate footprint: Single-name order flow equivalent to 15% of ADV concentrated in a 30-minute window
Result: Price moves 4% against the platform's own flow before completion
Impact: Aggregate client cost from self-inflicted impact exceeds any single account's expected slippage estimate by an order of magnitude
```

**Key Statistics**
- Aggregate platform-level order flow can represent a multiple of any single account's apparent footprint, especially for signal-driven rebalances triggered simultaneously across client bases
- Self-impact from uncoordinated concurrent execution is a recognized cause of cost leakage in multi-account algorithmic trading platforms
- Coordinated execution scheduling (netting, staggering) has been shown to reduce aggregate impact cost materially versus uncoordinated simultaneous execution

---

## Mitigation Strategies

1. **Order Netting**: Net offsetting orders across accounts before sending net flow to the market
2. **Aggregate Flow Awareness**: Compute platform-wide aggregate exposure per instrument before triggering correlated trades across many accounts
3. **Staggered Execution Scheduling**: Spread correlated trades across a longer window or multiple venues to reduce visible footprint
4. **Impact-Aware Signal Throttling**: When aggregate flow would exceed a materiality threshold of ADV, throttle or stagger the signal's rollout

### Metrics
- Aggregate platform order flow as % of ADV per instrument per session
- Self-impact cost (price move attributable to platform's own flow)
- Netting efficiency (% of gross flow eliminated via netting)

### Alerts
- Aggregate flow for a single instrument exceeds 10% of ADV in a session → P1
- Self-impact cost exceeds estimated slippage budget by >3x → P1

---

## References

- [Agentic Trading: When LLM Agents Meet Financial Markets](https://arxiv.org/abs/2605.19337)
- [Agentic AI Systems Applied to tasks in Financial Services: Modeling and model risk management crews](https://arxiv.org/abs/2502.05439)
