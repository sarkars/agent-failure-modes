# Embedding Retrieval Merges Similarly Named Issuer Entities in Data-Cleansing Pipeline

## Issue: A Data-Quality Agent Deduplicating Issuer Records Across Multiple Source Feeds Using Embedding Similarity Over Issuer Names, Rather Than Matching on a Unique Identifier Such as LEI or CUSIP Issuer Code, Merges Two Distinct Issuer Entities With Coincidentally Similar Names Into a Single Record, Corrupting Downstream Holdings and Exposure Calculations

**Frequency**: Occasional

**Symptoms**
- A single-issuer concentration-limit breach appears in the exposure report even though neither of the two underlying, genuinely distinct issuers individually holds a position anywhere near the limit
- Pulling either source feed's LEI or issuer code for the merged record shows two different identifiers, not one -- the merge has no identifier-level basis, only a name match
- Issuers most likely to collide are the ones whose names recur by construction: a parent that spun off a similarly-named affiliate, or a regional holding-company naming convention (e.g. "[Region] [Sector] Holdings") shared by otherwise unrelated groups
- Nothing in the merged record's formatting distinguishes it from a legitimately deduplicated one -- the pipeline does not tag records as "matched by name" versus "matched by identifier," so the merge looks authoritative downstream
- A compliance reviewer only catches the error by working backward from an exposure number that doesn't reconcile with either issuer's standalone filings, not from any signal the pipeline itself raised

**Root Cause**
The deduplication step scores candidate issuer pairs by embedding distance over the name string alone, so its notion of "same issuer" is really "textually closest name in the other feed" -- there is no step that requires the match to also agree on LEI, CUSIP, or another registry-backed identifier before the merge executes. This is a bond-specific failure mode: emerging-markets and holding-company issuer names are drawn from a small vocabulary of sector and geography terms, so the embedding space places unrelated issuers close together far more often than it does for, say, unique corporate legal names in a developed-markets equity universe, and the pipeline's confidence threshold was tuned against the latter, not the former.

**Example**
```
Data-quality agent reconciles issuer records from a custodian feed and a third-party reference-data feed for an emerging-markets bond portfolio
Custodian feed lists "Northbridge Energy Holdings Ltd"; reference-data feed separately lists "Northbridge Energy Ltd," a distinct, unrelated issuer with a different LEI and no corporate relationship to the first
Agent's embedding-similarity matching merges the two records into a single issuer entry based on name similarity alone
Combined exposure report shows a single issuer position that breaches the portfolio's single-issuer concentration limit, when neither underlying issuer individually breaches it
Risk reviewer flags the apparent breach, only to discover on identifier-level investigation that the two distinct issuers were incorrectly merged
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Retrieval-augmented and similarity-based matching systems are documented to surface a taxonomy of retrieval errors distinct from generation errors, including matching a topically or lexically similar but substantively unrelated record when similarity search is used in place of identifier-based lookup | [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1) |
| Knowledge-oriented retrieval-augmented generation surveys identify entity disambiguation across heterogeneous data sources as a distinct reliability challenge from single-source retrieval accuracy | [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677) |
| Research on agentic AI applied to financial-services modeling and model-risk-management tasks identifies entity-identity resolution as a distinct reliability requirement separate from the accuracy of downstream financial calculations | [Agentic AI Systems Applied to tasks in Financial Services: Modeling and model risk management crews](https://arxiv.org/abs/2502.05439) |

**Contributing Factors**
- Issuer deduplication across source feeds is performed via name similarity rather than LEI, CUSIP issuer code, or another unique identifier
- No validation step confirms a matched pair of records shares a unique identifier or a documented corporate relationship before they are merged into a single issuer entity
- Sectors or regions with high issuer name-collision rates are not flagged for mandatory identifier-based verification before similarity matching is trusted

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

- [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1)
- [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677)
- [Agentic AI Systems Applied to tasks in Financial Services: Modeling and model risk management crews](https://arxiv.org/abs/2502.05439)
