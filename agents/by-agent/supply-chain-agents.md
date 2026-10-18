# Supply Chain Agents: Business Goals, Failure Patterns, and Fixes

**Supply Chain Agents fail along 5 goals: Demand Forecasting, Supplier Risk, Inventory Optimization carry the most documented failures.** This page maps each goal to the failures that threaten it, so you can decide what to protect first and where the fixes are.

## Key Takeaways

- 25 documented failure patterns across 5 goals. What it does: forecast demand, optimize inventory, route logistics, and assess suppliers.
- The most documented goal is [Demand Forecasting](../by-use-case/supply-chain/goals/demand-forecasting/) with 7 patterns.
- Frequencies below are as recorded on each pattern page. They are not measured rates.
- Business-goal definitions (metric, baseline, owner, what counts as a failure) are not written yet for this agent. Define them before choosing which patterns to prioritize.

## Goals this agent must protect

| Goal | When it fails | Patterns |
|---|---|---|
| [Demand Forecasting](../by-use-case/supply-chain/goals/demand-forecasting/) | Demand-forecasting agents treat conversational, qualitative forecast adjustments ("bump it up for the campaign") as replacements for structured baseline computations | 7 |
| [Supplier Risk](../by-use-case/supply-chain/goals/supplier-risk/) | Supplier-risk agents anchor risk scores to mismatched historical-supplier analogs selected by name-similarity or description-text similarity rather than by | 6 |
| [Inventory Optimization](../by-use-case/supply-chain/goals/inventory-optimization/) | When replenishment is weekly), treat quality-hold flags recorded in free-text inspection notes as not relevant to available-to-promise calculations | 4 |
| [Logistics Routing](../by-use-case/supply-chain/goals/logistics-routing/) | Logistics-routing agents commit customer ETAs based on cached or stale traffic data without re-checking live disruption feeds | 4 |
| [Supplier Onboarding](../by-use-case/supply-chain/goals/supplier-onboarding/) | Supplier-onboarding agents extract certification fields from uploaded documents and treat extraction success as equivalent to verification against the issuing | 4 |

## Failures most often recorded

| Failure | What goes wrong | Recorded frequency |
|---|---|---|
| [Bullwhip Effect & Cascading Forecast Error](../by-use-case/supply-chain/goals/demand-forecasting/failures/bullwhip-effect.md) | Small Demand Variation at Retail Cascades to Large Forecast Errors Upstream; Overproduction/Underproduction at Manufacturing | Very Common |
| [New Product Cold-Start Misforecast](../by-use-case/supply-chain/goals/demand-forecasting/failures/new-product-cold-start-misforecast.md) | Agent Forecasts Demand for a Newly Launched SKU Using a Global Average New-Product Curve That Ignores Category- and Channel-Specific Adoption Patterns | Very Common |
| [Seasonal Demand Misses & Holiday Blindness](../by-use-case/supply-chain/goals/demand-forecasting/failures/seasonal-demand-misses.md) | Forecasting Model Fails to Account for Seasonal Variations; Massive Stockouts/Overstock on Seasonal Peaks | Very Common |
| [Carrier Capacity Blindness in Route Optimization](../by-use-case/supply-chain/goals/logistics-routing/failures/carrier-capacity-blindness.md) | Agent Optimizes Shipping Routes for Cost and Transit Time Using Carrier Capacity Assumptions That Are Stale Relative to Real-Time Constraints | Common |
| [Financial Distress Signal Blindness](../by-use-case/supply-chain/goals/supplier-risk/failures/financial-distress-signal-blindness.md) | Agent's Supplier Risk Monitoring Relies on Quarterly or Annual Financial Statements, Missing Faster-Moving Distress Signals That Precede a Supplier… | Common |
| [Geopolitical Risk Blindness in Supplier Risk Scoring](../by-use-case/supply-chain/goals/supplier-risk/failures/geopolitical-risk-blindness.md) | Agent's Supplier Risk Score Is Based on Financial and Delivery-Performance History Alone, Missing Geopolitical Exposure That Has Not Yet Materialized… | Common |

## Before you build: define each goal

For every goal in the table, write down: the metric and how you measure its baseline today; the person who owns it; what counts as a failure and how severe it is; who is told when it happens; and when a person takes over. Then use the failures above as your test list.

## Security and governance

Every agent also needs the cross-cutting checks in [security](../cross-cutting/security/), [accuracy](../cross-cutting/accuracy/), [governance](../cross-cutting/governance/), and [operations](../cross-cutting/operations/).

## Frequently Asked Questions

### What fails most often in supply chain agents?

The most documented goal is Demand Forecasting (7 patterns). The failures table above lists the ones recorded as most frequent. These are the library's records, not measured rates.

### Where should I start when building supply chain agents?

Define your business goals and what counts as failure, then test against the failure patterns for each goal. The section above lists what to write down.

## Related

- [All agents by business goal](./)
