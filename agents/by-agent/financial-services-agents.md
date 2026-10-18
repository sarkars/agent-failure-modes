# Financial Services Agents: Business Goals, Failure Patterns, and Fixes

**Financial Services Agents fail along 5 goals: Portfolio Recommendation Accuracy, Trading Execution, Regulatory Compliance carry the most documented failures.** This page maps each goal to the failures that threaten it, so you can decide what to protect first and where the fixes are.

## Key Takeaways

- 50 documented failure patterns across 5 goals. What it does: analyze portfolios, check compliance, and support trading and data-heavy decisions.
- The most documented goal is [Portfolio Recommendation Accuracy](../by-use-case/financial-services/goals/portfolio-recommendation-accuracy/) with 18 patterns.
- Frequencies below are as recorded on each pattern page. They are not measured rates.
- Business-goal definitions (metric, baseline, owner, what counts as a failure) are not written yet for this agent. Define them before choosing which patterns to prioritize.

## Goals this agent must protect

| Goal | When it fails | Patterns |
|---|---|---|
| [Portfolio Recommendation Accuracy](../by-use-case/financial-services/goals/portfolio-recommendation-accuracy/) | Portfolio recommendation failures happen across the full lifecycle | 18 |
| [Trading Execution](../by-use-case/financial-services/goals/trading-execution/) | When agents size, time, or route orders without modeling the actual cost and feasibility of execution | 11 |
| [Regulatory Compliance](../by-use-case/financial-services/goals/regulatory-compliance/) | When agents apply rules that are outdated, jurisdiction-mismatched | 9 |
| [Data Quality](../by-use-case/financial-services/goals/data-quality/) | When agents ingest, cleanse, or propagate data containing misattributed entities | 8 |
| [Market Data Freshness](../by-use-case/financial-services/goals/market-data-freshness/) | When agents rely on cached, stale, or asynchronously-delayed price data | 4 |

## Failures most often recorded

| Failure | What goes wrong | Recorded frequency |
|---|---|---|
| [Benchmark Misalignment in Portfolio Recommendations](../by-use-case/financial-services/goals/portfolio-recommendation-accuracy/failures/benchmark-misalignment.md) | Model Optimizes Against a Generic Benchmark That Does Not Match the Client's Actual Risk Profile, Goals, or Constraints | Very Common |
| [Correlation Breakdown in Portfolio Diversification](../by-use-case/financial-services/goals/portfolio-recommendation-accuracy/failures/correlation-breakdown.md) | Assumed Diversification Fails When Correlations Spike (Tail Dependence Not Captured) | Very Common |
| [Look-Ahead Bias in Backtests](../by-use-case/financial-services/goals/portfolio-recommendation-accuracy/failures/look-ahead-bias.md) | Model Uses Future Information in Backtest That Wouldn't Be Available in Real-Time Trading | Very Common |
| [Overfitting to Historical Market Regime](../by-use-case/financial-services/goals/portfolio-recommendation-accuracy/failures/overfitting-to-market-regime.md) | Model Optimized for Historical Regime (Bull Market) Fails in Regime Change (Bear Market, Stagflation) | Very Common |
| [Recency Bias in Portfolio Recommendations](../by-use-case/financial-services/goals/portfolio-recommendation-accuracy/failures/recency-bias.md) | Model Overweights Recent Performance; Recommends Assets That Performed Well Recently but Are Mean-Reverting | Very Common |
| [Slippage Underestimation in Trading Execution](../by-use-case/financial-services/goals/trading-execution/failures/slippage-underestimation.md) | Execution Agent's Pre-Trade Cost Model Systematically Understates Realized Slippage, Especially for Larger or Illiquid Orders | Very Common |

## Before you build: define each goal

For every goal in the table, write down: the metric and how you measure its baseline today; the person who owns it; what counts as a failure and how severe it is; who is told when it happens; and when a person takes over. Then use the failures above as your test list.

## Human-side failures

Because this agent talks to customers or patients, also check conversation-level failures: tone, handoff to a person, refusals, and choosing the wrong channel. See the [human-machine interface section](../by-capability/human-machine-interface/).

## Security and governance

Every agent also needs the cross-cutting checks in [security](../cross-cutting/security/), [accuracy](../cross-cutting/accuracy/), [governance](../cross-cutting/governance/), and [operations](../cross-cutting/operations/).

## Frequently Asked Questions

### What fails most often in financial services agents?

The most documented goal is Portfolio Recommendation Accuracy (18 patterns). The failures table above lists the ones recorded as most frequent. These are the library's records, not measured rates.

### Where should I start when building financial services agents?

Define your business goals and what counts as failure, then test against the failure patterns for each goal. The section above lists what to write down.

## Related

- [All agents by business goal](./)
