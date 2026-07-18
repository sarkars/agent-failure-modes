# Memory Quota Per Operation

## Issue
A tool caps the memory available to a single operation (a container memory limit, a serverless function's configured RAM, an in-process buffer ceiling). When the agent sends a request whose payload or intermediate working set exceeds that ceiling — a large file upload, a wide JSON response being deserialized in full, a big in-memory join — the operation is killed by an out-of-memory (OOM) reaper and the failure surfaces to the agent as an opaque, non-specific error rather than a clear "payload too large for allocated memory" message.

**Frequency**: Common

**Symptoms**
- Operations fail only on larger inputs, with no memory-specific error text — just a dropped connection, HTTP 500, or exit code 137
- Failures happen abruptly partway through processing rather than being rejected up front by request validation
- The same request succeeds when split into smaller pieces, implicating memory rather than a logical bug
- Server-side logs (if accessible) show OOM-killer or container-memory-limit-exceeded events correlated with the failure timestamp
- Retrying an oversized request produces the identical failure every time, unlike transient network errors

## Root Cause
Memory quotas are enforced at the infrastructure layer (container cgroup memory limits, serverless runtime RAM allocation, or an in-process buffer cap) independent of the tool's application-level request validation. Most tools validate structural correctness of a request (schema, required fields) but not the memory footprint the request will produce once processed — because that footprint depends on how the tool internally materializes the data (e.g., loading a whole file into memory rather than streaming it). The OOM kill happens below the application layer, so the tool's own error-handling code often never gets a chance to run, and the client just sees a connection drop or generic 5xx.

## Example
```
1. Agent uploads a CSV file to a data-import tool's "/import" endpoint for bulk processing.
   The import worker runs in a container with a 512 MB memory limit and loads the entire
   CSV into an in-memory DataFrame before validating it.
2. CSVs under 50 MB (roughly 200K rows) process reliably, peaking around 300 MB resident memory.
3. Agent submits a 180 MB CSV (batch export from another system, ~900K rows) as part of an
   automated nightly sync.
4. Memory usage climbs past 512 MB while parsing; the container's OOM killer sends SIGKILL
   to the worker process at the 640 MB mark.
5. The client-side HTTP call sees the connection reset with no response body — no status
   code, no error message referencing memory.
6. The agent's error handler logs "unknown connection error" and retries the exact same
   180 MB upload three more times, each failing identically, before giving up and paging
   on-call.
```

## Statistics
| Finding | Context |
|---------|---------|
| OOM-kill failures on file-processing endpoints typically show up on the top 2-5% of payload sizes seen in production traffic | Consistent with memory limits being sized for median payloads |
| Streaming/chunked processing implementations reduce OOM-related failures by an estimated 80-95% compared to load-entire-payload-into-memory implementations | Because peak resident memory becomes roughly constant instead of proportional to input size |
| A meaningful fraction of "connection reset" errors reported against self-hosted or containerized tool backends, often 10-25%, trace back to OOM kills rather than network issues | Hard to distinguish without server-side memory metrics |

## Mitigations
1. **Client-side payload size pre-checks**: Reject or pre-split payloads above a known-safe threshold before submission, based on empirically observed memory-per-byte ratios for the specific tool.
2. **Prefer streaming APIs**: Where the tool offers a streaming or chunked-upload variant, use it instead of a single large-payload call, since streaming implementations typically hold bounded memory regardless of total size.
3. **Chunk and reassemble**: Split large inputs (CSV rows, JSON arrays, file uploads) into memory-safe chunks processed independently, aggregating results client-side.
4. **Treat abrupt connection resets on large payloads as OOM-shaped**: Classify silent connection drops correlated with payload size as a distinct failure mode from generic network errors, and respond by shrinking the payload rather than blind-retrying.
5. **Request memory-tier upgrades where available**: For tools that offer configurable memory allocation per operation (e.g., serverless function tiers), route known-large operations to a higher-memory tier proactively.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `operation.oom_kill_count` | Count of operations terminated by an out-of-memory kill (server-side, if observable) or connection-reset-with-no-body pattern (client-side proxy) | Alert on any sustained increase over baseline |
| `operation.failure_rate_by_payload_size_p95` | Failure rate for the largest 5% of payloads vs. overall failure rate | Alert when p95 failure rate exceeds 3x overall |
| `operation.peak_memory_per_byte_ratio` | Observed peak memory usage divided by input payload size, where server metrics are available | Alert when ratio trends upward, indicating a regression to non-streaming processing |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Spike in silent connection resets on large payloads | Connection-reset-with-empty-body rate correlates (r > 0.7) with payload size percentile over trailing hour | High | Suspect OOM kill; switch affected traffic to chunked/streaming path |
| Sustained OOM kills after retries | Same logical request retried 2+ times, each failing at similar payload-processing stage | Medium | Stop blind retries, pre-split payload before resubmission |

## Related Patterns
- [Cpu Quota Per Job](./cpu-quota-per-job.md) - sibling per-operation resource ceiling, CPU instead of memory
- [Execution Time Quota](./execution-time-quota.md) - large payloads often hit both memory and time ceilings together
- [Storage Quota Exceeded](./storage-quota-exceeded.md) - related but distinct: persistent storage limits versus transient in-operation memory limits
