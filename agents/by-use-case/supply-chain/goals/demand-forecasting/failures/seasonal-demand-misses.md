# Seasonal Demand Misses & Holiday Blindness

## Issue: Forecasting Model Fails to Account for Seasonal Variations; Massive Stockouts/Overstock on Seasonal Peaks

**Frequency**: Very Common

**Symptoms**
- Winter sales 3x summer baseline
- Model trained on average; predicts flat demand
- Winter: Severe stockout (lost sales)
- Spring: Overstock (inventory writedowns)
- Seasonal patterns not learned or exploded on forecast

**Root Cause**
Many demand forecasting datasets span only 1-2 years; insufficient to learn multi-year seasonality. Models trained on recent data miss historical seasonal patterns. Or, seasonality handled but holiday effects unexpected (Thanksgiving pushes earlier than normal, disrupts forecast).

**Example**
```
Scenario: Toy retail demand
Historical pattern: 50% of annual sales in Q4 (holiday season)
Model trained on: Last 2 years data (non-representative year with low holiday sales)
Model forecast: Flat 25% per quarter
Q4 actual: 50% of annual volume
Result: Stockout in Q4 (lost 100M+ in sales); excess inventory Q1-Q3
Impact: Revenue loss; inventory write-offs; cash flow crisis
```

**Key Statistics**
- Seasonal variance: 2-5x baseline typical
- Holiday demand spike: 3-10x on peak days (Black Friday)
- Forecast accuracy without seasonality: 30-50%
- With seasonality: 70-85%

---

## Mitigation Strategies

1. **Multi-Year Data**: Use 3-5 years minimum to capture seasonality
2. **Holiday Calendars**: Integrate holiday dates; model holiday effects
3. **Promotion Effects**: Account for sales, deals driving demand spikes
4. **Hierarchical Forecasting**: Forecast by season separately; combine

### Metrics
- MAPE (mean absolute percentage error) by season
- Forecast accuracy during peak season (should be >80%)
- Inventory turnover by season

### Alerts
- Peak season forecast accuracy <70% → Needs retraining

---

## References

- [Seasonal Forecasting & Demand Planning](https://arxiv.org/abs/2102.10936)
- [Holiday & Promotional Effects on Demand](https://arxiv.org/abs/2007.08545)
