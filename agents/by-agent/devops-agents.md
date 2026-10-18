# DevOps Agents: Business Goals, Failure Patterns, and Fixes

**DevOps Agents fail along 8 goals: Anomaly Detection, Cost Optimization, Deployment Safety carry the most documented failures.** This page maps each goal to the failures that threaten it, so you can decide what to protect first and where the fixes are.

## Key Takeaways

- 30 documented failure patterns across 8 goals. What it does: watch systems, route alerts, respond to incidents, and manage deployments.
- The most documented goal is [Anomaly Detection](../by-use-case/devops/goals/anomaly-detection/) with 5 patterns.
- Frequencies below are as recorded on each pattern page. They are not measured rates.
- Business-goal definitions (metric, baseline, owner, what counts as a failure) are not written yet for this agent. Define them before choosing which patterns to prioritize.

## Goals this agent must protect

| Goal | When it fails | Patterns |
|---|---|---|
| [Anomaly Detection](../by-use-case/devops/goals/anomaly-detection/) | Anomaly-detection agents produce false positives and false negatives because they optimize a baseline or threshold against the wrong reference | 5 |
| [Cost Optimization](../by-use-case/devops/goals/cost-optimization/) | Cost-optimization agents make recommendations and autonomous actions based on data that looks current but isn't | 5 |
| [Deployment Safety](../by-use-case/devops/goals/deployment-safety/) | Deployment-safety agents fail to catch unsafe conditions before go-live because they apply the wrong checklist | 4 |
| [Monitoring](../by-use-case/devops/goals/monitoring/) | Monitoring agents produce blind spots in observability by applying sampling policies that drop exactly the rare events most critical for diagnosis | 4 |
| [Alert Routing](../by-use-case/devops/goals/alert-routing/) | When the routing decision rests on an input that looks authoritative but isn't | 3 |
| [Capacity Planning](../by-use-case/devops/goals/capacity-planning/) | Capacity-planning agents make recommendations that look accurate at the aggregate level but fail operationally because they optimize against a single signal | 3 |
| [Incident Response](../by-use-case/devops/goals/incident-response/) | Incident-response agents fail during triage and response because they retrieve a resolution based on surface-level symptom similarity instead of root-cause signature | 3 |
| [Rollback Safety](../by-use-case/devops/goals/rollback-safety/) | Rollback agents fail to actually restore working behavior because they treat orchestrator-level deployment success | 3 |

## Failures most often recorded

| Failure | What goes wrong | Recorded frequency |
|---|---|---|
| [Alert Fatigue from Agent-Tuned Threshold Misconfiguration](../by-use-case/devops/goals/anomaly-detection/failures/alert-fatigue-from-threshold-misconfiguration.md) | Agent Auto-Tunes Anomaly Detection Thresholds to Minimize False Positives on Historical Data, Inadvertently Suppressing Sensitivity to Genuinely… | Very Common |
| [Rightsizing Recommendation Overcorrection](../by-use-case/devops/goals/cost-optimization/failures/rightsizing-recommendation-overcorrection.md) | Agent Recommends Downsizing Compute Resources Based on Average Utilization, Ignoring Peak Load Requirements That Drive Actual Capacity Needs | Very Common |
| [Seasonal Blindness in Anomaly Detection](../by-use-case/devops/goals/anomaly-detection/failures/seasonal-blindness.md) | Anomaly Detection Model Flags Normal Seasonal Patterns as Anomalies; High False Positive Rate | Very Common |
| [Autoscaling Thrash from Reactive Agent Decisions](../by-use-case/devops/goals/capacity-planning/failures/autoscaling-thrash.md) | Agent-Driven Autoscaler Repeatedly Scales Up and Down in Short Cycles Because Scaling Decisions React to Instantaneous Metrics Without Accounting for… | Common |
| [Canary Analysis False Pass](../by-use-case/devops/goals/deployment-safety/failures/canary-analysis-false-pass.md) | Agent Approves a Canary Deployment as Healthy Based on Aggregate Metrics That Mask a Regression Affecting a Specific Traffic Segment | Common |
| [Correlation-Induced False Positives in Multi-Metric Anomaly Detection](../by-use-case/devops/goals/anomaly-detection/failures/correlation-induced-false-positives.md) | Multiple Correlated Metrics All Spike Together; Model Flags as Coordinated Attack But Actually Cascading Failure | Common |

## Before you build: define each goal

For every goal in the table, write down: the metric and how you measure its baseline today; the person who owns it; what counts as a failure and how severe it is; who is told when it happens; and when a person takes over. Then use the failures above as your test list.

## Security and governance

Every agent also needs the cross-cutting checks in [security](../cross-cutting/security/), [accuracy](../cross-cutting/accuracy/), [governance](../cross-cutting/governance/), and [operations](../cross-cutting/operations/).

## Frequently Asked Questions

### What fails most often in devops agents?

The most documented goal is Anomaly Detection (5 patterns). The failures table above lists the ones recorded as most frequent. These are the library's records, not measured rates.

### Where should I start when building devops agents?

Define your business goals and what counts as failure, then test against the failure patterns for each goal. The section above lists what to write down.

## Related

- [All agents by business goal](./)
