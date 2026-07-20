# Data Pipeline Backpressure Unhandled

## Issue
An agent's downstream consumer (a database writer, an LLM enrichment call, a rate-limited third-party sync) slows down, but the upstream producer stages of the pipeline keep emitting data at the original rate because no signal travels backward to tell them to slow down. The gap between production and consumption rate is absorbed by an in-memory or disk queue that has no bound, until it either fills and starts dropping messages or exhausts host memory and crashes the whole pipeline.

**Frequency**: Common

**Symptoms**
- Queue depth grows monotonically during load spikes and never drains back to baseline
- Producer-side metrics show steady throughput while consumer-side metrics show falling throughput, with no correlated slowdown upstream
- Out-of-memory crashes or forced restarts of queueing infrastructure during traffic spikes
- Silent message drops at an unbounded-but-capped buffer, discovered only when downstream data has gaps
- Consumer catches up hours later processing a backlog of now-stale data, producing outputs the agent treats as current

## Root Cause
Most pipelines are built and load-tested as independent stages connected by "fire and forget" queues, so the interface contract between producer and consumer never specifies what the producer should do when the consumer falls behind. Backpressure requires an explicit two-way signal (a bounded queue that blocks the producer, a credit-based flow control scheme, or a rate advertised by the consumer) and that signal is easy to omit because everything works fine under normal load — the failure mode only appears when consumer latency degrades, which is exactly the condition under which nobody is watching closely enough to add the missing feedback loop before it causes damage.

## Example
```
An agent pipeline ingests support tickets (avg 200/min), classifies them with
an LLM call (avg 150ms), and writes results to a ticket-routing queue consumed
by an on-call assignment service.

The LLM provider has a partial outage: classification latency jumps from
150ms to 4s per call. The ingestion stage keeps pulling 200 tickets/min from
the source queue and pushing them into an in-memory buffer feeding the
classification stage, because ingestion has no way to know classification
has slowed down.

Within 12 minutes the in-memory buffer grows from a few hundred tickets to
over 40,000, exceeding the container's memory limit. The pipeline process is
OOM-killed by the orchestrator. On restart, the in-memory buffer is lost
entirely -- 40,000 support tickets that were successfully ingested from the
source queue are never classified or routed, and there is no record they
existed because the source queue had already acknowledged and removed them.
```

## Statistics
| Finding | Context |
|---------|---------|
| Pipelines without bounded, blocking queues between stages report OOM or crash-induced data loss in an estimated 15-25% of sustained downstream slowdown incidents | Typical range observed in pipeline reliability postmortems |
| Adding bounded queues with producer-side blocking reduces unhandled-backpressure data loss incidents by an estimated 80-90% | Reported range across teams that retrofitted flow control |
| Median time from consumer slowdown onset to first dropped/lost message in unbounded-queue pipelines is on the order of minutes to tens of minutes, depending on buffer size and load | Estimated from incident timeline analysis |

## Mitigations
1. **Bounded, blocking queues**: Replace unbounded in-memory buffers with fixed-capacity queues that block or reject new writes from the producer once full, forcing the slowdown to propagate upstream instead of accumulating.
2. **Credit-based flow control**: Have the consumer advertise how many in-flight items it can accept, and require the producer to hold a credit before sending, so the rate is jointly negotiated rather than producer-dictated.
3. **Load-shedding with explicit policy**: When backpressure is sustained, deliberately drop or defer low-priority items according to a documented policy (rather than an implicit, unpredictable buffer-overflow drop) and log what was shed.
4. **Producer-side rate throttling on consumer lag signal**: Have the producer poll or subscribe to a consumer lag metric and self-throttle ingestion when lag exceeds a threshold, rather than requiring a hard block.
5. **Durable intermediate storage**: Route through a durable, disk-backed queue (rather than pure in-memory) between stages with different throughput characteristics, so a crash loses at most unacknowledged in-flight items, not the whole backlog.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| queue_depth | Number of items waiting between producer and consumer stage | Alert if growth is sustained for > 5 min without draining |
| producer_consumer_rate_delta | Difference between producer emit rate and consumer processing rate | Alert if consumer rate < 50% of producer rate for > 2 min |
| dropped_or_shed_message_count | Count of messages dropped due to buffer overflow or load shedding | Alert if > 0 for unbounded-queue pipelines (should be zero by design) |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Unbounded queue growth | queue_depth exceeds a defined capacity threshold with no sign of draining | High | Trigger producer throttling, page on-call, investigate consumer slowdown |
| Consumer lag exceeds SLA | End-to-end processing lag exceeds the pipeline's freshness SLA | Medium | Scale consumer capacity, evaluate load shedding policy |

## Related Patterns
- [Data Pipeline Latency](./data-pipeline-latency.md) - unhandled backpressure is the acute failure that chronic latency accumulation can trigger
- [Data Pipeline Lossy Transformation](./data-pipeline-lossy-transformation.md) - load-shedding under backpressure is a deliberate form of the same data loss this pattern causes accidentally
- [Data Pipeline Replay Idempotency](./data-pipeline-replay-idempotency.md) - recovering from a backpressure-induced crash often requires replaying the backlog, which needs idempotent processing to avoid duplicates
