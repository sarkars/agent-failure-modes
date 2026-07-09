# Unvalidated Improvement

## Issue: Improvement is deployed without eval/regression proof.

**Frequency**: Rare but Catastrophic

**Symptoms**
- Change log lacks test evidence.
- [Add more specific symptoms]

**Root Cause**
Improvement is deployed without eval/regression proof.

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
1. **Mandatory Eval Gate Before Deployment**: The deployment pipeline queries an eval service for a passing, artifact-linked eval run before allowing any promotion; a change with no linked eval result, or a failing one, is structurally blocked from reaching production regardless of urgency or confidence.
2. **Regression Suite as Deployment Precondition**: Require the full regression suite — not a spot check of the specific improvement's target case — to pass before deployment, so an "improvement" that quietly regresses unrelated behavior is caught before shipping.
3. **Statistical Significance Requirement for Metric Claims**: Any claimed improvement must demonstrate statistical significance versus baseline on a sufficient sample size before it can justify deployment; anecdotal or small-sample wins are insufficient evidence and are explicitly rejected by the gate.

### Detection & Response
1. **Deployment-Eval Linkage Audit**: Periodically scan deployed versions for missing or incomplete eval evidence in the change ledger, surfacing any deployment that slipped through without proper validation.
2. **Post-Deployment Shadow Comparison**: Run the new version against the baseline on live shadow traffic before or alongside full cutover, catching validation gaps that offline eval sets missed.
3. **Retroactive Eval Backfill and Freeze on Gaps**: When an unvalidated deployment is found, freeze it from further promotion (or roll it back) and require eval backfill before it can be considered stable, rather than grandfathering it in.

### Architecture Patterns
1. **Eval Gate CI/CD Integration**: A deployment pipeline step that queries the eval results store for a passing, artifact-hash-linked run before allowing promotion to proceed; missing or stale results block the pipeline automatically.
2. **Eval Results Store**: A versioned store of eval outcomes linked to specific model/prompt/tool artifact hashes, queryable by the deployment pipeline and browsable for audit purposes.
3. **Shadow/Canary Comparison Service**: Routes duplicate live traffic to both candidate and baseline versions, compares outcomes over a defined window, and feeds that comparison into the promotion decision alongside offline eval results.

### Metrics
1. **deployments_with_linked_eval_percent**: Target: 100%; Alert threshold: < 100%
2. **regression_suite_pass_rate_at_deploy_time**: Target: 100%; Alert threshold: any deploy with failing suite
3. **shadow_comparison_coverage_percent**: Target: 100% of major changes; Alert threshold: < 80%
4. **unvalidated_deployment_count**: Target: 0; Alert threshold: any occurrence detected via audit

### Alerts
1. **Deployment Without Linked Eval** (P1 - Critical): Condition - a deployment reaches production with no passing, linked eval record. Action: Block if still in pipeline; if already live, auto-rollback and open incident to determine how the gate was bypassed.
2. **Regression Suite Failure at Deploy Time** (P2 - Warning): Condition - regression suite fails but deployment was attempted anyway. Action: Halt deployment, require fix or explicit documented exception with elevated sign-off.
3. **Shadow Comparison Shows Underperformance** (P3 - Info): Condition - candidate underperforms baseline in shadow traffic before cutover. Action: Delay full promotion, investigate discrepancy between offline eval and live shadow results.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Critical |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
