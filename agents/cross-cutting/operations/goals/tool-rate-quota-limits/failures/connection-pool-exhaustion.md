# Connection Pool Exhaustion

## Issue
An agent's HTTP client (or the SDK wrapping a tool) maintains a fixed-size connection pool, typically sized for a single-threaded request/response app rather than an agent fanning out dozens of parallel tool calls. When the agent spawns concurrent sub-tasks that all hit the same tool, requests queue up waiting for a free connection from the pool and start timing out or erroring — even though the remote API itself has plenty of headroom and would happily serve the traffic.

**Frequency**: Common

**Symptoms**
- Requests hang or time out under load with no corresponding error or rejection from the remote server
- The remote API's own dashboards show low utilization and no rate-limit rejections at the same time the agent is failing
- Errors mention "connection pool exhausted," "timeout waiting for connection," or similar client-library-specific messages rather than HTTP status codes
- Failures cluster tightly around moments of high sub-agent fan-out (e.g., 20 parallel research tasks launched at once)
- Increasing the remote API's rate limit or quota does nothing to fix the failures

## Root Cause
HTTP client libraries (requests/urllib3, aiohttp, OkHttp, etc.) default to a conservative maximum number of connections per host (often 10-20) to avoid overwhelming servers by default. Agent frameworks that spin up many concurrent tool invocations — especially via parallel sub-agents or async fan-out — routinely exceed this default without anyone having deliberately configured a limit. The pool size was never chosen with the agent's concurrency profile in mind; it's an inherited library default that silently caps the agent's real throughput far below what both the agent's task graph and the remote service could otherwise sustain.

## Example
```
An orchestrator agent decomposes "summarize these 40 support tickets" into 40 parallel calls to the TicketingAPI connector, using an async HTTP client whose connection pool defaults to a max of 10 connections per host.

Calls 1-10 acquire a connection immediately and start executing.
Calls 11-40 block in the client's internal queue waiting for a connection to free up.
The orchestrator has a per-call timeout of 8 seconds (tuned for typical TicketingAPI latency).
Calls 21-40 never even reach the network — they're still waiting in the pool queue when their 8-second timeout fires, so they fail with "connection pool timeout" while TicketingAPI never saw the request at all.
The orchestrator reports 20 of 40 ticket summaries failed, and retries them one-by-one in serial, taking 10x longer than a properly pooled run would have.
```

## Statistics
| Finding | Context |
|---------|---------|
| Default per-host connection pool sizes in common HTTP libraries range from 6 to 20, often an order of magnitude below the concurrency agent fan-out patterns generate | Common default across popular HTTP client libraries |
| Connection-pool-related failures account for an estimated 10-20% of "tool unavailable" errors in agents that use unbounded parallel sub-task fan-out | Observed in production multi-agent orchestration systems |
| Raising pool size to match actual fan-out concurrency typically eliminates 90%+ of these failures with no other code change | Typical outcome of pool-size tuning remediation |

## Mitigations
1. **Size the pool to the fan-out, not the default**: Explicitly configure `max_connections`/`pool_maxsize` (or equivalent) on the HTTP client to match the agent's actual maximum concurrency per tool, not the library default, and document the reasoning next to the config.
2. **Bound fan-out at the orchestrator, not the pool**: Use a semaphore or task-queue with an explicit concurrency cap when launching parallel tool calls, so the agent's own concurrency never exceeds what the pool (and the remote service) can handle — making pool exhaustion structurally impossible rather than tuned around.
3. **Separate pools per tool**: Give each distinct external tool/host its own connection pool rather than sharing one global pool, so a burst against one tool can't starve connections needed for an unrelated tool.
4. **Distinguish pool-wait timeouts from network timeouts in logging**: Configure the client to raise a distinct exception type for "timed out waiting for a pooled connection" vs "timed out waiting for a server response," so on-call can immediately tell whether the fix is client-side config or a real remote issue.
5. **Load-test the fan-out path before production**: Run the agent's actual worst-case parallel fan-out pattern against a staging endpoint during development to surface pool sizing issues before they show up as intermittent production failures.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `http_client.pool_wait_time_ms` | Time a request spends queued waiting for a free pooled connection | Alert if p95 exceeds 500ms |
| `http_client.pool_exhaustion_count` | Count of requests that timed out while waiting for a pool connection (not a network timeout) | Alert if greater than 0 in any 5-minute window during production traffic |
| `tool.fanout_concurrency` | Actual peak concurrent in-flight calls to a given tool | Alert if it exceeds 80% of configured pool size |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Pool exhaustion detected | `pool_exhaustion_count` > 0 while remote API error rate is 0% | Warning | Increase pool size or add orchestrator-level concurrency cap; not a vendor issue |
| Sustained pool saturation | `pool_wait_time_ms` p95 > 1s for 10+ minutes | Critical | Page on-call; likely an unbounded fan-out bug spawning more concurrent calls than intended |

## Related Patterns
- [Per-Tool Concurrent Connections Exceeded](./per-tool-concurrent-connections-exceeded.md) - the remote-side counterpart of this client-side pool limit; both cap effective concurrency below the agent's fan-out
- [Per-Tool Max Parallel Requests](./per-tool-max-parallel-requests.md) - similar concurrency mismatch but enforced by the vendor at the request level instead of the client's connection layer
- [Connection Timeout No Retry](./connection-timeout-no-retry.md) - pool-wait timeouts are often misdiagnosed as this pattern if the agent doesn't distinguish timeout types
