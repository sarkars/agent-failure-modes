# Best-Case Projection Bias

## Issue: Sales forecasting model uses deal probability from salesperson input, which is inherently optimistic; projects deals that salesperson hopes will close rather than actual likelihood

**Frequency**: Common

**Symptoms**
- Pipeline shows $5M in "likely" deals next quarter
- Actual closed deals: $2M (40% variance)
- Sales team consistently over-optimistic by 40-60%
- Quarterly revenue targets miss due to forecast inaccuracy

**Root Cause**
Salespeople are incentivized to be optimistic; they estimate deal probability. Models trust input probability estimates without adjusting for optimism bias. Salespeople genuinely believe in their deals but lack statistical calibration—they think 70% probability when reality is 30%.

**Example**
```
Sales pipeline forecast:
- Deal A: $1M, salesperson says "90% close probability"
- Deal B: $500k, salesperson says "85%"
- Deal C: $400k, salesperson says "80%"
Total forecast: $1.9M at 85% avg probability = $1.6M expected value
Actual outcome:
- Deal A: LOST (salesperson misunderstood buyer intent)
- Deal B: CLOSED ($500k)
- Deal C: LOST (budget cut by buyer)
Actual revenue: $500k vs forecasted $1.6M
Impact: Revenue miss; stock price impact; forecast unreliable
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Salesperson probability overestimation: 40-60% | Sales ops analytics |
| Forecast accuracy improvement with calibration: 20-30% | Predictive analytics studies |
| Sales team confidence-reality gap: Consistent across companies | Salesforce benchmark data |

---

## Mitigation Strategies

1. **Probability calibration**: Adjust salesperson estimates downward (e.g., multiply by 0.6)
2. **Historical accuracy tracking**: Compare actual close rates to predicted; adjust model
3. **Independent scoring**: Have second person (manager/data analyst) estimate independent of salesperson

---

## Production Signals

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Forecast variance | Actual vs predicted >30% miss | P2 |
| Probability miscalibration | Deals "90% likely" consistently lost | P2 |

---

## References

- [Sales Forecast Accuracy](https://arxiv.org/abs/1806.07654) - Research on bias
- [Probability Calibration in Forecasting](https://arxiv.org/abs/1511.08099) - Calibration methods
