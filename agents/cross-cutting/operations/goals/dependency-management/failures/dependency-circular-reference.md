# Dependency Circular Reference

## Issue
Two or more services, modules, or agents depend on each other, directly or through an intermediate chain, in a cycle: Service A calls Service B during initialization or request handling, and Service B (directly, or via Service C) calls back into Service A before A has finished. Under normal, low-latency conditions the cycle can complete without anyone noticing, but under load, during startup ordering, or when one leg of the cycle is slow, the mutual wait never resolves and the system deadlocks or spins in an infinite resolution loop.

**Frequency**: Occasional

**Symptoms**
- Services hang indefinitely during startup with no error, only resolving after a manual restart in a specific order
- Requests time out with both sides logging "waiting for" the other, and neither log shows an actual error
- Dependency-resolution or module-loading logic recurses until it hits a stack-depth or recursion-guard limit and crashes
- The system works fine at low request volume but deadlocks appear only under concurrent load, when timing makes the cycle more likely to complete simultaneously in both directions
- Diagramming the actual runtime call graph, as opposed to the intended architecture diagram, reveals a cycle nobody had noticed

## Root Cause
Circular dependencies usually accumulate incrementally rather than being designed in: Service A is built to depend on B, and much later, a new feature in B needs a small piece of data or capability that happens to live in A, so a call back to A is added without anyone tracing the full dependency graph first. Because the cycle only manifests as a hang under specific timing conditions (both sides trying to acquire a lock/resource the other holds, both waiting on the other's response before responding themselves), and because most architecture documentation reflects intended dependencies rather than the actual runtime call graph, a circular dependency can exist for a long time without being triggered, until load, latency, or a startup-order change creates the exact interleaving that produces deadlock.

## Example
```
An order-fulfillment agent (Service A) calls an inventory-check agent
(Service B) synchronously before confirming an order, to verify stock is
available. This dependency (A -> B) is intentional and documented.

Months later, a new "reserve-and-hold" feature is added to Service B: when
inventory runs low, B needs to know whether there are pending high-priority
orders in A's queue before deciding whether to reserve stock preemptively.
An engineer adds a synchronous call from B back into A's
"get-pending-orders" endpoint to fetch that context. This creates an
undocumented cycle: A -> B -> A.

Under normal traffic, A's call to B completes before B's call back to A is
even relevant to a concurrent request, so the cycle never manifests as a
problem. During a flash sale, request volume spikes and both A and B's
thread pools saturate. A holds a connection open waiting on B's response;
B, handling a different but concurrent request, is waiting on a connection
to A that's stuck in A's now-full queue behind the original request. Both
services' thread pools fill with requests waiting on each other, and neither
recovers without manual intervention -- restarting one service to forcibly
break the cycle, dropping in-flight requests.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 60-70% of circular dependency incidents involve a cycle that was not present in the original architecture but introduced later by an incremental, locally reasonable change | Typical range observed in postmortems tracing cycle origin |
| Circular dependency deadlocks disproportionately appear during load spikes rather than steady-state traffic, since low concurrency rarely produces the precise mutual-wait timing | Estimated from incident timing analysis |
| Automated runtime call-graph analysis catches an estimated 70-85% of circular dependencies before they cause a production incident, versus manual architecture review alone | Reported range across teams using call-graph tooling |

## Mitigations
1. **Runtime call-graph auditing**: Periodically generate the actual runtime service call graph (not just the intended architecture diagram) from tracing data, and flag any cycle for explicit review.
2. **Asynchronous decoupling of cyclic calls**: Where a service genuinely needs data that would otherwise create a cycle, replace the synchronous callback with an asynchronous event/message or a periodically refreshed cache, breaking the synchronous mutual-wait condition.
3. **Dependency direction review at design time**: Require any new cross-service call to be reviewed against the existing dependency graph before merge, specifically checking whether it introduces a cycle with an existing call path.
4. **Timeout and circuit-breaker on every synchronous call**: Ensure every synchronous inter-service call has an aggressive timeout and circuit breaker, so a cyclic deadlock degrades into a bounded set of failed requests rather than an indefinite hang.
5. **Deadlock detection and forced-break tooling**: Instrument thread/connection pools to detect mutual-wait patterns (A waiting on B, B waiting on A) and automatically abort one side with a clear error, rather than requiring manual restart to break the cycle.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| cyclic_call_graph_edges | Count of detected cycles in the runtime service call graph | Alert if > 0 for any newly introduced cycle |
| mutual_wait_duration | Duration for which two services are simultaneously waiting on responses from each other | Alert if > configured timeout without resolution |
| thread_pool_saturation_correlated_pair | Correlation of thread/connection pool saturation events occurring simultaneously across two mutually dependent services | Alert on simultaneous saturation |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| New cycle detected in call graph | Automated call-graph analysis finds a new cycle not present in the prior audit | High | Block deploy or require architecture review before the change ships |
| Mutual deadlock in production | Two services show simultaneous mutual-wait beyond timeout threshold | High | Trigger circuit breaker/forced abort, page on-call, restart affected services in safe order |

## Related Patterns
- [Integration Order Dependency](./integration-order-dependency.md) - both concern implicit ordering/dependency assumptions between systems that aren't enforced by the architecture itself
- [Integration Cascading Failure](./integration-cascading-failure.md) - a circular dependency deadlock is one specific mechanism by which failure in one system cascades into another
- [Integration Timeout Mismatch](./integration-timeout-mismatch.md) - inconsistent timeout configuration across the two sides of a cycle affects how quickly (or whether) a deadlock resolves on its own
