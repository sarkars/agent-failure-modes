# Supply Chain AI Agent Failures by Goal: 25 Patterns, Causes, and Fixes

**Supply Chain failures in AI agents are grouped here into 5 goals, each with a catalog of named failure patterns, the symptoms you will see, the root cause, and mitigations you can copy.** Start from the symptom you are debugging, pick the matching goal below, and open its failure list.

## Key Takeaways

- This use case covers 5 goals and 25 documented failure patterns.
- The largest goal is [Demand Forecasting](demand-forecasting/) with 7 patterns.
- Each goal page explains the failure class, how to tell it apart from its neighbors, and which mitigations apply across its patterns.
- Each failure page covers the symptoms, an example, the root cause, and how to fix it.

## Supply Chain Goals

| Goal | What goes wrong | Patterns |
|---|---|---|
| [Demand Forecasting](demand-forecasting/) | Demand-forecasting agents treat conversational, qualitative forecast adjustments ("bump it up for the campaign") as replacements for structured baseline computations rather than deltas | 7 |
| [Inventory Optimization](inventory-optimization/) | Inventory-optimization agents miscalibrate safety stock using demand-variance estimates computed at the wrong aggregation level (monthly when replenishment is weekly) | 4 |
| [Logistics Routing](logistics-routing/) | Logistics-routing agents commit customer ETAs based on cached or stale traffic data without re-checking live disruption feeds | 4 |
| [Supplier Onboarding](supplier-onboarding/) | Supplier-onboarding agents extract certification fields from uploaded documents and treat extraction success as equivalent to verification against the issuing authority's own records | 4 |
| [Supplier Risk](supplier-risk/) | Supplier-risk agents anchor risk scores to mismatched historical-supplier analogs selected by name-similarity or description-text similarity rather than by structured-attribute matching (industry code, ownership, geography) | 6 |

**Total: 25 patterns**

## Frequently Asked Questions

### Where do I start if my supply chain agent is failing?

Match the symptom to a goal in the table above, then open that goal's page for how to tell its failures apart and where to look first. Each failure page ends in mitigations you can apply directly.

### How are these supply chain failure patterns organized?

By goal: the outcome the agent is supposed to achieve. Under each goal, a `failures` folder holds one page per pattern. For the full picture see the [Supply Chain overview](../).

## Related

- [Supply Chain overview](../)
- [All agent failure patterns](../../../)
