# CPU Saturation Cascade

## Issue
Inference serving is usually thought of as GPU-bound, but the CPU-side work around it — request tokenization, sampling/logits post-processing, tensor-parallel coordination, response serialization, and health-check handling — runs on a shared CPU pool that can saturate independently of GPU load. When one node's CPU saturates, the GPU sits partially idle waiting on CPU-bound preprocessing/postprocessing, so the fleet's effective throughput drops; the resulting backlog shifts load onto neighboring nodes, whose CPUs then saturate in turn, cascading a single node's bottleneck into a fleet-wide throughput collapse that shows up as a spike in cost-per-token because GPUs keep billing while doing less useful work.

**Frequency**: Occasional

**Symptoms**
- GPU utilization drops while CPU utilization on the same node climbs toward 100%, an inverted pattern from the usual GPU-bound expectation
- Per-token latency degrades on nodes with normal GPU load but elevated CPU load
- Load balancer health checks start failing intermittently on saturated nodes, causing them to be marked unhealthy and traffic to redistribute onto remaining nodes
- The redistribution causes the next node to reach CPU saturation within minutes, producing a visible wave pattern across the fleet in per-node CPU graphs
- Cost-per-token rises fleet-wide even though total GPU-hours billed stayed constant, because useful output per GPU-hour fell

## Root Cause
Tokenization, especially for long prompts or requests with many stop-sequence checks, and sampling logic (top-k/top-p filtering, repetition penalties, logit-bias application) run on the CPU in the request-handling path, not the GPU kernel. When request volume or prompt length increases, this CPU-side work scales with it, but capacity planning typically sizes CPU allocation as a fixed ratio to GPU count based on an average-case workload, not the CPU-heavier tail. Once a node's CPU saturates, the GPU on that node starts idling between batches waiting for the CPU to finish preparing the next batch's inputs or finish postprocessing the last batch's outputs — the node is now paying full GPU cost for reduced GPU work. The load balancer, seeing degraded response times or failed health checks (which are themselves CPU-scheduled and get starved), routes traffic away from the struggling node onto peers. Those peers absorb the extra load with the same fixed CPU:GPU ratio, and if they were already running close to their own CPU ceiling, they saturate next, propagating the bottleneck across the fleet in a self-reinforcing wave rather than staying contained to the originating node.

## Example
```
A 12-node inference fleet serves a coding-assistant agent. Each node has
8 GPU cores and 16 CPU cores, sized for an average prompt length of 2K
tokens with light sampling (temperature-only, no repetition penalty).

A new client integration starts sending prompts averaging 18K tokens
(large codebase context) with repetition-penalty and stop-sequence
matching enabled on every request. Tokenization and per-token repetition
penalty computation are 6-8x more CPU-expensive at this prompt length and
sampling configuration.

Node 4 is the first to receive a disproportionate share of these
requests. Its CPU hits 98% utilization while its GPU utilization drops
from a typical 85% to 40%, idling between batches waiting on CPU-bound
preprocessing. Health checks on node 4 start timing out (they compete
for the same saturated CPU scheduler), and the load balancer marks it
unhealthy, rerouting its traffic to nodes 3 and 5.

Nodes 3 and 5, now handling 1.5x their normal load with the same
CPU-heavy request mix, saturate within 4 minutes. The cascade reaches 6
of the 12 nodes over the next 20 minutes before an on-call engineer
identifies the CPU:GPU imbalance and manually caps concurrent requests
per node. Fleet-wide GPU-hours billed for the incident window are
unchanged, but useful throughput fell by roughly 55%, more than
doubling effective cost-per-token for the duration.
```

## Statistics
| Finding | Context |
|---------|---------|
| CPU-bound preprocessing/postprocessing can account for 10-30% of end-to-end request latency for long-context or heavy-sampling requests | Typical range depending on prompt length and sampling configuration |
| A single saturated node in a load-balanced fleet can trigger cascading saturation across 30-60% of the fleet within 15-30 minutes if CPU:GPU ratio is uniform and undersized | Estimated range from fleet-wide incident patterns |
| Effective cost-per-token during a CPU saturation cascade commonly rises 1.5-2.5x versus baseline, with GPU spend unchanged but useful throughput reduced | Typical range observed during incident postmortems |

## Mitigations
1. **Right-size CPU:GPU ratio for actual workload**: Benchmark CPU cost of tokenization and sampling against the real prompt-length and sampling-configuration distribution, not an average-case assumption, and provision CPU cores per node accordingly.
2. **Isolate health checks from the request-serving CPU pool**: Run health-check handlers on a reserved CPU core or separate lightweight process so they don't get starved by the same saturation they're meant to detect, avoiding false-unhealthy marks that trigger cascading reroutes.
3. **Offload CPU-heavy sampling to the GPU where possible**: Use serving-engine features that implement top-k/top-p filtering and repetition penalties as GPU kernels rather than CPU post-processing, reducing the CPU-bound share of the request path.
4. **Per-node concurrency caps tied to CPU headroom, not just GPU capacity**: Cap concurrent requests admitted per node based on observed CPU utilization, not solely GPU memory/utilization, so a node stops accepting new work before its CPU saturates.
5. **Gradual, capped traffic redistribution on node degradation**: Configure the load balancer to shed a saturated node's traffic gradually and cap how much extra load any single peer absorbs, rather than an all-at-once reroute that can saturate the next node in one step.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| cpu_gpu_utilization_ratio | Node CPU utilization divided by node GPU utilization | Alert if ratio inverts (CPU > GPU) sustained for 5 minutes |
| health_check_latency_p99 | p99 latency of the load balancer's health-check probe per node | Alert if > 3x baseline |
| fleet_saturated_node_count | Count of nodes currently at or above 90% CPU utilization | Alert if count increases by 2+ within a 10-minute window |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| CPU/GPU utilization inversion | cpu_gpu_utilization_ratio inverts on any node for 5+ minutes | Medium | Investigate request mix (prompt length, sampling config) driving CPU load on that node |
| Cascading saturation detected | fleet_saturated_node_count grows across 3+ nodes within 15 minutes | High | Page on-call, cap per-node concurrency fleet-wide, review recent traffic mix changes |

## Related Patterns
- [Concurrent Request Resource Explosion](./concurrent-request-resource-explosion.md) - a burst in concurrency can be the trigger event that pushes the first node into CPU saturation
- [Network Bandwidth Saturation](./network-bandwidth-saturation.md) - a parallel infrastructure-exhaustion mechanism where a different resource cascades into inference degradation
- [Throughput Per Dollar Optimization Failure](./throughput-per-dollar-optimization-failure.md) - the fleet-wide cost-per-token increase during a CPU cascade is a direct instance of this broader economic failure
