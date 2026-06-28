# Promotion Lift Overestimation

## Issue: Agent Forecasts Promotional Demand Lift Using a Generic Historical Multiplier That Does Not Account for Promotion-Specific Cannibalization or Pull-Forward Effects

**Frequency**: Common

**Symptoms**
- Forecast applies a flat lift multiplier (e.g., "promotions typically increase volume 3x") regardless of the specific promotion mechanic, depth of discount, or category
- Demand pulled forward from the weeks immediately following a promotion is not subtracted from the post-promotion forecast, causing a double-counted demand bump
- Cannibalization of full-price SKUs within the same category during the promoted item's lift period is not modeled, overstating net incremental demand
- Over-forecast leads to over-ordering; resulting excess inventory is discovered only after the promotion ends and sell-through stalls

**Root Cause**
Promotional lift is highly specific to the mechanic (discount depth, bundle vs. straight discount, category elasticity, and whether the promotion was advertised), but agents using a single historical average lift factor collapse this variation into one number. This systematically overstates lift for low-elasticity categories and understates pull-forward and cannibalization effects, both of which reduce the net new demand actually generated relative to the gross lift the flat multiplier predicts.

**Example**
```
Scenario: 20%-off promotion on a mid-tier appliance category
Historical average lift multiplier applied: 2.5x baseline demand
Actual mechanic-specific elasticity for this category/depth: closer to 1.6x
Pull-forward effect: 30% of the lift represents demand that would have occurred in the following 4 weeks anyway
Forecast: Orders placed for 2.5x baseline across the promotion window plus normal post-promotion baseline
Result: Post-promotion sell-through stalls; excess inventory accumulates
Impact: Markdown losses and warehouse space tied up in slow-moving excess stock
```

**Key Statistics**
- Promotional lift overestimation and the resulting excess-inventory cycle is a long-documented pattern in retail demand planning, closely related to the broader bullwhip-effect dynamics in supply chains
- Pull-forward (borrowing demand from future periods) is consistently identified in promotion-effectiveness research as a major component of gross lift that does not represent net incremental demand
- LLM-based demand forecasting research incorporating event/promotion-specific contextual knowledge (rather than flat historical multipliers) has been shown to improve forecast accuracy for promotional periods compared to naive multiplier approaches

---

## Mitigation Strategies

1. **Mechanic-Specific Elasticity Modeling**: Maintain elasticity estimates segmented by discount depth, promotion type, and category, rather than a single flat lift multiplier applied universally
2. **Pull-Forward Decomposition**: Explicitly model and subtract the pull-forward component of a promotion's lift from the net incremental forecast, and correspondingly reduce the post-promotion baseline forecast
3. **Cannibalization Accounting**: Forecast category-level demand alongside SKU-level promoted demand to capture substitution from full-price SKUs within the same category
4. **Post-Promotion Sell-Through Tracking**: Compare actual post-promotion sell-through against forecast to continuously recalibrate mechanic-specific elasticity estimates

### Metrics
- Forecast accuracy (MAPE) for promotional periods, segmented by promotion mechanic and category
- Pull-forward share of total gross lift, tracked per promotion
- Excess inventory and markdown rate following promotions, attributed back to forecast error

### Alerts
- Promotional forecast generated using a flat historical multiplier with no mechanic-specific elasticity adjustment → P2
- Post-promotion sell-through falls materially below forecast, indicating likely overestimated lift → P2

---

## References

- [EventCast: Hybrid Demand Forecasting in E-Commerce with LLM-Based Event Knowledge](https://arxiv.org/html/2602.07695v1)
- [LLMs for Supply Chain Management](https://arxiv.org/pdf/2505.18597)
