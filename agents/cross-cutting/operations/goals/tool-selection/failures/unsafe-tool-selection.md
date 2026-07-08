# Unsafe Tool Selection

## Issue: Agent uses destructive capability for exploratory work.

**Frequency**: Rare but Catastrophic

**Symptoms**
- Delete/update/deploy used during discovery.
- [Add more specific symptoms]

**Root Cause**
Agent uses destructive capability for exploratory work.

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
1. **Read-Only Default with Explicit Escalation**: Scope the agent's default credential set to read-only operations for any task phase classified as discovery/exploration. Destructive tools (delete, update, deploy) are only reachable through a separate, explicitly-granted write tier that requires the task to declare intent to modify state before the tier is unlocked.
2. **Least-Privilege Credential Separation**: Issue distinct credentials/roles for read vs. write vs. destructive operations rather than a single broad-scope credential, so even a model that "decides" to use a destructive tool during exploration is blocked at the auth layer, not just by prompt instruction.
3. **Dry-Run Requirement for Ambiguous-Intent Destructive Calls**: When task intent is ambiguous (e.g., "clean up X" could mean list-and-report or delete), require a dry-run/simulation mode that reports what would be affected without executing, and require explicit confirmation before the real destructive call is permitted.

### Detection & Response
1. **Intent-Phase Mismatch Detector**: Classify each task turn as discovery/exploration vs. execution based on task framing and prior tool calls; flag any destructive tool invocation (delete/update/deploy) that occurs while the task is still in a discovery-classified phase, since this is the direct signature of the failure.
2. **Privilege Escalation Audit**: Log every transition from read-tier to write/destructive-tier credentials with the justification the agent provided; review escalations that lack a clear preceding user instruction or task requirement for a destructive action.
3. **Near-Miss Gate Rejection Tracking**: Count how often the tiered access broker blocks a destructive call attempted without the required grant — a rising trend indicates the underlying prompt/policy is not adequately steering the agent away from destructive tools even though the gate is catching it.

### Architecture Patterns
1. **Tiered Tool Access Broker**: A broker service mediates all tool calls and enforces that destructive-tier tools are only invocable when the current task has an active, explicitly-granted write/destructive scope; read-only tier is the unconditional default for new sessions.
2. **Phase-to-Risk-Tier Policy Engine**: A policy engine maps declared task phase (discovery, planning, execution) to the maximum allowed tool risk tier, and the broker consults this engine on every call rather than trusting the agent's self-reported intent alone.
3. **Pre-State Snapshot and Rollback Log**: Every destructive call captures a pre-state snapshot of the affected resource before execution and writes it to an immutable audit log, enabling fast rollback if a destructive action is later determined to have been inappropriate for the task phase.

### Metrics
1. **destructive_call_in_discovery_phase_rate**: Target: 0%; Alert threshold: > 0 (any occurrence is critical)
2. **unauthorized_escalation_attempt_count**: Target: 0 successful unauthorized escalations; Alert threshold: any success, monitor attempt volume for trend
3. **dry_run_coverage_for_destructive_actions**: Target: 100% of ambiguous-intent destructive calls preceded by dry-run; Alert threshold: < 90%
4. **rollback_invocation_rate**: Target: < 1% of destructive calls; Alert threshold: > 3% (indicates frequent inappropriate destructive actions)

### Alerts
1. **Destructive Call During Discovery Phase** (P1 - Critical): Condition - delete/update/deploy invoked while task phase classifier indicates exploration/discovery. Action: Block execution if not yet committed, trigger rollback if committed, page on-call, freeze agent's write-tier grant pending review.
2. **Unauthorized Escalation Attempt** (P1 - Critical): Condition - agent attempts a destructive-tier call without an active write grant. Action: Hard block at broker, alert security/on-call, audit the session for prompt injection or policy bypass.
3. **Rising Near-Miss Rate** (P2 - Warning): Condition - broker-blocked destructive attempts trend upward week-over-week. Action: Review prompt/policy tuning, consider tightening phase classifier.

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
