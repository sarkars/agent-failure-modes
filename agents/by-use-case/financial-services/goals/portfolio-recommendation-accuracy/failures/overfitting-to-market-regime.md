# Overfitting to Historical Market Regime

## Issue: Model Optimized for Historical Regime (Bull Market) Fails in Regime Change (Bear Market, Stagflation)

**Frequency**: Very Common

**Symptoms**
- Model works great on training period
- Fails spectacularly when market conditions change
- Diversification breaks down in crisis (all assets correlated)
- Risk estimates prove wildly wrong

**Root Cause**
Models trained on bull market data (2010-2022 mostly) learn "stocks go up." When regime changes to bear market or stagflation, all assumptions break. Correlation structure changes; volatility spikes; safe assets become risky. Model has no experience with this regime.

**Example**
```
Scenario: Portfolio optimization model trained 2010-2021
Model: 60% stocks / 40% bonds (risk: 8% annualized volatility)
Reality 2022: Stagflation (stocks down, bonds down, correlation up)
Actual portfolio: 25% volatility, 15% drawdown
Impact: Client suffers 2x predicted risk in regime change
```

**Key Statistics**
- Historical Sharpe ratio (backtest): 1.2
- Forward Sharpe (2022-2024 in regime change): 0.3
- Correlation breakdown: Expected 0.2 stocks/bonds → Actual 0.6+ in crisis

---

## Mitigation Strategies

1. **Multi-Regime Data**: Include bear markets, recessions in training
2. **Scenario Analysis**: Test on 2008 crisis, stagflation, etc.
3. **Adaptive Allocation**: Dynamic weights based on regime detection
4. **Conservative Estimates**: Use worst historical period as baseline

### Metrics
- Sharpe ratio in multiple regimes (not just backtest)
- Max drawdown across regimes
- Correlation stability (does it hold in crisis?)

### Alerts
- Actual volatility >1.5x predicted → Regime change detected

---

## References

- [Regime-Switching Models in Finance](https://arxiv.org/abs/1912.01341)
- [Asset Correlation Breakdown in Crisis](https://arxiv.org/abs/2008.02304)
