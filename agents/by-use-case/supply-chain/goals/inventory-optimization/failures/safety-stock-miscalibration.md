# Safety Stock Miscalibration from Demand Variance Underestimation

## Issue: Agent Calculates Safety Stock Using a Demand Variance Estimate That Understates True Variability, Producing Stockouts Despite a "Safety" Buffer

**Frequency**: Common

**Symptoms**
- Safety stock formula uses a standard deviation of demand computed over a period that smooths out the actual volatility the item experiences (e.g., using monthly aggregates when replenishment cycles are weekly)
- Service-level target (e.g., 95% in-stock probability) is computed correctly given the input variance, but the input variance itself is too low, so the realized service level falls well short of target
- Lead-time variability (supplier delivery uncertainty) is held constant or ignored, when in practice lead time variance contributes as much to stockout risk as demand variance
- Stockouts cluster around specific SKUs with high demand volatility or unreliable suppliers, while the safety stock formula treats all SKUs with a uniform variance assumption

**Root Cause**
Safety stock formulas (e.g., z-score × standard deviation of demand over lead time) are only as good as the variance estimate fed into them. Agents that compute this variance from aggregated or smoothed historical data, or that ignore lead-time variability and assume a fixed lead time, systematically underestimate the true combined variance — demand variance and lead-time variance both compound the actual stockout risk, and using point estimates for either input produces a safety stock level calibrated to a much narrower distribution than the one the business actually faces.

**Example**
```
Scenario: SKU replenished weekly, but variance computed from monthly aggregated sales data
Computed demand std dev (monthly basis): Understates week-to-week volatility by smoothing out spikes
Lead time: Assumed fixed at 2 weeks, actual lead time varies 1-4 weeks depending on supplier capacity
Safety stock calculated: Based on understated demand variance and zero lead-time variance
Target service level: 95%
Realized service level: ~80%, with frequent stockouts during high-variance weeks or long-lead-time deliveries
Impact: Repeated stockouts on a SKU the formula believes is adequately buffered
```

**Key Statistics**
- Combined demand-and-lead-time variance models are well-established in inventory theory as necessary for accurate safety stock calculation, yet single-variance-source models remain common in practice due to data availability constraints
- Underestimated demand variance from over-aggregated historical windows is a frequently cited cause of realized service levels falling short of target in inventory optimization audits
- Agentic supply chain research applied to large-scale retail operations highlights variance-aware, SKU-segmented safety stock policies as outperforming uniform-variance approaches

---

## Mitigation Strategies

1. **Variance Computed at Replenishment-Cycle Granularity**: Compute demand variance at the same time granularity as the actual replenishment cycle (weekly variance for weekly replenishment), not a coarser aggregate that smooths out real volatility
2. **Combined Demand-Lead-Time Variance Formula**: Use a safety stock formula that explicitly incorporates both demand variance and lead-time variance, not lead time as a fixed constant
3. **SKU-Segmented Variance Profiles**: Maintain per-SKU (or per-SKU-cluster) variance estimates rather than a single global variance assumption, since volatility differs substantially across SKUs and suppliers
4. **Realized Service Level Feedback Loop**: Continuously compare realized in-stock rate against the target service level per SKU, and recalibrate the variance inputs when realized performance diverges from target

### Metrics
- Realized service level (in-stock rate) vs. target service level, per SKU
- Demand variance estimate granularity (matched to replenishment cycle or not)
- Stockout incidence rate segmented by supplier lead-time variability

### Alerts
- Realized service level falls more than a defined margin below target service level for a SKU over a sustained period → P2
- Safety stock calculation uses a fixed lead-time assumption for a supplier with documented lead-time variability above a defined threshold → P2

---

## References

- [LLMs for Supply Chain Management](https://arxiv.org/pdf/2505.18597)
- [Flowr — Scaling Up Retail Supply Chain Operations Through Agentic AI in Large Scale Supermarket Chains](https://arxiv.org/pdf/2604.05987)
