# Multi-Agent Handoff Drops Stale-Feed Flag Between Ingestion Agent and Valuation Agent

## Issue: A Market-Data Ingestion Agent Notes in Free Text That a Price Feed Showed No Update Across an Unusually Long Window and May Be Stale, but the Structured Price Record Handed Off to the Downstream Valuation Agent Has No Field for Staleness Suspicion, So the Valuation Agent Treats the Last Received Price as Current

**Frequency**: Common

**Symptoms**
- A position's valuation uses a price the ingestion agent's own notes flagged as suspiciously unchanged across an unusually long window, with no staleness field carried into the structured price record consumed by the valuation agent
- The structured handoff between ingestion and valuation agents contains only the last price and its nominal timestamp, with no field for a staleness suspicion the ingestion agent's free-text monitoring notes raised about that same price
- Valuation agents operating purely from the structured price record show a materially higher reliance rate on suspected-stale prices than valuation agents given the ingestion agent's full monitoring transcript alongside the record
- The staleness is discovered only when a separate reference feed or end-of-day reconciliation shows the price should have moved, by which point the valuation has already been published or used in a risk calculation
- The mismatch concentrates on lower-liquidity instruments and after-hours windows, where an unchanged price is more likely to be genuinely stale rather than a genuinely flat market, and where the ingestion agent's staleness suspicion is least likely to be cross-checked downstream

**Root Cause**
The valuation agent's pricing logic consumes only the structured price record produced by the ingestion stage, and that record was built to carry the latest price and timestamp, not whether the ingestion agent's own monitoring flagged the feed as suspiciously unchanged. Because a staleness suspicion is expressed through the ingestion agent's free-text monitoring notes rather than a structured staleness field, it has no corresponding place in the handoff schema and is therefore invisible to the valuation agent, even though the same model, given the ingestion transcript, would readily flag the price as suspect.

**Example**
```
Market-data ingestion agent monitors a thinly traded corporate bond's price feed and notes in free text: "Price unchanged for 14 consecutive updates over 6 hours during active trading hours -- unusual for this instrument, possible feed staleness"
Ingestion agent passes the structured price record to the valuation pipeline showing the last price and its nominal timestamp, with no staleness field
Valuation agent consumes the structured record, treats the price as current, and publishes the day's mark using it
Independent reference feed, checked during a later reconciliation, shows the bond actually traded twice during the unchanged window at materially different prices
Published mark is found to be stale, triggering a restatement and a review of risk exposure calculated off the incorrect valuation
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Surveys of multi-agent LLM system failures identify narrow handoff interfaces between staged agents, where a downstream agent's structured input omits a signal an upstream agent's free-text monitoring surfaced, as a distinct and recurring failure category | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Platform-orchestrated agentic workflow failure studies find that narrowing the interface between orchestrated stages to a fixed value-plus-timestamp schema is a primary mechanism by which a staleness or data-quality signal present upstream fails to reach a downstream consuming stage | [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735) |
| Research on agentic trading systems identifies the absence of a shared, continuously synced structured state between data-ingestion and valuation stages as a distinct reliability gap from either stage's individual pricing accuracy | [Agentic Trading: When LLM Agents Meet Financial Markets](https://arxiv.org/abs/2605.19337) |

**Contributing Factors**
- Structured price-record schema tracks only last price and nominal timestamp, with no field for a staleness suspicion raised during ingestion monitoring
- Ingestion agent's staleness monitoring output is recorded only in free-text notes, with no structured escalation path into the valuation agent's input
- No mandatory hold or flag is triggered in the valuation pipeline when the ingestion agent's free-text notes contain staleness-suspicion language, since the valuation agent's logic does not parse those notes

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

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735)
- [Agentic Trading: When LLM Agents Meet Financial Markets](https://arxiv.org/abs/2605.19337)
