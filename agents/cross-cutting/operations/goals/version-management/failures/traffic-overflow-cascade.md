# Traffic Overflow Cascade

## Issue
During a deployment or failover, traffic is shifted away from a set of agent instances — a canary rollback, a bad-version pool being drained, a zone failover — and redirected to the remaining healthy capacity, but the remaining pool wasn't sized to absorb the extra load. The sudden influx pushes the receiving instances past their own capacity limits, causing them to slow down or start failing too, which triggers their health checks to fail, which pulls them from rotation, which shifts their load onto whatever capacity is left — a cascading failure that starts as a routine traffic shift and ends with the entire fleet unhealthy, worse than the original problem the traffic shift was meant to fix.

**Frequency**: Occasional

**Symptoms**
- Latency and error rates spike sharply on the instances that received redirected traffic, shortly after a traffic-shift event
- Health check failures spread progressively across the fleet in a pattern that tracks the order instances were absorbing overflow, not a uniform onset
- Overall fleet capacity drops faster than the triggering event alone would explain, because healthy capacity is actively shrinking as a side effect of the shift
- The incident that triggered the traffic shift (e.g., a bad canary) looks minor in isolation, but the aggregate outage is far larger than the originally affected slice
- Post-incident review shows the receiving pool's capacity headroom was insufficient for the redirected volume, often known in advance but not accounted for at shift time

## Root Cause
Capacity planning for agent-serving fleets is often based on steady-state load with a modest headroom margin (e.g., 20% spare capacity for normal traffic variance), which is sufficient for gradual load growth but not for a step-function traffic shift that moves an entire pool's worth of load onto the rest of the fleet within seconds. Traffic-shifting mechanisms — canary rollback, zone failover, unhealthy-pool drain — are usually designed around correctness (does the shift route to a valid target) rather than capacity-awareness (can the target actually absorb this volume), so nothing in the shift logic checks whether the destination pool has enough spare capacity before redirecting. Because agent workloads often have expensive per-request cost (LLM inference calls, multi-step tool loops) relative to typical stateless services, each additional unit of redirected load consumes proportionally more of the receiving instances' capacity, making them more likely to tip over from a traffic shift that a lighter-weight service might have absorbed without issue.

## Example
```
Three-zone deployment of "PlannerAgent," each zone normally handling
~33% of traffic with roughly 15% spare capacity per zone (sized for
normal daily variance, not a full zone's worth of extra load).

Zone A's instances start failing health checks due to an unrelated
disk-pressure issue. The load balancer, per its configured failover
behavior, redirects Zone A's traffic entirely to Zones B and C,
roughly a 50% traffic increase for each of the remaining zones.

Zone B and C's 15% headroom is immediately exceeded. Request queues
build, p99 latency for LLM inference calls (already the dominant
cost per request) climbs past the health check's timeout threshold.
Within 90 seconds, a third of Zone B's instances start failing their
own health checks due to the overload, and the load balancer starts
redirecting Zone B's traffic to Zone C as well.

Zone C, now absorbing what was meant to be split across three zones,
fails within another 60 seconds. What started as a disk-pressure
issue on one-third of the fleet becomes a full outage across all
three zones within about four minutes, because the failover
mechanism at every stage assumed the receiving zone had spare
capacity without checking.
```

## Statistics
| Finding | Context |
|---------|---------|
| Capacity headroom sized for steady-state variance (commonly 10-20%) is frequently insufficient to absorb a full-pool traffic redirect during failover | Typical mismatch reported across teams reviewing cascading-failure postmortems |
| Cascading overflow failures are commonly reported as taking well under 5 minutes from initial trigger to fleet-wide impact once the first receiving pool tips over | Estimated from incident timelines in teams that experienced this pattern |
| Capacity-aware traffic shifting (checking destination headroom before redirecting, or shedding load instead of unconditionally redirecting) is reported to prevent the large majority of cascade escalations in teams that implemented it | Reported range across teams that added load-aware failover logic |

## Mitigations
1. **Capacity-aware traffic shifting**: Before redirecting a pool's traffic elsewhere, check whether the destination has sufficient headroom for the added volume, and if not, shed load (return a graceful degraded response) rather than unconditionally forwarding it and risking a cascade.
2. **N+2 or greater capacity headroom for critical pools**: Size spare capacity to absorb the loss of at least one full zone/pool, not just normal traffic variance, for any deployment topology relying on failover between a small number of large pools.
3. **Gradual, rate-limited traffic redirection**: When shifting traffic away from an unhealthy pool, ramp the redirect over a short window rather than an instantaneous full cutover, giving the receiving pool's autoscaler time to react before the full load lands.
4. **Load-shedding fallback at the edge**: Implement a fast, cheap degraded-mode response (e.g., a queued/deferred reply, or routing to a smaller model) that the receiving pool can fall back to under sudden overload, rather than letting every request compete for full-capacity processing until the pool tips over.
5. **Cascade circuit breaker across pools**: Detect when a traffic-shift event is triggering a chain of health-check failures across successive pools, and halt further automatic redirection (holding remaining pools stable) rather than letting the failover logic keep reacting mechanically pool by pool.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| receiving_pool_capacity_utilization | Utilization of a pool immediately after absorbing redirected traffic | Alert if > 85% within 60 seconds of a redirect event |
| cascade_propagation_count | Number of distinct pools that transition to unhealthy within a short window following an initial traffic-shift trigger | Alert if > 1 additional pool within 5 minutes |
| fleet_wide_capacity_trend | Aggregate healthy capacity across the fleet during an active traffic-shift event | Alert on any sustained downward trend exceeding the triggering event's expected impact |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Overflow cascade in progress | cascade_propagation_count exceeds 1 within the alert window | High | Halt further automatic traffic redirection, activate load shedding, page on-call for manual capacity intervention |
| Receiving pool overloaded post-redirect | receiving_pool_capacity_utilization exceeds threshold immediately after a shift | High | Throttle or pause the redirect, evaluate emergency capacity scale-out |

## Related Patterns
- [Circuit Breaker False Positive](./circuit-breaker-false-positive.md) - a related instability mechanism where a threshold-based reaction (breaker tripping or health check failing) removes capacity that then compounds load elsewhere
- [Health Check Flapping](./health-check-flapping.md) - overloaded instances failing and recovering under fluctuating load can flap in ways that repeatedly re-trigger overflow redirection
- [Traffic Routing Asymmetry](./traffic-routing-asymmetry.md) - both concern traffic distribution going wrong during a shift, one via uneven capacity absorption and one via inconsistent rule application
