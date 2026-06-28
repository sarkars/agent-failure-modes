# Liquidity Risk Mispricing in Recommendations

## Issue: Model Recommends Illiquid Assets; Prices Assumed Frictionless but Actual Bid-Ask Spreads Destroy Returns

**Frequency**: Common

**Symptoms**
- Backtest assumes buying at close price
- Live trading must buy at ask, sell at bid
- Bid-ask spread erodes 50-100% of expected alpha
- Position sizing fails in illiquid markets (cannot execute large orders)

**Root Cause**
Backtest data only has closing price, not bid-ask. Model doesn't account for trading friction. Illiquid assets have high spreads; assumptions of "free" trading cost more than expected return. Model blind to liquidity premium.

**Example**
```
Scenario: Emerging market bond fund recommendation
Backtest return (assumed perfect liquidity): 6%
Live trading (with bid-ask, slippage): 2%
Issue: Bid-ask spreads in EM bonds: 0.5-2%
Impact: Model strategy works in theory, loses money in practice
```

**Key Statistics**
- Bid-ask spread: 0.1% (liquid stocks) to 2%+ (illiquid assets)
- Impact on annual return: 0.5-2% per round-trip trade

---

## Mitigation Strategies

1. **Liquidity Adjustment**: Measure and deduct actual trading costs from backtest
2. **Liquidity Score**: Favor more liquid assets in recommendations
3. **Slippage Model**: Estimate bid-ask for different order sizes
4. **Position Sizing**: Reduce position size in illiquid assets

### Metrics
- Backtest return (bid-ask adjusted)
- Actual returns achieved in live trading

### Alerts
- Live return <80% of backtest → Trading friction issue

---

## References

- [Bid-Ask Spreads and Asset Returns](https://arxiv.org/abs/2201.09871)
- [Liquidity Adjusted Performance](https://arxiv.org/abs/1903.04201)
