# Agent Priority Inversion

## Issue
A low-priority agent acquires a shared resource (a database lock, a rate-limited API slot, a write lease on a document) and then stalls or runs slowly, while a high-priority agent that needs the same resource is forced to wait behind it. The high-priority agent's own urgency provides no mechanism to preempt the lower-priority holder, so the system's effective priority order is inverted: the task that matters least is dictating the pace of the task that matters most.

**Frequency**: Occasional

**Symptoms**
- A high-priority agent (e.g. handling a P1 incident) blocked waiting on a lock held by a background/batch agent
- Wait times for high-priority tasks that don't correlate with their declared priority
- Low-priority agents observed holding shared resources far longer than their task should require
- No priority information visible to the resource/lock manager itself
- Escalations resolved simply by killing the low-priority agent's process, restoring throughput immediately

## Root Cause
Most shared-resource managers (locks, semaphores, connection pools, rate limiters) are priority-blind: they grant access on a first-come-first-served or round-robin basis and have no concept of the requesting agent's task priority. When a low-priority agent acquires the resource first, there is no mechanism for a subsequently-arriving high-priority agent to preempt it, boost its priority, or jump the queue. The inversion is worsened when the low-priority agent's hold time is unpredictable — e.g. it's waiting on a slow downstream call itself — because the high-priority agent's wait time then becomes a function of an unrelated agent's tail latency rather than of the resource's actual availability.

## Example
```
An order-processing platform runs two agent classes against the same
inventory-database row lock:

- Nightly Reconciliation Agent (priority: low) locks SKU #88214 to
  recompute stock levels across warehouses, a task that normally takes
  200ms but is currently stalled because a downstream warehouse API is
  degraded, so the lock is held for 40+ seconds.
- Fraud-Hold Release Agent (priority: high) needs the same row lock to
  release a fraud hold on a $4,200 order before a 60-second SLA expires,
  so the order isn't auto-cancelled.

The lock manager has no priority field -- it queues requests in arrival
order. The Fraud-Hold Release Agent waits behind the Reconciliation
Agent's stalled lock for the full 40 seconds, missing 40 of its 60-second
SLA window before the lock frees and the release finally completes,
triggering an SLA-breach alert and a customer complaint.
```

## Statistics
| Finding | Context |
|---------|---------|
| Priority-blind shared resources are involved in an estimated 15-25% of SLA breaches in mixed-priority multi-agent systems | Typical range observed in production incident reviews |
| Median wait-time inflation for high-priority agents blocked by low-priority lock holders is reported in the 5-15x range versus uncontended access | Estimated from instrumented lock-wait telemetry |
| Adding priority inheritance or preemption to shared locks reduces high-priority wait-time outliers by roughly 70-80% in reported deployments | Reported range across teams that implemented priority-aware resource managers |

## Mitigations
1. **Priority inheritance**: When a high-priority agent blocks on a resource held by a low-priority agent, temporarily boost the holder's effective priority (and its resource allocation, e.g. CPU/API quota) so it finishes and releases faster, a well-established technique from real-time operating systems.
2. **Preemptible resource leases**: Design shared resources with short, renewable leases rather than indefinite locks, so a high-priority request can force a lease expiry and reclaim the resource within a bounded time.
3. **Priority-aware queueing at the resource manager**: Make the lock/semaphore/pool manager priority-conscious, granting access to the highest-priority waiter rather than strictly FIFO order.
4. **Separate resource pools by priority tier**: Where feasible, give high-priority agents a dedicated pool of connections/locks/rate-limit budget that low-priority agents cannot touch, eliminating contention entirely rather than managing it.
5. **Bounded hold-time enforcement**: Cap how long any agent, regardless of priority, may hold a shared resource, with automatic release and requeue on timeout, so a stalled low-priority holder cannot indefinitely block others.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| high_priority_wait_time_p95 | 95th percentile wait time for high-priority agents to acquire a contended resource | Alert if > 2x expected task duration |
| priority_inversion_events | Count of detected cases where a lower-priority holder blocked a higher-priority waiter beyond a threshold | Alert if > 0 for P1-tagged agents |
| resource_hold_time_by_priority | Distribution of hold times segmented by holder's declared priority | Alert if low-priority hold times exceed 10x median |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| High-priority agent blocked past SLA | A priority="high" agent's wait on a shared resource exceeds its task SLA fraction | High | Page on-call, force-release or preempt the blocking lock, investigate holder |
| Sustained low-priority lock hold | A low-priority agent holds a shared resource longer than its expected task duration | Medium | Investigate holder for stalls, consider auto-timeout policy |

## Related Patterns
- [Agent Resource Contention](./agent-resource-contention.md) - priority inversion is a specific failure mode within the broader class of resource contention
- [Deadlock in Multi-Agent](./deadlock-in-multi-agent.md) - both involve resource holds blocking other agents, though deadlock is circular and inversion is priority-order-only
- [Agent Timeout Cascade](./agent-timeout-cascade.md) - a stalled low-priority holder's unbounded hold time is often the root trigger for cascading timeouts elsewhere
