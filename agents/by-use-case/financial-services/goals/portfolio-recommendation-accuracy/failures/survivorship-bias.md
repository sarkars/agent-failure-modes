# Survivorship Bias in Training Data

## Issue: Model Trained Only on Survived Assets; Ignores Assets That Failed or Were Delisted

**Frequency**: Common

**Symptoms**
- Historical returns underestimate risk (failed assets missing)
- Overconfidence in asset classes
- Recommendations overestimate achievable returns
- Portfolio volatility higher than model predicts

**Root Cause**
Training data only includes assets that survived to present. Failed assets (bankruptcies, delistings) removed from dataset. Model learns "these assets reliably outperform" but ignores selection bias — assets that didn't survive were pruned.

**Example**
```
Scenario: Index replication model
Training data: S&P 500 constituents from 2020-2024
Missing: 20 companies that were delisted during this period
Model predicts: 10% average annual return
Reality: Actual index return 8% (wealth destroyed in delisted positions)
Impact: Underestimate disaster risk
```

**Key Statistics**
- Survivorship bias in returns: 1-3% annually (compounded)
- Volatility underestimation: 15-30% (models don't see tail risks)

---

## Mitigation Strategies

1. **Include Dead Assets**: Source historical data that includes delisted companies
2. **Adjust for Bias**: Apply statistical correction for survivorship bias
3. **Stress Testing**: Historical VaR should be shocked higher
4. **Longer History**: Longer time periods include more failures

### Metrics
- Return assuming all survived vs. actual (difference = bias)
- Volatility backtest (does realized match predicted?)

### Alerts
- Realized volatility >20% higher than predicted → Retrain with dead assets

---

## References

- [Survivorship Bias in Investment Returns](https://arxiv.org/abs/1807.00532)
- [Data Biases in Financial ML](https://arxiv.org/abs/2102.06800)
