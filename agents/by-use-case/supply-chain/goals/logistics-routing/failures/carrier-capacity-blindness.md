# Carrier Capacity Blindness in Route Optimization

## Issue: Agent Optimizes Shipping Routes for Cost and Transit Time Using Carrier Capacity Assumptions That Are Stale Relative to Real-Time Constraints

**Frequency**: Common

**Symptoms**
- Route plan assigns volume to a carrier/lane combination that looks optimal based on historical capacity data, but the carrier is currently capacity-constrained (peak season, equipment shortage, regional disruption) and cannot actually fulfill the assigned volume
- Agent's routing decision does not distinguish between contracted capacity (what the carrier is obligated to provide) and actually available capacity (what the carrier can provide given current demand from all its shippers)
- Booking rejections or partial fulfillment from the carrier are discovered only after the routing decision is finalized and shipment execution begins
- Cost-optimal routes cluster volume onto a small number of "cheapest" carriers without checking whether that concentration exceeds what any single carrier can realistically absorb during a peak period

**Root Cause**
Route optimization agents commonly treat carrier capacity as a static input — either a contracted ceiling or a historical-average availability figure — because real-time capacity signals from carriers are harder to obtain than cost and transit-time data. During peak periods or disruptions, actual available capacity can diverge sharply from either the contracted ceiling or the historical average, and a routing decision optimized against stale capacity assumptions will systematically over-commit volume to constrained carriers, discovering the mismatch only at booking or pickup time.

**Example**
```
Scenario: Peak holiday shipping season
Route optimization: Assigns 40% of total outbound volume to Carrier A based on it being the lowest-cost option per historical capacity data
Actual current capacity: Carrier A is operating at 95% utilization across all its shipper customers due to seasonal demand surge
Booking attempt: Partially rejected; only 60% of assigned volume can actually be accepted
Re-routing: Performed reactively, under time pressure, at higher cost on alternative carriers
Impact: Delayed shipments and higher realized cost than if real-time capacity had been considered upfront
```

**Key Statistics**
- Capacity-constrained peak periods are a well-documented driver of carrier booking rejections and route plan infeasibility in logistics operations
- Real-time or near-real-time carrier capacity visibility (versus static historical assumptions) is increasingly cited in logistics-AI research as a key differentiator for routing plan feasibility during disruption or peak periods
- Reactive re-routing under time pressure following a capacity mismatch is consistently more expensive than capacity-aware proactive routing, per logistics cost-efficiency studies

---

## Mitigation Strategies

1. **Real-Time Capacity Signal Integration**: Incorporate the most current available capacity signal from each carrier (booking acceptance rates, recent rejection history, carrier-reported availability) rather than relying on contracted ceilings or historical averages alone
2. **Capacity Concentration Limits**: Cap the share of total volume routed to any single carrier during periods of known capacity tightness, even if that carrier appears cost-optimal on paper
3. **Feasibility-Checked Optimization**: Treat capacity feasibility as a hard constraint in the route optimization, not a post-hoc check after the cost-optimal plan is generated
4. **Proactive Multi-Carrier Diversification During Peak Windows**: Pre-emptively diversify volume across more carriers ahead of known peak periods rather than waiting for booking rejections to trigger re-routing

### Metrics
- Booking acceptance rate vs. assigned volume, per carrier and per routing decision
- Reactive re-routing frequency and cost delta vs. original optimized plan
- Carrier capacity concentration (share of total volume) during peak vs. non-peak periods

### Alerts
- Route plan assigns volume to a carrier exceeding a defined concentration threshold during a known capacity-tight period → P2
- Booking rejection rate for a carrier exceeds a defined threshold within a routing cycle → P1

---

## References

- [LLMs for Supply Chain Management](https://arxiv.org/pdf/2505.18597)
- [Flowr — Scaling Up Retail Supply Chain Operations Through Agentic AI in Large Scale Supermarket Chains](https://arxiv.org/pdf/2604.05987)
