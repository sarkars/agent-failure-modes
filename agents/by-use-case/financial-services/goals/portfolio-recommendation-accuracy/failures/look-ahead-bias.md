# Look-Ahead Bias in Backtests

## Issue: Model Uses Future Information in Backtest That Wouldn't Be Available in Real-Time Trading

**Frequency**: Very Common

**Symptoms**
- Backtest performance 15-30% better than live trading
- Model can't explain the gap
- Trades reference future price data
- Index rebalancing dates used with perfect foresight

**Root Cause**
Backtesting code accidentally includes future information (next day's open price, dividend announcement dates not known until ex-date, etc.). Human error or subtle bug in data pipeline. Models learn patterns that are causally impossible (perfect foresight).

**Example**
```
Scenario: Momentum trading backtest
Bug: Signals generated using end-of-day close price (not available at trade time)
Backtest: 12% annual return
Live trading: 2% annual return (can't actually implement backtest signals)
Impact: Millions allocated to strategy that doesn't work
```

**Key Statistics**
- Look-ahead bias magnitude: 5-25% annual return overstatement
- Time-to-discovery: Often not caught until 6-12 months after deployment

---

## Mitigation Strategies

1. **Strict Data Timing**: Enforce "no future data" in code (timestamps on all data)
2. **Live Validation**: Compare backtest predictions to live performance weekly
3. **Code Review**: Data scientist peer review of signal generation
4. **Conservative Assumptions**: Use bid-ask mid, not close prices; assume slippage

### Metrics
- Backtest vs. live performance comparison
- Latency check: Signal generation time before market close

### Alerts
- Live performance >2 std below backtest → Investigate look-ahead bias

---

## References

- [Common Backtesting Mistakes](https://arxiv.org/abs/2105.08677)
- [Data Snooping in Financial Prediction](https://arxiv.org/abs/1903.00333)
