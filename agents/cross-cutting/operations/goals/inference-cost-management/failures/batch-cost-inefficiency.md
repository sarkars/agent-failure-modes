# Batch Cost Inefficiency

## Issue
An inference serving layer batches requests to amortize fixed per-request overhead (kernel launch, KV-cache setup, attention computation) across GPU-seconds, but the batching strategy itself wastes money — fixed-size batches get padded with empty slots when traffic doesn't fill them, a batch window that's too short forces many small batches instead of one efficient large one, or a window that's too long holds cheap requests hostage waiting for a batch to fill while GPUs idle. The result is that the same workload costs meaningfully more per token than a well-tuned batching policy would produce.

**Frequency**: Common

**Symptoms**
- GPU utilization graphs show a sawtooth pattern with regular idle gaps between batches
- Cost-per-1K-tokens is stable during peak traffic but spikes during off-peak hours
- Padding tokens (measured as batch_slots_allocated minus batch_slots_used) make up a large share of total processed tokens
- Average batch size is well below the configured max_batch_size even though queue depth data shows requests were waiting
- Doubling replica count doesn't proportionally reduce latency, suggesting each replica is running inefficient sub-capacity batches rather than the fleet being genuinely saturated

## Root Cause
Static batch-size and batch-window configurations are tuned for one traffic profile (usually peak load) and then left unchanged as traffic varies. Fixed-size batching allocates GPU memory and compute for the configured batch size regardless of how many requests actually arrive in the window, so at low traffic the engine still "pays" for a full batch's worth of compute against a half-empty batch — the padding is real GPU-seconds billed to nothing. Fixed-window batching has the opposite failure: a short window forces the scheduler to flush small batches even when a slightly longer wait would have let two or three more requests join, destroying the per-token amortization batching exists to provide. Continuous/dynamic batching engines reduce but don't eliminate this — request length heterogeneity means short requests still finish and vacate slots that sit idle until the next scheduling tick, and mismatched max-sequence-length settings force the scheduler to reserve worst-case memory per slot even for short prompts.

## Example
```
A team runs an inference service for a document-summarization agent behind
vLLM with a static configuration: max_batch_size=32, batch_window=50ms,
tuned during a load test that simulated business-hours peak traffic
(roughly 28-30 concurrent requests at any time).

Overnight, traffic drops to 4-6 concurrent requests. The scheduler still
opens batches sized for 32 slots because the deployment config wasn't
traffic-aware, and the 50ms window is too short for enough requests to
arrive and fill it. Each overnight batch runs at 15-20% occupancy.

Monthly GPU cost analysis shows:
- Peak hours (9am-6pm): $0.038 per 1K output tokens
- Off-peak hours (6pm-9am): $0.091 per 1K output tokens

The off-peak cost-per-token is 2.4x higher for functionally identical
requests, purely because the batch shape doesn't match the arrival rate.
Nobody notices for three months because the team monitors total daily
spend, which is dominated by peak-hour volume, not cost-per-token by
time-of-day.
```

## Statistics
| Finding | Context |
|---------|---------|
| Static batch configurations tuned for peak traffic typically run at 40-60% effective occupancy during off-peak windows | Typical range observed in production GPU serving deployments |
| Switching from fixed-size to continuous/dynamic batching commonly reduces per-token cost by 20-35% under variable traffic | Estimated range across teams migrating serving frameworks |
| Cost-per-token variance of 2-3x between peak and off-peak hours is a common signature of unmonitored batch inefficiency | Typical range inferred from time-of-day cost analyses |

## Mitigations
1. **Adopt continuous/dynamic batching**: Use serving engines (vLLM, TensorRT-LLM, TGI) that admit and evict requests from a batch continuously rather than waiting for a fixed window to fill, so slot occupancy tracks arrival rate instead of a static schedule.
2. **Traffic-aware batch-size scaling**: Tie max_batch_size and batch_window to a rolling estimate of concurrent request rate, widening the window during low-traffic periods and shrinking it during high-traffic bursts, rather than using one static value around the clock.
3. **Track cost-per-token by time window, not just total spend**: Add a dashboard metric that divides GPU-seconds billed by tokens actually processed, bucketed hourly, so padding waste is visible as a rate rather than hidden inside an aggregate daily cost figure.
4. **Bucket requests by expected length before batching**: Group short and long requests into separate batch queues so the scheduler doesn't reserve worst-case sequence-length memory for every slot in a mixed batch, reducing padding from length heterogeneity.
5. **Autoscale replica count against occupancy, not raw request count**: Scale down replicas when average batch occupancy is low even if request volume is nonzero, and scale up before occupancy saturation causes queueing, so the fleet size matches the batching efficiency curve rather than a naive request-count threshold.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| batch_occupancy_ratio | Batch slots actually used divided by batch slots allocated, per scheduling tick | Alert if 30-min average < 0.5 |
| cost_per_1k_tokens_hourly | GPU spend attributed to inference divided by tokens processed, bucketed hourly | Alert if any hour exceeds 1.5x the trailing 7-day median |
| padding_token_share | Padding tokens as a fraction of total tokens processed in a batch | Alert if > 25% sustained over 15 minutes |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Sustained low batch occupancy | batch_occupancy_ratio < 0.4 for more than 30 minutes outside a known low-traffic window | Medium | Investigate scheduler config; consider dynamic batch sizing or replica scale-down |
| Off-peak cost-per-token spike | cost_per_1k_tokens_hourly exceeds 2x the peak-hour baseline | High | Review batch window and size settings for the affected time window; check for a stale static config |

## Related Patterns
- [Latency Cost Tradeoff](./latency-cost-tradeoff.md) - batch sizing decisions sit directly on the latency/cost curve this pattern describes
- [Throughput Per Dollar Optimization Failure](./throughput-per-dollar-optimization-failure.md) - batching tuned for raw throughput without accounting for occupancy waste is a specific instance of this broader failure
- [Resource Reservation Insufficient](./resource-reservation-insufficient.md) - the inverse failure, where batch/replica sizing under-provisions rather than wastes capacity
