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

## Mitigation Strategies

### Prevention
1. **Continuous production sampling into golden set**: Regularly draw a representative sample of live production queries into the golden dataset on a fixed cadence, since golden data from a single time period is the root cause of the overlap collapse seen in the example (65% of production queries absent from golden data). Trade-off: requires ongoing labeling effort and privacy review of production data before it enters the golden set.
2. **Stratified-by-recency golden set composition**: Maintain the golden set as a rolling window weighted toward recent time periods rather than a static snapshot, since distribution shift occurs on timescales of weeks to months per the Distribution Shift Types table. Trade-off: discards older validated cases, risking loss of regression coverage for rare-but-recurring seasonal patterns.
3. **Synthetic augmentation for anticipated shifts**: Generate synthetic queries for known upcoming distribution changes (season, feature launch, calendar event) before they happen in production, rather than only reacting after accuracy drops. Trade-off: synthetic queries may not match real user phrasing and need validation against actual post-launch traffic.

### Detection & Response
1. **Distribution divergence monitoring (KL divergence / PSI)**: Continuously compute divergence between the golden-set query distribution and a rolling window of production queries, since the example's golden-to-production category match fell to 35%; trigger a golden-set refresh review when divergence crosses threshold.
2. **Per-category accuracy trend tracking**: Track accuracy broken out by query category rather than only in aggregate, since categories with no golden coverage (e.g., "Summer products: 52% accuracy") were invisible in the 94% aggregate golden-data score.
3. **Emerging-topic detection via clustering**: Run topic clustering on production queries and flag clusters that don't match any existing golden-set category, since new topics emerge at 5-10% per quarter and are otherwise undetectable by a static eval.

### Architecture Patterns
1. **Temporal golden-set registry**: Maintain versioned golden sets scoped to distinct time windows/seasons and evaluate them separately, so seasonal categories (Black Friday vs. Summer) are never diluted or crowded out by an aggregate eval.
2. **Shadow evaluation pipeline sampling live traffic**: Run continuous shadow evaluation against a stream of live production queries in parallel with the static golden-set eval, closing the missing production feedback loop identified in Contributing Factors.
3. **Stratified sampling harness**: Build the golden-set refresh pipeline to sample production queries proportionally to the current category distribution, re-weighting automatically as the distribution shifts rather than relying on the original creation-time snapshot.

### Metrics
1. **distribution_divergence_score**: Target: PSI below 0.1 vs. prior period; Alert when PSI exceeds 0.25
2. **golden_production_category_overlap_rate**: Target: >80% of production query volume matched to a golden category; Alert when overlap drops below 60%
3. **per_category_accuracy_floor**: Target: no category more than 15 points below aggregate accuracy; Alert on any category falling below floor
4. **golden_set_refresh_age_days**: Target: <90 days since last production-sample refresh; Alert when age exceeds 120 days

### Alerts
1. **Distribution Drift Threshold Exceeded** (P2): Condition - divergence metric between golden and rolling production distribution crosses alert threshold. Action: trigger golden-set refresh review, prioritize sampling underrepresented categories.
2. **Category Accuracy Cliff** (P1): Condition - any query category's production accuracy falls more than 20 points below its golden-set-measured accuracy. Action: page eval owner, audit category coverage, consider temporary escalation routing for that category.
3. **Emerging Topic With No Golden Coverage** (P3): Condition - topic clustering identifies a production cluster above volume threshold with zero matching golden entries. Action: add representative cases to the golden set within one sprint.

## References

- [Arize: Data Drift Detection](https://arize.com/blog/data-drift-detection/) - Monitoring distribution
- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - Evaluation limitations
- [FloTorch: RAG Performance Landscape](https://www.flotorch.ai/blogs/the-2026-rag-performance-landscape-what-every-enterprise-leader-needs-to-know) - Production vs eval
- [Braintrust: Agent Observability Guide 2026](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Drift monitoring
- [LinkedIn: Silent Failures of Production AI](https://www.linkedin.com/pulse/silent-failures-production-ai-why-most-llm-monitoring-praveen-juyal-iqgyc) - Distribution issues
