# No Incident Process

## Issue: No defined response for agent-caused failures.

**Frequency**: Common

**Symptoms**
- Slow remediation after AI incident.
- [Add more specific symptoms]

**Root Cause**
No defined response for agent-caused failures.

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
1. **Agent-Specific Incident Playbook**: Author a runbook covering agent-caused failure modes distinct from typical software incidents (hallucinated output sent to a user, unauthorized action taken, runaway tool-call loop, data leak via generated content) with pattern-specific first response steps, decision authority, and communication templates.
2. **Pre-Defined Severity Classification**: Establish severity tiers specific to agent incidents (e.g., SEV1: irreversible external action or financial/legal exposure; SEV2: incorrect but reversible action; SEV3: degraded quality with no external action) so responders classify and route immediately instead of debating severity mid-incident.
3. **Incident Response Drills**: Run periodic tabletop exercises simulating agent-caused failures (e.g., agent sends an unauthorized commitment, agent leaks PII in a response) so the on-call team has practiced the playbook before a real incident forces first contact under pressure.

### Detection & Response
1. **Automated Incident Trigger from Anomaly Signals**: Wire agent-specific anomaly detectors (spike in escalations, spike in tool-call failures, output flagged by a safety classifier) directly into the incident management system so an incident ticket opens automatically rather than depending on a human noticing.
2. **Incident Timeline Reconstruction Tooling**: Use the agent's audit trail (trace_id-linked perceive/decide/act logs) to auto-populate an incident timeline showing exactly what the agent saw, decided, and did leading up to the failure, cutting investigation time versus manual log spelunking.
3. **Post-Incident Review with Pattern Tagging**: Require every agent incident to close with a retro that tags the failure against a known pattern taxonomy (this catalog's categories) and records whether the playbook was followed, feeding back into playbook refinement.

### Architecture Patterns
1. **Agent Incident Command Structure**: Define a lightweight incident commander role for agent incidents with authority to trigger emergency mitigations (pause the agent, revoke a tool's access, roll back a version) without needing to work through the normal change-management approval chain during an active incident.
2. **Kill Switch Integration**: Build a circuit-breaker into the incident response tooling that lets the on-call responder immediately pause or throttle a specific agent, tool, or action type from the incident dashboard, rather than requiring a manual deploy to stop the bleeding.
3. **Incident-to-Playbook Linkage**: Tag each incident type in the ticketing system with a direct link to its corresponding playbook section, so responders land on the right runbook automatically instead of searching a wiki mid-incident.

### Metrics
1. **mean_time_to_detect_minutes**: Target: < 10 min; Alert threshold: > 30 min
2. **mean_time_to_mitigate_minutes**: Target: < 30 min (agent paused/action blocked); Alert threshold: > 90 min
3. **incidents_without_playbook_match_percent**: Target: < 10%; Alert threshold: > 25%
4. **post_incident_review_completion_rate_percent**: Target: 100% within 5 business days; Alert threshold: < 90%

### Alerts
1. **Agent Incident Triggered, No Playbook Match** (P1 - Critical): Condition - incident opened for an agent failure with no matching playbook entry. Action: Escalate to senior on-call for manual triage, fast-track new playbook creation post-incident.
2. **Mitigation SLA Breach** (P1 - Critical): Condition - agent-caused incident remains unmitigated past the target mitigation time. Action: Escalate to incident commander, consider emergency kill-switch activation.
3. **Post-Incident Review Overdue** (P3 - Info): Condition - closed incident has no completed retro after 5 business days. Action: Notify incident owner, block related agent changes until retro is filed.

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
