# Supply Chain AI Agent Failures by Goal: 25 Patterns, Causes, and Fixes

**Supply Chain AI agents fail in 5 distinct ways, grouped by the goal each failure breaks.** Find the goal that matches what you are seeing, open its list, and use the fix on each pattern page.

## Key Takeaways

- 25 documented patterns across 5 goals; the most documented is [Demand Forecasting](demand-forecasting/) with 7.
- Each pattern page gives the symptoms, an example, the root cause, and mitigations.

## Supply Chain Goals

| Goal | When it fails | Patterns |
|---|---|---|
| [Demand Forecasting](demand-forecasting/) | Demand-forecasting agents treat conversational, qualitative forecast adjustments ("bump it up for the campaign") as replacements for structured baseline computations rather than deltas | 7 |
| [Inventory Optimization](inventory-optimization/) | When replenishment is weekly), treat quality-hold flags recorded in free-text inspection notes as not relevant to available-to-promise calculations | 4 |
| [Logistics Routing](logistics-routing/) | Logistics-routing agents commit customer ETAs based on cached or stale traffic data without re-checking live disruption feeds | 4 |
| [Supplier Onboarding](supplier-onboarding/) | Supplier-onboarding agents extract certification fields from uploaded documents and treat extraction success as equivalent to verification against the issuing authority's own records | 4 |
| [Supplier Risk](supplier-risk/) | Supplier-risk agents anchor risk scores to mismatched historical-supplier analogs selected by name-similarity or description-text similarity rather than by structured-attribute matching… | 6 |

**Total: 25 patterns**

## Frequently Asked Questions

### How do you distinguish between a conversational adjustment and a forecast-model update?

A conversational adjustment ("bump it up for the campaign") should be routed through the forecasting model's own adjustment/override interface with a structured delta parameter. See [Demand Forecasting](demand-forecasting/).

### How do you catch analog-mismatch risk scores before they're used in a procurement decision?

Require every analog-informed risk score to surface which analog it was based on and whether key structured attributes (industry, country, ownership) matched. See [Supplier Risk](supplier-risk/).

### How do you catch safety-stock miscalibration before it causes stockouts?

Compare realized in-stock rate against the target service level for each SKU on a rolling basis. See [Inventory Optimization](inventory-optimization/).

## Related

- [Supply Chain overview](../)
- [All agent failure patterns](../../../)
