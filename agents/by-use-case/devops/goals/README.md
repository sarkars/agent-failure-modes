# Devops AI Agent Failures by Goal: 30 Patterns, Causes, and Fixes

**Devops AI agents fail in 8 distinct ways, grouped by the goal each failure breaks.** Find the goal that matches what you are seeing, open its list, and use the fix on each pattern page.

## Key Takeaways

- 30 documented patterns across 8 goals; the most documented is [Anomaly Detection](anomaly-detection/) with 5.
- Each pattern page gives the symptoms, an example, the root cause, and mitigations.

## Devops Goals

| Goal | When it fails | Patterns |
|---|---|---|
| [Alert Routing](alert-routing/) | When the routing decision rests on an input that looks authoritative but isn't — a service-ownership mapping that was never revalidated after a reorg | 3 |
| Anomaly Detection | Anomaly-detection agents produce false positives and false negatives because they optimize a baseline or threshold against the wrong reference — recent noise instead of a recall floor | 5 |
| [Capacity Planning](capacity-planning/) | Capacity-planning agents make recommendations that look accurate at the aggregate level but fail operationally because they optimize against a single signal | 3 |
| [Cost Optimization](cost-optimization/) | Cost-optimization agents make recommendations and autonomous actions based on data that looks current but isn't, configurations that lack required guards against non-financial side effects | 5 |
| [Deployment Safety](deployment-safety/) | Deployment-safety agents fail to catch unsafe conditions before go-live because they apply the wrong checklist, miss dependency incompatibilities, base approval on segment-obscured aggregate metrics | 4 |
| [Incident Response](incident-response/) | Incident-response agents fail during triage and response because they retrieve a resolution based on surface-level symptom similarity instead of root-cause signature matching | 3 |
| [Monitoring](monitoring/) | Monitoring agents produce blind spots in observability by applying sampling policies that drop exactly the rare events most critical for diagnosis | 4 |
| [Rollback Safety](rollback-safety/) | Rollback agents fail to actually restore working behavior because they treat orchestrator-level deployment success | 3 |

**Total: 30 patterns**

## Frequently Asked Questions

### What causes an anomaly detector to flag normal seasonal traffic as an incident?

A statistical baseline built on a simple mean-and-standard-deviation model with no explicit seasonal component — daily, weekly, and yearly traffic cycles look identical to a real spike unless the model decomposes trend and seasonality first. See Anomaly Detection.

### What causes a cost-optimization agent to act on data that is already out of date?

Billing/cost-export data is commonly delivered on a batch cycle (hours to a day) rather than in real time, and the agent's prompt and decision logic do not distinguish between "this export reflects current spend" and "this export is the most recent available snapshot." Without cross-checking the export's timestamp against a faster-refreshing live signal (current utilization, recent traffic), the agent can act on a snapshot that was already hours old at the time of decision. See Cost Optimization.

### What causes a deploy checklist to omit a critical safety gate?

When checklist selection is based on semantic similarity over service description rather than structured service attributes, two checklists with similar prose (both describing "a standard deploy review") can score equally in embedding space despite one being missing a section required for stateful services. See Deployment Safety.

## Related

- [Devops overview](../)
- [All agent failure patterns](../../../)
