# What Are the Most Common Inventory Optimization Failures in AI Agents?

**Inventory-optimization agents miscalibrate safety stock using demand-variance estimates computed at the wrong aggregation level (monthly when replenishment is weekly), treat quality-hold flags recorded in free-text inspection notes as not relevant to available-to-promise calculations, perform unit-conversion arithmetic via free-text reasoning instead of deterministic formulas, and borrow variance profiles from wrong-demand-driver analogs when setting safety stock for new SKUs.** These patterns concentrate around three categories: safety-stock miscalibration (variance underestimation, wrong analogs), multi-agent handoff brittleness (quality holds lost, reorder calculations operate on stale ATP), and arithmetic and unit-conversion errors in replenishment logic. Inventory errors manifest as stockouts (when safety stock is too low) or excess inventory (when it is too high), both with full working-capital impact.

## Key Takeaways

- 4 distinct failure patterns affect inventory optimization, grouped into three mechanisms: safety-stock miscalibration (variance granularity, wrong analogs), multi-agent handoff loss (quality-hold flags, compensation changes), and arithmetic/unit-conversion drift in reorder calculations.
- Safety-stock miscalibration from demand-variance underestimation affects 10-20% of SKUs when variance is computed at monthly or aggregated granularity while replenishment cycles are weekly, producing service-level gaps of 10-20 percentage points from target.
- Unit-conversion arithmetic errors in replenishment calculations occur at "occasional" frequency, concentrating on SKUs with non-round pack sizes or multi-tier packaging hierarchies, with order-quantity drift of 1-5 cases per recommendation on average.
- Multi-agent handoff drops (quality-hold flags, compensation adjustments) occur at "occasional" frequency when handoff schemas lack fields for transient state changes or when reconciliation checks don't run pre-action.

## Scope

- **Safety-Stock Miscalibration** — [safety-stock-miscalibration](failures/safety-stock-miscalibration.md), [embedding-retrieval-pulls-wrong-substitute-sku-as-safety-stock-variance-proxy](failures/embedding-retrieval-pulls-wrong-substitute-sku-as-safety-stock-variance-proxy.md). Variance estimates computed at the wrong granularity or from wrong-demand-driver analogs produce safety-stock levels calibrated to the wrong distribution.
- **Handoff Schema Brittleness & Stale State** — [multi-agent-handoff-drops-quality-hold-flag-between-receiving-agent-and-replenishment-agent](failures/multi-agent-handoff-drops-quality-hold-flag-between-receiving-agent-and-replenishment-agent.md). Quality-hold flags recorded in inspection notes are not captured in structured ATP fields; replenishment agent over-orders based on miscounted available inventory.
- **Arithmetic and Calculation Errors** — [unit-conversion-arithmetic-drift-in-llm-generated-reorder-quantity](failures/unit-conversion-arithmetic-drift-in-llm-generated-reorder-quantity.md). Reorder quantities computed via free-text reasoning about forecast, lead-time, and pack-size values drift from the deterministic result by 5-10% on SKUs with non-round pack sizes.

## When Inventory Optimization Matters

- Inventory levels are a direct function of demand forecast accuracy and safety-stock calibration; forecast errors and service-level miscalibration both drive excess or shortage with full working-capital impact.
- SKUs with high demand volatility or unreliable suppliers require variance-aware, supplier-specific safety stock; a uniform safety-stock policy misses these nuances and either over-buffers low-volatility SKUs or under-buffers high-volatility ones.
- Multi-agent inventory workflows (receiving/inspection → replenishment → purchasing) introduce coordination points where state synchronization is critical; quality holds and recent change must propagate to replenishment calculations.

## Cross-Pattern Insight

