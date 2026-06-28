# New Product Cold-Start Misforecast

## Issue: Agent Forecasts Demand for a Newly Launched SKU Using a Global Average New-Product Curve That Ignores Category- and Channel-Specific Adoption Patterns

**Frequency**: Very Common

**Symptoms**
- New SKU with no sales history is forecast using a generic "new product ramp curve" derived from an average across all historical product launches, regardless of category
- Launch-channel-specific dynamics (e-commerce-only launch vs. broad retail distribution) are not reflected in the forecast, even though they produce very different early adoption shapes
- Comparable/analogous product selection for cold-start forecasting is done by category label alone, without checking whether the analogous products are actually similar in price point, target customer, or marketing support
- Forecast error is largest in the first 4-8 weeks post-launch, precisely when inventory and production commitments are most consequential and hardest to walk back

**Root Cause**
Cold-start demand forecasting for new products has no SKU-specific historical data to learn from, so agents fall back on either a generic ramp-curve template or an "analogous product" lookup. When the generic template is not segmented by category, price tier, and launch channel, or when analogous product selection is done by superficial category matching rather than genuine similarity (price point, target segment, promotional support), the resulting forecast reflects an average launch pattern that may not resemble this specific product's actual adoption curve at all.

**Example**
```
Scenario: New premium-tier SKU launched exclusively through e-commerce channel
Cold-start forecast: Uses a generic new-product ramp curve averaged across all historical launches (mass-market, broad retail distribution)
Actual adoption pattern: Premium e-commerce-only launches ramp more slowly initially, then accelerate as reviews accumulate — a materially different shape
Initial production/inventory commitment: Based on the generic curve's faster initial ramp
Result: Overproduction in weeks 1-4, followed by stockout risk in weeks 8-12 when actual demand accelerates past the generic curve's prediction
Impact: Capital tied up in early excess inventory, then missed sales from underestimated later demand
```

**Key Statistics**
- New product introduction forecast error rates are consistently reported as substantially higher than forecast error for established SKUs across retail and CPG demand planning research
- Analogous-product (lookalike) forecasting methods show materially better accuracy when similarity is computed on price point, channel, and target segment jointly, rather than category label alone
- The first weeks post-launch are repeatedly identified as both the highest-forecast-error period and the period where inventory/production decisions have the least flexibility to correct course

---

## Mitigation Strategies

1. **Segmented Ramp-Curve Templates**: Maintain separate cold-start ramp-curve templates segmented by category, price tier, and launch channel, rather than a single global average curve
2. **Multi-Dimensional Analogous Product Matching**: Select comparable products for cold-start forecasting based on similarity across price point, target customer segment, and promotional support jointly, not category label alone
3. **Staged Commitment with Early Signal Recalibration**: Commit production/inventory in stages, recalibrating the forecast against the first 1-2 weeks of actual sell-through before committing to later-stage volumes
4. **Explicit Uncertainty Bands for New Launches**: Report cold-start forecasts with wider, explicitly stated uncertainty bands compared to established-SKU forecasts, so downstream planning treats them with appropriate caution

### Metrics
- Forecast error (MAPE) for new product launches in the first 4, 8, and 12 weeks, compared to established-SKU forecast error
- Inventory imbalance (excess or shortage) attributable to cold-start forecast error
- Accuracy improvement from staged recalibration against early sell-through signal

### Alerts
- New product launch forecast generated without channel/price-tier-segmented ramp curve → P2
- Actual week 1-2 sell-through deviates from cold-start forecast by more than a defined margin without triggering recalibration → P2

---

## References

- [EventCast: Hybrid Demand Forecasting in E-Commerce with LLM-Based Event Knowledge](https://arxiv.org/html/2602.07695v1)
- [Flowr — Scaling Up Retail Supply Chain Operations Through Agentic AI in Large Scale Supermarket Chains](https://arxiv.org/pdf/2604.05987)
