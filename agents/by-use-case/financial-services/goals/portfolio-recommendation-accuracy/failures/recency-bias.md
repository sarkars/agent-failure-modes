# Recency Bias in Portfolio Recommendations

## Issue: Model Overweights Recent Performance; Recommends Assets That Performed Well Recently but Are Mean-Reverting

**Frequency**: Very Common

**Symptoms**
- Recommendations chase recent winners (high drawdown risk)
- Portfolio concentrated in recently-hot sectors
- Underrepresents assets in recent downturn (buying low missed)
- High portfolio turnover from chasing trends

**Root Cause**
Recommendation models trained on historical return data develop implicit time-series momentum bias. Recent periods have higher data density; models weight them more. No explicit mean-reversion prior built in. Temporal data suggests "what went up will stay up" (false).

**Example**
```
Scenario: Robo-advisor portfolio construction
Tech sector: +40% in last 6 months
Model recommendation: Overweight tech (40% of portfolio)
Reality: Tech sector mean-reverting; subsequent 6 months: -15%
Client loss: Significant underperformance
Impact: Poor risk-adjusted returns; client dissatisfaction
```

**Key Statistics**
- Win rate (positive returns in subsequent period): 40-55% (barely >50%)
- Concentration in recent winners: 30-50% of portfolio often in top 3 performers
- Turnover: 50-100% quarterly (transaction costs erode returns)

---

## Mitigation Strategies

1. **Mean-Reversion Prior**: Explicitly penalize recent strong performers
2. **Longer Lookback**: Use 3-5 year data, not 1-2 year
3. **Fundamental Factors**: Base recommendations on earnings, valuations, not price momentum
4. **Turnover Penalties**: Penalize high turnover in optimization

### Metrics
- Recommendation accuracy in forward period (>50% = good)
- Portfolio turnover (lower is better)
- Concentration (lower is better)

### Alerts
- Turnover >50% quarterly → Review model bias
- Win rate <55% → Model underperforming

---

## References

- [Momentum and Reversal in Asset Returns](https://arxiv.org/abs/2205.05808)
- [Behavioral Bias in Algorithmic Trading](https://arxiv.org/abs/2302.12784)
