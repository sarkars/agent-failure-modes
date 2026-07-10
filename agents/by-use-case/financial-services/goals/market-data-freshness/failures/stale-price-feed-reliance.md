# Stale Price Feed Reliance

## Issue: Agent Generates Recommendations or Risk Calculations Using Cached or Delayed Price Data Without Detecting Staleness

**Frequency**: Very Common

**Symptoms**
- Risk and recommendation outputs reference prices that are minutes-to-hours old during fast-moving markets
- Agent does not surface a "data as of" timestamp prominently, or surfaces an inaccurate one
- Thinly traded or after-hours assets show last-traded prices used as if they were live, masking large moves
- Discrepancies appear between the agent's stated price and the actual executable price at trade time

**Root Cause**
Many market-data integrations cache prices for performance or cost reasons, or fail over silently to a secondary feed with different latency characteristics. Agents built to "always answer" will report the last value retrieved rather than checking feed staleness or feed-source health, and rarely surface uncertainty when an upstream feed has stopped updating.

**Example**
```
Scenario: Agent recommends rebalancing trade using a cached equity price 45 minutes old
Market event: Earnings surprise drops the stock -18% intraday
Agent's risk calc: Uses pre-drop price, shows "no rebalancing needed"
Actual market: Position is now significantly underweight target risk band
Impact: Client misses a rebalancing window; realized loss exceeds what timely data would have flagged
```

**Key Statistics**
- Feed staleness incidents (>5 min lag undetected) occur in a measurable fraction of multi-vendor market-data pipelines during high-volatility sessions
- Silent failover to secondary feeds with different update frequency is a leading root cause of price-staleness incidents in post-incident reviews
- Stale-price-driven trade and risk miscalculations are a recurring finding in operational risk audits of automated advisory platforms

---

## Mitigation Strategies

### Prevention

1. **Mandatory price-staleness gating with explicit timestamp validation**: Implement pre-output gate: before any price-dependent recommendation (trade, rebalance, risk calc), system must: (a) Query current timestamp from price feed, (b) Calculate staleness = now - last_update_timestamp, (c) Validate staleness <SLA_threshold (2 min for liquid instruments, 15 min for illiquid). Fail-safe: if staleness exceeds threshold OR timestamp unavailable, return "[CANNOT RECOMMEND - price data stale or unavailable; data as of [timestamp] - [N] minutes old]" rather than proceeding with recommendation. Every output includes explicit "Data as of [YYYY-MM-DD HH:MM:SS UTC]" disclosure. Root cause mitigation: Prevents silent use of stale cache by enforcing timestamp validation and disclosure.

2. **Multi-source cross-validation with divergence detection**: For all high-stakes price-dependent decisions (trades >$1M, margin call triggers, portfolio recommendations), implement dual-source lookup: (Primary: vendor A, Secondary: vendor B). Compare prices: if divergence >1%, investigate root cause (one feed stale, different last-trade sources, etc.) before recommending. Log price comparison and source health status alongside recommendation. Root cause: Detects stale feed via cross-source discrepancy.

3. **Feed health monitoring with heartbeat detection and failover guards**: Implement feed monitor: tracks update frequency per instrument per source. On each price update, compares to expected frequency (e.g., "should update every 5 seconds for liquid equities"). If no update for 2x expected interval, mark feed as "potentially stale" and trigger: (a) Alert to operations, (b) Query secondary source, (c) Disable stale-feed use for new recommendations until restored, (d) Flag any in-flight recommendations using stale data. Root cause: Catches feed failures before they silently propagate through recommendations.

### Detection & Response

1. **Price-staleness audit logging with timestamp provenance**: For every recommendation/risk-calc, log: (a) prices used (instrument, price, timestamp), (b) staleness at time of use, (c) data source (primary vs. secondary), (d) confidence level (high if <30 sec old, low if >2 min), (e) cross-source discrepancy if checked. Alert when: (1) price staleness >SLA threshold at recommendation time, (2) timestamp missing or unverifiable, (3) price from secondary source without disclosure, (4) cross-source divergence >1%.

2. **Retrospective trade-vs-price accuracy audit**: After trade execution, compare agent's recommended price vs. actual execution price. If divergence >0.5%, investigate: was agent using stale data? Compute stale-price error rate: "# of trades with >0.5% price slippage / total trades". Alert if error rate exceeds 0.1% (indicates persistent stale-price issues).

### Architecture Patterns

1. **Price-Freshness Gating Service**: Input: (instrument_list) → Query current prices from primary source + timestamps → Validate staleness <SLA → Cross-check against secondary source if divergence detected → Output: (price_vector, timestamp_vector, staleness_vector, confidence_vector). All outputs include timestamp and staleness. Blocking gate: if any instrument >SLA staleness, halts recommendation generation.

2. **Multi-Source Feed Monitor**: Tracks both primary and secondary price feeds. Monitors: (a) update frequency per instrument, (b) last-update timestamp, (c) gap detection (no update for >2x expected interval), (d) comparison (primary vs. secondary prices). On gap or divergence: alerts operations, logs event, triggers secondary-source activation.

3. **Feed Failover Controller**: On primary feed health degradation, automatically: (1) Activates secondary feed, (2) Marks all prices from primary as "potentially stale", (3) Disables new recommendations until primary restored or secondary validated, (4) Flags all in-flight recommendations from stale primary for re-evaluation.

### Key Metrics

| Metric | Target | Alert Threshold | Measurement Method |
|--------|--------|-----------------|--------------------|
| Price Feed Staleness (Liquid Instruments) | <30 sec | >2 min | Time since last update timestamp for liquid equities/FX during market hours |
| Price Feed Staleness (Illiquid) | <15 min | >60 min | Time since last update for thinly traded/after-hours instruments |
| Freshness Disclosure Rate | 100% | <99% | % of price-dependent outputs with explicit "data as of [timestamp]" disclosure |
| Cross-Source Price Divergence | <0.5% | >1% | # of divergence events >1% between primary and secondary prices / total cross-checks |
| Feed Availability Uptime | >99.9% | <99% | % of market hours with functional price feeds (both primary and secondary) |

### Alerts & Escalation

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Price Data Exceeds Staleness SLA | Price timestamp older than 2 min (liquid) or 15 min (illiquid) at time of recommendation | CRITICAL | Halt recommendation; alert to operations; attempt to refresh from secondary source; disclose staleness to client |
| Feed Health Degradation | Primary price feed missing expected updates for >2x expected interval (no update in last 10 sec for liquid instrument) | CRITICAL | Activate secondary feed; mark primary as stale; disable new recommendations until primary restored; flag in-flight recommendations |
| Cross-Source Price Divergence | Primary and secondary prices differ >1% on same instrument (indicates stale feed) | HIGH | Investigate which source is stale; apply secondary price for new recommendations; alert to data operations |

---

## References

- [Standard Benchmarks Fail -- Auditing LLM Agents in Finance Must Prioritize Risk](https://arxiv.org/abs/2502.15865)
- [Agentic Trading: When LLM Agents Meet Financial Markets](https://arxiv.org/abs/2605.19337)
