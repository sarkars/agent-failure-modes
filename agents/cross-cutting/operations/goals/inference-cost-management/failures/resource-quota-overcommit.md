# Resource Quota Overcommit

## Issue
A platform team allocates GPU/CPU/memory quotas to multiple inference workloads (teams, models, or environments) that sum to more than the physical capacity actually available, betting on the statistical assumption that not everyone will hit peak demand simultaneously — a standard and often reasonable cloud-capacity technique. When that assumption breaks (correlated demand spikes, a shared upstream event driving traffic to several agents at once, or one workload's usage pattern shifting), multiple workloads contend for the same physical resources at the same time, and instead of one workload being cleanly capacity-constrained, all of them experience degraded throughput and elevated latency simultaneously, which the serving layer often resolves through more replicas or emergency reserved capacity purchased at a premium.

**Frequency**: Occasional

**Symptoms**
- Multiple, ostensibly independent workloads or teams report inference latency degradation at the same time, with no single workload showing an obvious traffic spike large enough to explain it alone
- Cluster-level GPU allocation dashboards show combined requested quota exceeding physical node capacity, a state that looks fine until multiple tenants request near their quota simultaneously
- Noisy-neighbor complaints ("workload A is fine but workload B's latency spikes whenever workload A runs a batch job") recur periodically
- Emergency capacity is provisioned at on-demand/premium pricing during contention events that could have been avoided with better isolation, even though aggregate reserved capacity utilization looks healthy on average
- Post-incident review shows the sum of workloads' allocated quotas was 130-180% of physical cluster capacity, a ratio nobody had explicitly reviewed or approved as a risk tradeoff

## Root Cause
Overcommitting quotas is a deliberate and often correct capacity-efficiency technique — physical resources are expensive, and provisioning every workload's peak demand as dedicated capacity would leave most of the cluster idle most of the time. The technique fails when the overcommit ratio is set without modeling correlation between workloads' demand patterns: if several inference workloads share a triggering event (a marketing campaign that drives traffic to multiple product surfaces at once, a shared upstream dependency's incident causing every downstream agent to retry simultaneously, or simply multiple teams' batch jobs scheduled at the same wall-clock hour because that's when everyone's cron jobs default to), their "independent" peaks become correlated, and the overcommit ratio that was safe under an independence assumption is unsafe under the real correlation structure. Most platforms don't actively measure or monitor cross-workload demand correlation — they set an overcommit ratio once (often copied from a generic cloud-capacity-planning heuristic) and revisit it only after a contention incident, so the risk accumulates silently as more workloads are added to a shared cluster without anyone re-evaluating whether the original independence assumption still holds.

## Example
```
A shared inference cluster serves 6 internal AI agents (customer support,
sales-enablement, internal search, code review, a marketing-content
generator, and a data-analysis assistant) with a combined allocated GPU
quota of 340 GPU-equivalents against 220 physically available GPUs on
the cluster, a 1.55x overcommit ratio set 18 months earlier when the
cluster hosted 3 workloads with genuinely uncorrelated traffic patterns.

A company-wide product launch drives a coordinated spike: the marketing-
content generator runs a large batch job producing launch-day copy, the
sales-enablement agent sees elevated usage from the sales team preparing
launch materials, and customer support sees elevated ticket volume as
the launch reaches customers — three of the six workloads spike within
the same 2-hour window, something the original overcommit ratio never
modeled because it was set when these were independent, low-correlation
workloads with different usage cadences.

Combined demand hits 290 GPU-equivalents against 220 physical GPUs.
The cluster scheduler throttles all three spiking workloads
simultaneously rather than fully serving any of them; each experiences
2-4x normal latency. The on-call team provisions 40 GPUs of on-demand
premium-priced capacity to relieve contention, at roughly 2.8x the cost
of the cluster's reserved-capacity rate, for the 5 hours it takes for
demand to subside naturally. The emergency capacity costs more than the
entire month's reserved-capacity savings the overcommit ratio had been
generating.
```

## Statistics
| Finding | Context |
|---------|---------|
| Shared inference clusters commonly run overcommit ratios of 1.3-1.8x physical capacity based on historical utilization, without explicit correlation modeling between tenant workloads | Typical range observed in multi-tenant GPU cluster configurations |
| Emergency on-demand capacity purchased during a contention event commonly costs 2-4x the equivalent reserved-capacity rate | Typical range for on-demand versus reserved GPU pricing |
| Correlated-demand contention incidents on overcommitted clusters are more likely during shared triggering events (product launches, upstream incidents, scheduled batch windows) than during organic, uncorrelated traffic growth | Typical pattern observed in multi-tenant capacity incident postmortems |

## Mitigations
1. **Model demand correlation explicitly, not just independence by default**: Before setting or increasing an overcommit ratio, review whether workloads share triggering events (marketing calendars, upstream dependencies, common batch-job scheduling windows) that would break the independence assumption the ratio relies on.
2. **Tiered quota guarantees with a hard floor per workload**: Give each workload a guaranteed minimum allocation it can always claim (sized to avoid a full outage) plus access to a shared burst pool, so contention degrades workloads proportionally to their burst usage rather than starving all of them simultaneously.
3. **Stagger predictable correlated-demand events**: Where multiple workloads' batch jobs or peak-usage windows are schedulable (not driven by external user traffic), deliberately stagger them across different times rather than defaulting to the same wall-clock scheduling window.
4. **Pre-negotiated fast-access burst capacity at reserved-adjacent pricing**: Establish a burst-capacity agreement with the infrastructure provider ahead of time, rather than relying on ad hoc on-demand provisioning during a live contention incident, to avoid the premium-pricing penalty of reactive procurement.
5. **Periodically re-review the overcommit ratio as the tenant mix changes**: Treat the overcommit ratio as a living risk parameter that gets re-evaluated whenever a new workload joins the shared cluster or an existing workload's traffic pattern changes materially, not a value set once and left unexamined.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| cluster_overcommit_ratio | Sum of allocated quota across all tenants divided by physical cluster capacity | Alert if exceeds the reviewed/approved ceiling for the current tenant mix |
| concurrent_tenant_peak_count | Number of tenants simultaneously operating above 80% of their individual quota | Alert if 2+ tenants concurrently exceed 80% for 10+ minutes |
| on_demand_capacity_spend_ratio | On-demand/premium capacity spend as a fraction of total infra spend for the period | Alert if > 10% of period spend, indicating reactive rather than planned procurement |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Correlated multi-tenant contention | concurrent_tenant_peak_count reaches 2+ tenants simultaneously above 80% quota usage | High | Page infra on-call, evaluate emergency burst capacity, notify affected workload owners |
| Overcommit ratio exceeds reviewed ceiling | cluster_overcommit_ratio exceeds the last-approved value after a new tenant onboarding | Medium | Trigger a capacity-planning review before the ratio is allowed to persist |

## Related Patterns
- [Resource Reservation Insufficient](./resource-reservation-insufficient.md) - overcommit at the cluster level is one common cause of an individual workload's reservation proving insufficient under real peak load
- [Concurrent Request Resource Explosion](./concurrent-request-resource-explosion.md) - correlated demand spikes across tenants can trigger this pattern's contention dynamics simultaneously across a shared cluster
- [CPU Saturation Cascade](./cpu-saturation-cascade.md) - shares the mechanism of one workload's resource pressure degrading others sharing the same infrastructure
