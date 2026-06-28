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

1. **Mandatory Freshness Timestamps**: Require every price-dependent output to carry an explicit "data as of" timestamp, validated against a max-staleness SLA
2. **Feed Health Checks**: Monitor heartbeat/update frequency per instrument and flag feeds that have stopped updating
3. **Staleness-Aware Degradation**: When data exceeds staleness threshold, agent must refuse or flag low confidence rather than silently using cached values
4. **Multi-Source Cross-Check**: Cross-validate prices against a secondary source before high-stakes actions (trade recommendations, margin calls)

### Metrics
- Price feed staleness (seconds/minutes since last update, per instrument)
- % of agent outputs with explicit freshness disclosure
- Cross-source price discrepancy rate

### Alerts
- Feed staleness >2 min for actively traded instruments during market hours → P1
- Feed staleness >15 min for any instrument used in a live recommendation → P1
- Cross-source price discrepancy >1% → P2

---

## References

- [Standard Benchmarks Fail -- Auditing LLM Agents in Finance Must Prioritize Risk](https://arxiv.org/abs/2502.15865)
- [Agentic Trading: When LLM Agents Meet Financial Markets](https://arxiv.org/abs/2605.19337)
