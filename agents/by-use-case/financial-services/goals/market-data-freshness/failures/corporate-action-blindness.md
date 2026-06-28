# Corporate-Action Blindness

## Issue: Agent Fails to Adjust Prices, Positions, or Historical Series for Splits, Dividends, Mergers, or Spin-Offs

**Frequency**: Common

**Symptoms**
- Sudden, large "price drop" flagged as an anomaly when it is actually an unadjusted stock split or special dividend
- Historical return calculations show impossible jumps across a split or merger date
- Position quantity not updated after a spin-off, leaving the client's reported holdings incomplete
- Backtests trained on unadjusted price series produce systematically biased signals around action dates

**Root Cause**
Corporate actions (splits, dividends, mergers, spin-offs, ticker changes) require explicit adjustment logic applied to both historical series and live positions. Many data pipelines apply adjustments asynchronously or incompletely, and agents consuming "raw" feeds without action-aware adjustment treat the resulting discontinuities as genuine price moves or, worse, silently misstate position values.

**Example**
```
Scenario: Company executes a 4-for-1 stock split overnight
Agent's data feed: Price series not yet back-adjusted
Agent observes: Price drops from $400 to $100 "overnight"
Agent action: Flags as -75% crash, recommends emergency portfolio review
Reality: No change in position value; pure stock-split artifact
Impact: False alarm triggers unnecessary client outreach and erodes trust in the system
```

**Key Statistics**
- Unadjusted corporate-action artifacts are a recurring cause of false-positive anomaly alerts in market-data-driven agents
- Spin-off and merger events that are not fully reflected in position records cause position-value misstatements until manually reconciled, typically within 1-5 trading days in affected pipelines
- Backtests on unadjusted historical data around action dates show spurious volatility spikes that bias signal-generation models

---

## Mitigation Strategies

1. **Action-Aware Data Pipeline**: Source corporate-action calendars explicitly and apply back-adjustment to historical series before any backtest or signal generation
2. **Position Reconciliation on Action Dates**: Automatically reconcile position quantities and cost basis against custodian records on known action dates
3. **Anomaly Suppression Window**: Suppress price-anomaly alerts around confirmed corporate-action dates pending adjustment confirmation
4. **Action Calendar Cross-Check**: Cross-reference price discontinuities against a corporate-action calendar before flagging as anomalies

### Metrics
- % of corporate actions auto-adjusted within SLA (target: <1 trading day)
- False-positive anomaly rate attributable to unadjusted actions
- Position reconciliation lag after confirmed action events

### Alerts
- Price discontinuity >10% with no confirmed action match → P2 (investigate)
- Confirmed action not reflected in position records within 1 trading day → P1
- Backtest signal generation running on unadjusted series → P2

---

## References

- [Toward Reliable Evaluation of LLM-Based Financial Multi-Agent Systems](https://arxiv.org/abs/2603.27539)
- [Agentic AI Systems Applied to tasks in Financial Services: Modeling and model risk management crews](https://arxiv.org/abs/2502.05439)
