# No Change Management

## Issue: Prompt/tool/model changes go live without review.

**Frequency**: Common

**Symptoms**
- Regression after unreviewed change.
- A one-line prompt tweak meant to fix a narrow edge case causes a broad regression across unrelated use cases.
- Engineers cannot identify which specific change caused a production regression because multiple prompt/tool/model edits shipped together without individual review.
- "Who changed this and why" cannot be answered for a live prompt, because edits were made directly in a shared config without version history.

**Root Cause**
Prompt/tool/model changes go live without review.

**Example**
```
An engineer edits the production system prompt directly in an admin
panel to fix a formatting bug in one response type, then saves
immediately without running it against the eval suite or getting a
second reviewer.

The edit inadvertently removes a clause instructing the agent to always
cite its data source. Within an hour, the agent begins generating
unsourced financial figures in customer-facing responses.

Because the change wasn't logged with an author, timestamp, or diff, and
no eval regression was run, it takes the on-call team 6 hours to
identify the prompt edit — rather than the change itself — as the root
cause, during which the agent serves the flawed behavior to thousands
of users.
```

**Contributing Factors**
- Prompts/tool schemas are editable directly in a live admin panel or config file with no review requirement.
- No automated eval suite runs against proposed changes before they reach production.
- Changes are not versioned individually, so a batch of edits can't be isolated to identify which one caused a regression.
- Emergency/hotfix paths exist that bypass the review gate with no requirement for retroactive review.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Review gate enforcement | A prompt/tool/model change submitted without approval | Deployment is blocked | Change reaches production without a recorded approval |
| Pre-deploy regression detection | A change that fails 2+ golden eval cases | Deployment is blocked and flagged | Change deploys despite eval regression |
| Automated rollback trigger | Post-deploy metrics breach threshold within monitoring window | Agent auto-reverts to last known-good version | Bad version remains live past the monitoring window |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| review_gate_bypass_rate | 0% | Audit deployment log for changes lacking a recorded approval |
| eval_regression_catch_rate | 100% | Inject known-bad changes into the pipeline and verify all are blocked pre-deploy |
| auto_rollback_trigger_accuracy | 100% | Simulate a post-deploy metric breach and confirm automatic rollback fires within the target window |

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
| unreviewed_change_count | > 0 changes deployed without passing review gate |
| pre_deploy_eval_pass_rate_percent | any regression vs. baseline |
| post_deploy_regression_incidents_per_month | > 1 |
| mean_time_to_rollback_minutes | > 60 min |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Unreviewed Change Deployed | A prompt/tool/model change reached production without passing the review gate | Critical |
| Post-Deploy Metric Regression | Key behavior metric breaches threshold after a change | Critical |
| Emergency Change Bypass Used | A change was pushed via emergency/hotfix path bypassing normal review | Info |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
