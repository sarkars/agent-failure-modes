# Memory Priority Inversion

## Issue
A shared memory store's write path — a queue, a lock, a single-threaded writer — has no concept of write priority, so a burst of low-priority writes (verbose interaction logging, background enrichment, routine housekeeping updates) can occupy the write pipeline or hold a lock long enough that a high-priority write (a safety-relevant correction, a critical status update) queues behind them and is delayed well past when it was needed. The delay isn't caused by the high-priority write being slow itself — it's blocked waiting for unrelated, lower-value writes to clear ahead of it in a shared, priority-blind pipeline.

**Frequency**: Occasional

**Symptoms**
- A critical memory update is delayed noticeably longer than its own processing time would predict
- Delay correlates with a burst of unrelated, lower-priority write activity on the same store/queue/lock
- High-priority writes have no fast-path or preemption mechanism distinct from routine writes
- Incident timelines show the critical write was submitted promptly but sat queued behind other work
- Problem worsens under load and disappears when background write volume is low, pointing to contention rather than logic error

## Root Cause
Most memory write pipelines are built as a single FIFO queue or a single lock guarding the write path, because that's the simplest way to guarantee ordering and avoid write conflicts. This design has no notion that some writes matter more than others — a routine "log this interaction" write and a "flag this account as fraudulent, block further actions" write are processed identically, in submission order, through the same channel. Under normal, low-volume conditions this is invisible because the queue rarely backs up. Under bursty load — a spike of background writes, a batch job, a flood of low-priority updates — the shared, undifferentiated pipeline becomes a bottleneck, and because there's no priority lane or preemption, a high-priority write submitted during that burst simply waits its turn behind everything queued ahead of it, regardless of how urgent it is.

## Example
```
Shared memory write queue processes writes strictly FIFO, one at a
time, average write latency 15ms.

14:00:00.000 - A background enrichment job begins bulk-writing
                2,000 low-priority "interaction metadata" updates
                to the same queue, submitted in a tight loop.

14:00:03.400 - A fraud-detection sub-agent writes a critical update:
                "account #5521 flagged: suspicious transaction
                pattern, suspend further automated approvals" —
                submitted to the same FIFO queue, landing behind
                roughly 220 of the bulk enrichment writes already
                queued ahead of it.

14:00:06.700 - The critical fraud-flag write finally processes,
                ~3.3 seconds after submission (vs. the expected
                ~15ms for an uncontended write).

In the intervening 3.3 seconds, an unrelated automated approval
workflow reads account #5521's memory (still showing no fraud
flag, since the write hadn't processed yet) and approves a
transaction that should have been blocked, because the safety-
critical write was stuck behind thousands of routine log entries
in a priority-blind queue.
```

## Statistics
| Finding | Context |
|---------|---------|
| FIFO write queues without priority lanes typically show tail latency for any individual write scaling directly with concurrent queue depth, regardless of that write's importance | Typical behavior for undifferentiated FIFO write pipelines |
| Bursty low-priority write volume (batch jobs, bulk logging) is a common trigger for the worst-case delays observed in priority-blind memory pipelines | Reported pattern across teams operating mixed-priority write workloads |
| Adding a priority queue or separate fast-path for critical writes reduces observed high-priority write latency substantially under the same burst conditions | Estimated from before/after comparisons in teams that added priority lanes |

## Mitigations
1. **Priority queues/lanes**: Split the write pipeline into priority tiers (critical/normal/background) with the critical lane processed first or given dedicated capacity, so background bursts cannot delay critical writes.
2. **Write preemption for critical updates**: Allow a critical-priority write to jump ahead of queued lower-priority writes rather than waiting strictly in submission order.
3. **Rate-limit low-priority bulk writers**: Throttle background/batch write jobs to a rate that leaves headroom for critical writes to be processed promptly even during a burst.
4. **Separate infrastructure for high-volume low-priority writes**: Route routine logging/enrichment writes to a different queue or store entirely, so they physically cannot contend with the path used for critical updates.
5. **Priority-aware latency monitoring**: Track write latency segmented by priority tier, not just in aggregate, so a critical-tier latency regression isn't masked by an overall healthy average dominated by low-priority traffic.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| critical_write_latency_p95 | 95th percentile latency specifically for critical-priority writes | Alert if > 500ms |
| queue_depth_at_critical_submit | Number of lower-priority writes queued ahead of a critical write at submission time | Alert if > 10 |
| priority_inversion_incident_count | Count of critical writes whose processing was measurably delayed by queued lower-priority writes | Alert if > 0 |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Critical write delayed by queue contention | A critical-priority write's latency exceeds threshold while lower-priority writes are queued ahead of it | High | Escalate to on-call, manually expedite the write, review priority-lane coverage |
| Background write burst detected | A batch/bulk writer submits volume likely to cause queue contention | Medium | Throttle the bulk writer, verify priority lane isolation is in place |

## Related Patterns
- [Memory Interleaving Corruption](./memory-interleaving-corruption.md) - both are consequences of a write pipeline not being designed for the concurrency/priority realities of production load
- [Memory Loss on Reboot](./memory-loss-on-reboot.md) - checkpointing added to prevent reboot loss can itself add to write-path contention that triggers priority inversion
- [Retrieval Confidence Miscalibration](./retrieval-confidence-miscalibration.md) - unrelated failure surface, but both illustrate a subsystem (queue priority, relevance scoring) missing a signal the agent implicitly assumes exists
