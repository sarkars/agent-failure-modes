# DevOps Incident Triage Agent: Business Goals, Failure Definitions, and Test List

An agent that reads alerts, classifies incidents, notifies the right on-call person, and takes only safe, pre-approved actions.

> **Read this first.** These are design starting points to adapt with your own business owners, not benchmarks or advice. No target numbers are given because none can be set without your baseline.

## Scope (a starting point)

**The agent does:**
- Classify alert severity and likely impact
- Notify the right on-call responder, respecting maintenance windows
- Run pre-approved safe actions and keep a timeline

**The agent does not:**
- Roll back or deploy without approval above its tier
- Change its own alerting rules or permissions
- Declare root cause without evidence

## Business goals

| # | Goal | Success means | Owner |
|---|---|---|---|
| G1 | Classify and match incidents correctly | Alerts are given the right severity and tied to the right service and past experience. | Head of site reliability |
| G2 | Notify the right people without causing fatigue | The right on-call person is paged for the right reasons, and suppression rules are honored. | On-call program owner |
| G3 | Act only within safe, approved limits | The agent takes only the actions it is allowed to, and can show the rollback worked. | Head of site reliability with security |
| G4 | Keep an accurate record of what happened | The timeline and the postmortem draft match the evidence. | Incident commander and reliability lead |

## Goal definitions

