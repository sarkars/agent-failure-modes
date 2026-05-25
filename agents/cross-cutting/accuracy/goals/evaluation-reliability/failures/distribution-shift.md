# Distribution Shift

## Issue: Production Queries Differ Significantly from Golden Dataset

**Frequency**: Very Common

**Symptoms**
- Good eval scores, poor production performance
- Model degrades over time without changes
- Certain user segments poorly served
- Seasonal or trending queries fail
- New topics completely missed

**Root Cause**
Golden datasets represent a snapshot of query distribution at creation time. Production queries evolve: user behavior changes, new topics emerge, seasonal patterns shift, and demographics expand. The gap between golden data distribution and current production distribution causes systematic failures on query types not represented in evaluation.

**Example**
```
Scenario: E-commerce product assistant

Golden dataset created: Black Friday 2025
Production evaluation: Summer 2026

Golden data distribution:
  - "Best deals on..." queries: 35%
  - Electronics focus: 45%
  - Gift-related: 25%
  - Price comparison: 40%
  - Winter products: 30%

Summer 2026 production distribution:
  - "Best deals on..." queries: 8%  ← Seasonal shift
  - Electronics focus: 25%  ← Category shift
  - Gift-related: 5%  ← Seasonal shift
  - Price comparison: 15%  ← Behavior shift
  - Summer products: 40%  ← Not in golden set
  - Outdoor gear: 25%  ← Not in golden set
  - Sustainability queries: 15%  ← New trend

Overlap analysis:
  - Golden → Production match: 35%
  - Production queries not in golden: 65%
  
Performance impact:
  - Golden data accuracy: 94%
  - Production accuracy: 71%
  - Gap explanation: Distribution mismatch

Categories with no golden data:
  - Summer products: 52% accuracy
  - Outdoor gear: 48% accuracy
  - Sustainability: 61% accuracy
```

**Key Statistics**
From Distribution Research (2026):
- Query distributions shift 20-40% within 6 months
- Seasonal variation: 30-50% of queries affected
- New topics emerge at 5-10% per quarter
- Distribution shift causes 40% of model degradation
- Only 15% of organizations track distribution drift

**Distribution Shift Types**
| Type | Cause | Timeline |
|------|-------|----------|
| Temporal | Time of day/week/year | Hours to months |
| Seasonal | Holidays, weather, events | Weeks to months |
| Trend | Viral topics, news | Days to weeks |
| Demographic | User base changes | Months to years |
| Product | New features, offerings | Days to months |
| Covariate | Input characteristics change | Ongoing |

**Contributing Factors**
- Golden data from single time period
- No distribution monitoring
- Static evaluation strategy
- No production feedback loop
- Infrequent golden data refresh
- No drift detection system

**Mitigation Strategies**
1. **Distribution monitoring**: Track query distribution over time
2. **Drift detection**: Alert when production differs from golden
3. **Continuous sampling**: Regularly add production queries to golden
4. **Stratified evaluation**: Weight eval by current distribution
5. **Temporal golden sets**: Separate evals for different time periods
6. **Synthetic augmentation**: Generate queries for underrepresented areas

**Detection**
- Compare golden vs. production query distributions
- Track topic/category accuracy over time
- Monitor drift metrics (KL divergence, PSI)
- Alert on emerging query patterns
- Audit accuracy drops for distribution causes

## References

- [Arize: Data Drift Detection](https://arize.com/blog/data-drift-detection/) - Monitoring distribution
- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - Evaluation limitations
- [FloTorch: RAG Performance Landscape](https://www.flotorch.ai/blogs/the-2026-rag-performance-landscape-what-every-enterprise-leader-needs-to-know) - Production vs eval
- [Braintrust: Agent Observability Guide 2026](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Drift monitoring
- [LinkedIn: Silent Failures of Production AI](https://www.linkedin.com/pulse/silent-failures-production-ai-why-most-llm-monitoring-praveen-juyal-iqgyc) - Distribution issues
