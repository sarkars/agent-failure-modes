# Missing Data Mishandling in Financial Models

## Issue: Model Handles Missing Data Incorrectly (Mean Imputation, Deletion); Introduces Bias or Information Loss

**Frequency**: Common

**Symptoms**
- Financial data has gaps (no trading on weekends, holiday closures)
- Model imputes mean price → Artificially smooth volatility
- Model deletes rows with missing data → Survivor bias
- Forward-fill creates lookahead bias

**Root Cause**
Missing data is inherent in time series (no trading on holidays). Naive imputation (mean, forward-fill) has serious consequences. Mean imputation reduces volatility unrealistically. Forward-fill uses future data. Deletion introduces survivor bias. No unified "right" way; context matters.

**Example**
```
Scenario: Trading model trained on stock prices
Data: Monday-Friday trading prices
Weekend/Holiday: No trading (prices missing Saturday-Sunday)
Naive handling: Forward-fill (Friday price = Saturday price = Sunday price)
Result: Continuous time series but artificial (weekends have zero volatility)
Model learns: "Volatility is lower than reality"
Forward testing: Actual weekend returns volatile (market opens with gap)
Impact: Model underestimates risk; position sizing too aggressive
```

**Key Statistics**
- Data completeness: 80-95% typical (weekends, holidays missing)
- Volatility reduction by mean imputation: 10-30%
- Lookahead bias from careless forward-fill: 1-3% annual return bias

---

## Mitigation Strategies

1. **Explicit Handling**: Mark missing explicitly; don't impute
2. **Time-Aware Models**: Models that handle irregular time series (e.g., transformer attention on actual dates)
3. **Domain Knowledge**: Use market-specific rules (no trading weekends; use Friday close for Monday open)
4. **Sensitivity Analysis**: Test multiple imputation methods; report uncertainty

### Metrics
- Volatility before/after imputation (should preserve realistic volatility)
- Model performance on data with vs. without missing
- Backtest vs. forward performance gap

### Alerts
- Volatility estimate <70% of actual → Check imputation method

---

## References

- [Missing Data in Financial Time Series](https://arxiv.org/abs/1911.03634)
- [Imputation Methods & Statistical Bias](https://arxiv.org/abs/2007.05134)
