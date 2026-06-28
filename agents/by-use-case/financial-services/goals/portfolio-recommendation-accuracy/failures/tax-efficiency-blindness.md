# Tax-Efficiency Blindness in Recommendations

## Issue: Model Recommends Portfolio Without Accounting for Tax Impact; After-Tax Returns Much Lower Than Pre-Tax Predictions

**Frequency**: Common

**Symptoms**
- Pre-tax return prediction: 8%
- Post-tax realized return: 4-5% (tax impact not modeled)
- High-turnover strategies generate tax drag
- Model doesn't account for tax-loss harvesting opportunities

**Root Cause**
Backtests often use pre-tax returns (cleaner data). Taxes vary by jurisdiction, holding period, account type. Models trained on price returns don't learn tax impact. Tax-efficient investing is a distinct skill; models don't learn it unless explicitly modeled.

**Example**
```
Scenario: Index fund recommendation
Pre-tax annual return: 8%
Tax rate: 25% on gains
After-tax return: 8% * (1 - 0.25) = 6%
Model recommendation: "8% expected return"
Client reality: Gets 6% after taxes
Expectation mismatch: 2% annual drag compounds to 25% portfolio value loss over 10 years
```

**Key Statistics**
- Tax drag: 1-3% annually (varies by account, holding period)
- Tax-loss harvesting benefit: 0.5-1% annually if implemented
- Model prediction gap: 20-40% of model error

---

## Mitigation Strategies

1. **After-Tax Modeling**: Model taxes explicitly (jurisdiction, account type)
2. **Tax-Loss Harvesting**: Recommend tax-loss harvesting opportunities
3. **Turnover Penalty**: Penalize high-turnover strategies in recommendations
4. **Tax-Aware Rebalancing**: Prefer tax-efficient rebalancing methods

### Metrics
- Pre-tax vs. post-tax returns (gap should be <1%)
- Tax-loss harvesting opportunities identified
- Turnover by strategy (lower is better for tax efficiency)

### Alerts
- Post-tax return <80% of pre-tax → Tax drag issue

---

## References

- [Tax-Efficient Investing with AI](https://arxiv.org/abs/2106.14237)
- [Tax-Loss Harvesting & Portfolio Optimization](https://arxiv.org/abs/1809.03456)
