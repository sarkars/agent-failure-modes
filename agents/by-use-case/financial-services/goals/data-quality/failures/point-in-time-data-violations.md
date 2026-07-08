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

### Prevention

1. **Implement multi-layer entity resolution with hierarchy validation**: Maintain a master entity reference database with parent-subsidiary relationships, guaranteed updater, transaction account mappings. Use persistent unique identifiers (LEI, ISIN, internal ID) instead of name-based matching. On every exposure lookup, resolve through hierarchy graph and validate against current regulatory filings. Root cause: Ensures exposure always attributed to correct legal entity accounting for corporate structure changes.

2. **Establish regulatory compliance gates with before/after checks**: Before any trading decision or exposure update, verify: (1) Counterparty regulatory status (sanctions check, credit rating current), (2) Position size vs. single-name concentration limit at ultimate parent level, (3) Exposure vs. concentration risk limits across correlated counterparties. Abort if any gate fails. Root cause: Prevents trades that violate compliance rules by checking compliance before execution.

3. **Implement market data freshness validation with latency bounds**: Every market data feed includes timestamp. Before using data for decisions, verify: (1) Timestamp within acceptable age (e.g., <30s for prices, <1d for ratings), (2) Data not marked as stale by upstream provider, (3) Cross-feed consistency check (e.g., bid-ask spread reasonable). Reject stale/inconsistent data with alert. Root cause: Prevents decisions based on outdated market information.

### Detection & Response

1. **Exposure aggregation audit with parent-level rollup**: Daily batch job re-computes all exposure aggregations at ultimate parent level from scratch (not incremental). Compares against operational system. Flags: (1) Missing hierarchy mappings, (2) Exposure misattributed to legal entity instead of parent, (3) Concentration violations only visible at parent level. Reports with detailed reconciliation.

2. **Regulatory compliance violation detection**: Monitor all executed trades against post-hoc compliance checks. Flag violations: (1) Counterparty now in breach of sanctions/credit triggers after trade, (2) Concentration limit exceeded at parent level, (3) Position size violates regulatory limits for entity type. Generate audit trail for each violation with decision data.

### Architecture Patterns

1. Corporate Hierarchy Graph Service: Maintains versioned parent-subsidiary-guarantee relationships. API: resolve_to_parent(entity_id, as_of_date) -> parent_id + risk_correlation. Fetches from regulatory filings (daily), M&A feeds (real-time), credit data (weekly). Triggers recomputation on family structure changes. Serves through cache with fallback to DB.

2. Pre-Trade Compliance Engine: Rule engine evaluates every proposed trade against: sanctions checks, concentration limits (computed at parent + correlated entities), regulatory position size limits, data freshness gates. Blocks non-compliant trades with detailed audit log of which rule failed why.

3. Market Data Freshness Orchestrator: Aggregates feeds from multiple market data providers with explicit 'as of' timestamps. Computes data freshness for each field (bid, ask, last_traded, credit_spread). Feeds below threshold age marked as 'stale'. Risk system rejects decisions using stale feeds with incident log.

### Key Metrics

| Metric | Target | Alert Threshold | Measurement Method |
|--------|--------|-----------------|--------------------|
| Parent-Level Aggregation Accuracy | >99.5% | <99% | Percentage of counterparty exposure correctly rolled up to ultimate parent vs. attributed to legal entity only |
| Hierarchy Graph Staleness (Post-Restructuring) | <7 days | >14 days | Max time between corporate restructuring announcement and hierarchy graph update for known counterparties |
| Compliance Gate Pass Rate | 99.9% | <99.5% | Percentage of proposed trades passing all pre-trade compliance checks |
| Market Data Freshness Compliance | >98% | <95% | Percentage of market data points within acceptable age bounds before use in decisions |
| Post-Trade Violation Detection Rate | >95% | <90% | Percentage of actual compliance violations caught by post-trade audit vs. total violations |

### Alerts & Escalation

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Parent-Level Concentration Breach | Ultimate parent exposure exceeds concentration limit while legal-entity-level exposures individually within limits | CRITICAL | Halt new trades to counterparty family; escalate to risk committee; generate audit report |
| Stale Hierarchy on Restructuring | Known M&A/spin-off event affecting held counterparty with no hierarchy update >7 days | HIGH | Page data team; trigger priority hierarchy refresh; mark affected counterparties for manual review |
| Stale Market Data in Decision | Market data >30s old used for pricing decision, or >1d old used for risk assessment | HIGH | Reject decision; alert trader; log incident with full decision trace for audit |


## References

- [Toward Reliable Evaluation of LLM-Based Financial Multi-Agent Systems](https://arxiv.org/abs/2603.27539)
- [Standard Benchmarks Fail -- Auditing LLM Agents in Finance Must Prioritize Risk](https://arxiv.org/abs/2502.15865)
