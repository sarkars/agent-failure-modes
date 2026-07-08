# Unvalidated Truncated Reference-Data Batch Query Certified as Fully Cleansed

## Issue: A Data-Quality Agent Running a Batch Validation Pass Against a Reference-Data Source (a Security Master, an Issuer Registry) to Cleanse a Set of Records Receives a Row-Capped or Paginated Query Result Covering Only Part of the Requested Record Set, and Certifies the Entire Batch as "Validated, No Discrepancies Found" Based on That Partial Result, Without Checking the Returned Row Count Against the Number of Records Actually Submitted for Validation

**Frequency**: Common

**Symptoms**
- Cleansing-pass certification states "batch validated, zero discrepancies" while the underlying reference-data query actually returned validation results for only a fraction of the submitted records
- The reference-data source's response includes a returned-row-count field or pagination cursor showing fewer rows came back than were submitted, but the agent's certification step does not check for or surface this gap
- Records omitted from the truncated response are absent from the discrepancy list entirely, rather than being flagged as "not validated," so downstream consumers cannot distinguish "checked and clean" from "never actually checked"
- Re-running the identical batch query with explicit pagination handling (reconciling returned row count against submitted row count and following every cursor to exhaustion) surfaces validation results for the omitted records, some of which contain genuine discrepancies the original pass never saw
- The failure recurs specifically on large batch submissions (full security-master refreshes, newly onboarded fund's complete holdings list), since those are the submissions most likely to exceed a single page or row cap on the reference-data source's query interface

**Example**
```
Data-quality agent runs a nightly cleansing pass validating sector classification, country of risk, and issuer identifiers for a batch of 8,000 newly onboarded security records against an external reference-data registry
Registry's batch-query API returns validation results for the first 6,500 records due to a per-call row cap, along with a "rows_returned: 6500, rows_submitted: 8000" field and a pagination cursor
Agent's certification, generated directly from the 6,500 returned results, states "batch validated: 8,000 records reviewed, 12 discrepancies flagged" -- the count claimed (8,000) does not match what was actually returned and checked (6,500), and the 1,500 omitted records are simply absent from the discrepancy list rather than marked unchecked
Among the 1,500 never-actually-validated records is a security with an incorrect country-of-risk classification that drives an exposure-limit calculation; the misclassification is only caught weeks later when a risk report shows an unexplained limit breach
Re-running the batch query with the pagination cursor followed to exhaustion immediately surfaces the country-of-risk discrepancy for that security, confirming it was never actually checked in the original "fully validated" pass
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| LLM agents frequently assert task completion (here, "batch validated") based on the apparent shape of a returned result rather than verifying the result reflects the complete requested scope, a pattern documented as false success driven by surface-level closing signals rather than ground-truth verification | [From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents](https://arxiv.org/html/2606.09863) |
| Tool-use error detection research finds agents frequently fail to treat an incomplete, capped, or paginated tool result as a distinct error condition requiring follow-up, instead generating output as if a complete result had been returned | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Agent-environment interaction failure research documents that agents frequently act on a tool's returned result without verifying it matches the scope of the original request, treating any successful API call as evidence of task completion regardless of completeness | [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504) |

**Contributing Factors**
- No explicit instruction or guardrail requires the agent to reconcile a reference-data query's returned row count against the submitted row count, or to follow pagination cursors to exhaustion, before issuing a batch-validation certification
- Large batch submissions are exactly the cases most likely to need a full cleansing pass and also the cases most likely to exceed a single page or row cap on the reference-data source's query interface, compounding the risk
- The certification output format has no field distinguishing "checked and clean" from "not actually returned by the query," so an omitted record is indistinguishable from a confirmed-clean one
- Pagination and row-cap handling for reference-data batch queries is treated as a generic engineering concern rather than a data-quality-critical control, so it is not consistently enforced across every reference-data integration

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

- [From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents](https://arxiv.org/html/2606.09863)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504)
