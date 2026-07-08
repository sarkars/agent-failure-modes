# Corporate Hierarchy Misattribution

## Issue: Agent Attributes Risk, Exposure, or Performance Data to the Wrong Entity Within a Corporate Family Due to Incomplete Parent-Subsidiary Mapping

**Frequency**: Common

**Symptoms**
- Credit risk or exposure aggregation treats a subsidiary as an independent counterparty, missing concentration risk that should be aggregated at the ultimate parent level
- A subsidiary's financial distress signal is not propagated to the risk assessment of sibling subsidiaries or the parent, even when cross-default or guarantee provisions link them
- Ticker/entity resolution incorrectly merges or splits financial data between a parent and subsidiary that share similar names, attributing performance or news to the wrong entity in the hierarchy
- Recently completed mergers, spin-offs, or restructurings are not reflected in the hierarchy mapping promptly, causing exposure calculations to use a stale corporate structure

**Root Cause**
Corporate hierarchies are dynamic — entities merge, spin off, get acquired, and restructure — and accurately mapping exposure or risk to "the right entity" requires maintaining a current, complete parent-subsidiary-affiliate graph rather than treating each named counterparty as independent. Agents that resolve counterparties by name or ticker alone, without maintaining and continuously updating this hierarchy graph, will misattribute risk whenever the named entity is part of a larger structure whose relationships are not reflected in the data the agent is using.

**Example**
```
Scenario: Bank holds credit exposure to three separate subsidiaries of the same parent conglomerate, each booked as an independent counterparty
Risk aggregation: Computes single-name concentration limits per subsidiary, treating each as unrelated
Actual risk: All three subsidiaries are linked by parent guarantees and would likely default together in a parent-level distress scenario
True aggregated exposure: Exceeds the single-counterparty concentration limit when correctly rolled up to the parent
Risk system: Reports each subsidiary's exposure as within limits because the parent-level aggregation was never computed
Impact: Concentration risk is understated; a parent-level distress event would produce correlated losses across all three "independent" exposures simultaneously
```

**Key Statistics**
- Failure to aggregate exposure at the ultimate parent/beneficial-owner level (rather than at the immediate legal-entity level) is a recurring supervisory finding in credit risk management reviews
- Entity resolution errors involving similarly-named parent/subsidiary pairs are a documented data quality issue in financial reference data management
- Large-scale corporate restructuring events (M&A, spin-offs) create a documented lag window during which legacy hierarchy data remains in active use before being corrected, during which misattribution risk is elevated

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

- [FinVault: Benchmarking Financial Agent Safety in Execution-Grounded Environments](https://arxiv.org/pdf/2601.07853)
- [Position: Standard Benchmarks Fail – LLM Agents Present Overlooked Risks](https://www.arxiv.org/pdf/2502.15865v1)
