# What Are the Most Common Logistics Routing Failures in AI Agents?

**Logistics-routing agents commit customer ETAs based on cached or stale traffic data without re-checking live disruption feeds, select transit-time benchmarks for new lanes using description-text similarity instead of mode and border-crossing structure, treat carrier capacity as a static contracted ceiling rather than querying live carrier utilization, and fail to carry customs-hold risk flags from routing commentary into customer-facing ETA commitments.** These patterns cluster around three categories: cached/stale data treated as live (traffic conditions, capacity), retrieval mismatch (wrong historical lanes as benchmarks), and multi-agent handoff loss (customs-risk language in routing notes but not in ETA-commitment schema). Routing failures manifest as missed customer commitments (delayed arrivals), booking rejections (over-committed carrier capacity), or compliance violations (customs holds not flagged in advance).

## Key Takeaways

- 4 distinct failure patterns affect logistics routing, grouped into three mechanisms: stale or cached data (traffic, carrier capacity), retrieval mismatch (wrong-mode lane selection), and multi-agent handoff loss (customs-risk flags, disruption events).
- Stale-cached-traffic-feed ETA failures occur at "occasional" frequency, tightens around the time window immediately following a disruption event's onset, then disappear once the traffic tool's cache naturally refreshes (typically 15-60 minutes lag).
- Carrier-capacity-blindness affects 10-30% of route plans during peak seasons when optimal cost routes over-concentrate volume on the cheapest carriers, which are also capacity-constrained; booking-rejection rates spike during these windows.
- Transit-time-benchmark mismatches (wrong mode, wrong border-crossing count) cause 10-20% ETA miss rates for new lanes when benchmarks are selected by description similarity instead of structured-attribute matching.

## Scope

- **Stale and Cached Data Treated as Live** — [stale-cached-traffic-feed-treated-as-live-in-eta-commitment](failures/stale-cached-traffic-feed-treated-as-live-in-eta-commitment.md). Traffic/transit-time tool returns cached response from before a major disruption; agent commits ETA against pre-disruption conditions without checking cache timestamp against live disruption events.
- **Capacity Blindness** — [carrier-capacity-blindness](failures/carrier-capacity-blindness.md). Route optimization assumes carrier capacity is the contracted ceiling or a static historical average; actual available capacity varies with other shippers' demand and peak-period utilization.
- **Retrieval Mismatch: Lane Selection** — [embedding-retrieval-selects-wrong-historical-lane-as-transit-time-benchmark](failures/embedding-retrieval-selects-wrong-historical-lane-as-transit-time-benchmark.md). Transit-time estimate for a new lane borrowed from a historical lane selected by region-pair description similarity but differing in transport mode or border-crossing count.
- **Handoff Loss: Customs-Risk Flags** — [multi-agent-handoff-drops-customs-hold-flag-before-customer-eta-commitment](failures/multi-agent-handoff-drops-customs-hold-flag-before-customer-eta-commitment.md). Routing agent notes elevated customs-hold risk at a border crossing in commentary, but customer-notification agent generates ETA from transit-time fields alone, ignoring the risk note.

## When Logistics Routing Matters

- Customer ETA commitments are contractual: missing committed arrival dates creates service failures, customer escalations, and financial penalties.
- Carrier booking rejections discovered after route optimization is complete force reactive re-routing under time pressure at higher cost than capacity-aware proactive routing.
- Customs and border-crossing delays are time-variable and region-specific; a route plan that ignores current customs-risk or disruption status commits to an ETA that is structurally at risk of being missed.

## Cross-Pattern Insight

