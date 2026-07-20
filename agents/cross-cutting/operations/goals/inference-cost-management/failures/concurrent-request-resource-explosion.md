# Concurrent Request Resource Explosion

## Issue
A sudden spike in concurrent inference requests — from a traffic burst, a retry storm, or an agent fan-out pattern that issues many parallel sub-calls — exhausts GPU memory, CPU, or connection-pool capacity faster than autoscaling or admission control can react. Instead of degrading gracefully, the serving layer either crashes (taking down in-flight requests and forcing expensive retries) or silently over-admits requests into an already-saturated batch, driving per-request latency and cost up simultaneously as the system thrashes rather than serves.

**Frequency**: Common

**Symptoms**
- GPU out-of-memory (OOM) errors or process crashes coincide with sharp spikes in requests-per-second
- Request queue depth grows faster than it drains, with p99 latency climbing into the tens of seconds before recovering
- A retry storm follows the initial spike as timed-out clients resubmit, roughly doubling or tripling effective request volume
- Autoscaler adds replicas minutes after the spike started, well after the existing fleet has already OOM'd or begun throttling
- Cost spikes disproportionately to legitimate traffic growth because failed/retried requests still consume GPU-seconds before failing

## Root Cause
Inference servers have a hard ceiling on concurrent sequences they can hold in GPU memory (bounded by KV-cache size), but admission control is frequently either absent or tuned against average load rather than burst load. When concurrency exceeds that ceiling, the server either OOMs outright or the scheduler keeps admitting requests into a batch that no longer fits, causing every request in the batch — not just the new ones — to slow down or fail. Autoscalers compound the problem because they react to a lagging metric (CPU/GPU utilization or queue depth) with a startup latency measured in minutes (container pull, model load, warm-up), so by the time new capacity comes online the burst has already caused cascading failures and the retry storm those failures generate. Agent architectures make this worse than typical web traffic because a single user action can fan out into many parallel LLM calls (sub-agent dispatch, tool-call verification, multi-sample voting), so concurrency can spike in a step-function rather than a gradual ramp.

## Example
```
An agent orchestration platform lets a top-level planning agent spawn up to
8 parallel sub-agents per task, each making its own inference calls. A
product launch drives a burst of 200 simultaneous user sessions within a
90-second window, each triggering the 8-way fan-out.

Expected concurrent inference load: ~200 requests.
Actual concurrent load: ~1,600 requests (200 sessions x 8 sub-agents),
because the fan-out multiplier wasn't accounted for in capacity planning.

The inference fleet (sized for 400 concurrent sequences) hits its KV-cache
ceiling within 20 seconds. New requests queue, then start timing out at
the 30-second client-side timeout. Timed-out clients' retry logic
resubmits automatically, adding another ~600 requests on top of the
already-queued 1,200.

The autoscaler adds 3 new GPU replicas, but each takes 4 minutes to pull
the container image and load model weights. By the time they're ready,
the burst has passed, but the fleet spent 6 minutes processing failed and
retried requests — consuming an estimated 40% more GPU-seconds than the
original 200 legitimate sessions would have cost on their own.
```

## Statistics
| Finding | Context |
|---------|---------|
| Retry storms following a capacity-exhaustion event commonly add 30-80% extra effective request volume on top of the original burst | Typical range observed in production incident postmortems |
| Reactive autoscalers typically take 2-5 minutes to bring new inference capacity online (image pull, model load, warm-up) | Typical range for GPU-backed inference services |
| Agent fan-out patterns (parallel sub-agent or multi-sample calls) can multiply effective concurrency 3-10x relative to top-level request count | Estimated range depending on fan-out depth and branching factor |

## Mitigations
1. **Admission control with backpressure**: Reject or queue-with-explicit-signal requests once in-flight concurrency approaches the KV-cache ceiling, returning a fast, cheap "retry later" response instead of accepting a request that will fail expensively mid-batch.
2. **Fan-out-aware capacity planning**: Size inference fleets against effective concurrency (top-level requests times average fan-out multiplier), not raw top-level request counts, and instrument fan-out depth as a first-class capacity metric.
3. **Client-side jittered backoff, not naive retry**: Require agent orchestration and client SDKs to use exponential backoff with jitter on retry, and cap total retry attempts, so a capacity event doesn't automatically compound into a retry storm.
4. **Pre-warmed standby capacity**: Keep a small pool of already-warm replicas idle (or serving low-priority traffic that can be preempted) so burst absorption doesn't wait on cold-start latency.
5. **Circuit breakers on fan-out depth**: Cap the number of parallel sub-agent or sample calls a single user action can trigger, with a fallback to sequential execution or reduced sample count when the platform is near capacity.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| concurrent_sequences_in_flight | Number of sequences currently held in GPU KV-cache across the fleet | Alert if > 85% of fleet ceiling for more than 1 minute |
| retry_request_ratio | Retried requests as a fraction of total incoming requests | Alert if > 20% over a 5-minute window |
| queue_depth_growth_rate | Rate of change of pending request queue depth | Alert if positive and accelerating for 2+ consecutive intervals |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Concurrency approaching KV-cache ceiling | concurrent_sequences_in_flight exceeds 85% of fleet capacity | High | Trigger admission control / backpressure, page on-call, check for fan-out anomaly |
| Retry storm detected | retry_request_ratio exceeds 20% while queue_depth_growth_rate is positive | High | Enable aggressive rate limiting on retries, notify client teams, investigate root capacity event |

## Related Patterns
- [Resource Reservation Insufficient](./resource-reservation-insufficient.md) - describes the under-provisioning that leaves headroom too thin to absorb a concurrency spike in the first place
- [Latency Cost Tradeoff](./latency-cost-tradeoff.md) - the retry storm this pattern causes is a direct, unplanned worsening of both latency and cost simultaneously
- [Memory Fragmentation Allocation Failure](./memory-fragmentation-allocation-failure.md) - a related mechanism by which concurrent load causes allocation failures even when raw capacity looks sufficient
