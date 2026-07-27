# What Are the Most Common Traffic Routing and Load Balancing Failures in AI Agents?

**Traffic routing and load balancing fail when agents send all traffic to one backend, when load balancers get stuck in unhealthy-host-only mode, when traffic routing decisions are made without health checks, or when circuit breakers don't activate before cascading failures occur.** Traffic routing and load balancing are foundational to reliability in scaled agent systems — yet failures here are often invisible until a cascade occurs. The patterns documented here are still being collected; this goal area awaits additional empirical data from production traffic-routing and load-balancing incidents.

## Key Takeaways

- Traffic routing and load balancing are infrastructure concerns but affect agent reliability directly.
- Patterns in this goal area are under active collection; teams deploying agents at scale should prioritize load balancing testing.
- Common traffic routing failures include sticky sessions that don't adapt to unhealthy hosts, health checks that don't accurately reflect host health, and circuit breakers that don't activate early enough.
- Load balancing strategy depends on traffic pattern: uniform distribution works for steady-state, but bursty traffic requires adaptive algorithms.

## Scope

This goal encompasses traffic distribution across multiple backends, health checking and failover, circuit breaking, and adaptive load balancing.

## When Traffic Routing Matters

- An agent system is deployed across multiple backends or instances, where traffic must be distributed.
- Some backends or instances become unhealthy; traffic must failover to healthy ones.
- Traffic is bursty; some backends get overloaded while others are idle.

## Cross-Pattern Insight

Traffic routing failures result from assuming uniform traffic and healthy backends. Load balancers are configured once during deployment and don't adapt as traffic patterns or backend health changes. The mitigation is continuous health monitoring and adaptive routing: measure backend health (latency, error rate, resource usage), adjust traffic distribution continuously rather than relying on initial configuration, and implement circuit breakers that activate quickly when backends degrade.

## Frequently Asked Questions

### How do you detect when a backend is unhealthy?
Regular health checks (ping, synthetic request) determine if backend is responding. But health checks that only check connectivity don't catch degraded backends. Measure backend latency and error rate; if latency is high or error rate is elevated, consider backend unhealthy even if it responds to pings.

### What should happen if all backends are unhealthy?
Fail fast with clear error messaging. Don't attempt to route to any backend or queue indefinitely. Alert operators immediately so they can fix the issue.

## Patterns

This goal area is currently under active pattern collection. As empirical data from production traffic routing and load balancing failures becomes available, documented patterns will be added here.

## Related Goals

- [Real-Time Performance](../real-time-performance/) — load balancing affects latency distribution
- [Reliability and Resilience](../reliability-and-resilience/) — load balancing is foundational to resilience
- [Observability Monitoring](../observability-monitoring/) — backend health monitoring enables adaptive routing
