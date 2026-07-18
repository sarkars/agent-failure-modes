# Per-Tool Minimum Usage Penalty

## Issue
A vendor contract commits the organization to a minimum monthly usage tier (e.g. "at least 100,000 calls/month or pay for 100,000 regardless"), and an agent's cost-optimization logic — designed to minimize call volume by caching aggressively, batching requests, or routing to a cheaper alternative tool when possible — reduces usage below that committed tier. The effective cost per call actually made goes up, because the fixed minimum fee is now spread across fewer calls, even though every individual optimization looked correct in isolation.

**Frequency**: Occasional

**Symptoms**
- Vendor invoice shows a flat minimum-commitment charge that doesn't decrease even as call volume drops
- Effective cost-per-call (invoice total divided by calls made) rises in months where the agent used the tool less
- Cost-saving changes (adding a cache layer, routing some traffic to a competitor tool) correlate with higher blended per-call cost rather than lower total spend
- Finance flags a tool as "underutilized" relative to its committed contract tier while engineering believes they successfully reduced usage
- No cost model component accounts for the committed-minimum contract term at all — only the marginal per-call price is tracked

## Root Cause
Agent cost-optimization logic is typically built against a marginal-cost model: each avoided call is assumed to save money at the tool's per-call rate. This is true for pure usage-based pricing but false under committed-minimum or tiered-commitment contracts, where the organization has pre-paid for a volume tier regardless of actual usage. Engineering teams building the optimization logic frequently don't have visibility into the commercial contract terms negotiated separately by procurement, so the cost model has no representation of the minimum-commitment structure at all.

## Example
```
The company has a contract with "DataEnrichCo" committing to a minimum
of 200,000 calls/month at $0.02/call ($4,000/month minimum), with any
usage above 200,000 also billed at $0.02/call. There is no discount for
using fewer than 200,000.

An engineer notices the agent calls DataEnrichCo redundantly for repeat
lookups on the same entity within a session, and adds a caching layer
that cuts DataEnrichCo calls by 40%, from roughly 210,000/month to
126,000/month. The change ships as a clear cost-saving win in the sprint
review, with an estimated savings of 84,000 x $0.02 = $1,680/month.

The actual invoice the following month is still $4,000 (the committed
minimum, since 126,000 < 200,000), so realized savings are $0 — while the
effective cost per call actually used rose from $0.019 (4,000/210,000) to
$0.032 (4,000/126,000). The caching change also puts the account at risk
of the vendor reducing the negotiated per-call rate at renewal, since the
usage no longer justifies the volume tier the pricing was based on.
```

## Statistics
| Finding | Context |
|---------|---------|
| Committed-minimum or minimum-spend contract terms are common in enterprise API/data vendor agreements, often in the 60-90% range of a negotiated volume tier | Common structure in enterprise usage-based contracts |
| A meaningful share of engineering-driven cost-optimization efforts on vendor tools are executed without checking the underlying contract's commitment structure | Frequently observed gap between engineering and procurement/finance visibility |
| Effective cost-per-call increases of 20-60% have been observed following usage-reduction efforts on tools with committed minimums | Typical range when optimization pushes usage meaningfully below the committed tier |

## Mitigations
1. **Contract-aware cost model**: Encode each tool's actual commercial terms (committed minimum, tier breakpoints, true marginal cost above/below commitment) into the cost model used by optimization logic, not just the list price per call.
2. **Finance/procurement sync before optimization work**: Require a check against the current vendor contract terms before shipping usage-reduction changes to any tool with commercial billing, as a standard step in the review process.
3. **Utilization-target monitoring**: Track actual usage against the committed tier as an explicit metric, and alert when usage is trending meaningfully below the commitment (wasted spend) rather than only alerting on overage.
4. **Right-size commitments at renewal**: Use realized usage data to renegotiate the committed tier at contract renewal instead of leaving usage-reduction savings uncaptured indefinitely.
5. **Route optimization by contract state, not just marginal price**: Have caching/routing logic check whether the target tool is currently under its committed minimum for the billing period, and prefer routing traffic to it (rather than a competitor) when the calls are effectively already paid for.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| commitment_utilization_ratio | Actual monthly usage divided by the contractually committed minimum tier | Alert if < 80% for two consecutive months |
| effective_cost_per_call | Total monthly invoice divided by actual calls made | Alert if it rises > 15% month-over-month without a rate change |
| optimization_change_contract_review_flag | Whether a shipped usage-reduction change was checked against active vendor contract terms | Alert if a usage-reduction change ships without this check for a committed-minimum tool |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Under-commitment utilization | commitment_utilization_ratio falls below 80% for a committed-minimum tool | Medium | Route more eligible traffic to the underutilized tool, flag for renewal renegotiation |
| Optimization shipped without contract check | A caching/routing change reduces call volume to a committed-minimum tool without a documented contract review | High | Roll back or reroute, add contract-check gate to the deploy process |

## Related Patterns
- [Per-Tool Tiered Pricing Unknown](./per-tool-tiered-pricing-unknown.md) - both involve pricing structures that reward or penalize specific usage volumes in ways the agent doesn't model
- [Hidden Tool Costs Not Visible](./hidden-tool-costs-not-visible.md) - both are cases where the true cost mechanics live outside the API response the agent's cost tracker reads
- [Cross-Tool Total Budget Exceeded](./cross-tool-total-budget-exceeded.md) - contract-blind routing decisions compound with aggregate budget visibility gaps
