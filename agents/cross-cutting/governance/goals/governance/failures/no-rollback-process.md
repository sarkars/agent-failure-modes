# No Rollback Process

## Issue: Cannot revert bad prompt/model/tool changes quickly.

**Frequency**: Common

**Symptoms**
- Bad release persists in production.
- A bad prompt change stays live for hours because reverting it requires reconstructing the previous version from memory or scattered commits.
- The team discovers during an actual incident that the "rollback procedure" has never been tested and doesn't actually work.
- Reverting a model version pin breaks because the vendor's "latest" alias has moved on and the exact prior snapshot is no longer identifiable.

**Root Cause**
Cannot revert bad prompt/model/tool changes quickly.

**Example**
```
A prompt change intended to make the agent's tone more concise ships to
production. It inadvertently causes the agent to omit required legal
disclaimers from loan-related responses.

The on-call engineer wants to revert immediately, but the previous
prompt version only exists as an old Slack message and a
partially-remembered diff — there is no versioned artifact with an
unambiguous "last known-good" pointer.

Reconstructing the exact prior prompt takes 45 minutes of
cross-referencing chat history and old deployment logs, during which the
agent continues serving non-compliant responses to loan applicants.
```

**Contributing Factors**
- Configuration changes (prompts, tool schemas, model pins) are not stored as versioned, individually addressable artifacts.
- No "last known-good" pointer is maintained alongside the live configuration.
- Rollback procedures are documented but never exercised, so they're unproven when actually needed.
- Model version routing uses floating aliases ("latest") rather than pinned snapshots, making a vendor-side update itself unrollbackable.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Rollback execution time | Trigger rollback to last known-good version | Configuration reverts within target time | Rollback takes longer than target or fails to complete |
| Rollback drill | Scheduled rollback drill against a non-production environment | Drill completes successfully, restoring known-good behavior | Drill fails or reveals the rollback path doesn't work |
| Post-rollback verification | Rollback executed after a detected regression | Eval suite re-run confirms known-good behavior is restored | Rollback completes but eval suite still shows regression |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| rollback_execution_time | < 10 min | Time a triggered rollback from initiation to confirmed reversion |
| rollback_drill_pass_rate | 100% | Track pass/fail outcomes of scheduled rollback drills over time |
| post_rollback_eval_pass_rate | 100% | Re-run the eval suite immediately after each rollback and confirm baseline is restored |

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
| mean_time_to_rollback_minutes | > 30 min |
| rollback_drill_success_rate_percent | < 100% |
| bad_release_dwell_time_minutes | > 60 min |
| rollback_verification_pass_rate_percent | < 100% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Bad Release Detected, No Rollback Executed | Post-deploy metrics breach threshold and no rollback initiated within target window | Critical |
| Rollback Execution Failure | Rollback command fails to restore last known-good version | Critical |
| Rollback Drill Failure | Scheduled rollback drill does not complete successfully | Info |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
