# Geopolitical Risk Blindness in Supplier Risk Scoring

## Issue: Agent's Supplier Risk Score Is Based on Financial and Delivery-Performance History Alone, Missing Geopolitical Exposure That Has Not Yet Materialized as a Performance Problem

**Frequency**: Common

**Symptoms**
- A supplier with a strong historical delivery and financial track record receives a low risk score, even though it is concentrated in a region facing escalating trade restrictions, sanctions risk, or political instability
- Risk model treats geopolitical signals (tariff changes, export controls, regional conflict indicators) as out-of-scope context rather than a scored input
- Single-region supplier concentration is not flagged as a structural risk factor independent of any individual supplier's performance
- Risk score does not update until an actual disruption (shipment delay, customs hold) has already occurred, by which point mitigation lead time has been lost

**Root Cause**
Supplier risk scoring agents are commonly built on structured operational data — on-time delivery rate, quality defect rate, financial health ratios — because this data is readily available and historically predictive of supplier-specific performance risk. Geopolitical risk is a different category of exposure: it is forward-looking, driven by external policy and conflict signals rather than the supplier's own track record, and a supplier can have a flawless historical record right up until a regional event disrupts it. A risk model that only ingests historical performance data has no signal path to capture this exposure before it manifests as an actual delivery failure.

**Example**
```
Scenario: Key electronics component sourced from a single supplier in a region with escalating export-control tensions
Historical performance: 99% on-time delivery, strong financials — risk score: Low
Geopolitical signal (not modeled): New export control proposal under discussion affecting this exact component category
Risk score: Remains "Low" because no operational metric has yet been affected
Event occurs: Export restriction enacted; shipments held at customs
Impact: Supply disruption with no advance mitigation lead time, despite the risk being visible in policy discussion months earlier
```

**Key Statistics**
- Single-region supplier concentration combined with geopolitical exposure is repeatedly identified as a structural supply chain vulnerability in resilience research, independent of any individual supplier's operational track record
- Agentic and multi-agent supply chain risk research increasingly recommends incorporating external policy/conflict signal feeds rather than relying on operational history alone for forward-looking risk
- Disruptions originating from geopolitical/regulatory events rather than supplier-specific operational failure have grown as a share of major supply chain disruptions in recent years, per industry resilience reporting

---

## Mitigation Strategies

1. **Geopolitical Signal Ingestion**: Incorporate external geopolitical/trade-policy signal feeds (tariff changes, export control proposals, conflict indices) as a distinct, regularly updated input to the supplier risk score, separate from operational performance data
2. **Concentration Risk Flagging**: Explicitly score single-region or single-country sourcing concentration as a structural risk factor, regardless of the individual supplier's track record
3. **Forward-Looking Scenario Modeling**: Periodically run "what if" scenario assessments for key suppliers against plausible geopolitical events affecting their region, rather than waiting for an event to occur
4. **Dual-Sourcing Trigger**: Automatically flag single-sourced critical components in geopolitically exposed regions for dual-sourcing evaluation, independent of current performance metrics

### Metrics
- % of critical-component suppliers with geopolitical exposure signal incorporated into their risk score
- Single-region/single-supplier concentration rate for critical components
- Lead time between a geopolitical signal change and a corresponding risk score update

### Alerts
- Critical component single-sourced from a region with an active geopolitical risk signal, with no dual-sourcing mitigation in progress → P1
- Supplier risk score unchanged despite a new geopolitical signal directly affecting that supplier's region/category → P2

---

## References

- [Agentic LLMs in the Supply Chain: Towards Autonomous Multi-Agent Consensus-Seeking](https://arxiv.org/pdf/2411.10184)
- [LLMs for Supply Chain Management](https://arxiv.org/pdf/2505.18597)
