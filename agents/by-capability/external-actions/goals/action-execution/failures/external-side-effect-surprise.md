# External Side-Effect Surprise

## Issue: Agent misses that action triggers notifications, billing, shipment, or deployment.

**Frequency**: Common

**Symptoms**
- Stakeholder receives unexpected alert/change.
- [Add more specific symptoms]

**Root Cause**
Agent misses that action triggers notifications, billing, shipment, or deployment.

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
1. **Side-Effect Manifest Declaration**: Define explicit manifest for each action listing all intended external side-effects (notifications, billing triggers, cascading deletes, deployments, etc.). Manifest stored as versioned, reviewable artifact. Action execution only triggers side-effects explicitly listed in manifest.
2. **Side-Effect Approval UI**: For actions with side-effects, present comprehensive approval interface listing all effects with human-readable descriptions (who gets notified? which systems affected?). Require explicit agent/user confirmation before proceeding. Show impact scope (number of users affected, systems impacted).
3. **Side-Effect Scope Limitation**: Restrict side-effect scope with granular authorization. Example: cascade delete only affects resources agent has permission to delete. Unintended side-effects blocked at execution layer.

### Detection & Response
1. **Unintended Side-Effect Detection**: Post-action, compare actual resource state changes with declared side-effects manifest. Flag undeclared changes (side-effect executed without permission). Log: expected side-effects vs actual side-effects, anomalies.
2. **Cascading Change Audit**: Track all resources modified by action including cascades and side-effects. Alert if single action cascades affect unexpectedly high resource count (> threshold). Example: delete policy affects 10k+ users = alert.
3. **Third-Party Service Call Validation**: Log all external API calls triggered by agent actions with: service, operation, parameters, result. Validate each call against approved side-effect registry. Non-registered calls rejected with alert.

### Architecture Patterns
1. **Explicit Side-Effect Registry**: Maintain authoritative registry of action_type → permitted_side_effects[] mappings. All side-effects must be registered before action execution. Non-registered side-effects automatically blocked and logged.
2. **Side-Effect Intercept Middleware**: Layer between agent and external systems that intercepts all outbound calls (APIs, notifications, billing events, deployments). Validates each call against side-effect manifest before delegating. Fail-closed: no manifest entry = call blocked.
3. **Change Audit Log with Causality Tracking**: Immutable log of all resource changes with causality chain: initial_action → side_effect_1 → side_effect_2. Track: timestamp, actor, change type, reason code. Enable traceability and incident response.

### Metrics
1. **unintended_side_effects_per_action**: Target: 0; Any unintended side-effect is critical failure
2. **side_effect_manifest_coverage_percent**: Target: 100%; Every side-effect must be declared
3. **cascading_modifications_exceeding_threshold_per_day**: Target: 0; Alert on unexpected cascade scope
4. **external_api_call_validation_rate_percent**: Target: 100%; Every external call must pass validation
5. **side_effect_approval_denial_rate_percent**: Target: < 2%; Low denial rate indicates manifest accuracy

### Alerts
1. **Unintended Side-Effect Detected** (P1 - Critical): Condition - resource modified outside declared side-effects. Action: Immediately block action execution, security audit, attempt rollback if possible, notify stakeholders.
2. **High Cascading Impact Detected** (P1 - Critical): Condition - single action triggers modification of > threshold resources (e.g., 1000). Action: Auto-pause action, require explicit approval with impact review, executive notification.
3. **Unregistered External Call Attempt** (P1 - Critical): Condition - agent action triggers API call to unregistered external service. Action: Block call, security alert, investigation, update side-effect registry.

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

- [CSA-Agentic-Profile](https://labs.cloudsecurityalliance.org/agentic/agentic-nist-ai-rmf-profile-v1/)
- Note: Agentic AI governance profile built around NIST RMF.
