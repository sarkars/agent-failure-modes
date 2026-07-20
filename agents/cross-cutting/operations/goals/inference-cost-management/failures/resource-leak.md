# Resource Leak

## Issue
A gradual, unbounded leak of memory, GPU memory, file handles, or connection-pool slots in the inference-serving process accumulates over the service's uptime until it degrades throughput or crashes the process, requiring a restart to fully recover. Because the leak is slow, it doesn't trip acute alerting thresholds early — instead it manifests as a steady decline in requests served per GPU-hour as the process approaches its limit, silently raising cost-per-token for hours or days before anyone notices, and then as a hard outage when the leak finally exhausts the resource.

**Frequency**: Occasional

**Symptoms**
- Memory or GPU-memory usage on inference processes climbs steadily and monotonically over days between restarts, with no corresponding traffic growth to explain it
- Throughput per GPU-hour (requests served or tokens generated per hour) declines gradually over a process's uptime, correlated with time-since-restart rather than traffic volume
- Process crashes or requires manual restart at a fairly predictable uptime interval, and each restart brings an immediate, temporary recovery in throughput and latency
- Connection pool exhaustion errors or file-descriptor limit errors appear intermittently, more frequently as uptime increases
- Cost-per-token trends upward over the days following a deployment and resets after each restart, producing a recognizable sawtooth pattern in cost dashboards

## Root Cause
Leaks in inference-serving processes commonly originate in code paths that are exercised on every request but only rarely audited for cleanup correctness — request-scoped tensors or CUDA memory allocations that aren't properly freed on certain error paths, connection or session objects held by retry/streaming logic that don't get released if a client disconnects mid-stream, or Python-level object references (common in ML serving stacks) kept alive by a cache, callback, or logging handler that wasn't scoped to expire. Because each individual leaked allocation is small relative to total capacity, the effect is invisible on a per-request basis and only becomes measurable as an aggregate trend over many thousands of requests and significant uptime — this is exactly the kind of signal that request-level testing and short-duration load tests don't surface, since they don't run long enough to accumulate a visible leak. Error and edge-case paths (client disconnects, request timeouts, malformed inputs that trigger an exception before cleanup code runs) are disproportionately likely sources because they're less thoroughly tested than the happy path, and a serving process handling meaningful production traffic will hit those edge cases often enough for the leak to compound steadily.

## Example
```
A conversational agent's inference server uses a custom streaming
response handler that opens a CUDA memory buffer per request to
accumulate generated tokens before flushing them to the client
connection. On the happy path, the buffer is explicitly freed after the
final token is streamed. On the path where a client disconnects
mid-stream (common for a chat UI where users navigate away before a
response finishes), an exception is raised, but the buffer-free call
sits after the exception-triggering code and never executes.

Client mid-stream disconnects happen on roughly 3% of requests in normal
usage. At the service's volume of ~50,000 requests/hour, this leaks
roughly 1,500 unfreed buffers per hour, each holding on average 40MB of
GPU memory reserved for the (now-abandoned) response.

Over a 30-hour period between scheduled restarts, cumulative leaked GPU
memory grows to consume roughly 18% of the node's total GPU memory,
reducing the KV-cache capacity available for legitimate concurrent
requests. Effective batch size the node can sustain drops accordingly,
and throughput per GPU-hour declines by an estimated 22% by hour 28
compared to hour 2 post-restart, even though request volume and mix are
unchanged. The team's existing 48-hour scheduled restart cadence was
long enough for the leak to meaningfully erode throughput before each
reset, adding an estimated 12-15% avoidable cost across the fleet before
the leak was found and fixed.
```

## Statistics
| Finding | Context |
|---------|---------|
| Resource leaks in long-running inference processes commonly cause a 10-25% throughput decline over multi-day uptime windows before restart | Typical range observed in production leak postmortems |
| Client-disconnect and error/exception code paths account for a disproportionate share of identified serving-process leaks relative to their share of total request volume | Typical pattern observed across serving-stack leak investigations |
| Scheduled restarts as a workaround (rather than fixing the leak) commonly still leave 5-15% avoidable cost on the table from throughput decline accumulated before each restart | Estimated range depending on restart cadence relative to leak rate |

## Mitigations
1. **Audit and test cleanup on error and disconnect paths specifically**: Prioritize testing resource cleanup (buffer frees, connection releases, session teardown) on exception and client-disconnect paths, not just the happy path, since these are the most common leak sources and the least tested by default.
2. **Use resource-scoped context managers/RAII patterns**: Structure request-handling code so resource allocation and cleanup are tied to a scope that's guaranteed to execute on exit (context managers, try/finally, RAII-style wrappers) rather than relying on cleanup code placed after logic that might raise before reaching it.
3. **Track throughput-per-GPU-hour against uptime, not just absolute values**: Add a metric and dashboard specifically correlating throughput or resource usage against time-since-last-restart, so a leak's gradual signature is visible as a trend rather than hidden inside noisy absolute numbers.
4. **Automated leak detection via memory-growth-rate alerting**: Alert on sustained, monotonic memory or GPU-memory growth that doesn't correlate with traffic growth, rather than only alerting once the resource is nearly exhausted.
5. **Treat scheduled restarts as a stopgap, not a fix**: If a restart cadence is in place to manage a known leak, track and report the cost of throughput decline accumulated before each restart, so there's a visible incentive to root-cause and fix the leak rather than let the workaround become permanent.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| memory_growth_rate_uncorrelated_with_traffic | Rate of memory/GPU-memory growth normalized against traffic volume | Alert if positive and sustained for 6+ hours without traffic growth |
| throughput_per_gpu_hour_vs_uptime | Throughput per GPU-hour tracked as a function of time since last process restart | Alert if declining trend exceeds 10% over a rolling 24-hour uptime window |
| unclean_disconnect_resource_delta | Resource usage delta attributable to requests that ended via error/disconnect versus normal completion | Alert if per-disconnect resource delta is nonzero/positive |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Sustained memory growth without traffic correlation | memory_growth_rate_uncorrelated_with_traffic positive for 6+ hours | Medium | Investigate recent code changes to request-handling and error paths; check disconnect-path cleanup |
| Throughput decline correlated with uptime | throughput_per_gpu_hour_vs_uptime declines > 10% within 24 hours of restart | Medium | Schedule investigation into leak source; consider temporary restart cadence adjustment |

## Related Patterns
- [Memory Fragmentation Allocation Failure](./memory-fragmentation-allocation-failure.md) - both degrade effective node capacity over uptime and resolve with a restart, though fragmentation and leaks are distinct mechanisms
- [Disk Space Exhaustion](./disk-space-exhaustion.md) - the same slow-accumulation-to-crisis pattern applied to disk rather than memory/connections
- [Resource Quota Overcommit](./resource-quota-overcommit.md) - a leak can push a node toward the kind of contention that overcommitted quotas are designed (and fail) to absorb
