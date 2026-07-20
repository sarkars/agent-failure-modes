# Model Downgrade Silent Failure

## Issue
A cost-optimizing router automatically shifts traffic from a higher-quality (and higher-cost) model to a cheaper one — based on budget pressure, rate limits, or a tuning change — without any mechanism to measure or surface the resulting quality impact. The downgrade is deliberate and often reasonable as a cost decision, but it is invisible: no dashboard, alert, or user-facing signal distinguishes "answered by the model we validated for this task" from "answered by a cheaper substitute picked to save money."

**Frequency**: Common

**Symptoms**
- Output quality on a task category drops after a routing config change, but nothing in monitoring flags the change as the cause because quality isn't tracked per routing decision
- Cost dashboards show the downgrade as a clean win (lower spend, same request volume) with no corresponding quality metric to weigh against it
- Users or downstream teams notice degraded results anecdotally weeks before any internal system flags the routing change
- The same task type receives inconsistent quality depending on which cost-tier threshold it happened to fall into that day, with no visibility into which tier served which request
- Rolling back a downgrade after user complaints requires manually correlating complaint timing with routing config history, since the two aren't linked

## Root Cause
Cost-based routers are typically built to optimize a single visible metric — spend per request or requests-per-dollar — because that metric is easy to measure in real time, while quality is hard to measure in real time and is usually only evaluated offline, periodically, or not at all for production traffic. This asymmetry means the routing system has a tight feedback loop for cost and no feedback loop for quality, so it will happily shift traffic toward cheaper models whenever budget pressure or a tuning pass suggests it, with nothing in the loop to resist the shift even when quality suffers. The downgrade is also usually implemented as a global or category-level threshold change rather than a per-request decision, so it silently reclassifies an entire slice of traffic at once, and unless someone happens to be watching quality metrics for exactly that slice at exactly that time, the regression goes unnoticed until it accumulates into a visible pattern of complaints.

## Example
```
A support-ticket triage agent uses a router that shifts 30% of "routine"
category tickets from a premium model ($0.03/ticket) to a budget model
($0.004/ticket) after a cost-review meeting sets a new monthly spend
target.

The budget model is measurably worse at detecting sarcasm and implied
urgency in ticket text - a known but previously deprioritized quality gap
- so it under-escalates a growing share of "routine"-classified tickets
that actually needed urgent handling.

Spend drops 22% that month, hitting the cost target and getting reported
as a win in the ops review. Three weeks later, a spike in customer
complaints about slow escalation is investigated and traced back to the
routing change - by which point roughly 400 tickets were mishandled with
no quality metric having flagged the downgrade at the time it happened.
```

## Statistics
| Finding | Context |
|---------|---------|
| Cost-driven routing changes are tracked with real-time dashboards in the substantial majority of production systems, while quality impact of the same changes is typically evaluated only periodically or not at all | Typical pattern observed across agent-routing infrastructure reviews |
| Quality regressions from silent downgrades are usually detected via user complaints or downstream error spikes rather than internal monitoring, with a lag on the order of days to weeks | Estimated from postmortems of routing-related quality incidents |
| Pairing every routing config change with a mandatory quality-delta evaluation before full rollout substantially reduces the detection lag for downgrade-driven regressions | Typical range reported by teams that added this gate |

## Mitigations
1. **Quality-cost paired dashboards**: Track a quality metric (task success rate, escalation accuracy, user satisfaction) alongside cost for every routing tier, so a downgrade's tradeoff is visible in the same view as its savings, not just in a separate offline eval.
2. **Shadow evaluation before full rollout**: Route a small percentage of traffic to the proposed cheaper model and compare quality against the current model before shifting the full traffic share, rather than switching all at once based on cost projections alone.
3. **Routing-change changelog linked to quality metrics**: Log every routing config change with a timestamp and automatically annotate quality dashboards at that timestamp, so quality dips can be correlated with routing changes without manual archaeology.
4. **Quality floor guardrails**: Define a minimum acceptable quality threshold per task category that the router cannot cross regardless of cost pressure, treating it as a hard constraint rather than a soft consideration.
5. **Automatic rollback triggers**: Configure automatic reversion to the prior routing config if quality metrics for a downgraded category drop below a defined threshold within a monitoring window after the change.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| quality_score_by_routing_tier | Task success/quality metric broken out by which model tier served the request | Alert if any tier's quality drops > 10% after a routing change |
| cost_savings_vs_quality_delta | Paired view of cost reduction and quality change for any routing config change | Alert if quality delta is negative and unreviewed |
| routing_change_to_complaint_lag | Time between a routing config change and the first related quality complaint | Track as a detection-speed metric, alert if consistently > 48h |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Quality floor breached after downgrade | quality_score_by_routing_tier falls below the defined floor for a task category | High | Auto-rollback to prior routing config, notify routing owner |
| Unreviewed downgrade shipped | A routing change reducing model tier for a category ships without a paired quality evaluation | Medium | Block further rollout, require shadow evaluation before proceeding |

## Related Patterns
- [Model Capability Mismatch](./model-capability-mismatch.md) - both involve routing decisions optimized on one axis (cost or capability metadata) while silently ignoring quality/compatibility impact
- [Model Load Balancing Failure](./model-load-balancing-failure.md) - a related failure where routing optimizes for availability instead of cost, with a similar lack of quality feedback in the loop
- [Model Selection Nondeterminism](./model-selection-nondeterminism.md) - unstable or inconsistently-applied routing rules make it harder to attribute quality changes to any single downgrade decision
