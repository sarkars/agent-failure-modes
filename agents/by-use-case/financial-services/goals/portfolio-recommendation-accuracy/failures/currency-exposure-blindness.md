# Unhedged Currency Exposure & FX Risk

## Issue: Model Recommends International Assets Without Accounting for Currency Risk; FX Movements Dwarf Asset Returns

**Frequency**: Common

**Symptoms**
- Recommends foreign assets with strong fundamentals
- Currency moves opposite to asset returns (correlation -0.8 to -1.0)
- Returns in home currency: negative, despite positive local returns
- Model blind to currency beta

**Root Cause**
Models trained on local returns (asset returns in its currency). When investing in foreign assets from home perspective, FX risk is huge (often >50% of volatility for small countries). Models don't account for this unless data is already currency-adjusted.

**Example**
```
Scenario: US investor in Euro assets
European asset: +5% return in EUR
EUR/USD exchange rate: -5% (EUR weakens)
Return to US investor: 0% (or -5% if unlucky)
Model recommendation: Still positive (didn't account for FX)
Impact: Currency losses offset gains; client disappointed
```

**Key Statistics**
- FX volatility: 5-20% annual depending on currency pair
- FX correlation with assets: Often -0.5 to -0.8 (diversifying but risk-hiding)

---

## Mitigation Strategies

1. **Currency-Adjusted Returns**: Use home-currency returns in training
2. **FX Hedging**: Recommend hedging for FX exposure or accept FX risk
3. **Currency Beta**: Measure and disclose currency sensitivity
4. **Regional Diversification**: Diversify across regions to average FX

### Metrics
- Return in home currency vs. asset currency
- Currency contribution to volatility

### Alerts
- Unhedged FX exposure >30% of portfolio → Require FX consideration

---

## References

- [Currency Risk in International Portfolios](https://arxiv.org/abs/1809.04328)
- [FX Correlation with Equity Returns](https://arxiv.org/abs/2012.04447)
