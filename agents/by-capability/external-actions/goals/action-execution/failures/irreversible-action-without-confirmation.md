# Irreversible Action Without Confirmation

## Issue: Agent deletes/sends/pays/deploys without approval.

**Frequency**: Rare but Catastrophic

**Symptoms**
- Destructive action without confirmation marker.
- [Add more specific symptoms]

**Root Cause**
Agent deletes/sends/pays/deploys without approval.

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
1. **Confirmation Requirement for Irreversible Actions**: Flag all irreversible actions (delete, terminate, archive-with-no-restore, permanent-disable) and require explicit human confirmation before execution. Action does not proceed without confirmation record. Confirmation must come from authorized human approver (not automated).
2. **Reversibility Classification Matrix**: Classify every action by reversibility level: reversible (easily undone), compensable (can be undone with compensation), irreversible (no undo). Only irreversible actions require mandatory confirmation. Maintain reversibility matrix in action registry.
3. **Confirmation Audit Trail with Immutable Record**: Log confirmation request with: action details, requester_agent, approver_human, approval_timestamp, approval_rationale. Store confirmation record in immutable audit log before action execution. Enables compliance and incident investigation.

### Detection & Response
1. **Unconfirmed Irreversible Action Detection**: Monitor action execution logs; flag any irreversible action lacking corresponding confirmation record. Alert on detection. Correlate agent with confirmation denial rate.
2. **Bulk Irreversible Action Detection**: Alert if agent executes 2+ irreversible actions in 5-minute window without confirmations (potential bulk delete attack). Pause agent pending review.
3. **Resource Orphaning Detection**: Track resource lifecycle; alert if irreversible action on parent resource leaves orphaned child resources (data integrity issue). Trigger investigation and potential compensation.

### Architecture Patterns
1. **Two-Phase Commit Pattern for Irreversible Actions**: Stage irreversible action with confirmation request. Require human approval via confirmation UI. Only then execute atomic commit. Automatic rollback if no confirmation within timeout window.
2. **Action Reversibility Metadata System**: Attach reversibility flag to all action definitions. Use flag to enforce confirmation gating at execution layer. Example: DELETE operation always has reversibility='irreversible'.
3. **Confirmation Workflow Middleware**: Intercept all irreversible actions. Route to confirmation workflow. Confirmation must complete with human approval before executing action. Timeout after 24hrs auto-cancels if no response.

### Metrics
1. **irreversible_actions_without_confirmation_per_day**: Target: 0; Any unconfirmed irreversible action is critical
2. **confirmation_rate_percent_for_irreversible**: Target: 100%; Every irreversible action must be confirmed
3. **confirmation_latency_p50_minutes**: Target: < 5; Approvers respond quickly
4. **confirmation_denial_rate_percent**: Target: < 5%; Low denial indicates accurate confirmation requests
5. **cancelled_irreversible_actions_post_timeout_per_month**: Target: < 3; Timeout cancellations should be rare

### Alerts
1. **Irreversible Action Without Confirmation** (P1 - Critical): Condition - irreversible action executed without human confirmation record. Action: Immediate investigation, potential rollback attempt, audit escalation, stakeholder notification.
2. **Confirmation Timeout Expired** (P2 - Warning): Condition - irreversible action staged but no confirmation within 24hrs. Action: Auto-cancel staged action, notify approver/requester, request resubmission.
3. **High Irreversible Action Volume** (P1 - Critical): Condition - agent executes 3+ irreversible actions in 1hr or 10+ in 1 day. Action: Require additional approval layer, immediate agent review, potential suspension.

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

- [OWASP-LLM-Top10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- Note: LLM application risks including prompt injection, insecure output handling, supply chain, sensitive information disclosure, excessive agency.
