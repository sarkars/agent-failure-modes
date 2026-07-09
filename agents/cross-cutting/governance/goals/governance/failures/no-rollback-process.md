# No Rollback Process

## Issue: Cannot revert bad prompt/model/tool changes quickly.

**Frequency**: Common

**Symptoms**
- Bad release persists in production.
- [Add more specific symptoms]

**Root Cause**
Cannot revert bad prompt/model/tool changes quickly.

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
1. **Reversibility-by-Design Requirement**: Require every prompt, tool, or model change to be deployable as an atomic, versioned artifact with a corresponding "previous known-good" pointer maintained at all times, so a rollback is a pointer swap rather than a reconstructive effort under pressure.
2. **Tested Rollback Runbook**: Maintain a documented, regularly exercised rollback procedure specific to agent configuration (not generic infra rollback) covering prompt reversion, tool schema reversion, and model version pinning, verified via periodic rollback drills so the procedure is proven to work before it's needed in a real incident.
3. **Immutable Version History**: Store every deployed configuration version (prompt text, tool definitions, model pin) with a unique version ID in an immutable history, so "last known-good" is always an unambiguous, retrievable artifact rather than something reconstructed from memory or scattered commits.

### Detection & Response
1. **Automated Bad-Release Detection**: Monitor post-deployment metrics (error rate, eval score, escalation rate) against a baseline immediately after each change, so a bad release is flagged within minutes rather than persisting until a human notices degraded behavior.
2. **One-Command Rollback Trigger**: Provide on-call engineers a single action (CLI command, dashboard button) that reverts to the last known-good version without requiring a full deployment cycle, minimizing the time a bad release stays live once detected.
3. **Rollback Verification Check**: After executing a rollback, automatically re-run the eval suite against the reverted version to confirm it actually restores known-good behavior, rather than assuming the rollback succeeded.

### Architecture Patterns
1. **Blue-Green Configuration Deployment**: Maintain two live configuration slots (active and previous) for prompts/tools/model pins, so promoting a new version keeps the prior version warm and instantly reactivatable rather than requiring a rebuild.
2. **Rollback API/Service**: Expose a dedicated rollback endpoint in the deployment service that accepts a target version ID and atomically repoints the agent's live configuration, decoupled from the forward-deployment pipeline so rollback isn't blocked by the same gates that slow down normal releases.
3. **Version-Pinned Model Routing**: Route model calls through a layer that pins to an explicit model version/snapshot rather than a floating "latest" alias, so a vendor-side model update can't itself become an unrollbackable change.

### Metrics
1. **mean_time_to_rollback_minutes**: Target: < 10 min from detection; Alert threshold: > 30 min
2. **rollback_drill_success_rate_percent**: Target: 100% of scheduled drills succeed; Alert threshold: < 100%
3. **bad_release_dwell_time_minutes**: Target: < 15 min in production before rollback; Alert threshold: > 60 min
4. **rollback_verification_pass_rate_percent**: Target: 100%; Alert threshold: < 100%

### Alerts
1. **Bad Release Detected, No Rollback Executed** (P1 - Critical): Condition - post-deploy metrics breach threshold and no rollback initiated within target window. Action: Page on-call, execute rollback immediately, open incident.
2. **Rollback Execution Failure** (P1 - Critical): Condition - rollback command fails to restore last known-good version. Action: Escalate to senior engineer, manual intervention, consider full agent pause until resolved.
3. **Rollback Drill Failure** (P3 - Info): Condition - scheduled rollback drill does not complete successfully. Action: Investigate rollback tooling gap, remediate before next production deployment.

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
