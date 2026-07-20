# Latency Cost Tradeoff

## Issue
A team facing a latency SLA responds by throwing more resources at the problem — larger batch sizes tuned down, more replicas kept warm, over-provisioned reserved capacity, or speculative/parallel decoding enabled everywhere — without measuring the cost curve those choices sit on. Latency and cost-per-token trade off against each other in inference serving (bigger batches lower cost but raise latency; more replicas lower latency but raise idle-capacity cost), and optimizing hard for one dimension without a stated budget for the other routinely produces a service that hits its latency target at 3-5x the cost a slightly relaxed target would have required, or conversely a service that's cheap but silently fails its latency SLA under real traffic.

**Frequency**: Common

**Symptoms**
- Cost-per-token rises sharply after a latency-focused optimization pass, with no corresponding increase in request volume to justify it
- p50 latency is well under the SLA target with significant headroom, while cost graphs show the fleet running underutilized to protect that headroom
- Engineering postmortems reference "we added replicas to fix latency" with no accompanying cost-impact analysis in the same decision
- A/B tests or rollout comparisons show a latency improvement of a few hundred milliseconds costing a disproportionate increase in GPU-hours
- No documented latency-cost frontier or target exists; decisions are made reactively per incident rather than against a stated tradeoff curve

## Root Cause
Latency and cost are governed by shared, opposing levers at the serving layer: larger batch sizes improve GPU utilization and lower cost-per-token but increase per-request queueing and completion latency because each request waits for the batch to fill or for other requests in its batch to finish; more replicas reduce queueing latency by adding parallel capacity but increase idle-capacity cost when utilization per replica drops; speculative decoding and parallel sampling reduce latency for the accepted output but consume extra compute for draft/discarded tokens, raising cost per successful token. Teams treat these as independent engineering knobs, tuning whichever one is on fire (usually latency, since it's the customer-visible SLA) without a policy connecting the two — so a latency incident gets resolved by scaling up or shrinking batches, and the cost consequence is discovered separately, later, and disconnected from the decision that caused it. Without an explicit, quantified latency-cost frontier (e.g. "we accept p95 up to 2.5s in exchange for X% lower cost"), every latency fix defaults to the cost-blind direction because latency failures are immediately visible (user complaints, SLA breaches) while cost failures are visible only in a monthly bill review.

## Example
```
A code-review agent has an SLA of p95 latency under 4 seconds. During a
traffic ramp, p95 latency creeps to 5.8 seconds, triggering an SLA
violation. The on-call engineer's fastest lever is reducing max_batch_size
from 24 to 8, which cuts per-request queueing time and brings p95 back to
3.1 seconds within the hour.

The fix works and the incident is closed. Nobody revisits the batch size
once traffic normalizes. Over the following month, the smaller batch size
persists as the new default because "it fixed the SLA violation" and
reverting it feels risky.

A cost review three months later finds:
- Cost-per-1K-tokens rose from $0.041 to $0.079 (93% increase) after the
  batch-size change, because GPU occupancy per batch dropped from ~85%
  to ~35% at the new size.
- p95 latency during the same period averaged 2.4 seconds, nearly 40%
  under the 4-second SLA target — far more headroom than the SLA
  required.

The team was paying for a latency target roughly twice as strict as the
actual requirement, an estimated $31,000/month in avoidable GPU cost,
because the emergency fix was never revisited against the real tradeoff
once the fire was out.
```

## Statistics
| Finding | Context |
|---------|---------|
| Reducing batch size to cut p95 latency by roughly 40-50% commonly increases cost-per-token by 60-100%, depending on how far from optimal occupancy the new batch size lands | Typical range observed across inference serving benchmarks |
| Latency-driven infrastructure changes made during incident response are revisited or cost-reviewed in a minority of cases within 90 days | Estimated range based on typical postmortem/incident-followup practices |
| Services with an explicit stated latency-cost frontier commonly run 20-35% cheaper than equivalent services optimized reactively per-incident | Estimated range from teams that adopted formal SLA/cost budgeting |

## Mitigations
1. **Define and document an explicit latency-cost frontier**: Before tuning any lever, state the actual SLA requirement (not "as fast as possible") and the cost ceiling, and treat every latency or cost change as a move along that documented curve rather than an isolated fix.
2. **Revisit incident-driven infrastructure changes on a schedule**: Any change made during an SLA-violation incident (batch size, replica count, timeout values) gets a mandatory follow-up review within a fixed window (e.g. 2 weeks) to check whether it's still necessary once traffic normalizes.
3. **Model cost impact before applying a latency fix**: Require a quick cost-per-token projection alongside any proposed latency mitigation, so the tradeoff is visible to the decision-maker at the time of the decision, not discovered later.
4. **Prefer targeted over global levers**: Use per-endpoint or per-priority-tier batch/replica tuning instead of fleet-wide changes, so a latency fix for one SLA-critical path doesn't inflate cost for traffic that never needed the tighter target.
5. **Track headroom, not just SLA compliance**: Alert when actual latency is running significantly better than the SLA requires (large positive headroom), since that's a signal of overspend just as much as an SLA breach is a signal of underspend.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| sla_headroom_ratio | (SLA target latency - actual p95 latency) / SLA target latency | Alert if > 0.35 sustained (likely overspend) or < 0.05 (at risk of breach) |
| cost_per_token_vs_baseline | Current cost-per-token relative to a rolling pre-incident baseline | Alert if > 1.5x baseline without a corresponding traffic increase |
| batch_occupancy_ratio | Batch slots used versus allocated, tracked alongside latency | Alert if occupancy drops below 50% following a latency-motivated config change |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Large SLA headroom sustained | sla_headroom_ratio > 0.35 for 7+ days | Medium | Review recent latency-motivated infra changes for possible relaxation and cost recovery |
| Cost spike after latency fix | cost_per_token_vs_baseline exceeds 1.5x within 48 hours of a batch/replica config change | High | Review the change against the documented latency-cost frontier; confirm it's still necessary |

## Related Patterns
- [Batch Cost Inefficiency](./batch-cost-inefficiency.md) - batch size is the primary shared lever in both this pattern's tradeoff and batching's occupancy waste
- [Throughput Per Dollar Optimization Failure](./throughput-per-dollar-optimization-failure.md) - optimizing latency without a cost frontier is a common specific cause of this broader metric failure
- [Resource Reservation Insufficient](./resource-reservation-insufficient.md) - the opposite failure mode, where cost-minimization pressure leaves too little headroom for latency
