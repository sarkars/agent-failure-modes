# Factor-Crowding Blindness in Portfolio Recommendations

## Issue: Model Recommends Factor Exposures Without Awareness of Market-Wide Crowding, Causing Correlated Unwind Risk

**Frequency**: Common

**Symptoms**
- Recommended portfolio loads heavily on popular factors (value, momentum, quality) that are simultaneously crowded across many other funds
- Model has no visibility into aggregate positioning data (13F filings, prime brokerage surveys, ETF flows)
- Sudden, sharp factor reversals ("quant quakes") cause losses uncorrelated with idiosyncratic stock fundamentals
- Backtests look attractive because crowding effects are invisible in single-strategy historical returns

**Root Cause**
Factor-based recommendation models are typically trained on a single portfolio's historical factor returns, not on market-wide positioning data. They cannot observe that thousands of other funds hold the same factor tilts. When liquidity providers retreat, crowded factors unwind simultaneously regardless of fundamentals, producing correlated losses the model never priced in.

**Example**
```
Scenario: Quant equity model recommends overweight to "momentum" factor
Model basis: Momentum factor Sharpe = 1.1 over trailing 3 years
Hidden context: Momentum is the most crowded factor among multi-manager platforms
Trigger: Macro surprise causes rapid de-risking across funds
Result: Momentum factor drops -12% in 4 trading days (a "quant quake")
Impact: Portfolio loses far more than factor volatility alone would predict
```

**Key Statistics**
- Historical quant quakes (e.g., Aug 2007, 2018, 2026) have produced 3-7 standard-deviation factor moves over single-digit numbers of trading days
- Crowding-adjusted factor risk models reduce false-confidence in factor Sharpe estimates by an estimated 20-40%
- Funds with concentrated single-factor exposure see 2-3x higher drawdown volatility during deleveraging events vs. multi-factor diversified peers

---

## Mitigation Strategies

1. **Crowding Proxies**: Incorporate 13F concentration, short interest, and ETF flow data as crowding signals in the factor model
2. **Factor Diversification Constraints**: Cap exposure to any single factor regardless of its standalone attractiveness
3. **Liquidity-Adjusted Sizing**: Size positions by estimated days-to-liquidate under stress, not just average daily volume
4. **Deleveraging Scenario Tests**: Simulate correlated multi-fund unwind scenarios, not just idiosyncratic stock shocks

### Metrics
- Factor concentration percentile vs. market-wide positioning estimates
- Days-to-liquidate under 3x normal volume stress
- Realized factor drawdown vs. crowding-adjusted VaR

### Alerts
- Factor exposure in top decile of estimated market crowding → P2
- Days-to-liquidate under stress >5 trading days for >20% of portfolio → P2
- Realized factor drawdown exceeds crowding-adjusted VaR by >2x → P1

---

## References

- [Exposing Product Bias in LLM Investment Recommendation](https://arxiv.org/abs/2503.08750)
- [Your AI, Not Your View: The Bias of LLMs in Investment Analysis](https://arxiv.org/abs/2507.20957)
