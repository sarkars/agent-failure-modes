# Execution Time Quota

## Issue
A tool enforces a hard maximum execution time per call (a Lambda-style 15-minute cap, a synchronous API's 30-second gateway timeout, a query engine's statement timeout). When the agent issues a request whose natural completion time exceeds that ceiling — a large data export, a bulk transform, a long-running search — the call is killed at the boundary with no partial results returned and often no clear indication that a timeout, rather than a crash, was the cause.

**Frequency**: Very Common

**Symptoms**
- Requests that succeed on small datasets fail consistently once input size crosses a threshold, and the failure time is suspiciously round (e.g., always ~30s, always ~900s)
- API returns a generic gateway timeout (504) or connection-reset error rather than a tool-specific "exceeded max execution time" message
- No partial output is returned even though the operation was clearly making progress when killed
- Agent's retry of the identical request fails at the same elapsed time every time
- Task appears to "hang" from the agent's perspective rather than fail fast

## Root Cause
Execution-time quotas exist to bound resource consumption and preserve responsiveness for other tenants sharing the same infrastructure, so tool providers set a ceiling independent of any particular request's actual complexity. The agent typically has no way to know, ahead of time, whether a given request's data volume or algorithmic complexity will push it past that ceiling, because the tool doesn't expose an estimated-duration or cost-preview API. Compounding this, many execution environments do not checkpoint or stream partial results, so hitting the wall produces a total loss of work rather than a truncated-but-usable output.

## Example
```
1. Agent calls a reporting tool's "generate-full-export" endpoint for a customer with
   2 million transaction records. The tool enforces a 60-second synchronous request timeout.
2. For customers with under 50,000 records, the export reliably completes in 8-15 seconds.
3. This customer's export requires joining across 4 tables and takes an estimated 95 seconds
   to fully materialize.
4. At the 60-second mark, the API gateway returns HTTP 504 Gateway Timeout. The export job
   itself keeps running server-side but its result is discarded since the client connection
   is gone.
5. The agent's retry logic retries the same synchronous call three times, each timing out
   identically at 60 seconds, burning nearly 3 minutes of wall-clock time for zero result.
6. No error in the agent's logs mentions record count or duration; it just sees three
   consecutive 504s and surfaces "export failed" to the end user.
```

## Statistics
| Finding | Context |
|---------|---------|
| Execution-time-quota failures are among the most common causes of "silent hang then fail" behavior reported in agent tool-call telemetry, often 20-40% of long-task failures | Consistent with synchronous API timeout ceilings being common across REST tooling |
| Switching from synchronous to async/polling job patterns has been observed to reduce timeout-related failures by 70-90% for tasks with variable-length inputs | Because the client-side connection timeout no longer bounds the actual work duration |
| Median "wasted" time from blind retries against a hard timeout is 2-4x the timeout duration itself before an agent gives up or escalates | From repeated identical-duration failures before backoff kicks in |

## Mitigations
1. **Prefer async job patterns**: Where the tool offers an async/polling or webhook-based variant of a long-running operation, use it instead of the synchronous endpoint so execution time isn't bounded by a request-response timeout.
2. **Pre-flight duration estimation**: Query record counts, file sizes, or other complexity proxies before issuing the call, and route requests likely to exceed the quota toward chunked or async paths rather than attempting the synchronous call at all.
3. **Chunk large operations**: Break an oversized request into multiple smaller calls (e.g., paginated exports, date-range-bounded queries) each comfortably within the time quota, and reassemble results client-side.
4. **Detect timeout-shaped failures explicitly**: Treat failures whose elapsed time equals the known quota ceiling as a distinct error class from generic failures, and skip blind retries in favor of switching strategy (chunking, async) immediately.
5. **Checkpointing where supported**: For tools that support resumable operations (cursor-based pagination, resumable uploads), persist progress markers so a timeout doesn't discard already-completed work.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `tool_call.duration_at_timeout_ratio` | Ratio of calls whose failure occurs within 2% of the known timeout ceiling | Alert above 15% of failed calls |
| `tool_call.blind_retry_after_timeout_count` | Count of retries issued against an identical request after a timeout-shaped failure | Alert above 3 per request chain |
| `tool_call.sync_call_p95_duration_s` | P95 duration of synchronous calls to timeout-prone endpoints | Alert when p95 exceeds 80% of the known quota |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Repeated timeout-boundary failures | 3+ consecutive failures at duration within 2% of quota ceiling for the same logical request | High | Halt blind retries, switch to async/chunked strategy |
| Rising p95 approaching timeout ceiling | `sync_call_p95_duration_s` trending toward 80%+ of quota over 7 days | Medium | Proactively migrate endpoint usage to async pattern before failures spike |

## Related Patterns
- [Cpu Quota Per Job](./cpu-quota-per-job.md) - CPU throttling is a frequent underlying cause of hitting the execution-time wall
- [Memory Quota Per Operation](./memory-quota-per-operation.md) - another fixed per-call resource ceiling that fails without partial results
- [Latency Sla Violation](../../tool-sla-quality-limits/failures/latency-sla-violation.md) - related but distinct: SLA latency overruns versus a hard-enforced execution cutoff
