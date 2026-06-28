# Single Supplier Bottleneck Risk

## Issue: Supply Chain Optimization Concentrates All Sourcing from Single Supplier (Lowest Cost); Blind to Failure Risk

**Frequency**: Common

**Symptoms**
- Model: "Supplier X has lowest cost; order 100% from X"
- Supplier X experiences disruption (natural disaster, bankruptcy, labor strike)
- Supply chain paralyzed; cannot fulfill orders
- No backup supplier; recovery takes weeks/months

**Root Cause**
Optimization models minimize cost without explicit supply chain resilience constraints. Single-supplier solutions are optimal cost-wise; models don't quantify disruption risk. Nassim Taleb's "fragility" — looks good until it breaks catastrophically.

**Example**
```
Scenario: Semiconductor component sourcing
Suppliers: Taiwan (cost $5/unit), Japan (cost $8/unit)
Model optimization: "Source 100% from Taiwan (lowest cost)"
Taiwan earthquake 2024: All chip fabs shut down
Supply disruption: 6-month recovery
Company impact: Cannot manufacture products; lost revenue $100M+

Expected: Model should diversify (80% Taiwan, 20% Japan) for resilience
Impact: Concentration risk not captured in cost model
```

**Key Statistics**
- Single-supplier concentration: 30-50% typical in optimized supply chains
- Disruption event frequency: Every 5-10 years per supplier
- Recovery time: 1-12 months depending on event
- Revenue loss: 10-50% during disruption

---

## Mitigation Strategies

1. **Resilience Constraints**: Require multi-supplier (min 2-3 suppliers per component)
2. **Disruption Modeling**: Include disruption probability in cost model
3. **Supplier Diversification**: Geographic + company diversification
4. **Safety Stock**: Keep buffer inventory for critical components

### Metrics
- Supplier concentration ratio (should be <70% from single supplier)
- Disruption recovery time (should be <4 weeks)
- Redundancy cost vs. disruption risk (trade-off analysis)

### Alerts
- Single supplier >70% → Diversify sourcing

---

## References

- [Supply Chain Resilience & Optimization](https://arxiv.org/abs/2011.07653)
- [Disruption Risk in Supply Networks](https://arxiv.org/abs/2001.09842)
