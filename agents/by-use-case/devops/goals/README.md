# Devops AI Agent Failures by Goal: 30 Patterns, Causes, and Fixes

**Devops failures in AI agents are grouped here into 8 goals, each with a catalog of named failure patterns, the symptoms you will see, the root cause, and mitigations you can copy.** Start from the symptom you are debugging, pick the matching goal below, and open its failure list.

## Key Takeaways

- This use case covers 8 goals and 30 documented failure patterns.
- The largest goal is [Anomaly Detection](anomaly-detection/) with 5 patterns.
- Each goal page explains the failure class, how to tell it apart from its neighbors, and which mitigations apply across its patterns.
- Each failure page covers the symptoms, an example, the root cause, and how to fix it.

## Devops Goals

| Goal | What goes wrong | Patterns |
|---|---|---|
| [Alert Routing](alert-routing/) | Alert-routing agents page the wrong team when the routing decision rests on an input that looks authoritative but isn't | 3 |
| [Anomaly Detection](anomaly-detection/) | Anomaly-detection agents produce false positives and false negatives because they optimize a baseline or threshold against the wrong reference | 5 |
| [Capacity Planning](capacity-planning/) | Capacity-planning agents make recommendations that look accurate at the aggregate level but fail operationally because they optimize against a single signal | 3 |
| [Cost Optimization](cost-optimization/) | Cost-optimization agents make recommendations and autonomous actions based on data that looks current but isn't, configurations that lack required guards against non-financial side effects | 5 |
| [Deployment Safety](deployment-safety/) | Deployment-safety agents fail to catch unsafe conditions before go-live because they apply the wrong checklist, miss dependency incompatibilities, base approval on segment-obscured aggregate metrics | 4 |
| [Incident Response](incident-response/) | Incident-response agents fail during triage and response because they retrieve a resolution based on surface-level symptom similarity instead of root-cause signature matching | 3 |
| [Monitoring](monitoring/) | Monitoring agents produce blind spots in observability by applying sampling policies that drop exactly the rare events most critical for diagnosis, configuring metrics with unbounded labels that overflow storage | 4 |
| [Rollback Safety](rollback-safety/) | Rollback agents fail to actually restore working behavior because they treat orchestrator-level deployment success (pods are Ready, the rollout state is Succeeded) as sufficient validation that the application is healthy | 3 |

**Total: 30 patterns**

## Frequently Asked Questions

### Where do I start if my devops agent is failing?

Match the symptom to a goal in the table above, then open that goal's page for how to tell its failures apart and where to look first. Each failure page ends in mitigations you can apply directly.

### How are these devops failure patterns organized?

By goal: the outcome the agent is supposed to achieve. Under each goal, a `failures` folder holds one page per pattern. For the full picture see the [Devops overview](../).

## Related

- [Devops overview](../)
- [All agent failure patterns](../../../)
