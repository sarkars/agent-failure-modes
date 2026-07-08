# Business-Context Blindness

## Issue: Technically correct answer is commercially wrong.

**Frequency**: Common

**Symptoms**
- Customer/business metric harmed despite correctness.
- [Add more specific symptoms]

**Root Cause**
Technically correct answer is commercially wrong.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- [List factors that make this failure more likely]

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| [Test name] | [Input] | [Expected output] | [What indicates failure] |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |

---

## Mitigation Strategies

### Prevention
1. **Business KPI-Aware Eval Framework**: Define success metrics beyond technical correctness. Evaluate agent decisions by: customer_satisfaction, revenue_impact, lifetime_value_impact, churn_risk, operational_cost. Build evals that score decisions on business KPIs, not just logical correctness.
2. **Business Context Injection**: Provide agent with business context (customer value tier, account health, seasonality, competitor risk). Example: 'Offer customer VIP with high LTV a replacement instead of refund (lower cost, higher satisfaction)'. Encode business heuristics as decision guidance.
3. **Cross-Functional Eval Reviews**: Have product/business stakeholders review agent decisions quarterly. Identify cases where technically correct decisions harm business KPIs. Use findings to retrain/adjust agent priorities.

### Detection & Response
1. **KPI Impact Monitoring**: After agent decision, measure business KPI impact (customer_satisfaction, churn, NPS, revenue). Flag decisions that are technically correct but harm KPIs. Example: 'Refund processed (correct) but customer churn rate increased 5x that month'.
2. **Cohort Analysis by Decision Type**: Track cohorts of decisions (decisions_A vs decisions_B). Compare business outcomes between cohorts. If cohort_A has worse business outcomes despite technical correctness, flag for review.
3. **Context-Aware Outcome Tracking**: For each decision, track: decision_type, business_context (customer_tier, LTV, sentiment), technical_correctness, business_outcome_6_months_later. Correlate to identify context-blindness patterns.

### Architecture Patterns
1. **Business Context Enrichment Layer**: Pre-decision, enrich agent context with: customer_ltv, account_health_score, seasonality_factor, competitor_threat_level, business_priority_vector. Agent uses context to make business-aware decisions.
2. **Multi-Objective Optimization**: Frame decision as optimization problem with: technical_correctness, customer_satisfaction, revenue_impact, cost, churn_risk. Use weighted scoring to find business-optimal solution (not just technically correct).
3. **Decision Post-Audit Trail**: For each decision, log: decision, technical_correctness_score, business_context, predicted_business_outcome, actual_business_outcome_6mo_later. Feedback loop for model improvement.

### Metrics
1. **business_kpi_degradation_post_decision_percent**: Target: 0%; No decisions harm business KPIs
2. **customer_satisfaction_score_pre_vs_post_decision**: Target: Improvement or neutral; Alert if decline > 5%
3. **revenue_impact_positive_rate_percent**: Target: > 80%; Decisions should improve or maintain revenue
4. **customer_churn_rate_by_decision_cohort**: Target: < baseline churn; Alert if cohort churn > 2x baseline
5. **business_context_utilization_rate_percent**: Target: 100%; Agent uses available business context

### Alerts
1. **Business KPI Degradation** (P2 - Warning): Condition - business metric (satisfaction, NPS, churn) degrades post-decision vs pre-decision baseline. Action: Investigate decision reasoning, review business context available, potential decision reversal.
2. **High-Value Customer Harm** (P1 - Critical): Condition - decision harms high-LTV customer (LTV > threshold) resulting in churn risk or satisfaction drop. Action: Escalate to account team, manual review, potential intervention.
3. **Cohort Business Outcome Degradation** (P2 - Warning): Condition - cohort of decisions exhibits business outcomes 20% worse than control cohort. Action: Investigate decision pattern, business context factors, potential model adjustment.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | High |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
