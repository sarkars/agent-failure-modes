# Correlation Breakdown in Portfolio Diversification

## Issue: Assumed Diversification Fails When Correlations Spike (Tail Dependence Not Captured)

**Frequency**: Very Common

**Symptoms**
- Expected correlations: 0.2 (low, diversifying)
- Crisis correlations: 0.8+ (high, not diversifying)
- "Diversified" portfolio moves in lockstep during crashes
- Tail risk much higher than predicted

**Root Cause**
Correlations estimated from normal-market data. Tail events (crashes) exhibit different dynamics; correlations spike. Models assume constant correlation; don't capture tail dependence or regime-switching. Asset classes designed to be uncorrelated actually tank together in crises.

**Example**
```
Scenario: 60/40 stock/bond portfolio
Normal times: Correlation 0.1 (good diversification)
2022 crisis: Correlation 0.6 (both stocks and bonds down)
Portfolio volatility expected: 8%; Actual: 15%
Drawdown expected: 12%; Actual: 25%
Impact: Client's risk tolerance breached despite "diversified" portfolio
```

**Key Statistics**
- Normal correlation: 0.1-0.3
- Crisis correlation: 0.6-0.9
- Tail correlation premium: 0.5-0.7 higher in crisis

---

## Mitigation Strategies

1. **Tail Dependence Modeling**: Use copulas or extreme value theory
2. **Stress Test Correlations**: Assume 0.8-0.9 correlation in tail scenarios
3. **Crisis Hedges**: Add explicit tail-hedging positions
4. **Dynamic Allocation**: Adjust weights based on correlation regime

### Metrics
- Correlation across market regimes (normal vs. crisis)
- Portfolio volatility backtest (actual vs. predicted)

### Alerts
- Actual portfolio volatility >1.5x predicted → Correlation assumption broken

---

## References

- [Tail Dependence in Financial Returns](https://arxiv.org/abs/2004.11768)
- [Systemic Risk and Asset Correlation](https://arxiv.org/abs/1503.07427)
