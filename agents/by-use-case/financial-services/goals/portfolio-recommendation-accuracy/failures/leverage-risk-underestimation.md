# Leverage Risk Underestimation

## Issue: Model Underestimates Risk from Leverage; Recommends Leveraged Strategies Without Adequate Risk Buffer

**Frequency**: Common

**Symptoms**
- Leverage amplifies returns in bull markets (looks great in backtest)
- Leverage amplifies losses in bear markets (catastrophic in forward period)
- Model doesn't simulate worst-case scenarios
- Volatility estimates too low; actual leverage causes margin calls

**Root Cause**
Backtests show leverage enhancing returns during bull markets (2010-2021). Models learn "leverage is good." But leverage is a double-edged sword; tail risk under-estimated. VaR-style risk models don't capture tail events well. Models trained on "normal" market conditions fail in crises.

**Example**
```
Scenario: 2x leveraged stock index fund
Backtest 2010-2021 (bull market): 2x leverage returns 20% annually
Model recommendation: "2x leverage optimal for risk-return profile"
Forward testing 2022-2023: Market down 20%, leverage amplifies to 40% loss
Client: Forced to liquidate at loss due to margin call
Expected return: 20%, Actual: -40%
Impact: Catastrophic loss; client lawsuit
```

**Key Statistics**
- Bull market 2x leverage: 2x returns, acceptable drawdown
- Bear market 2x leverage: 2x drawdown, potential margin call, liquidation forced
- Leverage risk premium: 3-5% annually in worst-case (not captured in standard models)

---

## Mitigation Strategies

1. **Tail Risk Modeling**: Stress-test with 2008-2011 crisis scenarios
2. **Margin Call Analysis**: Model forced liquidation in drawdown scenarios
3. **Leverage Caps**: Recommend leverage <1.5x for retail, <2x even for pros
4. **Drawdown Limits**: Set maximum acceptable drawdown; scale back leverage

### Metrics
- Maximum drawdown with leverage (should be <30%)
- Leverage ratio change over time (track concentration)
- Margin maintenance ratio (buffer before call)

### Alerts
- Leverage risk premium underestimated >3% → Retrain

---

## References

- [Leverage and Systemic Risk](https://arxiv.org/abs/1703.06897)
- [Tail Risk in Leveraged Strategies](https://arxiv.org/abs/2002.09474)
