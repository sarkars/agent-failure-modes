# Model Load Balancing Failure

## Issue
A router distributing calls across multiple model instances or provider endpoints (for throughput or redundancy) continues sending a disproportionate share of traffic to an instance that has become slow, degraded, or partially unhealthy, because the balancer's routing signal (round-robin, static weights, or a stale health check) doesn't reflect the instance's actual current condition. Requests routed to the degraded instance experience elevated latency or error rates while the balancer keeps treating it as a fully healthy peer.

**Frequency**: Occasional

**Symptoms**
- Latency and error rates are elevated for a subset of requests correlated with a specific backend instance or region, while overall traffic distribution stays roughly even across instances
- A provider-side capacity or degradation event affects only one endpoint, but the balancer keeps sending its configured static share of traffic there instead of shifting away
- Health checks pass (the instance responds to a lightweight ping) while real task-completion latency or quality on that instance has degraded, because the health check doesn't measure the same thing as production traffic
- Retried requests that land on a different instance succeed quickly, while requests pinned or hashed to the degraded instance keep failing or timing out
- The imbalance is only discovered through downstream user complaints tied to specific requests, not through the load balancer's own metrics, which show normal-looking aggregate throughput

## Root Cause
Load balancers are usually configured with a routing policy — round-robin, static weighted split, or a simple liveness health check — chosen for simplicity and low overhead, and that policy typically doesn't incorporate real-time, request-representative signals like actual completion latency, error rate, or output quality from the specific instance. A lightweight health check (e.g. a fast ping endpoint) can report an instance as healthy even when it is struggling under load or has degraded output quality, because the check measures reachability, not the quality of service under the deployment's actual traffic pattern. Without a feedback loop connecting per-instance real traffic outcomes back into the routing weights, the balancer has no way to learn that one instance is underperforming and continues sending it a full share of traffic until someone manually intervenes or a static weight is adjusted after the fact.

## Example
```
An agent platform load-balances calls across three regional deployments of
the same model, evenly split 33/33/34% by a static round-robin policy,
with health checks pinging a lightweight `/health` endpoint every 30
seconds.

One regional deployment begins experiencing elevated queueing due to a
capacity issue on the provider side. Its `/health` endpoint still
responds normally (it's a separate, lightweight path), so the balancer
keeps routing a full third of traffic there.

Requests landing on the degraded region see completion latency climb from
a typical 1.2s to 9-14s over a two-hour window. Aggregate platform metrics
barely move, since two-thirds of requests are unaffected, and no alert
fires because the metric being watched (overall p50 latency) is diluted
by the healthy instances. Users hitting the degraded region file latency
complaints before the platform team notices the regional imbalance.
```

## Statistics
| Finding | Context |
|---------|---------|
| Lightweight liveness health checks catch a minority of real-world degradation events (partial capacity issues, elevated queueing) compared to checks incorporating actual task latency/error signals | Typical range observed comparing liveness-only vs. traffic-aware health checking |
| Per-instance latency/error metrics are diluted below alerting thresholds in aggregate views when only a fraction of instances are degraded, in the substantial majority of partial-outage incidents | Estimated from postmortems of regional/instance-level degradation events |
| Dynamic, outcome-weighted routing (shifting traffic share based on real-time success/latency) typically reduces user-facing impact duration of instance-level degradation by a majority relative to static-weight routing | Typical range reported by teams that added outcome-weighted balancing |

## Mitigations
1. **Outcome-weighted dynamic routing**: Route traffic share based on real-time per-instance success rate and completion latency rather than a static split, automatically shifting load away from degrading instances.
2. **Task-representative health checks**: Replace or supplement lightweight liveness pings with periodic synthetic requests that mirror real production task shape, so health checks measure what users actually experience.
3. **Per-instance metric breakdown in monitoring**: Track and alert on latency/error rate per backend instance, not only in aggregate, so a partial degradation isn't diluted below detection thresholds.
4. **Automatic circuit breaking**: Temporarily remove an instance from the routing pool once its per-instance error/latency metrics cross a threshold, restoring it only after it demonstrates recovery through the same task-representative checks.
5. **Fast failover with request-level retry**: When a request to one instance times out or errors, retry immediately against a different instance rather than surfacing the failure, bounding user-facing impact while the balancer's weights catch up.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| per_instance_latency_p95 | 95th-percentile completion latency broken out by backend instance | Alert if any instance exceeds 2x the fleet median |
| per_instance_error_rate | Error/timeout rate broken out by backend instance | Alert if any instance exceeds 3x the fleet median |
| health_check_vs_task_outcome_divergence | Gap between health-check-reported status and actual task success/latency for the same instance | Alert if divergence detected for > 5 minutes |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Instance-level degradation detected | per_instance_latency_p95 or per_instance_error_rate breaches threshold for a specific instance | High | Circuit-break the instance out of rotation, shift traffic to healthy peers |
| Health check divergence from real traffic | Health check reports healthy while task-outcome metrics show degradation on the same instance | Medium | Investigate health check adequacy, add task-representative synthetic probes |

## Related Patterns
- [Model Downgrade Silent Failure](./model-downgrade-silent-failure.md) - both involve routing decisions that silently degrade user experience because the routing signal doesn't reflect real quality/performance impact
- [Model Selection Nondeterminism](./model-selection-nondeterminism.md) - inconsistent instance selection compounds the difficulty of isolating and diagnosing a specific degraded instance
- [Model Version Incompatibility](./model-version-incompatibility.md) - regional/instance deployments can silently diverge in version, turning a load-balancing issue into a compatibility issue as well
