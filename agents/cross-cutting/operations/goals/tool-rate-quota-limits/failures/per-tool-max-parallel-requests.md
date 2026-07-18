# Per-Tool Max Parallel Requests

## Issue
A tool rejects any request beyond N simultaneously in-flight requests per account, regardless of connection count or overall request rate — a request-level concurrency cap rather than a connection-level or rate-based one. An agent orchestrator that dispatches parallel tool calls without an explicit concurrency throttle routinely exceeds this in-flight limit during fan-out, causing a wave of immediate rejections that has nothing to do with total volume or open connections.

**Frequency**: Common

**Symptoms**
- Requests fail instantly with errors like "max concurrent requests exceeded" or "too many in-flight requests," distinct from both 429 rate-limit and connection-refused errors
- Failures happen specifically when several tool calls are dispatched at nearly the same moment, not when the same total volume is spread out sequentially
- The rejected requests' count roughly matches "total parallel dispatch minus N," where N is the vendor's undocumented or lightly-documented parallelism cap
- Retrying rejected requests immediately (without waiting for in-flight requests to complete) produces the same rejection again
- The tool's request-per-second and daily-quota metrics look completely healthy at the time of the failures

## Root Cause
Some APIs limit concurrency at the request-processing layer itself (e.g., a fixed worker pool sized N behind the API gateway) rather than at the network/connection layer or via a token-bucket rate limiter. This is architecturally different from a connection limit — the vendor may allow many open connections but only process N requests at a time across all of them — and different from a rate limit, since it's about *how many requests are outstanding right now*, not *how many were sent in a time window*. Agent orchestrators typically model tool capacity as either "requests per second" or "concurrent connections," and have no separate concept of "requests currently awaiting a response," so this cap is invisible until it's hit.

## Example
```
A document-processing agent uses the "OCRExtract" tool to pull text from 25 scanned PDFs in parallel, one tool call per document, expecting near-linear speedup.

OCRExtract's backend processes requests through a fixed worker pool of 6 — it accepts many concurrent connections but only actively works on 6 requests at once, silently queuing others without documenting a queue.
In practice, OCRExtract enforces a hard reject (not a queue) once 10 requests are simultaneously in-flight from one account, to protect the queue from growing unbounded.
The agent dispatches all 25 OCR calls at once. Calls 11-25 are rejected instantly with "max parallel requests (10) exceeded."
The agent's retry logic re-dispatches the failed 15 immediately, since it has no concept of "wait for an in-flight slot" — they're rejected again because the first 10 are still processing.
The batch takes several retry cycles and multiple minutes to fully complete work that a concurrency-aware dispatcher sized to 10 would have finished in two clean waves.
```

## Statistics
| Finding | Context |
|---------|---------|
| Request-level parallelism caps (distinct from connection or rate limits) appear in an estimated 15-25% of processing-heavy third-party APIs (OCR, transcription, document conversion, ML inference) | Common in compute-bound backend services |
| Orchestrators lacking an explicit in-flight-request throttle see 2-3x more retry cycles when their fan-out width exceeds the vendor's parallelism cap by more than 2x | Observed in production document/media processing pipelines |
| Matching client-side dispatch concurrency to the vendor's documented (or empirically discovered) parallel-request cap typically converts multi-cycle retry storms into a single clean wave of the same total work | Typical outcome of concurrency-matching remediation |

## Mitigations
1. **Throttle dispatch concurrency to the discovered cap**: Use a bounded worker pool or semaphore at the orchestrator level sized to the tool's max in-flight requests, and route all calls to that tool through it, regardless of which sub-agent originated the call.
2. **Empirically discover the cap when undocumented**: If the vendor doesn't publish a parallel-request limit, binary-search for it in a controlled test (ramp concurrency until rejections start) and record the value as configuration rather than rediscovering it via production failures.
3. **Queue on rejection instead of immediate re-dispatch**: When a "max parallel requests" error is detected, hold the rejected task in a local queue and release it only as in-flight slots free up (tracked by the same semaphore), rather than blindly retrying into the same wall.
4. **Centralize concurrency accounting across sub-agents**: Ensure the in-flight counter is shared globally per tool, not per sub-agent — independent sub-agents each staying "under 5 concurrent calls" can still collectively blow past a global cap of 10 if they don't share state.
5. **Prefer the tool's native batch or async job API where available**: Many services with tight synchronous parallelism caps offer a bulk-submit-and-poll pattern instead, which sidesteps the in-flight request limit entirely.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `tool.inflight_requests` | Current count of requests dispatched to the tool awaiting a response | Alert if it approaches the known/discovered parallelism cap |
| `tool.max_parallel_rejection_count` | Count of rejections specifically attributable to the parallel-request cap | Alert if greater than 0 in any 5-minute window |
| `dispatch.concurrency_vs_cap_ratio` | Ratio of orchestrator's dispatch width to the tool's known cap | Alert if ratio exceeds 1.5x, indicating dispatch isn't throttled |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Parallelism cap breach | `max_parallel_rejection_count` > 0 during a fan-out dispatch | Warning | Verify orchestrator concurrency semaphore matches the tool's cap; add if missing |
| Repeated retry-storm on same tool | Same batch retried 3+ times against the parallelism cap without converging | Critical | Halt naive retries; switch to queue-based dispatch or the tool's batch API |

## Related Patterns
- [Per-Tool Concurrent Connections Exceeded](./per-tool-concurrent-connections-exceeded.md) - a network-layer sibling of this request-layer concurrency cap; both need an orchestrator-side throttle
- [Connection Pool Exhaustion](./connection-pool-exhaustion.md) - client-side concurrency limits can mask or compound this vendor-side cap
- [Per-Tool Burst Rate Exceeded](./per-tool-burst-rate-exceeded.md) - both are triggered by uncoordinated parallel dispatch, but this is an in-flight cap rather than a time-window cap
