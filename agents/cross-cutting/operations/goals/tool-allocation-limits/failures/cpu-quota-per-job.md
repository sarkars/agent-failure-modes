# Cpu Quota Per Job

## Issue
A tool executes agent-submitted work as a job (e.g., a serverless function, a batch data-processing task, a sandboxed code-execution call) under a fixed CPU quota — a cgroup limit, a vCPU-second cap, or a throttling policy. When the agent's request involves more computation than expected (a larger dataset, an unexpectedly expensive query plan, a recursive operation), the job gets throttled mid-execution or killed outright by the orchestrator, and the agent receives a generic failure with no indication that CPU exhaustion was the cause.

**Frequency**: Common

**Symptoms**
- Jobs that succeed on small inputs fail unpredictably on larger ones with no clear error message
- Execution time balloons just before failure, consistent with CPU throttling rather than a hard crash
- Error messages are generic ("job failed", "internal error", exit code 137 or 143) with no CPU-specific diagnostic
- Retrying the identical request sometimes succeeds (when the host had spare capacity) and sometimes fails (when it didn't), making the failure look nondeterministic
- Jobs that call CPU-bound library functions (regex on large text, image processing, cryptographic operations) fail more often than I/O-bound ones

## Root Cause
Multi-tenant execution platforms enforce per-job CPU quotas to guarantee fair scheduling and prevent noisy-neighbor effects, typically via cgroups CPU shares/quota or a hard vCPU-second budget. The agent's request-construction logic has no insight into the CPU cost of the operation it's requesting — it only knows the logical task ("summarize this file," "transform this dataset") — so it cannot predict when a given input will exceed the quota. When the quota is hit, the orchestrator either throttles the process (making it appear to hang) or sends SIGKILL, and this signal rarely propagates back through the tool's API as a distinguishable "CPU quota exceeded" error versus any other failure.

## Example
```
1. Agent calls a document-processing tool's "extract-tables" endpoint on a 40-page PDF.
   The job runs in a container with a CPU quota of 2 vCPU-seconds per 10 wall-clock seconds
   (i.e., throttled to 20% if it tries to use more).
2. For a typical 5-page PDF, table extraction finishes in 1.5 CPU-seconds — well under quota.
3. This 40-page PDF has several pages with dense nested tables, pushing actual CPU need
   to ~9 vCPU-seconds.
4. The cgroup begins throttling the process at the 2-second mark; the job's wall-clock
   time balloons from an expected 2s to 45s as it fights for CPU slices.
5. The orchestrator's own job-timeout (unrelated to the CPU quota, set at 30s) fires first
   and kills the container.
6. The tool's API returns HTTP 500 "internal processing error" with no mention of CPU
   throttling; the agent's retry logic retries the identical request and fails identically
   every time, since the input size hasn't changed.
```

## Statistics
| Finding | Context |
|---------|---------|
| CPU-quota-induced job failures are typically 3-8x more likely on the top 5% largest inputs by size/complexity | Consistent with quota limits being sized for median, not tail, workloads |
| A meaningful share of "flaky" job failures in multi-tenant execution platforms trace back to CPU throttling rather than logical bugs, in the range of 15-30% based on typical incident retrospectives | Hard to isolate without host-level cgroup metrics |
| Adding input-size-based pre-checks before job submission has been observed to cut CPU-quota failures by roughly half | Because oversized inputs are rejected/routed before consuming a quota slot |

## Mitigations
1. **Pre-submission complexity estimation**: Estimate the CPU cost of a request from proxy signals (input size, page count, recursion depth) before submitting, and route oversized requests to a higher-quota tier or split them into smaller sub-jobs.
2. **Chunking and batching**: For processing tasks that scale with input size, split large inputs into quota-safe chunks processed sequentially or in parallel across multiple jobs rather than one oversized job.
3. **Distinguish throttling from failure in monitoring**: Where the platform exposes cgroup or job-level CPU metrics, surface "throttled" as a distinct state from "failed" so retries and alerting can react differently.
4. **Quota-aware retry with backoff to a bigger tier**: On ambiguous failures correlated with large inputs, retry against a higher-CPU-quota execution tier instead of blindly retrying the same configuration.
5. **Timeout headroom below the kill threshold**: Set the agent's own client-side timeout comfortably below the platform's hard-kill timeout so the agent can detect and log "likely CPU-bound stall" before the orchestrator's SIGKILL erases diagnostic context.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `job.cpu_throttled_pct` | Percentage of job wall-clock time spent CPU-throttled (from cgroup cpu.stat) | Alert above 30% |
| `job.failure_rate_by_input_size_p95` | Job failure rate for the top 5% largest inputs vs. overall | Alert when p95 failure rate > 3x overall |
| `job.oom_or_sigkill_count` | Count of jobs terminated by SIGKILL/exit 137 | Alert on any sustained increase week-over-week |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Elevated CPU-quota kills | `oom_or_sigkill_count` rate doubles over trailing 1-hour baseline | High | Check for a recent shift in input size/complexity distribution, consider quota tier bump |
| Sustained throttling on retries | Same job ID retried >2 times with `cpu_throttled_pct` > 50% each time | Medium | Route job to higher-CPU tier or split input before further retries |

## Related Patterns
- [Memory Quota Per Operation](./memory-quota-per-operation.md) - same class of resource-limit failure, memory instead of CPU
- [Execution Time Quota](./execution-time-quota.md) - CPU throttling often manifests as hitting the execution-time limit
- [Storage Quota Soft Limit](./storage-quota-soft-limit.md) - degraded-performance-before-hard-failure pattern shared across resource types
