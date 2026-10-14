# Financial Services AI Agent Failures by Goal: 50 Patterns, Causes, and Fixes

**Financial Services failures in AI agents are grouped here into 5 goals, each with a catalog of named failure patterns, the symptoms you will see, the root cause, and mitigations you can copy.** Start from the symptom you are debugging, pick the matching goal below, and open its failure list.

## Key Takeaways

- This use case covers 5 goals and 50 documented failure patterns.
- The largest goal is [Portfolio Recommendation Accuracy](portfolio-recommendation-accuracy/) with 18 patterns.
- Each goal page explains the failure class, how to tell it apart from its neighbors, and which mitigations apply across its patterns.
- Each failure page covers the symptoms, an example, the root cause, and how to fix it.

## Financial Services Goals

| Goal | What goes wrong | Patterns |
|---|---|---|
| [Data Quality](data-quality/) | Data quality failures in financial systems occur when agents ingest, cleanse, or propagate data containing misattributed entities, stale hierarchies, fabricated values | 8 |
| [Market Data Freshness](market-data-freshness/) | Market data freshness failures occur when agents rely on cached, stale, or asynchronously-delayed price data, corporate-action information, or reference rates without detecting staleness, leading to valuations, risk calculations | 4 |
| [Portfolio Recommendation Accuracy](portfolio-recommendation-accuracy/) | Portfolio recommendation failures happen across the full lifecycle: backtests trained on biased historical data (survivorship, look-ahead, recency, overfitting) produce inflated expected returns | 18 |
| [Regulatory Compliance](regulatory-compliance/) | Regulatory compliance failures in financial agents occur when agents apply rules that are outdated, jurisdiction-mismatched, or incompletely propagated across multi-agent handoffs | 9 |
| [Trading Execution](trading-execution/) | Trading execution failures occur when agents size, time, or route orders without modeling the actual cost and feasibility of execution, or when they misdiagnose what actually filled versus what was intended | 11 |

**Total: 50 patterns**

## Frequently Asked Questions

### Where do I start if my financial services agent is failing?

Match the symptom to a goal in the table above, then open that goal's page for how to tell its failures apart and where to look first. Each failure page ends in mitigations you can apply directly.

### How are these financial services failure patterns organized?

By goal: the outcome the agent is supposed to achieve. Under each goal, a `failures` folder holds one page per pattern. For the full picture see the [Financial Services overview](../).

## Related

- [Financial Services overview](../)
- [All agent failure patterns](../../../)
