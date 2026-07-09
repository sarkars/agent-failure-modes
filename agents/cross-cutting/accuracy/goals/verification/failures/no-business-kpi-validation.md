# No Business Kpi Validation

## Issue: Output looks correct but harms CSAT, conversion, compliance, or cost.

**Frequency**: Common

**Symptoms**
- Task metric OK; business metric worsens.
- [Add more specific symptoms]

**Root Cause**
Output looks correct but harms CSAT, conversion, compliance, or cost.

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
1. **KPI-Linked Eval Design**: Map every eval metric explicitly to a downstream business KPI (task accuracy -> CSAT, response time -> conversion, tone compliance -> complaint rate) with a documented hypothesis of the expected relationship, reviewed before the eval is approved as a ship gate.
2. **Pre-Launch Business Impact Simulation**: Before full rollout, run the agent against a held-out sample scored on task metrics AND estimate business impact using a proxy model (cost-per-interaction, projected CSAT from historical correlation) so misalignment is caught before real customers are affected.
3. **Guardrail Metrics Alongside Task Metrics**: Define explicit guardrail thresholds for compliance-sensitive and cost-sensitive metrics (max cost per resolution, zero tolerance for compliance-flagged language) that must hold even if task accuracy improves, preventing optimization that trades business harm for task-metric gains.

### Detection & Response
1. **Task-Metric vs. Business-KPI Correlation Monitoring**: Track task eval score and matched real-world business KPI (CSAT survey results, conversion rate, cost per interaction, compliance flag rate) on a shared dashboard per release; alert when task metric improves or stays flat while a linked business KPI degrades.
2. **Cohort-Level Business Outcome Analysis**: Segment production interactions by agent version and compare business outcomes (CSAT, conversion, escalation rate) across cohorts using statistical significance testing, not just eyeballing trend lines.
3. **Compliance and Cost Outlier Scanning**: Run automated scans over production interactions for compliance violations (regulated language, unauthorized claims) and cost outliers (unusually long tool-call chains, excessive retries) that a task-only eval would never surface.

### Architecture Patterns
1. **KPI Correlation Pipeline**: A scheduled job joins per-release task eval scores with downstream business metrics from the analytics warehouse (CSAT surveys, conversion events, billing/cost data, compliance flags) on a common release-version key, publishing a correlation report before each rollout decision.
2. **Guardrail Gate in Release Pipeline**: The release pipeline enforces hard guardrail thresholds (max cost per interaction, zero compliance flags in canary) as blocking checks independent of the primary task-accuracy eval, so a task-metric win can't ship over a business-harm regression.
3. **Canary Rollout with Business-Metric Rollback Trigger**: New agent versions ship to a small percentage of traffic first, with automatic rollback triggered if business KPIs (not just task metrics) regress beyond threshold during the canary window.

### Metrics
1. **task_kpi_correlation_coefficient**: Target: > 0.6 positive correlation between task eval and linked KPI; Alert threshold: < 0.2 or negative
2. **cost_per_resolution**: Target: within budgeted range; Alert threshold: > 20% increase release-over-release
3. **compliance_flag_rate_per_1000_interactions**: Target: 0; Alert threshold: > 0
4. **csat_delta_post_release_pct**: Target: >= 0; Alert threshold: < -3% versus pre-release baseline

### Alerts
1. **Business KPI Regression Despite Task-Metric Pass** (P1 - Critical): Condition - task eval score meets bar but a linked business KPI (CSAT, conversion, compliance flag rate) regresses beyond threshold in canary or post-release window. Action: Halt rollout/auto-rollback, require KPI-linked eval redesign before re-attempting release.
2. **Cost Outlier Spike** (P2 - Warning): Condition - cost per resolution increases more than 20% release-over-release. Action: Investigate tool-call efficiency, cap or throttle release traffic pending review.
3. **Compliance Flag Detected** (P1 - Critical): Condition - any production interaction flagged for compliance violation. Action: Immediate escalation to compliance team, pause affected flow pending review.

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
