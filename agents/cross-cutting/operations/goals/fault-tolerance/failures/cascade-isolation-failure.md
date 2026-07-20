# Cascade Isolation Failure

## Issue
A system has bulkheads in place — separate connection pools, separate thread pools, separate tenant shards, separate rate limits — intended to contain a failure to the subsystem where it originates. During an actual cascade, the isolation boundary turns out to be leaky: a shared resource that was assumed to be partitioned (a shared thread pool, a shared database instance, a shared upstream dependency, a shared control plane) is in fact common to both the failing subsystem and the ones meant to be protected, so the failure crosses the boundary anyway. The bulkhead exists on paper and in the architecture diagram, but not in the actual runtime resource graph.

**Frequency**: Occasional

**Symptoms**
- A failure in subsystem A degrades subsystem B despite B having its own dedicated connection pool, rate limit, or circuit breaker configuration
- Post-incident analysis finds a shared resource (thread pool, DB connection, DNS resolver, control-plane API) that both subsystems depended on, contrary to the isolation design
- Isolation configuration exists and looks correct in code review, but load testing or chaos experiments were never run to verify it actually contains a real failure
- "Noisy neighbor" complaints in a multi-tenant system despite documented per-tenant resource quotas

## Root Cause
Isolation boundaries are usually designed at the logical/architectural level (separate services, separate queues, separate rate-limit buckets) but implemented on top of shared infrastructure (a shared Kubernetes node pool, a shared database cluster, a shared DNS resolver, a shared logging sidecar, a shared connection pool library with a global default size). The isolation design assumes the boundary is enforced at every layer, but it's common for one layer — often the lowest, least-visible one — to be pooled or shared for cost or operational simplicity. Because the bulkhead has never been tested under an actual saturating failure (only reviewed on paper), the gap isn't discovered until a real cascade crosses it.

## Example
```
Architecture: TenantA and TenantB are isolated at the API-gateway layer
(separate rate limits) and at the application layer (separate service
instances). Both, however, connect to the same underlying Postgres
cluster via the same PgBouncer connection pooler, configured with a
single shared pool of 200 connections rather than per-tenant pools.

13:10:00 - TenantA runs a bulk import job that opens a burst of
           long-running queries, consuming 180 of the 200 shared
           PgBouncer connections.

13:10:45 - TenantB's normal traffic, completely unrelated to TenantA's
           import, starts queuing for connections because only 20 remain
           and TenantB's steady-state need is 40.

13:11:30 - TenantB's API latency spikes from 80ms to 4s as requests wait
           for a connection slot. TenantB's on-call is paged, sees no
           anomaly in TenantB's own service metrics or rate-limit
           counters (both look healthy), and initially rules out a
           shared-resource cause because "we're isolated at the gateway
           and app layer."

13:25:00 - A database engineer notices PgBouncer pool saturation and
           traces it to TenantA's import job. The "isolation" that both
           teams believed existed stopped one layer above the actual
           shared bottleneck.
```

## Statistics
| Finding | Context |
|---------|---------|
| A significant share of "isolated" multi-tenant or multi-service architectures share at least one unpartitioned resource at the infrastructure layer | Commonly identified during chaos-engineering and dependency audits |
| Isolation gaps are typically discovered during a live incident rather than in design review or testing | Estimated from postmortem root-cause categorization |
| Systems that run regular fault-injection tests specifically targeting bulkhead boundaries catch a majority of isolation gaps before a real cascade | Reported range across teams with chaos-engineering practices |

## Mitigations
1. **Full-stack resource audit**: Explicitly enumerate every layer a request passes through (gateway, app, connection pool, DB, DNS, logging/telemetry sidecars) and verify partitioning exists at each layer, not just the ones most visible in the architecture diagram.
2. **Fault injection targeting bulkheads specifically**: Run chaos experiments that intentionally saturate one subsystem's resource usage and verify neighboring subsystems remain unaffected, rather than only testing that each subsystem individually degrades gracefully.
3. **Per-tenant/per-subsystem resource quotas at every shared layer**: Where a resource must be shared for cost reasons (e.g. a connection pooler), enforce per-tenant sub-limits within it rather than a single global pool.
4. **Dependency graph verification tooling**: Automatically detect when two supposedly-isolated subsystems both depend on the same infrastructure resource (same DB instance, same pool, same rate-limit bucket) and flag it as an isolation violation.
5. **Isolation boundary documentation with verification status**: Track each claimed bulkhead with an explicit "last verified under load" date, distinguishing tested isolation guarantees from merely designed ones.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| shared_resource_saturation_cross_impact | Correlation between one subsystem's resource saturation and a nominally isolated subsystem's latency/error rate | Alert if correlation exceeds defined threshold during an incident |
| bulkhead_verification_age | Time since a claimed isolation boundary was last verified under a real fault-injection test | Alert if > 90 days |
| noisy_neighbor_incident_count | Incidents where isolated tenants/subsystems report impact from another tenant's/subsystem's load | Track trend; alert on recurrence |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Cross-boundary saturation detected | A shared low-level resource (connection pool, DNS, node pool) crosses a saturation threshold while attributed load comes predominantly from one nominally-isolated subsystem | High | Apply emergency per-tenant throttling at the shared layer, page infra on-call |
| Unverified bulkhead flagged | An isolation boundary's verification age exceeds threshold | Low | Schedule a fault-injection test for that boundary |

## Related Patterns
- [Single Point of Failure](./single-point-of-failure.md) - the shared resource that breaks isolation is frequently an undocumented single point of failure
- [Cascade Branching](./cascade-branching.md) - isolation failure is one of the mechanisms that turns what should be a contained fault into a branching cascade
- [Cascade Resilience Failure](./cascade-resilience-failure.md) - both involve a resilience mechanism (bulkhead vs. retry/breaker) that fails to perform its intended containment function
