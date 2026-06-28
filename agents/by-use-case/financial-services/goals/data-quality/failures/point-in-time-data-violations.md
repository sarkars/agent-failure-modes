# Point-in-Time Data Violations

## Issue: Backtests and Live Recommendations Use Data That Was Not Actually Available at the Decision Timestamp (Look-Ahead via Restated/Revised Data)

**Frequency**: Common

**Symptoms**
- Backtest performance looks strong but degrades sharply in live trading
- Financial statement data used in a historical simulation reflects later restatements, not the originally reported (and often erroneous) figures
- Index membership or credit ratings applied retroactively as of "today's" classification rather than the classification in effect at the historical date
- Earnings estimates in a backtest use the final/actual consensus rather than the estimate that existed before the print

**Root Cause**
Most fundamental and reference datasets are stored "as of latest" rather than "as of the point in time the user is replaying." Database joins on company identifiers without point-in-time versioning silently substitute current (more accurate, later-revised) data into historical scenarios, inflating backtest performance because the model is implicitly using information it could not have had on that date.

**Example**
```
Scenario: Earnings-surprise trading strategy backtest, 2018-2024
Database: Vendor's "actuals" table reflects most recent restated EPS figures
Original 2019 print: Company reported EPS = $1.10 (later restated to $0.85)
Backtest signal: Computed using restated $0.85 figure, "predicting" the eventual restatement
Backtest result: Strategy shows alpha that depends on info unavailable at trade time
Impact: Live deployment underperforms backtest by a wide margin because the live data is, correctly, not yet restated
```

**Key Statistics**
- Point-in-time data violations are among the most common causes of backtest-to-live performance decay cited in quant research post-mortems
- Restatement rates for reported financials are non-trivial across multi-year samples, meaning a meaningful fraction of historical "actuals" differ from what was originally available
- Properly point-in-time-versioned datasets have been shown to materially reduce overstated backtest Sharpe ratios versus "latest snapshot" datasets

---

## Mitigation Strategies

1. **Point-in-Time Database Architecture**: Store every data revision with an "as-of" and "knowledge date" timestamp; query strictly by knowledge date during backtests
2. **Vendor Audit**: Verify whether market-data vendors provide true point-in-time history or "latest restated" snapshots before relying on them for backtests
3. **Restatement Flagging**: Explicitly flag and separately analyze the impact of any restated fields used in historical signal construction
4. **Live/Backtest Parity Checks**: Periodically replay recent live decisions through the backtest pipeline to confirm identical data was available at both times

### Metrics
- % of backtest data fields confirmed point-in-time versioned
- Backtest-to-live performance decay (Sharpe ratio delta)
- Count of restated fields detected in backtest dataset

### Alerts
- Backtest uses a non-point-in-time-versioned data source for a production strategy → P1
- Backtest-to-live Sharpe decay exceeds 50% → P2 (investigate data leakage)

---

## References

- [Toward Reliable Evaluation of LLM-Based Financial Multi-Agent Systems](https://arxiv.org/abs/2603.27539)
- [Standard Benchmarks Fail -- Auditing LLM Agents in Finance Must Prioritize Risk](https://arxiv.org/abs/2502.15865)