All four logistics-routing patterns share a common theme: the agent commits to a customer-facing ETA based on partial or stale state without verifying current reality. When a traffic tool returns a cached response, the agent treats the timestamp as current without cross-checking against a live disruption feed. When selecting a transit-time benchmark, the agent matches on topical similarity (region description) without verifying structural similarity (transport mode, border-crossing architecture). When selecting routes, the agent optimizes for cost against static or historical capacity assumptions without querying current carrier availability. When generating a customer ETA, the agent pulls from transit-time fields without re-scanning routing commentary for risk flags. The customer commitment is irrevocable once sent; if the underlying state has changed, the agent cannot recover. Mitigation requires: live disruption-event coupling to cache-invalidation, structured-attribute pre-filtering for benchmark selection, real-time or near-real-time carrier-capacity signals, and mandatory risk-metadata fields in handoffs that force explicit representation of every flagged risk before commitment.

## Frequently Asked Questions

### How do you detect a stale-cached transit-time response before committing an ETA?

Check the transit-time tool's response timestamp against the most recent known disruption events for that corridor. If the response data is older than a disruption event onset time, the response is stale relative to current conditions and should not be used for a customer commitment. Implement event-coupled cache invalidation: invalidate the tool's cache immediately for any corridor flagged by the disruption-monitoring feed, rather than relying on a time-based TTL.

### What makes a transit-time benchmark lane appropriate?

An appropriate benchmark matches on transport mode (ocean vs. air, LTL vs. full truckload), number of border crossings, and transshipment-point architecture — not just region-pair description similarity. A new ocean lane through two borders should be benchmarked against other ocean lanes with comparable border counts, not against air-freight lanes sharing the same region pair but having entirely different transit-time profiles.

### How do you prevent carrier-capacity over-commitment?

Incorporate the most current available carrier-capacity signal (booking acceptance rates, recent rejection history, carrier-reported available slots) rather than relying on contracted ceilings or historical averages. Cap the share of total volume routed to any single carrier during known capacity-tight periods. Treat capacity feasibility as a hard constraint in route optimization, not a post-hoc check after the cost-optimal plan is generated.

### How do customs-hold risk flags get lost in ETA commitments?

Customer-notification agents typically generate ETAs from structured transit-time fields only, not from routing commentary. Unless a customs-risk flag is explicitly captured in a structured field on the shipment record and required ETA-commitment logic checks it, routing commentary about elevated hold risk remains invisible to the customer-notification agent. Fix: add mandatory customs-risk field to shipment schema; require routing agent to populate it; require ETA logic to apply a buffer when the field indicates elevated risk.

### How do you test whether an ETA miss was due to stale routing data or actual operational failure?

Compare the original ETA commitment timestamp against your own system's knowledge of disruption events: if a disruption event was flagged before or at the time of ETA commitment, check whether the tool output's timestamp reflects the disruption. If not, the ETA was committed against stale conditions. This determines whether the root cause is tool staleness or a genuine operational change post-commitment.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Stale Cached Traffic Feed Treated as Live in ETA Commitment](failures/stale-cached-traffic-feed-treated-as-live-in-eta-commitment.md) | Traffic tool returns cached response from before disruption event; agent commits ETA without checking cache timestamp against live disruption feed |
| [Carrier Capacity Blindness in Route Optimization](failures/carrier-capacity-blindness.md) | Route optimization assumes static or historical carrier capacity; actual available capacity varies with peak-period utilization and other shippers' demand |
| [Embedding Retrieval Selects Wrong Historical Lane as Transit-Time Benchmark for New Route](failures/embedding-retrieval-selects-wrong-historical-lane-as-transit-time-benchmark.md) | Transit-time benchmark for new lane selected by region-pair description similarity; differs in transport mode or border-crossing count from actual new lane |
| [Multi-Agent Handoff Drops Customs-Hold Flag Before Customer ETA Commitment](failures/multi-agent-handoff-drops-customs-hold-flag-before-customer-eta-commitment.md) | Routing agent notes elevated customs-hold risk; customer-notification agent generates ETA from transit-time fields only, ignoring the risk note |

**Total: 4 patterns**

## Related Goals

- [Demand Forecasting](../demand-forecasting/) — upstream; demand forecast drives shipment volume and timing; forecast error propagates into carrier-capacity and routing-resource constraints.
- [Inventory Optimization](../inventory-optimization/) — upstream; inventory levels constrain shipment capacity and shipment scheduling decisions.
