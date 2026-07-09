# No Human Owner

## Issue: No accountable owner for agent decisions/actions.

**Frequency**: Common

**Symptoms**
- Incident lacks clear owner for remediation.
- [Add more specific symptoms]

**Root Cause**
No accountable owner for agent decisions/actions.

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
1. **Mandatory Owner Assignment at Deployment**: Block any agent from being deployed to production without a named individual (not a team alias) recorded as the accountable owner in the deployment manifest, covering decision authority, escalation contact, and on-call responsibility.
2. **RACI Registration per Agent Capability**: For each capability/tool the agent has, register who is Responsible, Accountable, Consulted, and Informed, so that when an incident touches a specific action type, the accountable party is immediately identifiable rather than requiring an org-chart hunt.
3. **Ownership Transfer Workflow**: Require any change of agent ownership (team reorg, employee departure) to go through an explicit handoff process that updates the ownership registry before the transfer is considered complete, preventing agents from silently becoming ownerless.

### Detection & Response
1. **Ownerless Agent Scanning**: Periodically cross-reference the agent inventory against the ownership registry and HR/team roster to detect agents whose owner has left the company, changed teams, or was never assigned, flagging them for immediate reassignment.
2. **Owner Responsiveness Tracking**: Monitor response time when an owner is paged for an incident or review request; repeated non-response indicates the named owner is not actually accountable in practice and the registry entry needs correction.
3. **Incident Owner Resolution Time**: Track how long it takes to identify and engage the accountable owner from the moment an incident touching that agent is opened; a growing resolution time signals ownership records are stale or ambiguous.

### Architecture Patterns
1. **Ownership Registry Service**: Maintain a queryable registry mapping agent_id → owner → backup_owner → team → escalation_path, integrated with the incident management and paging system so ownership lookup is automatic during an incident rather than manual.
2. **Deployment Manifest Enforcement**: Require the CI/CD pipeline that deploys agent configuration to read owner metadata from the manifest and reject deployment if the owner field is empty or references a deactivated account.
3. **Org-Change Webhook Integration**: Wire the ownership registry to HR/identity system events (departure, team change) so owner records are automatically flagged stale the moment the underlying employee status changes, rather than waiting for a periodic audit.

### Metrics
1. **ownerless_agent_count**: Target: 0; Alert threshold: > 0
2. **stale_owner_record_count**: Target: 0; Alert threshold: > 0 (owner departed/changed teams without registry update)
3. **owner_response_time_to_page_minutes**: Target: < 15 min for P1 incidents; Alert threshold: > 60 min
4. **incident_owner_identification_time_minutes**: Target: < 5 min; Alert threshold: > 30 min

### Alerts
1. **Agent Deployed Without Owner** (P1 - Critical): Condition - deployment manifest missing or references invalid owner. Action: Block deployment, require ownership assignment before retry.
2. **Owner Unreachable During Incident** (P1 - Critical): Condition - accountable owner does not respond to page within SLA. Action: Escalate to backup owner and team lead, initiate ownership review post-incident.
3. **Owner Departure Detected** (P2 - Warning): Condition - HR/identity event indicates named owner has left the company or team. Action: Freeze non-essential agent changes, trigger mandatory reassignment workflow within 5 business days.

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
