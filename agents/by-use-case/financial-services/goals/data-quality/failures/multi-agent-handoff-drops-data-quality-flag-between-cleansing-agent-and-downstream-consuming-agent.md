# Multi-Agent Handoff Drops Data-Quality Flag Between Cleansing Agent and Downstream Consuming Agent

## Issue: A Data-Cleansing Agent Notes in Free Text That a Field It Cleaned Was Ambiguous or Low-Confidence, but the Structured Cleansed Record Handed Off to a Downstream Risk- or Pricing-Consuming Agent Has No Field for Cleansing Confidence, So the Downstream Agent Treats the Value as Fully Reliable

**Frequency**: Occasional

**Symptoms**
- A downstream risk or pricing calculation uses a cleansed field value with full confidence, even though the data-cleansing agent's own notes describe that field as ambiguous, inferred, or resolved by a low-confidence heuristic rather than a clean source match
- The structured cleansed record handed off to the downstream consuming agent contains the field's final value and a "cleansed" status flag, but no field capturing the cleansing agent's confidence level or method (direct source match vs. inferred/imputed)
- Downstream agents operating purely from the structured cleansed record show a materially higher reliance rate on low-confidence-cleansed fields than agents given the cleansing agent's full reasoning transcript alongside the record
- The low-confidence origin of a field surfaces only when a risk or valuation output is later challenged and a reviewer traces the field back through the cleansing agent's transcript, by which point the output has already been used downstream
- The mismatch concentrates on fields where the cleansing agent had to choose among multiple plausible source values or infer a value from a partial record, since those are the cases where a confidence distinction would matter most

**Root Cause**
The downstream consuming agent's logic operates on the structured cleansed record's fixed schema, and that schema was built to track whether a field was cleansed and what its final value is, not the confidence or method behind that cleansing. Because a low-confidence resolution is expressed through the cleansing agent's free-text reasoning rather than a structured confidence field, it has no corresponding place in the handoff schema and is therefore invisible to the downstream agent, even though the same model, given the full cleansing transcript, would readily flag the value as uncertain.

**Example**
```
Data-cleansing agent reconciles a corporate bond's maturity date across two source feeds that show different values, and notes in free text: "Feeds disagree by 6 months; resolved to the later date based on a pattern match to the issuer's typical amortization schedule, not a confirmed source value"
Cleansing agent records the resolved maturity date in the structured cleansed record with status "cleansed," with no field for resolution confidence or method
Structured record handed off to a downstream risk-duration agent shows the maturity date as cleansed, with no indication it was inferred rather than source-confirmed
Risk-duration agent uses the inferred maturity date with full confidence in a portfolio duration calculation
Discrepancy surfaces during a quarterly model-validation review when the actual maturity date, confirmed from the bond's prospectus, differs from the inferred value used in the duration calculation
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Surveys of multi-agent LLM system failures identify narrow handoff interfaces between staged agents, where a downstream agent's structured input omits a confidence or provenance signal an upstream agent's free-text reasoning surfaced, as a distinct and recurring failure category | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Platform-orchestrated agentic workflow failure studies find that narrowing the interface between orchestrated stages to a fixed value-plus-status schema is a primary mechanism by which a confidence or method signal present upstream fails to reach a downstream consuming stage | [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735) |
| Research on agentic AI applied to financial-services modeling and model-risk-management tasks identifies the absence of a shared, confidence-aware structured state between sequential cleansing and consuming agents as a distinct reliability gap from either agent's individual accuracy | [Agentic AI Systems Applied to tasks in Financial Services: Modeling and model risk management crews](https://arxiv.org/abs/2502.05439) |

**Contributing Factors**
- Structured cleansed-record schema tracks only final field value and cleansed/not-cleansed status, with no field for resolution confidence or method
- Cleansing agent's reasoning about ambiguous or inferred resolutions is recorded only in free-text notes, with no structured escalation path into the downstream consuming agent's input
- No mandatory flag or hold is triggered in downstream calculations when the cleansing agent's free-text notes contain low-confidence or inference language, since the consuming agent's logic does not parse those notes

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
- [Agentic AI Systems Applied to tasks in Financial Services: Modeling and model risk management crews](https://arxiv.org/abs/2502.05439)
