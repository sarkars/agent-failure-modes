# No Human Owner

## Issue: No accountable owner for agent decisions/actions.

**Frequency**: Common

**Symptoms**
- Incident lacks clear owner for remediation.
- An incident review stalls because no one can say who has the authority to decide whether to pause the agent.
- The agent's original creator has left the company and no formal handoff ever assigned a successor.
- Multiple teams assume "someone else" is responsible for the agent's behavior, so obvious issues go unaddressed for months.

**Root Cause**
Ownership is never made a deployment requirement in the first place: an agent can reach production with no mandatory, named individual recorded as accountable, and whatever ownership does exist tends to live informally — a Slack thread, one engineer's personal knowledge — rather than in an enforced registry. Because the org defaults to treating "whoever built it" as the implicit owner, and no process exists to formally reassign that role when the builder leaves or changes teams, the agent quietly becomes ownerless the moment that person exits, and no one discovers the gap until an incident requires someone to take responsibility.

**Example**
```
A pricing agent was built by an engineer on the growth team as a side
project 14 months ago. It quietly became load-bearing for a checkout
flow. The engineer left the company 6 months ago; no ownership transfer
was recorded.

The agent starts applying an incorrect discount rule after an upstream
API schema change. Customer support escalates, but the on-call engineer
paged has never touched this agent and doesn't know who built it, what
its intended behavior is, or who has authority to pause it.

It takes 9 hours and three escalations up the management chain to find
someone willing to take responsibility for disabling the agent, during
which the incorrect discount is applied to several hundred orders.
```

**Contributing Factors**
- Agents can be deployed to production without a mandatory, named-individual owner recorded anywhere.
- No process exists to reassign ownership when the original owner leaves the company or changes teams.
- Ownership is recorded informally (a Slack channel, an engineer's personal knowledge) rather than in a queryable, enforced registry.
- Teams treat "who owns this" as implicit from who built it, which breaks down once that person moves on.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Deployment ownership gate | Deployment manifest with an empty or invalid owner field | Deployment is blocked | Agent deploys to production without a valid owner |
| Departure-triggered flag | Simulated HR departure event for a recorded agent owner | Agent is flagged for reassignment within the SLA window | Agent remains attributed to a departed owner with no flag |
| Incident owner resolution | Incident opened for an agent with a registered owner | Owner is identified and paged within the target time | Incident responders cannot identify or reach an accountable owner |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| deployment_owner_gate_enforcement_rate | 100% | Attempt test deployments with missing/invalid owner fields and confirm all are blocked |
| departure_flag_latency | < 24h | Simulate an owner departure event and measure time until the agent is flagged |
| incident_owner_resolution_time | < 5 min | Time how long it takes a simulated incident responder to identify the accountable owner via the registry |

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
| ownerless_agent_count | > 0 |
| stale_owner_record_count | > 0 |
| owner_response_time_to_page_minutes | > 60 min |
| incident_owner_identification_time_minutes | > 30 min |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Agent Deployed Without Owner | Deployment manifest missing or references invalid owner | Critical |
| Owner Unreachable During Incident | Accountable owner does not respond to page within SLA | Critical |
| Owner Departure Detected | HR/identity event indicates named owner has left the company or team | Warning |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
