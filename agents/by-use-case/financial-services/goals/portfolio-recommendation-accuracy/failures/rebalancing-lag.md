# Rebalancing Lag in Portfolio Recommendations

## Issue: Agent Recommends Target Allocations but Fails to Account for Execution Lag, Letting Portfolios Drift Far From Target Before Rebalancing Triggers

**Frequency**: Common

**Symptoms**
- Actual portfolio weights drift 5-15% away from model's "target" allocation between rebalancing cycles
- Model's risk/return projections assume continuous rebalancing that never actually happens
- Tax-loss harvesting opportunities missed because rebalancing checks run on a fixed calendar schedule, not on drift thresholds
- Client portfolios carry unintended factor or sector tilts that accumulated silently since the last rebalance

**Root Cause**
Recommendation models typically output a static target allocation as if it is instantaneously and continuously maintained. In practice, rebalancing is batch-scheduled (monthly/quarterly) or threshold-triggered with operational lag (trade settlement, tax considerations, cash flow timing). The model's backtested performance assumes frictionless rebalancing, but live portfolios drift, and the agent has no mechanism to flag or quantify that drift against its own recommendation.

**Example**
```
Scenario: Target allocation = 60% equity / 40% bonds, rebalanced quarterly
Month 1: Equity rallies 12%, bonds flat
Actual drift by month 3: 68% equity / 32% bonds (8pp drift)
Model's risk dashboard: Still reports "60/40, moderate risk" (using target, not actual weights)
Market correction in month 3: Portfolio takes equity-level losses while client believes risk is moderate
Impact: Risk disclosure to client is stale; losses exceed disclosed risk band
```

**Key Statistics**
- Quarterly-rebalanced portfolios drift 5-10pp from target allocation on average during trending markets
- Threshold-based rebalancing (5% band) reduces tracking error vs. calendar-based rebalancing by 30-50%
- Risk dashboards using stale target weights instead of live actual weights misstate portfolio risk in 1 of every 4-5 client reviews in audited samples

**Contributing Factors**
- Calendar-based rather than drift-based rebalancing triggers
- No live reconciliation between model's stated target and custodian's actual holdings
- Tax-loss harvesting constraints delaying rebalancing trades beyond the model's assumed timeline

---

## Mitigation Strategies

1. **Drift-Threshold Rebalancing**: Trigger rebalancing on allocation drift bands (e.g., ±5%), not just calendar dates
2. **Live Weight Reconciliation**: Feed actual custodian holdings back into the risk dashboard, not the static target
3. **Drift-Aware Risk Disclosure**: Recompute and disclose risk metrics using actual current weights, flagging when drift exceeds materiality thresholds
4. **Tax-Aware Rebalancing Logic**: Model the tax cost of rebalancing trades explicitly rather than assuming frictionless execution

### Metrics
- Allocation drift (actual vs. target weight, pp)
- Time since last rebalance vs. drift-threshold breach
- Risk dashboard staleness (time since last reconciliation with actual holdings)

### Alerts
- Drift >7pp from target on any major asset class → P2
- Risk dashboard not reconciled with actual holdings in >30 days → P2
- Drift >10pp combined with market volatility spike → P1

---

## References

- [Agentic AI Systems Applied to tasks in Financial Services: Modeling and model risk management crews](https://arxiv.org/abs/2502.05439)
- [Agentic Trading: When LLM Agents Meet Financial Markets](https://arxiv.org/abs/2605.19337)
