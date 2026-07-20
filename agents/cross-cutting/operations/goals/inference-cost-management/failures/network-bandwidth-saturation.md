# Network Bandwidth Saturation

## Issue
Inference traffic — especially large prompt payloads (long context windows, embedded images/documents), streaming token responses to many concurrent clients, and cross-node traffic for tensor-parallel or pipeline-parallel model sharding — saturates available network bandwidth on a node or rack. Once bandwidth saturates, requests that should be GPU-bound become network-bound: token streaming stalls, tensor-parallel all-reduce operations slow the entire batch down to the pace of the slowest network hop, and unrelated services sharing the same network fabric see cascading timeouts, all while GPUs sit fed at a fraction of their real throughput and continue billing at full rate for degraded output.

**Frequency**: Rare

**Symptoms**
- GPU utilization drops while network interface utilization on the same node approaches link capacity
- Token streaming to clients shows irregular, "chunky" delivery instead of smooth token-by-token pacing, especially under high concurrent-connection counts
- Tensor-parallel or multi-node inference latency degrades disproportionately compared to single-node latency, pointing to inter-node all-reduce/all-gather traffic as the bottleneck
- Unrelated services on the same physical network segment or rack experience timeouts or elevated latency correlated with inference traffic spikes
- Cost-per-token rises during bandwidth-saturated periods because GPU-seconds are billed against a batch that's waiting on network I/O rather than computing

## Root Cause
Large-context and multimodal inference workloads move substantially more data per request than earlier text-only, short-context assumptions baked into network capacity planning — a single request with a 100-page PDF or several embedded images can carry tens of megabytes of input payload, and streaming responses to hundreds of concurrent long-running connections multiplies outbound bandwidth demand in a way that scales with concurrency, not just request count. For multi-GPU model-parallel serving (tensor parallelism across GPUs, and especially across nodes), every forward pass requires synchronizing partial results across the parallel group via network-bound collective operations (all-reduce, all-gather); if the interconnect between those GPUs is bandwidth-constrained (e.g. falling back to standard Ethernet instead of a high-bandwidth fabric like InfiniBand or NVLink for cross-node communication), the collective operation — and therefore the whole batch — runs at the network's pace regardless of how fast the GPUs themselves could compute. Because bandwidth is a shared, fungible resource across everything on the same physical link or rack, saturation from inference traffic doesn't stay contained to inference — it degrades any other service sharing that fabric, and capacity planning that only accounts for GPU and memory headroom misses this entirely.

## Example
```
A multimodal document-analysis agent is deployed with tensor parallelism
across 4 GPUs per node, using standard 25Gbps Ethernet for inter-GPU
communication (the team hadn't budgeted for InfiniBand given cost
constraints). Requests routinely include multi-page scanned documents as
image inputs, averaging 15MB per request after preprocessing.

A batch push of overnight document-processing jobs sends 40 concurrent
requests, each requiring image payload transfer plus the tensor-parallel
all-reduce traffic for every forward pass across the 4-GPU group. Network
utilization on the node's interconnect hits 92% of the 25Gbps link
capacity.

GPU utilization drops to 45% because each GPU spends increasing time
blocked waiting on the all-reduce step to complete across the
network-constrained interconnect. Per-request latency roughly triples.
Because GPUs are still allocated and billed for the full duration
(reserved capacity), but throughput fell by more than half, effective
cost-per-processed-document rises by an estimated 120% during the
saturated window.

A separate internal service sharing the same rack's top-of-rack switch
(an unrelated metrics-collection pipeline) also reports elevated latency
and dropped connections during the same window, initially investigated
as an unrelated incident until network utilization graphs reveal the
inference workload as the shared root cause.
```

## Statistics
| Finding | Context |
|---------|---------|
| Multimodal or long-context inference requests can carry 10-100x the payload size of short-text requests, materially changing network capacity requirements | Typical range depending on modality and context length |
| Falling back to standard Ethernet instead of a high-bandwidth fabric for multi-node tensor parallelism commonly reduces effective throughput by 30-60% under sustained load | Estimated range from multi-node serving benchmarks |
| Network-bound GPU idling during bandwidth saturation events commonly raises effective cost-per-token by 50-100% for the duration of the saturation | Estimated range based on GPU utilization drop during saturation incidents |

## Mitigations
1. **Provision high-bandwidth interconnect for model-parallel serving**: Use NVLink/NVSwitch for intra-node and InfiniBand (or equivalent) for inter-node GPU communication when running tensor or pipeline parallelism, rather than relying on standard datacenter Ethernet for collective operations.
2. **Capacity-plan network bandwidth alongside GPU and memory**: Include network throughput as an explicit dimension in inference capacity planning, sized against realistic payload sizes (including multimodal/long-context requests), not assumed to be a non-bottleneck.
3. **Compress and pre-process large payloads before the network hop**: Downsample images, chunk or summarize oversized document inputs, and use efficient serialization for streaming responses to reduce the bandwidth footprint per request without degrading task quality.
4. **Isolate inference traffic from other services at the network level**: Use dedicated network segments, QoS policies, or bandwidth reservations for inference traffic so saturation from a traffic spike doesn't cascade into unrelated services sharing the same fabric.
5. **Alert on network utilization as a first-class capacity signal**: Monitor and alert on interconnect and NIC utilization with the same rigor as GPU/memory utilization, since network-bound degradation produces the same cost-per-token symptom through a different, easily overlooked mechanism.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| network_interface_utilization | Percentage of NIC or interconnect bandwidth capacity in use | Alert if > 80% sustained for 5 minutes |
| gpu_network_idle_ratio | Fraction of GPU idle time attributable to waiting on network-bound collective operations | Alert if > 20% during a batch window |
| tensor_parallel_allreduce_latency | Time spent in cross-GPU/cross-node all-reduce operations per forward pass | Alert if exceeds 2x the single-node baseline |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Network saturation on inference node | network_interface_utilization > 85% for 5+ minutes | High | Investigate payload sizes and concurrent connection count; consider payload compression or traffic isolation |
| GPU idling on network wait | gpu_network_idle_ratio > 25% sustained | Medium | Check interconnect fabric type and tensor-parallel configuration; consider provisioning higher-bandwidth links |

## Related Patterns
- [CPU Saturation Cascade](./cpu-saturation-cascade.md) - a parallel infrastructure-bottleneck mechanism where a different shared resource saturates and cascades into inference degradation
- [Concurrent Request Resource Explosion](./concurrent-request-resource-explosion.md) - a concurrency spike can be the trigger event that drives network bandwidth into saturation, particularly for streaming or large-payload workloads
- [Latency Cost Tradeoff](./latency-cost-tradeoff.md) - network-bound latency degradation forces the same cost-vs-latency tension as compute-bound causes, but from an often-unmonitored source
