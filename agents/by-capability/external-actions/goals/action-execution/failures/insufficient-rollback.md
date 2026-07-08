# Insufficient Rollback

## Issue: Agent cannot undo a bad action.

**Frequency**: Rare but Catastrophic

**Symptoms**
- No revert path after failure.
- [Add more specific symptoms]

**Root Cause**
Agent cannot undo a bad action.

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
1. **Rollback Workflow Definition**: For each action, define explicit rollback/compensation workflow. Document: what changes will be made → what compensating changes undo them → rollback execution steps. Pre-test rollback paths before deploying action in production.
2. **Reversible Defaults for Data Modification**: Design all data modifications with reversibility in mind. Example: use soft-delete instead of hard-delete, store snapshots of modified records, implement point-in-time restore. Default to reversible operations.
3. **Compensating Transaction Pattern**: For multi-step operations, define compensating transaction for each step. If operation fails mid-flight, execute compensation chain in reverse order to restore pre-action state. Test compensation paths regularly.

### Detection & Response
1. **Rollback Failure Detection**: Monitor rollback execution. Alert if rollback fails to restore expected state. Track: rollback_attempt, success/failure, time_to_restore, residual_state_delta. Log all rollback failures.
2. **State Restoration Verification**: After rollback completes, query resource state and verify it matches pre-action snapshot. Flag rollbacks that fail to fully restore state (partial rollback). Escalate partial rollbacks.
3. **Unrevertible Action Tracking**: Identify actions that cannot be rolled back (hard deletes, external API side-effects with no undo). Flag these as critical. Log all attempts to rollback unrevertible actions.

### Architecture Patterns
1. **Snapshot-Based Rollback**: For each action, create snapshot of affected resources pre-execution. Store snapshot in immutable store. On rollback, restore snapshot state. Enables point-in-time recovery.
2. **Compensation Transaction Registry**: Maintain registry of all compensation transactions (reverse operations). Each action has associated compensation_transaction_id. Enable automated compensation on failure.
3. **Event Sourcing with Replay**: Store all state changes as immutable events with reverse operations defined. Rollback by replaying events up to point before bad action, then applying compensation events.

### Metrics
1. **rollback_success_rate_percent**: Target: 100%; Alert threshold: < 95%; Track: successful rollbacks vs attempts
2. **rollback_execution_time_seconds_p95**: Target: < 60; Fast restoration is critical
3. **action_failures_without_rollback_per_day**: Target: 0; All failures must be rollback-able
4. **state_restoration_accuracy_percent**: Target: 100%; Rollback must restore exact pre-action state
5. **compensation_transaction_coverage_percent**: Target: 100%; Every action must have defined compensation

### Alerts
1. **Rollback Failure Detected** (P1 - Critical): Condition - rollback attempted but failed to restore state. Action: Immediate manual intervention, storage team alert, potential data recovery procedures, stakeholder notification.
2. **Unrevertible Action Executed** (P1 - Critical): Condition - agent executed action flagged as unrevertible without special approval. Action: Investigation, potential action denial, policy update.
3. **Compensation Transaction Missing** (P1 - Critical): Condition - action failed but no compensation transaction defined. Action: Immediate escalation, manual recovery attempt, post-incident review to add compensation path.

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

- [CSA-Agentic-Profile](https://labs.cloudsecurityalliance.org/agentic/agentic-nist-ai-rmf-profile-v1/)
- Note: Agentic AI governance profile built around NIST RMF.
