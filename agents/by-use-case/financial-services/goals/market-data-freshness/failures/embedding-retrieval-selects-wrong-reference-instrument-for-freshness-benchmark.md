# Embedding Retrieval Selects Wrong Reference Instrument for Freshness Benchmark

## Issue: A Market-Data Freshness-Monitoring Agent Checking Whether an Illiquid Instrument's Price Is Plausibly Current Selects a "Comparable" Reference Instrument Using Embedding Similarity Over Free-Text Descriptions Rather Than Matching on Sector, Duration, and Credit-Quality Attributes, Producing a Freshness Benchmark That Moves Differently From the Instrument Being Checked

**Frequency**: Occasional

**Symptoms**
- An illiquid instrument's unchanged price is judged "plausibly current" against a reference instrument's price movement, even though the reference instrument differs materially in sector, duration, or credit quality from the instrument being checked
- The agent's reference-instrument selection is driven by a similarity match over free-text instrument descriptions, not by matching structured attributes such as sector classification, duration bucket, or credit-rating tier
- Auditing the selected reference instrument against the structured attributes of the instrument being checked shows a mismatch on at least one attribute that materially affects expected price co-movement
- The freshness check passes (reference instrument also appears unchanged or moved similarly) at a rate inconsistent with how often the reference instrument and the checked instrument actually share the structured attributes that would make their price movements comparable
- The mismatch concentrates on instruments with generic or sparse free-text descriptions, since those produce the least attribute-specific embedding signal and the highest chance of a superficially similar but structurally unrelated match

**Root Cause**
Selecting a comparable reference instrument by embedding similarity over free-text descriptions optimizes for the most textually similar description, not for confirming that two instruments share the structured attributes that actually drive correlated price movement. When an illiquid instrument's description is generic or sparse, the similarity signal driving the match does not distinguish a textually similar but structurally unrelated instrument from a true comparable, so the freshness benchmark ends up comparing the checked instrument's lack of price movement against an instrument that was never expected to move similarly in the first place.

**Example**
```
Freshness-monitoring agent checks an illiquid municipal bond's unchanged price over a multi-day window against a "comparable" reference instrument selected by embedding similarity over instrument descriptions
Selected reference instrument shares similar descriptive language ("revenue bond," "infrastructure") but differs materially in duration (3 years longer) and credit tier (one notch lower) from the checked bond
Reference instrument's price also happened to be flat over the same window, so the agent concludes the checked bond's unchanged price is plausibly current
Independent reconciliation, using a reference instrument matched on duration bucket and credit tier rather than description similarity, shows that a true comparable moved materially during the window
Checked bond's price is later found to have been stale; the freshness check's reference-instrument selection had compared it against an instrument that was never expected to co-move with it
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Retrieval-augmented and similarity-based matching systems are documented to surface a taxonomy of retrieval errors distinct from generation errors, including matching a topically or lexically similar but substantively unrelated record when similarity search is used in place of structured-attribute matching | [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1) |
| Knowledge-oriented retrieval-augmented generation surveys identify attribute-based disambiguation across structurally similar candidates as a distinct reliability challenge from single-source retrieval accuracy | [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677) |
| Research on agentic trading systems identifies comparable-instrument selection grounded in structured attributes, rather than free-text description similarity, as a distinct requirement for benchmarking illiquid-instrument pricing | [Agentic Trading: When LLM Agents Meet Financial Markets](https://arxiv.org/abs/2605.19337) |

**Contributing Factors**
- Reference-instrument selection for freshness benchmarking is performed via description-embedding similarity rather than matching on sector, duration bucket, and credit-rating tier
- No validation step confirms the selected reference instrument shares the structured attributes that drive comparable price movement before it is used as a freshness benchmark
- Instruments with generic or sparse free-text descriptions are not flagged for mandatory structured-attribute matching when an embedding-similarity reference selection is used

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
- [Agentic Trading: When LLM Agents Meet Financial Markets](https://arxiv.org/abs/2605.19337)
