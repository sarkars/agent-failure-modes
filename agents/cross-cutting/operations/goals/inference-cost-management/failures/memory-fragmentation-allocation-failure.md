# Memory Fragmentation Allocation Failure

## Issue
An inference server's GPU has enough total free memory to serve a new request's KV-cache, but that free memory is scattered across many small, non-contiguous blocks left behind by requests of varying sequence lengths finishing and freeing memory at different times. The allocator can't satisfy the new request's contiguous-block requirement and either rejects it (a false-capacity-exhaustion error on a GPU that's nominally 40% free) or triggers an expensive defragmentation/compaction pass that stalls the whole batch — either way, the fleet needs more replicas than total memory usage alone would suggest, directly inflating cost-per-token.

**Frequency**: Occasional

**Symptoms**
- Requests fail with out-of-memory or allocation errors while fleet-wide GPU memory utilization dashboards show significant headroom (e.g. 30-40% "free")
- Allocation failures correlate with long-running nodes (high uptime since last restart) more than with raw traffic volume
- Restarting the inference process on an affected node immediately resolves the errors without any traffic or config change
- Memory fragmentation ratio (free-but-non-contiguous versus total free) trends upward over a node's uptime and resets to near-zero after restart
- Effective usable capacity per node degrades over time, forcing earlier autoscaling triggers and more replicas than the workload's actual memory footprint requires

## Root Cause
KV-cache memory allocation is highly heterogeneous: a 200-token chat request and a 32,000-token document-analysis request request very different contiguous block sizes, and they arrive and complete in an unpredictable interleaved order. Naive or block-based allocators that don't actively defragment will, over enough allocate/free cycles, leave the address space checkerboarded with small free gaps that individually can't satisfy a new large-sequence request even though their sum exceeds what's needed. This is the classic external-fragmentation problem, but it's especially costly in GPU-inference contexts because GPU memory is a hard, expensive, and comparatively small resource (tens of gigabytes versus terabytes of host RAM), so a percentage of unusable free memory translates directly into fewer sequences the node can serve concurrently — and therefore more replicas needed to hit the same throughput target. PagedAttention-style allocators (used by engines like vLLM) mitigate this by allocating in fixed-size pages rather than variable contiguous blocks, but fragmentation can still occur at the page-table or block-pool level under adversarial-enough sequence-length mixes, and older or custom serving stacks without paged allocation are fully exposed to the classic failure.

## Example
```
A document-analysis agent runs on a serving stack with a non-paged,
contiguous-block KV-cache allocator (a custom fork predating the team's
migration to vLLM). Request lengths are bimodal: 70% are short chat-style
queries (under 500 tokens) and 30% are long document-ingestion requests
(15,000-30,000 tokens).

Over a node's 6-day uptime between routine restarts, thousands of short
requests allocate and free small blocks while long requests allocate and
free large blocks at less frequent, uncorrelated intervals. By day 5, the
memory address space has fragmented into many small free gaps averaging
1,200 tokens each, totaling 38% of GPU memory "free" by the aggregate
metric.

A new 22,000-token document-ingestion request arrives. No single free gap
is large enough to hold its KV-cache, despite 38% aggregate free memory.
The allocator returns an OOM-style error, the request fails, and the
client retries — which fails again for the same reason, since the retry
lands on the same fragmented node.

The autoscaler, seeing the failure as a capacity signal, adds 2
additional replicas to absorb long-document traffic, even though a
simple restart of the fragmented node would have restored its full
usable capacity. The extra replicas run for the following week before a
cost review identifies the pattern and the team adds a scheduled
fragmentation-triggered restart, after which replica count drops back to
baseline.
```

## Statistics
| Finding | Context |
|---------|---------|
| Non-paged KV-cache allocators under bimodal or highly variable sequence-length workloads commonly reach 25-45% unusable "free" memory within days of continuous uptime | Typical range observed in custom/legacy serving stacks |
| Migrating to a paged-attention allocator (fixed-size block allocation) commonly reduces fragmentation-driven allocation failures by 80%+ | Estimated range based on paged-allocator adoption case reports |
| Fragmentation-driven autoscaling (adding replicas to compensate for unusable free memory rather than genuine capacity shortage) commonly adds 10-20% avoidable fleet cost when unaddressed | Estimated range from postmortems identifying the root cause |

## Mitigations
1. **Adopt paged/block-based KV-cache allocation**: Use or migrate to serving engines with paged-attention-style memory management (fixed-size pages rather than variable contiguous blocks), which largely eliminates classic external fragmentation by design.
2. **Scheduled proactive restarts on long-running nodes**: For stacks without paged allocation, schedule periodic restarts (or rolling recycling) of long-uptime nodes before fragmentation reaches a level that causes allocation failures, trading a small planned disruption for avoided emergency capacity additions.
3. **Track fragmentation ratio as a distinct metric from raw free memory**: Instrument the allocator to report "largest contiguous free block" alongside "total free memory" so fragmentation is visible before it causes a failure, rather than only showing up as an unexplained OOM.
4. **Sequence-length-aware request routing**: Route long-sequence requests to a dedicated pool of nodes (or ones recently restarted) separate from high-churn short-request traffic, reducing the adversarial interleaving that drives fragmentation.
5. **Diagnose allocation failures before autoscaling**: Add a check in the autoscaling/incident-response runbook to distinguish "genuine capacity shortage" from "fragmentation on an otherwise-capable node" before adding replicas, since the fixes (restart vs. scale-up) are different and only one is genuinely needed.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| largest_contiguous_free_block_ratio | Largest contiguous free memory block divided by total free memory | Alert if < 0.5 (severe fragmentation) |
| allocation_failure_rate_at_high_free_memory | Allocation failures occurring while aggregate free memory exceeds 25% | Alert if nonzero, indicates fragmentation rather than genuine exhaustion |
| node_uptime_vs_fragmentation_correlation | Fragmentation ratio tracked against node uptime since last restart | Alert if fragmentation ratio trend is monotonically increasing past a defined threshold |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Fragmentation-driven allocation failure | Allocation failure occurs while aggregate free memory > 25% | High | Restart the affected node; investigate whether a paged allocator migration is warranted |
| High fragmentation approaching threshold | largest_contiguous_free_block_ratio < 0.6 on any node | Medium | Schedule proactive restart before failures occur; avoid autoscaling in response |

## Related Patterns
- [Resource Leak](./resource-leak.md) - both degrade a node's effective capacity gradually over uptime until a restart resolves them, though the underlying mechanism differs
- [Concurrent Request Resource Explosion](./concurrent-request-resource-explosion.md) - fragmentation reduces the effective ceiling that a concurrency spike can push past, making the explosion more likely at a given nominal capacity
- [Resource Reservation Insufficient](./resource-reservation-insufficient.md) - fragmentation-driven failures are often misdiagnosed as this pattern, leading to unnecessary over-provisioning instead of the correct fix
