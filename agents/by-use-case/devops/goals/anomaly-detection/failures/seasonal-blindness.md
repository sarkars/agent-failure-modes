# Seasonal Blindness in Anomaly Detection

## Issue: Anomaly Detection Model Flags Normal Seasonal Patterns as Anomalies; High False Positive Rate

**Frequency**: Very Common

**Symptoms**
- Spike in traffic on Black Friday → Flagged as anomaly
- Predictable seasonal patterns misclassified as outages
- False alerts during holidays, weekends
- Alert fatigue from seasonal false positives

**Root Cause**
Anomaly detection typically uses statistical baselines (mean ± 3σ). Seasonal variations not modeled. Traffic patterns have daily (traffic higher during day), weekly (higher weekdays), and yearly (holiday, seasonal) components. Models that don't explicitly handle seasonality flag normal variations as anomalies.

**Example**
```
Scenario: Server CPU anomaly detection
Model: Baseline CPU = 30% ± 10%
Reality: CPU on Black Friday = 45% (within normal seasonal peak)
Model: "CPU spike 45%! Alert: Potential DDoS attack"
Investigation: False alarm (normal Black Friday traffic)
Impact: Alert fatigue; real issues masked by false positives
```

**Key Statistics**
- False positive rate without seasonality: 20-40% during seasonal peaks
- False positive rate with seasonality model: 1-5%
- Seasonal variation magnitude: 2-5x normal baseline

---

## Mitigation Strategies

1. **Seasonal Decomposition**: Explicitly model trend, seasonal, and residual components
2. **Baseline by Season**: Maintain separate baselines for each season/day-type
3. **Prophet/SARIMA**: Use time-series forecasting models that handle seasonality
4. **Anomaly on Residuals**: Detect anomalies on residuals after removing seasonality

### Metrics
- False positive rate (should be <2%)
- True positive rate (should be >80%)
- Precision/Recall

### Alerts
- FP rate >5% → Retrain with seasonality model

---

## References

- [Seasonal Anomaly Detection](https://arxiv.org/abs/2107.12171)
- [Time Series Forecasting with Seasonality](https://arxiv.org/abs/2004.13408)
