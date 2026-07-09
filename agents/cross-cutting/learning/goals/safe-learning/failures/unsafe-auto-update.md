# Unsafe Auto-Update

## Issue: Agent updates itself without approval.

**Frequency**: Rare but Catastrophic

**Symptoms**
- Prompt/model/tool changes occur automatically in prod.
- [Add more specific symptoms]

**Root Cause**
Agent updates itself without approval.

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
1. **Human Approval Gate for Production Changes**: Any self-modification the agent proposes (prompt edit, tool config change, model swap) is routed to a human/governance approval queue and cannot reach production without explicit sign-off; the agent's runtime process has no code path that writes directly to production configuration.
2. **Least-Privilege Update Permissions**: The agent's runtime identity is granted read-only access to its own configuration store; applying an approved change requires a separate deployment pipeline with distinct credentials the agent process never holds, so even a compromised or misbehaving agent cannot self-promote a change.
3. **Staged/Canary Rollout Requirement**: No update, even one that has been approved, is allowed to go to 100% of traffic immediately; it must first pass a canary stage on a small traffic slice with automated health checks before broader promotion.

### Detection & Response
1. **Configuration Drift Detection**: Continuously diff the running configuration/prompt/model against the last signed, approved release; any mismatch is treated as an unauthorized change and triggers immediate alerting, independent of how the drift occurred.
2. **Unauthorized Write Attempt Monitoring**: Audit-log every write attempt to the config/prompt/model store and flag any write not tied to an approved change ticket, including attempts that were blocked by permissions (near-misses are still signal).
3. **Automatic Rollback on Canary Failure**: If canary-stage metrics (error rate, policy violations, quality scores) breach threshold, automatically revert to the prior version without waiting for a human to notice and trigger the rollback manually.

### Architecture Patterns
1. **Immutable Config Store with Signed Releases**: Production reads only from versioned, cryptographically signed artifacts; the agent process is architecturally incapable of writing to this store, only a separate release pipeline with its own credentials can.
2. **Canary Deployment Pipeline**: New versions are routed to a small percentage of traffic first, with automated health/policy checks gating promotion to full rollout, and instant rollback wired to the same health-check signal.
3. **Change Approval Service**: A governance component separate from the agent runtime that requires explicit human or board sign-off recorded before any promotion job is permitted to run, with the approval record linked to the deployed artifact hash.

### Metrics
1. **unauthorized_config_write_attempts_count**: Target: 0; Alert threshold: any occurrence
2. **canary_stage_coverage_percent**: Target: 100% of updates pass through canary; Alert threshold: < 100%
3. **auto_rollback_events_per_month**: Target: tracked, low single digits; Alert threshold: sudden spike indicating unstable update source
4. **mean_time_to_detect_drift**: Target: < 5 minutes; Alert threshold: > 30 minutes

### Alerts
1. **Unauthorized Production Change Detected** (P1 - Critical): Condition - running config/prompt/model differs from the last signed, approved release with no matching approval record. Action: Immediate freeze of the agent's update path, automatic rollback to signed release, security/governance incident opened.
2. **Canary Health Breach** (P2 - Warning): Condition - canary-stage metrics cross threshold during staged rollout. Action: Automatic rollback of canary traffic, block promotion, notify the update's approver.
3. **Configuration Drift Detected** (P3 - Info): Condition - periodic diff finds any mismatch between running and signed state, even transient. Action: Investigate deployment pipeline integrity, confirm no unauthorized write path exists.

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
