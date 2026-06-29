# Self-Verification Illusion in Post-Rollback Health Confirmation

## Issue: After Executing an Automated Rollback, an Agent Asked to Confirm the Rollback Resolved the Incident Re-Queries the Same Deployment-Control-Plane Status Field It Used to Confirm the Rollback Itself Completed -- Which Correctly Shows "Rollback Successful" -- and Reports the Incident Resolved, Without Independently Checking Actual Service Health Signals (Error Rate, Latency, Real User Traffic) That Would Show the Underlying Regression Is Still Occurring

**Frequency**: Common

**Symptoms**
- Agent's post-rollback report states "Rollback completed successfully; incident resolved," citing only deployment-control-plane status (e.g., "Deployment state: ROLLED_BACK")
- Actual error-rate or latency dashboards continue showing the regression unchanged minutes after the rollback completes, because the rollback target itself was not the actual cause, or a stateful side effect persisted
- The agent's "verification" step queries the identical API and field used to confirm the rollback's mechanical completion, never querying an independent health signal
- On-call engineers, trusting the agent's "resolved" status, deprioritize the incident and are paged again shortly after when the regression is noticed independently
- The pattern recurs specifically when the rollback target was not the true root cause -- the deployment-control-plane correctly reports the rollback mechanically succeeded, which the agent conflates with the incident being resolved

**Root Cause**
Asking the same model to verify its own action's success using the same data source and reasoning path that confirmed the action's mechanical execution produces a confirmation that is largely a restatement of "the rollback command succeeded," not an independent check of whether the underlying problem is gone. Mechanical rollback completion and incident resolution are two different facts; the agent's verification step collapses them because the easiest, most available evidence (the control-plane status it already has) only speaks to the former.

**Example**
```
Incident: elevated 500 error rate; agent identifies the most recent deploy as the likely cause and triggers an automated rollback
Rollback executes; deployment-control-plane reports: "Deployment state: ROLLED_BACK, target version: v412"
Agent is asked to confirm the incident is resolved before closing it
Agent re-queries the deployment-control-plane status (same source, same field) and reports: "Rollback successful; incident resolved"
Actual cause was a downstream cache invalidation triggered by v413's deploy, not v413's code itself; rolling back the code did not clear the stale cache entries
Error rate, visible on the real-user-monitoring dashboard the agent never queried, remains elevated for another 25 minutes until a separate on-call engineer manually clears the cache
Post-incident review finds the agent's "verification" step never touched an actual health metric, only the rollback's own mechanical status
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Tool-use miscalibration research finds self-verification steps that reuse the same evidence source as the original action systematically overstate confidence relative to independent checks | [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264) |
| Failure taxonomies for platform-orchestrated agentic workflows identify confirmation steps that re-derive from the same execution trace as the original action as a recurring source of false-positive task completion | [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735) |
| Execution-provenance research argues that verifying an autonomous action's real-world effect requires evidence independent of the action's own reported status, since self-reported completion does not establish outcome correctness | [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1) |

**Contributing Factors**
- No requirement that post-rollback verification query a data source independent of the deployment-control-plane (e.g., real-user-monitoring, synthetic checks, error-rate dashboards)
- "Rollback successful" and "incident resolved" are treated as the same status field in the agent's workflow rather than two distinct claims requiring separate evidence
- Stateful side effects (caches, queues, schema changes) that a code rollback does not automatically reverse are not flagged as requiring a separate health check
- Incident-closure pressure favors the fastest available confirmation signal, and the control-plane status is returned fastest

---

## Mitigation Strategies

1. **Independent Health-Signal Gate**: Require incident closure to be gated on an independent health metric (error rate, latency, real-user-monitoring) returning to baseline, not solely on deployment-control-plane rollback status
2. **Distinct Claims Requirement**: Treat "rollback mechanically completed" and "incident resolved" as separate claims, each requiring its own evidence source, in the agent's reporting template
3. **Stateful-Side-Effect Checklist**: For rollbacks of deploys that touch caches, queues, or schemas, require an explicit check that those side effects were also reverted or are otherwise confirmed non-causal
4. **Delayed Re-Check**: Require a second, independent health check several minutes after the rollback before final closure, to catch regressions that do not clear immediately

### Metrics
- Rate of incidents reopened or re-paged within a short window after agent-reported "resolved" status
- Proportion of post-rollback verifications that query only deployment-control-plane status versus an independent health signal
- Mean time between agent-reported resolution and actual return-to-baseline on independent health metrics

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Resolution without independent check | Incident closed citing only control-plane rollback status | P1 | Reopen; require independent health-signal confirmation |
| Re-page after closure | Incident re-escalates within a short window of agent-reported resolution | P1 | Audit verification step; treat as false-positive closure |
| Stateful side effect unconfirmed | Rollback of a deploy with known stateful side effects closed without a side-effect check | P2 | Require explicit side-effect verification before re-closing |

---

## References

- [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264)
- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735)
- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