All four inventory-optimization patterns share a vulnerability to silent state divergence: the replenishment agent's calculation operates on a view of inventory state (available-to-promise, variance estimates) that is cached, aggregated, or computed on assumptions that no longer hold. When variance is computed at monthly aggregation but replenishment is weekly, the agent's safety-stock calculation is silently operating on understated variance. When quality holds exist in inspection notes but not in the ATP schema, the agent's reorder calculation counts held inventory as available. When arithmetic is performed via free-text reasoning instead of a deterministic formula, the result drifts silently from the correct value. None of these failures produce an obvious signal — the replenishment recommendation looks plausible — until the actual demand or supply pattern reveals the miscalibration. Mitigation requires: variance computed at replenishment-cycle granularity with explicit lead-time variance included; structured quality-hold and change-event fields on inventory records; and deterministic calculation formulas for reorder quantities, never free-text reasoning about arithmetic.

## Frequently Asked Questions

### How do you catch safety-stock miscalibration before it causes stockouts?

Compare realized in-stock rate against the target service level for each SKU on a rolling basis. If a SKU with a 95% target service level consistently runs out (realized 85% in-stock), the safety-stock inputs (variance, lead time) are likely understated. Recalibrate variance inputs and recompute. Test the new variance estimate on a holdout period to check whether realized service level improves to target.

### How does variance computed at monthly granularity fail for weekly replenishment?

Monthly aggregation smooths out week-to-week spikes. A SKU that sees 50 units one week and 150 the next will show a monthly aggregate (averaging ~600 over 4 weeks) that misses the true week-to-week volatility. Safety stock based on the monthly aggregate is calibrated to a narrower distribution than what actually occurs, producing stockouts during high-variance weeks. Compute variance at the same time granularity as the replenishment cycle.

### How do you prevent quality-hold quantities from being miscounted as available?

Add a structured quality-hold field to inventory schemas separate from usable on-hand. Require receiving agents to populate it directly from inspection determinations. Require replenishment agents to exclude held quantities from available-to-promise calculations by default. Run reconciliation checks comparing hold-status language in inspection notes against the structured field before reorder calculations run.

### What's the best way to fix unit-conversion arithmetic errors?

Use a deterministic calculation function/tool for the final order quantity instead of free-text reasoning. Pass tool outputs (forecast, lead-time, pack-size) as typed, structured values to the calculation function, not embedded in a natural-language prompt the model reasons over in prose. The model's reasoning about which values to retrieve is fine; its arithmetic on those values should be delegated to a formula.

### How do you test whether a variance-proxy SKU is actually comparable?

Once the new SKU accumulates enough sales history (typically 4-8 weeks), compute its actual coefficient of variation. Compare it to the borrowed-variance proxy's COV. If they diverge by more than 20-30%, the proxy was mismatched. Replace the borrowed estimate with the directly-computed one and adjust safety stock accordingly. Track which proxy SKUs consistently mismatch for demand-driver classification audit.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Safety Stock Miscalibration from Demand Variance Underestimation](failures/safety-stock-miscalibration.md) | Variance computed at monthly aggregation instead of weekly replenishment cycle; lead-time variance held constant instead of estimated |
| [Embedding Retrieval Pulls Wrong Substitute SKU as Safety-Stock Variance Proxy](failures/embedding-retrieval-pulls-wrong-substitute-sku-as-safety-stock-variance-proxy.md) | Variance-proxy selection by description similarity instead of demand-driver classification; topically similar SKU has different volatility profile |
| [Multi-Agent Handoff Drops Quality-Hold Flag Between Receiving Agent and Replenishment Agent](failures/multi-agent-handoff-drops-quality-hold-flag-between-receiving-agent-and-replenishment-agent.md) | Quality-hold status exists in inspection notes but not in available-to-promise schema; replenishment counts held lot as usable |
| [Unit-Conversion Arithmetic Drift in LLM-Generated Reorder Quantity](failures/unit-conversion-arithmetic-drift-in-llm-generated-reorder-quantity.md) | Reorder quantity computed via free-text reasoning over forecast/lead-time/pack-size instead of deterministic formula; arithmetic drifts 1-5 units on non-round packs |

**Total: 4 patterns**

## Related Goals

- [Demand Forecasting](../demand-forecasting/) — upstream; demand forecast accuracy drives the base replenishment level; forecast errors propagate into inventory variance.
- [Logistics Routing](../logistics-routing/) — downstream; inventory levels constrain shipment capacity and carrier selection decisions.
