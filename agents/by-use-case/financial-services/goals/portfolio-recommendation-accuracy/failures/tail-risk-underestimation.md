# Tail-Risk Underestimation in Portfolio Recommendations

## Issue: Model Optimizes for Mean-Variance Efficiency While Ignoring Fat-Tail and Black-Swan Risk

**Frequency**: Common

**Symptoms**
- Recommended portfolios show low historical volatility but large drawdowns during crashes
- VaR/CVaR estimates from the model are far lower than realized losses in stress periods
- Allocation skewed toward strategies with positive skew in calm markets but severe left-tail exposure (e.g., short volatility, carry trades)
- Stress-test results diverge sharply from live performance during regime shifts

**Root Cause**
Mean-variance and most ML-based portfolio optimizers assume approximately Gaussian return distributions. Real asset returns exhibit fat tails and negative skew, especially for strategies that harvest risk premia (short vol, merger arb, carry). Models trained on calm-period data never see tail events, so they underprice the probability and magnitude of extreme co-movements.

**Example**
```
Scenario: Robo-advisor recommends "low volatility" equity-income portfolio
Historical Sharpe (5yr calm period): 1.4, annualized vol: 8%
Model output: "Low risk allocation, 95% VaR = -3%"
Reality: March 2026 liquidity event — correlated drawdown across "low vol" basket
Actual loss: -22% in 3 weeks (7x model's stated VaR)
Impact: Client portfolios breach risk mandates; regulatory inquiry into model risk controls
```

**Key Statistics**
- Realized drawdowns during tail events average 3-8x model-predicted VaR for mean-variance optimized portfolios
- Strategies with positive historical skew but tail risk ("picking up nickels in front of a steamroller") account for a disproportionate share of crisis-period agent losses
- Backtests excluding 2008, 2020, and 2026 stress windows overstate Sharpe ratios by 30-60%

---

## Mitigation Strategies

1. **CVaR/Expected Shortfall Optimization**: Replace variance-based objectives with CVaR at the 1-5% tail, not just variance
2. **Stress-Scenario Injection**: Force the model to evaluate candidate portfolios against historical and synthetic crisis scenarios (2008, 2020, flash crashes)
3. **Tail-Risk Factor Exposure Limits**: Cap exposure to known tail-risk factors (short vol, illiquid credit, leveraged carry)
4. **Regime-Conditional Risk Models**: Use regime-switching or extreme value theory (EVT) models instead of single Gaussian covariance estimates

### Metrics
- Realized vs. model-predicted CVaR ratio (target: <1.5x)
- Stress-test drawdown vs. mandate limit
- Tail-risk factor exposure (% of portfolio in known tail-risk strategies)

### Alerts
- Realized/predicted CVaR ratio >2x → P1 (model risk review)
- Stress-test drawdown exceeds mandate by >10% → P1
- Tail-risk factor exposure >25% of portfolio → P2

---

## References

- [Standard Benchmarks Fail -- Auditing LLM Agents in Finance Must Prioritize Risk](https://arxiv.org/abs/2502.15865)
- [Agentic AI Systems Applied to tasks in Financial Services: Modeling and model risk management crews](https://arxiv.org/abs/2502.05439)
- [Toward Reliable Evaluation of LLM-Based Financial Multi-Agent Systems](https://arxiv.org/abs/2603.27539)
