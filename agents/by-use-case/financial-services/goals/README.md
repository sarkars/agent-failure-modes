# Financial Services AI Agent Failures by Goal: 50 Patterns, Causes, and Fixes

**Financial Services AI agents fail in 5 distinct ways, grouped by the goal each failure breaks.** Find the goal that matches what you are seeing, open its list, and use the fix on each pattern page.

## Key Takeaways

- 50 documented patterns across 5 goals; the most documented is [Portfolio Recommendation Accuracy](portfolio-recommendation-accuracy/) with 18.
- Each pattern page gives the symptoms, an example, the root cause, and mitigations.

## Financial Services Goals

| Goal | When it fails | Patterns |
|---|---|---|
| [Data Quality](data-quality/) | When agents ingest, cleanse, or propagate data containing misattributed entities, stale hierarchies, fabricated values, or unresolved ambiguities—and pass that corrupted data downstream to pricing | 8 |
| [Market Data Freshness](market-data-freshness/) | When agents rely on cached, stale, or asynchronously-delayed price data, corporate-action information, or reference rates without detecting staleness, leading to valuations, risk calculations | 4 |
| Portfolio Recommendation Accuracy | Portfolio recommendation failures happen across the full lifecycle: backtests trained on biased historical data (survivorship, look-ahead, recency, overfitting) produce inflated expected returns | 18 |
| [Regulatory Compliance](regulatory-compliance/) | When agents apply rules that are outdated, jurisdiction-mismatched, or incompletely propagated across multi-agent handoffs | 9 |
| [Trading Execution](trading-execution/) | When agents size, time, or route orders without modeling the actual cost and feasibility of execution, or when they misdiagnose what actually filled versus what was intended | 11 |

**Total: 50 patterns**

## Frequently Asked Questions

### Can a better backtest eliminate look-ahead and survivorship bias without changing the data preparation?

No. See Portfolio Recommendation Accuracy.

### Can a better slippage model fix underestimation without changing how orders are sized and timed?

Partially. See Trading Execution.

### What is the difference between multi-jurisdiction conflict and regulatory-rule outdatedness?

Outdatedness: a single rule has changed in a single jurisdiction (old rule: 50% leverage; new rule: 30% leverage), and the agent applies the old rule. See Regulatory Compliance.

## Related

- [Financial Services overview](../)
- [All agent failure patterns](../../../)
