# What Are the Most Common Market Data Freshness Failures in AI Agents?

**Market data freshness failures occur when agents rely on cached, stale, or asynchronously-delayed price data, corporate-action information, or reference rates without detecting staleness, leading to valuations, risk calculations, and trading decisions grounded in data that no longer reflects market conditions or operational reality.** The core mechanism is silent degradation: a price feed can stop updating for hours and still pass basic connectivity checks, a corporate-action adjustment can be delayed days post-event, and an agent has no native signal that the data it is consuming diverged from the live market. Freshness failures are particularly acute in illiquid instruments and after-hours windows where misdiagnosis of staleness is common because flat prices can be genuinely flat or genuinely stale.

## Key Takeaways

- 4 distinct failure patterns affect market data freshness, spanning stale price feeds, corporate-action blindness, freshness-benchmark mismatches via embedding retrieval, and multi-agent handoff gaps where staleness signals drop.
- Stale price feed reliance is documented as very common in operational-risk audits of automated advisory platforms, with feed staleness incidents occurring in a measurable fraction of multi-vendor pipelines during high-volatility sessions.
- Corporate-action blindness produces false-positive anomaly alerts that erode client trust and false-negative position misstatements when spin-offs or mergers are not reflected in position records for days.
- Multi-agent handoff drops of staleness signals are indistinguishable in form from other schema-gap failures: the ingestion agent flags staleness in free text, but the valuation agent never receives that flag because the structured price record has no field for it.

## Scope

- **Stale Price Feeds and Caching** — [stale-price-feed-reliance](failures/stale-price-feed-reliance.md). Cached or delayed prices used without detecting staleness; silent failover to secondary feeds with different latency characteristics undetected.
- **Corporate Action Blindness** — [corporate-action-blindness](failures/corporate-action-blindness.md). Splits, dividends, mergers, and spin-offs not adjusted in historical series or live positions, producing false anomalies or understated position values.
- **Freshness-Benchmark Retrieval Mismatches** — [embedding-retrieval-selects-wrong-reference-instrument](failures/embedding-retrieval-selects-wrong-reference-instrument-for-freshness-benchmark.md). Freshness checks for illiquid instruments benchmark against a textually similar but structurally unrelated reference instrument with different price-movement dynamics.
- **Multi-Agent Handoff Drops Staleness Flags** — [multi-agent-handoff-drops-stale-feed-flag](failures/multi-agent-handoff-drops-stale-feed-flag-between-ingestion-agent-and-valuation-agent.md). Ingestion agent's free-text staleness suspicion never reaches valuation agent because the structured price record omits a staleness field.

## When Market Data Freshness Matters

- Valuations or risk calculations consume prices that flow through a caching layer or secondary feed whose update frequency is not continuously monitored
- Agents make trading, rebalancing, or risk-assessment recommendations based on prices without surfacing the age of the data or an explicit staleness verification step
- Portfolios contain illiquid instruments where a flat price can legitimately persist for days, making manual staleness detection difficult without independent reference instruments

## Cross-Pattern Insight

All 4 market-data-freshness patterns share a common root mechanism: data staleness is expressed asynchronously and separately from the data value itself (a timestamp, an ingestion agent's monitoring note, a reference instrument's price movement), and consuming agents often optimize for output fluency over freshness verification. The reliable fix is architectural: implement mandatory pre-output gating that queries the current timestamp from the data source, compares it against an SLA, and refuses to generate recommendations if data exceeds staleness threshold. For benchmarking against reference instruments, constrain matches to structurally comparable instruments (same duration, credit tier, liquidity profile) before applying embedding similarity. For handoffs, add a structured `staleness_flag` field to every price record, with downstream validation that any flagged price triggers manual review before use.

## Frequently Asked Questions

### What is the difference between a stale price feed and a genuinely flat market for an illiquid instrument?

Stale: the feed stopped updating even though trading occurred elsewhere (reference feeds show prices moved, or time has passed beyond the expected update interval for that instrument). Flat: trading occurred but at the same price, or no trading occurred and the last price remains current. Distinguish them by (1) checking expected update frequency for this instrument (stale if no update for 2x that interval), (2) cross-referencing against independent sources (if those show different prices, the original feed is stale), (3) verifying the ingestion timestamp against current time. Do not assume flat=current.

### Can a better reference instrument selection algorithm fix freshness-benchmark mismatches without changing the retrieval method?

Not fully. Embedding similarity over free-text instrument descriptions will always favor keyword overlap over structural attributes. Filter candidate reference instruments by duration bucket and credit tier before applying embedding similarity, and verify the retrieved instrument's actual attributes match the checked instrument's on both dimensions before using it as a benchmark. Structural pre-filtering is mandatory; embedding can then rank within the pre-filtered cohort.

### How do you catch a multi-agent handoff drop of a staleness flag in production before it causes a valuation error?

Require a structured `staleness_flag` or `data_quality_issues` field in every price handoff record, with mandatory post-handoff validation: before any price is used in a calculation, a validator checks that field and routes any price with a flag to manual review. Log the field's presence/absence alongside every calculation so audit can distinguish prices that crossed a staleness-aware boundary from those that did not.

### What is the shortest acceptable staleness SLA for different instrument types?

Liquid equities/FX during market hours: <30 seconds. Illiquid equities/corporate bonds: <15 minutes. After-hours instruments: <1 hour or "mark as after-hours with last bid-ask" rather than attempting live-price staleness. Index/futures: <1 minute. Set these per instrument class and monitor SLA breaches as a hard alert that triggers secondary-source activation.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Stale Price Feed Reliance](failures/stale-price-feed-reliance.md) | Cached/delayed prices used without staleness detection; silent failover undetected |
| [Corporate Action Blindness](failures/corporate-action-blindness.md) | Splits, dividends, mergers not adjusted; false anomalies or position misstatements result |
| [Embedding Retrieval Selects Wrong Reference Instrument](failures/embedding-retrieval-selects-wrong-reference-instrument-for-freshness-benchmark.md) | Freshness check for illiquid instrument benchmarks against textually similar but structurally unrelated comparable |
| [Multi-Agent Handoff Drops Stale-Feed Flag](failures/multi-agent-handoff-drops-stale-feed-flag-between-ingestion-agent-and-valuation-agent.md) | Ingestion agent's free-text staleness suspicion omitted from structured price record passed to valuation agent |

**Total: 4 patterns**

## Related Goals

- [Data Quality](../data-quality/) — historical point-in-time accuracy and entity identity; market freshness is about real-time staleness
- [Trading Execution](../trading-execution/) — execution agents depend on current market data to size and time orders; stale data directly affects realized slippage
