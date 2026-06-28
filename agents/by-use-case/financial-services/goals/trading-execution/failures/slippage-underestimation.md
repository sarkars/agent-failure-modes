# Slippage Underestimation in Trading Execution

## Issue: Execution Agent's Pre-Trade Cost Model Systematically Understates Realized Slippage, Especially for Larger or Illiquid Orders

**Frequency**: Very Common

**Symptoms**
- Realized execution price consistently worse than pre-trade estimated price, beyond what bid-ask spread alone explains
- Slippage estimates derived from average daily volume but ignore intraday liquidity patterns (open/close auctions, lunch lull)
- Performance attribution shows persistent negative "execution alpha" that the model never learns to correct for
- Larger orders show disproportionately worse slippage than the model's linear cost assumption predicts

**Root Cause**
Many execution-cost models assume a linear or square-root relationship between order size and price impact calibrated on average historical conditions. They do not adapt to current order-book depth, time-of-day liquidity, or the order's own footprint as it executes. The result is a pre-trade cost estimate that looks reasonable in isolation but is consistently optimistic versus realized fills, particularly for less liquid names or stressed markets.

**Example**
```
Scenario: Agent submits a buy order for 2% of average daily volume
Pre-trade estimate: Expected slippage = 8 bps vs. arrival price
Execution: Order worked over 2 hours during low-liquidity midday window
Realized slippage: 35 bps vs. arrival price
Cumulative impact: Over a quarter of similar trades, underestimated slippage erodes ~40bps of annual strategy alpha
```

**Key Statistics**
- Linear/static slippage models underestimate realized cost by 2-4x for orders >1% of ADV in studies of institutional execution data
- Time-of-day liquidity variation accounts for a large share of intraday slippage variance not captured by static volume-based models
- Persistent negative execution alpha attributable to slippage underestimation is a commonly cited gap between paper and live strategy performance

---

## Mitigation Strategies

1. **Order-Book-Aware Cost Models**: Use real-time depth-of-book and recent trade-and-quote data to estimate impact, not just historical ADV
2. **Time-of-Day Liquidity Curves**: Model intraday liquidity seasonality explicitly (open/close auctions vs. midday lull)
3. **Post-Trade Calibration Loop**: Continuously compare realized vs. estimated slippage and recalibrate the cost model with a feedback loop
4. **Adaptive Order Slicing**: Size and pace child orders dynamically based on live liquidity signals rather than a fixed schedule

### Metrics
- Realized vs. pre-trade estimated slippage (bps), tracked per order-size bucket
- Execution alpha (cumulative slippage cost vs. benchmark)
- Model calibration error trend over time

### Alerts
- Realized slippage exceeds pre-trade estimate by >2x on >10% of orders in a session → P2
- Cumulative execution alpha drag exceeds strategy's gross alpha budget → P1

---

## References

- [Agentic Trading: When LLM Agents Meet Financial Markets](https://arxiv.org/abs/2605.19337)
- [Toward Reliable Evaluation of LLM-Based Financial Multi-Agent Systems](https://arxiv.org/abs/2603.27539)
