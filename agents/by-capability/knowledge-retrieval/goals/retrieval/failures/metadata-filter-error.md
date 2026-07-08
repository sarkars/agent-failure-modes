# Metadata Filter Error

## Issue: Wrong date, version, region, product, role, or policy filter.

**Frequency**: Common

**Symptoms**
- Correct doc excluded by filter.
- [Add more specific symptoms]

**Root Cause**
Wrong date, version, region, product, role, or policy filter.

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
1. **Comprehensive Metadata Filter Tests**: Create test suite for each filter combination (date_ranges, status_values, category_hierarchies, region_filters). Example: filter='status=active AND date>2024-01-01 AND region=US'. Execute tests in CI/CD. Measure: precision, recall, specific_query_correctness.
2. **Filter Relaxation Fallback**: If filter returns 0 results, auto-relax filter (drop strictest constraint). Log relaxation for analysis. Display notice to user: 'No exact matches; showing close matches (region relaxed from US to North_America)'.
3. **Filter Validation Rules**: Define validation rules per filter type. Date_range filter must have valid start/end. Category filter must reference existing category. Validate before applying filter.

### Detection & Response
1. **Zero-Result Filter Queries**: Track queries where filter returns 0 results. Alert if rate > threshold (indicates filter too strict or data missing). Analyze: which filter combinations return 0 results most often?
2. **Filter Error Patterns**: Monitor filter errors by type (date_range, status, category). Identify patterns (e.g., 'status=inactive always returns 0' = filter misconfiguration). Flag for investigation.
3. **Filter vs No-Filter Result Comparison**: For filtered queries, compare results to same query without filters. If filter removes relevant results, flag as false negative (over-filtering).

### Architecture Patterns
1. **Metadata Schema Validation**: Maintain schema for all metadata fields (types, valid_values, constraints). Validate filters against schema before execution. Prevent invalid filter combinations.
2. **Filter Translation Layer**: User-facing filters translated to backend query language (SQL, Elasticsearch DSL, etc.). Translation layer validates and optimizes filters before execution.
3. **Filter Audit Trail**: Log all filters applied to query, their values, filter result_count. Attach filter metadata to retrieved documents for traceability and debugging.

### Metrics
1. **zero_result_filter_queries_percent**: Target: < 3%; Alert threshold: > 8%
2. **filter_error_rate_percent**: Target: < 0.5%; Alert threshold: > 2%
3. **filter_validation_coverage_percent**: Target: 100%; All filters validated
4. **false_negative_rate_from_filters_percent**: Target: < 1%; Alert threshold: > 5%
5. **filter_relaxation_event_rate_per_day**: Target: < 5; Alert if relaxations spike

### Alerts
1. **Filter Returning Zero Results** (P2 - Warning): Condition - filter applied, result_count=0. Action: Log filter config, suggest relaxation, offer no-filter results, investigate if data exists.
2. **Filter Configuration Error** (P1 - Critical): Condition - filter fails validation checks. Action: Block query, return error with suggested fix, alert data team.
3. **Filter False Negative** (P1 - Critical): Condition - filter excludes relevant documents later marked relevant. Action: Audit filter logic, update filter rules, consider filter removal or adjustment.

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

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
