# Agent Resource Contention

## Issue
Multiple agents operating concurrently compete for the same limited resource — a shared LLM inference quota, a database connection pool, a third-party API's rate limit, or a GPU worker pool — and none of them individually has enough context to know how much of the resource other agents are currently consuming. As contention rises, every agent's individual performance degrades (higher latency, more throttling, more retries), and the degradation compounds because retries themselves consume more of the scarce resource, pushing the system further from recovery.

**Frequency**: Very Common

**Symptoms**
- Latency and error rates that scale non-linearly with the number of concurrently active agents
- Agents independently retrying against a resource that is already saturated, worsening the saturation
- Resource utilization dashboards showing sustained near-100% usage with a long queue of waiting requests
- No single agent's logs show an obvious root cause because each agent only sees its own slice of degraded performance
- Performance restored simply by reducing the number of concurrently running agents, without any code change

## Root Cause
Individual agents are typically designed and tested in isolation, each assuming it has exclusive or near-exclusive access to shared infrastructure. When deployed at scale, N agents contend for a resource sized for far fewer concurrent consumers, and no component in the system has global visibility into aggregate demand versus supply. Each agent's local retry and backoff logic is tuned to its own perceived failures, not to the shared resource's actual saturation level, so agents behave as independent, uncoordinated consumers of a commons — the classic tragedy-of-the-commons dynamic applied to compute and API resources.

## Example
```
A customer-support platform runs up to 200 concurrent conversation agents,
all calling the same underlying LLM provider through a shared API key
with a 500 requests/minute limit.

09:14 - Normal load: 60 concurrent agents, ~180 req/min, p50 latency 400ms.
09:22 - A marketing campaign drives a traffic spike; 200 agents now active,
        combined demand hits ~640 req/min against the 500 req/min cap.
09:23 - The provider begins returning 429 (rate limited) responses. Each
        agent's retry logic independently backs off 2s and retries.
09:24 - The retry storm adds ~150 req/min of retry traffic on top of the
        original demand, pushing effective demand to ~790 req/min.
09:26 - p50 latency climbs to 6.2s, p99 exceeds 30s; several agents hit
        their own internal timeout and abandon the conversation entirely,
        surfacing an error to the customer.
09:31 - An on-call engineer manually caps concurrent agents at 80; demand
        drops under the rate limit and latency recovers within 90 seconds.
```

## Statistics
| Finding | Context |
|---------|---------|
| Shared-resource contention is cited as a factor in an estimated 30-40% of multi-agent latency incidents | Typical range observed in production postmortems |
| Uncoordinated retry storms are estimated to add 20-50% extra load on top of original demand during a contention event | Estimated from instrumented rate-limit incident logs |
| Adding centralized admission control or a token-bucket gate typically reduces contention-driven error spikes by 60-80% | Reported range across teams that added shared-resource gating |

## Mitigations
1. **Centralized admission control**: Route all agents' resource requests through a shared gate (token bucket, semaphore, or queue) that enforces the true capacity limit, rather than letting each agent independently discover the limit via failures.
2. **Coordinated backoff with jitter**: Replace independent per-agent retry logic with a shared or synchronized backoff strategy that accounts for aggregate demand, using randomized jitter to avoid retry storms re-synchronizing.
3. **Fair-share or weighted allocation**: Give each agent (or agent class) an explicit share of the shared resource, so no single burst of agents can starve the rest.
4. **Autoscaling tied to resource headroom, not just queue depth**: Scale the number of concurrently active agents based on observed headroom in the shared resource, not solely on incoming task volume, to prevent oversubscription.
5. **Circuit breaking with graceful degradation**: When aggregate demand approaches the resource limit, have agents shed non-critical work or switch to a cheaper fallback path rather than all continuing to compete at full intensity.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| shared_resource_utilization | Aggregate utilization of the contended resource across all agents | Alert if > 85% sustained for 5 min |
| retry_storm_ratio | Ratio of retry traffic to original request traffic on the shared resource | Alert if > 0.3 |
| concurrent_agent_count_vs_capacity | Number of concurrently active agents relative to resource-sized capacity | Alert if demand exceeds capacity for > 2 min |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Shared resource saturation | shared_resource_utilization exceeds 90% with growing queue depth | High | Page on-call, engage admission control / concurrency cap |
| Retry storm detected | retry_storm_ratio exceeds threshold for 3 consecutive minutes | High | Enable coordinated backoff, throttle new agent spawns |

## Related Patterns
- [Agent Priority Inversion](./agent-priority-inversion.md) - a specific case of contention where priority ordering, not just volume, causes the degradation
- [Agent Timeout Cascade](./agent-timeout-cascade.md) - contention-driven latency is a common trigger for downstream timeout cascades
- [Inter-Agent Latency Imbalance](./inter-agent-latency-imbalance.md) - contention can produce or worsen the latency imbalance between agents sharing the same resource
