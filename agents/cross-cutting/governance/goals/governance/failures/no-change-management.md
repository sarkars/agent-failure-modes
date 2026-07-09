# No Change Management

## Issue: Prompt/tool/model changes go live without review.

**Frequency**: Common

**Symptoms**
- Regression after unreviewed change.
- [Add more specific symptoms]

**Root Cause**
Prompt/tool/model changes go live without review.

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
1. **Mandatory Review Gate on Prompt/Tool/Model Changes**: Require every change to system prompts, tool definitions, or model/version selection to go through a pull-request-style review with at least one independent approver before it can reach production, enforced by branch protection or a deployment gate that checks for approval status.
2. **Pre-Deployment Regression Suite**: Run the existing eval suite (golden test cases, adversarial prompts, known regression cases) against every proposed change before merge, and block deployment if pass rate drops below the established baseline for that agent.
3. **Staged Rollout for Behavioral Changes**: Route changes through a canary or staged environment (shadow traffic or a small percentage of real traffic) before full production rollout, so regressions surface against a bounded blast radius rather than the entire user base.

### Detection & Response
1. **Change-Correlated Regression Monitoring**: Tag every production behavior metric (error rate, escalation rate, user complaint rate, eval score) with the active prompt/tool/model version, and automatically diff metrics before/after each deployment to surface regressions tied to a specific change.
2. **Automated Rollback Trigger**: If post-deployment metrics breach a defined threshold within a monitoring window after a change goes live, automatically revert to the last known-good version and alert the on-call engineer rather than waiting for manual detection.
3. **Change Audit Trail Review**: Periodically review the change log for changes that bypassed the review gate (e.g., emergency hotfixes) and confirm they received retroactive review, closing the loop on any exceptions granted under time pressure.

### Architecture Patterns
1. **Version-Controlled Configuration Store**: Store prompts, tool schemas, and model version pins as versioned artifacts in source control (not inline in application code or a mutable admin panel), so every change has a diff, an author, and a reviewable history.
2. **CI/CD Gate for Agent Configuration**: Wire the eval suite and review requirement into the same CI/CD pipeline used for application code, so agent-configuration deployments are blocked exactly like a failing test would block a code deploy.
3. **Canary Traffic Router**: Deploy a routing layer that can split live traffic between the current production version and a candidate version, with automated metric comparison, before promoting the candidate to 100% traffic.

### Metrics
1. **unreviewed_change_count**: Target: 0; Alert threshold: > 0 changes deployed without passing review gate
2. **pre_deploy_eval_pass_rate_percent**: Target: 100% (matches or exceeds baseline); Alert threshold: any regression vs. baseline
3. **post_deploy_regression_incidents_per_month**: Target: 0; Alert threshold: > 1
4. **mean_time_to_rollback_minutes**: Target: < 15 min from detection; Alert threshold: > 60 min

### Alerts
1. **Unreviewed Change Deployed** (P1 - Critical): Condition - a prompt/tool/model change reached production without passing the review gate. Action: Immediate rollback, incident review, tighten deployment gate enforcement.
2. **Post-Deploy Metric Regression** (P1 - Critical): Condition - key behavior metric breaches threshold within the monitoring window after a change. Action: Auto-rollback to last known-good version, notify on-call, open incident.
3. **Emergency Change Bypass Used** (P3 - Info): Condition - a change was pushed via emergency/hotfix path bypassing normal review. Action: Require retroactive review within 24 hours, log exception in change audit trail.

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
