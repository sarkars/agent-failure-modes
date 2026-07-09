# Happy-Path-Only Evals

## Issue: Edge cases are missing from tests.

**Frequency**: Occasional

**Symptoms**
- Failures cluster on unusual cases.
- [Add more specific symptoms]

**Root Cause**
Edge cases are missing from tests.

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
1. **Edge-Case Taxonomy-Driven Test Generation**: Build an explicit taxonomy of edge-case categories (empty/null input, boundary values, malformed format, unsupported locale, extreme length, concurrent/rate-limited calls, partial tool failure) and require minimum test coverage per category before an eval suite is considered complete.
2. **Boundary Value & Mutation-Based Fuzzing**: Programmatically mutate existing happy-path cases (truncate, duplicate fields, swap types, inject unicode/emoji, remove required fields) to generate edge variants automatically, rather than relying solely on hand-authored cases.
3. **Production Long-Tail Mining**: Mine production logs for the bottom percentile by frequency (rare intents, unusual formatting, atypical session lengths) and require these long-tail cases be represented in the eval suite at a minimum ratio (e.g., 20% of cases from the bottom quartile of frequency).

### Detection & Response
1. **Per-Category Pass Rate Breakdown**: Score eval runs broken out by edge-case category, not just aggregate pass rate; flag categories with pass rate below the aggregate by more than a set margin.
2. **Production Failure Clustering Analysis**: Cluster production failures weekly (embedding or rule-based) and cross-reference each cluster against existing eval categories; clusters with no matching eval category are flagged as coverage gaps.
3. **Coverage Gap Backfill Trigger**: Any production failure cluster identified as uncovered automatically opens a ticket to add representative cases to the eval suite within a fixed SLA.

### Architecture Patterns
1. **Layered Eval Suite (Core + Edge + Adversarial)**: The eval pipeline runs three tiers — core happy-path, edge-case taxonomy, and adversarial/red-team — reporting pass rates separately so edge-case regressions can't hide behind a strong core score.
2. **Fuzzing Harness as CI Stage**: A mutation-fuzzing tool runs as a required CI stage that generates N edge variants per PR touching the agent's prompt/logic and fails the build if any variant produces an unhandled exception or obviously wrong output.
3. **Failure Cluster-to-Eval-Case Pipeline**: An automated service ingests production failure clusters, deduplicates against existing eval cases, and stages new edge-case candidates for reviewer approval.

### Metrics
1. **edge_case_category_coverage_pct**: Target: 100% of taxonomy categories have >= 5 cases; Alert threshold: < 80%
2. **edge_case_pass_rate_pct**: Target: within 5 points of core happy-path pass rate; Alert threshold: gap > 15 points
3. **uncovered_failure_cluster_count**: Target: 0 open past SLA; Alert threshold: > 3 open past 2 weeks
4. **long_tail_case_ratio_pct**: Target: >= 20% of eval cases from bottom-quartile-frequency production inputs; Alert threshold: < 10%

### Alerts
1. **Edge-Case Pass Rate Collapse** (P1 - Critical): Condition - any edge-case category pass rate falls more than 20 points below core pass rate. Action: Block release, require root-cause fix or explicit risk acceptance from eng lead.
2. **Recurring Uncovered Failure Cluster** (P2 - Warning): Condition - the same production failure cluster shape recurs without a matching eval case for 2+ weeks. Action: Escalate to eval owner for mandatory case addition.
3. **Taxonomy Coverage Drift** (P3 - Info): Condition - edge-case category coverage drops below 80% after a suite refactor. Action: Notify test owner to backfill missing categories.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Medium |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
