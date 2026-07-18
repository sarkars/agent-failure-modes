# Per-Tool Concurrent Connections Exceeded

## Issue
A tool's backend enforces a hard cap on the number of simultaneous open connections per account or API key (common with database connectors, legacy SOAP/XML-RPC services, and some SaaS APIs built on connection-oriented protocols). When an agent's orchestrator executes multiple sub-tasks in parallel, each holding open its own connection to the same tool for the duration of a long-running call, the agent can open more concurrent connections than the vendor allows — and unlike a request-rate limit, this failure mode has nothing to do with how many requests per second are being sent, only how many are open at once.

**Frequency**: Common

**Symptoms**
- New tool calls fail immediately with "too many connections" or "connection limit exceeded" errors while a handful of earlier calls are still in-flight
- The failure rate correlates with call *duration* and *concurrency*, not call *volume* — a few slow parallel calls trigger it faster than many quick sequential ones
- Long-running calls (e.g., a report generation or large data export) are disproportionately likely to be the ones still holding a connection when a new call is rejected
- The same parallel workload succeeds when run with fewer concurrent branches, even though total request count is identical
- Vendor support explains the limit as "N concurrent connections per API key," a number often much lower than the request-rate limit would suggest is safe

## Root Cause
Connection-oriented protocols and stateful backends (database connections, persistent sessions, some enterprise APIs) charge server-side resources per open connection rather than per request, so vendors cap concurrent connections independently of — and often much more strictly than — request throughput. Agent orchestrators built around request-rate thinking ("I'm under my requests/minute budget, I'm fine") have no equivalent concept of tracking *how many connections are simultaneously open*, especially when sub-agents run independently and don't share visibility into each other's in-flight connections.

## Example
```
A data-analysis agent uses the "WarehouseDB" connector, which enforces a hard limit of 8 concurrent connections per credential — a limit that has nothing to do with queries-per-second.

The orchestrator spawns 15 parallel sub-agents, each running its own long analytical query (each query takes 20-90 seconds and holds one connection open the whole time).
Connections 1-8 open successfully and start executing their queries.
Connections 9-15 are rejected outright with "connection limit exceeded (8/8 in use)" — not queued, just refused.
The orchestrator's error handling treats this as a query failure and marks those 7 sub-agents' tasks as failed, rather than recognizing it as "wait for a connection to free up and retry."
Total requests sent (15) was nowhere near any documented rate limit, but the concurrency ceiling was breached almost immediately.
```

## Statistics
| Finding | Context |
|---------|---------|
| Concurrent-connection limits for connection-oriented backends (databases, legacy enterprise APIs) commonly range from 5 to 20 per credential, far below typical agent fan-out concurrency | Common across database and enterprise-system connectors |
| Agents that don't distinguish "connection rejected" from "request failed" retry inefficiently, often retrying via a fresh connection attempt that also gets rejected rather than queuing for a slot | Observed pattern in orchestration systems lacking connection-aware retry logic |
| Adding a client-side concurrency semaphore matched to the vendor's documented connection limit eliminates the large majority of these rejections | Typical outcome of concurrency-capping remediation |

## Mitigations
1. **Cap orchestrator concurrency to the connection limit**: Use a semaphore or worker pool sized to the tool's documented max concurrent connections (not the rate limit) when dispatching parallel sub-tasks that hold connections open for the tool's duration.
2. **Queue, don't reject, at the orchestrator boundary**: When the concurrency cap is reached, queue additional sub-tasks to wait for a slot to free rather than dispatching them and letting the vendor reject them — this converts a hard failure into a scheduling delay.
3. **Shorten connection hold time where possible**: For tools that support it, use statement-level or short-lived connections (open, execute, close) instead of holding one connection open for an entire multi-step sub-task, reducing the window during which a connection counts against the limit.
4. **Distinguish connection-limit errors from generic failures in retry logic**: Detect the specific "too many connections" error signature and retry with backoff plus a wait-for-slot strategy, rather than treating it identically to an unrelated tool error.
5. **Monitor concurrent-connection headroom, not just request rate**: Track in-flight connection count per tool as a first-class metric alongside request-rate metrics, since the two failure modes are independent and one being healthy says nothing about the other.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `tool.concurrent_connections_open` | Current number of simultaneously open connections to the tool | Alert if it reaches 90% of the documented limit |
| `tool.connection_rejected_count` | Count of calls rejected specifically due to concurrency limit (not rate limit) | Alert if greater than 0 in any 5-minute window |
| `tool.avg_connection_hold_time_s` | Average duration a connection stays open per sub-task | Rising trend alongside rejection count indicates long-held connections are the driver |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Concurrency ceiling hit | `concurrent_connections_open` reaches the documented max and new calls are rejected | Warning | Confirm orchestrator concurrency semaphore is configured; add queuing if missing |
| Sustained concurrency starvation | Rejection rate stays above 0 for 10+ minutes despite queuing | Critical | Reduce sub-task concurrency or request a higher connection limit from the vendor |

## Related Patterns
- [Connection Pool Exhaustion](./connection-pool-exhaustion.md) - a client-side version of the same concurrency-vs-capacity mismatch, caused by the agent's own HTTP client rather than a vendor-enforced cap
- [Per-Tool Max Parallel Requests](./per-tool-max-parallel-requests.md) - the request-level analog of this connection-level limit; both require an orchestrator-side concurrency cap
- [Per-Tool Burst Rate Exceeded](./per-tool-burst-rate-exceeded.md) - parallel fan-out often trips both a burst-rate limit and a concurrent-connection limit simultaneously
