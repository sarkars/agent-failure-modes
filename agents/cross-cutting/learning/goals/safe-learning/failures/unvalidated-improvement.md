# Unvalidated Improvement

## Issue: Improvement is deployed without eval/regression proof.

**Frequency**: Rare but Catastrophic

**Symptoms**
- Change log lacks test evidence.
- A prompt/model change is shipped on the strength of a demo or a handful of manually-checked examples ("looks better to me") rather than a passing run of the regression suite or a statistically significant eval comparison against baseline.
- Production metrics regress shortly after a confidently-described "improvement" ships, and post-hoc investigation finds no eval run, or a failing one, was ever linked to that deployment.

**Root Cause**
The deployment pipeline has no hard gate requiring a linked, passing eval or regression result before a change is promoted, so whether validation happens at all is left to the author's discretion rather than being structurally enforced. A handful of hand-picked examples that look obviously better is treated as sufficient proof, especially under the time pressure to ship a confidently-described win immediately, even though a small anecdotal sample can't surface regressions outside the categories it happened to sample. Without a shadow or canary comparison against live traffic, gaps that a limited offline eval set missed — like a category of input the hand-picked examples never touched — aren't caught until they're already affecting production users.

**Example**
```
A team fine-tunes a new version of their document-summarization agent and tries it on five sample
documents the product manager picked; all five summaries look noticeably better than the current
production version. Excited by the result, they ship the new version company-wide the same afternoon,
skipping the regression suite because "it's clearly an improvement." A week later, support tickets
spike: the new version, while better on long-form articles like the five samples, has quietly gotten
worse at summarizing short technical documents -- a regression the full eval suite would have caught
in minutes, but which the five hand-picked examples never touched.
```

**Contributing Factors**
- Deployment pipeline has no hard gate requiring a linked, passing eval/regression result before promotion.
- Confidence from a small number of hand-picked or anecdotal examples is treated as sufficient evidence of improvement.
- Time pressure ("it's clearly better, ship it now") discourages waiting for the full regression suite or a statistically significant comparison to complete.
- No shadow/canary comparison against live traffic exists to catch gaps that a limited offline eval set missed.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Missing eval-link deployment attempt | Candidate deployment with no linked eval run in the eval results store | Deployment pipeline blocks promotion until a passing, linked eval result exists | Deployment proceeds with no eval evidence attached |
| Anecdotal-only validation | Change validated only against 5 hand-picked examples, full regression suite not run | Gate rejects the change and requires the full regression suite to pass first | Change ships on the basis of the 5 examples alone |
| Shadow comparison discrepancy | Candidate version underperforms baseline on a category absent from the offline eval set, but shown via shadow traffic | Promotion is delayed pending investigation of the shadow discrepancy | Candidate is promoted to full traffic despite shadow underperformance |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| deployments_with_linked_eval_percent (eval) | 100% | Audit recent deployments for a passing, artifact-hash-linked eval record |
| regression_suite_pass_rate_at_deploy_time (eval) | 100% | Confirm the full regression suite result recorded at the time of each deployment |
| improvement_claim_sample_size | statistically sufficient (e.g., n >= 200 or per power analysis) | Check the sample size backing any "improvement" claim used to justify a deployment |

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
| unvalidated_deployment_count | any occurrence detected via audit |
| deployments_with_linked_eval_percent | < 100% |
| shadow_comparison_coverage_percent | < 80% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Deployment Without Linked Eval | a deployment reaches production with no passing, linked eval record | Critical |
| Regression Suite Failure at Deploy Time | regression suite fails but deployment was attempted anyway | Medium |
| Shadow Comparison Shows Underperformance | candidate underperforms baseline in shadow traffic before cutover | Low |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