For every goal: how to measure it, how to find your baseline, what counts as a failure and how severe it is, and when the agent hands over to a person. Baseline method for all goals: Take a sample of conversations or cases the way a person handled them over a period you choose (one vendor's guidance uses 90 days as an example) and compute the same measure. A statement like "it takes too long" is not a baseline.

### G1. Classify and match incidents correctly

| Field | Definition |
|---|---|
| How to measure | Severity agreement with the incident commander's final call; share of alerts matched to the wrong runbook. |
| A failure is | A look-alike past incident or runbook is applied to a different problem. |
| Severity | Critical: a major outage classified as minor. High: a wrong runbook followed. Medium: a wrong service tag. |
| Hand over to a person when | Low confidence in the match, or customer impact is possible. |

**Failures to test for this goal (from the library):**
- [Embedding Retrieval Pulls Similar-but-Unrelated Past Incident as Resolution Precedent](../../by-use-case/devops/goals/incident-response/failures/embedding-retrieval-pulls-similar-but-unrelated-past-incident-as-resolution-precedent.md): An Incident-Response Agent That Retrieves a Past Incident's Resolution Steps via Semantic Similarity Search Over Incident Descriptions,…
- [Embedding Retrieval Misroutes Alert via Similar Runbook Match](../../by-use-case/devops/goals/alert-routing/failures/embedding-retrieval-misroutes-alert-via-similar-runbook-match.md): An Alert-Routing Agent That Decides Which Team to Page by Retrieving the Most Semantically Similar Past Incident Runbook for the Incoming…

### G2. Notify the right people without causing fatigue

| Field | Definition |
|---|---|
| How to measure | Pages to the wrong person; pages during known maintenance; time to acknowledgment. |
| A failure is | Alerts misrouted, maintenance-window suppression lost in a handoff, or affected segments omitted from communications. |
| Severity | High: a critical page missed or misrouted. Medium: a needless page. |
| Hand over to a person when | No acknowledgment within the set time. |

**Failures to test for this goal (from the library):**
- [On-Call Escalation Misroute](../../by-use-case/devops/goals/alert-routing/failures/on-call-escalation-misroute.md): Agent Routes a Critical Alert to the On-Call Engineer Listed in a Static Ownership Map That No Longer Matches the Service's Actual Current…
- [Multi-Agent Handoff Drops Maintenance-Window Suppression Flag Between Scheduler and Alert Router](../../by-use-case/devops/goals/alert-routing/failures/multi-agent-handoff-drops-maintenance-window-suppression-flag-between-scheduler-and-alert-router.md): A Maintenance-Scheduling Agent That Reasons, in Its Own Planning Output, That a Specific Set of Alerts Should Be Suppressed During a…
- [Multi-Agent Handoff Drops Affected-Customer Segment Before Comms Notification](../../by-use-case/devops/goals/incident-response/failures/multi-agent-handoff-drops-affected-customer-segment-before-comms-notification.md): A Triage Agent That Determines, in Its Own Investigation Output, That an Incident Affects Only a Specific Customer Segment -- e.g.,…

### G3. Act only within safe, approved limits

| Field | Definition |
|---|---|
| How to measure | Actions taken above the agent's tier without approval. Target: zero. Rollbacks later found partial or false-success. |
| A failure is | Partial rollbacks reported as complete, orchestrator status mistaken for application health, a canary that falsely passes. |
| Severity | Critical: an unapproved destructive action. High: a rollback reported healthy that was not. |
| Hand over to a person when | Any action above the agent's approved tier. |

**Failures to test for this goal (from the library):**
- [Partial Rollback State Corruption](../../by-use-case/devops/goals/rollback-safety/failures/partial-rollback-state-corruption.md): Agent Initiates an Automated Rollback of a Bad Deployment Without Accounting for Stateful Side Effects (Schema Changes, Queued Messages,…
- [Orchestrator Status Mistaken for Application Health After Rollback](../../by-use-case/devops/goals/rollback-safety/failures/orchestrator-status-mistaken-for-application-health-after-rollback.md): Rollback Agent Declares a Rollback Successful Based on the Deployment Orchestrator Reporting "Rollout Succeeded," Without Verifying That…
- [Canary Analysis False Pass](../../by-use-case/devops/goals/deployment-safety/failures/canary-analysis-false-pass.md): Agent Approves a Canary Deployment as Healthy Based on Aggregate Metrics That Mask a Regression Affecting a Specific Traffic Segment
- [Uncontrolled Destructive Actions Without Confirmation](../../cross-cutting/security/goals/security-autonomy/failures/uncontrolled-destructive-actions.md): Agent Executes Irreversible Operations (Delete, Destroy, Drop) Without User Approval

### G4. Keep an accurate record of what happened

| Field | Definition |
|---|---|
| How to measure | Postmortem claims that a reviewer finds unsupported; timeline gaps. |
| A failure is | Root cause attributed to the wrong cause, or events missing from the timeline. |
| Severity | High: a wrong root cause accepted. Medium: gaps. |
| Hand over to a person when | Any root-cause statement without evidence goes to a human. |

**Failures to test for this goal (from the library):**
- [Root Cause Misattribution in Agent-Drafted Postmortems](../../by-use-case/devops/goals/incident-response/failures/root-cause-misattribution-in-postmortems.md): Agent Drafting an Incident Postmortem Attributes Root Cause to the Last Change Deployed Before the Incident, Without Verifying a Causal Link

## Operations concerns for this agent

| Area | Why it matters here | Patterns |
|---|---|---|
| [Tool Reliability](../../cross-cutting/operations/goals/tool-reliability/) | The agent acts through monitoring, deploy, and paging tools | 19 |
| [Tool Access Scope Limits](../../cross-cutting/operations/goals/tool-access-scope-limits/) | Least privilege for production tools | 16 |
| [State Consistency](../../cross-cutting/operations/goals/state-consistency/) | Rollbacks and deploys leave state that must be reconciled | 8 |
| [Fault Tolerance](../../cross-cutting/operations/goals/fault-tolerance/) | Incident tools fail when the system is failing | 20 |
| [Agent Handoffs Delegation](../../cross-cutting/operations/goals/agent-handoffs-delegation/) | Flags and overrides must survive agent-to-agent transfers | 10 |
| [Human Oversight Reliability](../../cross-cutting/operations/goals/human-oversight-reliability/) | Approvals and escalation during an incident | 8 |
| [Real Time Performance](../../cross-cutting/operations/goals/real-time-performance/) | Speed matters in an incident | 12 |
| [Traceability](../../cross-cutting/operations/goals/traceability/) | Every action needs a record | 8 |
| [Cost Efficiency](../../cross-cutting/operations/goals/cost-efficiency/) | Alert storms can run up model and tool costs | 15 |

## Security and governance to check

- [Security Autonomy](../../cross-cutting/security/goals/security-autonomy/) (security)
- [Tool Authorization Limits](../../cross-cutting/security/goals/tool-authorization-limits/) (security)
- [Approval Workflows](../../cross-cutting/governance/goals/approval-workflows/) (governance)
- [Runtime Security](../../cross-cutting/security/goals/runtime-security/) (security)

## Decisions your business owner must make

- Autonomy tiers: which actions are automatic, which need approval
- Which services are in scope
- Severity definitions and who can change them
- Where the record of actions is stored

## Related

- [All agents by business goal](../)
