# Disk Space Exhaustion

## Issue
Inference nodes accumulate disk usage from request/response logs, prompt-cache and KV-cache spill files, downloaded model checkpoints (including duplicate versions kept for rollback), and container image layers. When disk fills up, the failure isn't graceful — model loading fails for new deployments, log writes start silently failing or blocking, and in some serving stacks the engine crashes outright — taking healthy GPU capacity offline and forcing traffic onto fewer nodes, which raises effective cost-per-token even though the root cause has nothing to do with compute pricing.

**Frequency**: Occasional

**Symptoms**
- Node health checks fail with "no space left on device" errors despite GPU and CPU metrics looking normal
- New model deployments or autoscaled replicas fail to start because the checkpoint download can't complete
- Request logs or trace exports show gaps corresponding to periods when the log-writing disk was full
- Disk usage graphs show a slow, steady climb over days/weeks followed by a sharp cliff (node crash or eviction) rather than a sudden spike
- Cost-per-successful-request rises because a fraction of the fleet is offline or degraded while GPU billing for those nodes continues (in reserved/committed capacity) or replacement nodes are provisioned redundantly

## Root Cause
Model artifacts, prompt/KV-cache spill-to-disk mechanisms, and verbose request/response logging are all designed for correctness and debuggability, not disk-budget awareness, so none of them self-limit by default. Model registries commonly keep every previously deployed checkpoint version for rollback safety, and each large language model checkpoint can be tens of gigabytes; without an explicit retention policy, disk usage grows monotonically with every deployment. Serving engines that spill KV-cache to disk under memory pressure (to avoid OOM-killing requests) treat disk as a safety valve, but that valve has no back-pressure of its own — it fills silently until the disk itself is the constraint. Logging pipelines default to verbose modes during initial rollout and are rarely revisited once the team has moved on to the next launch, so log volume grows with traffic and is rarely pruned or rotated aggressively enough to keep pace. Because none of these subsystems coordinate on a shared disk budget, exhaustion is a slow accumulation across independent unmanaged growth sources that only becomes visible when the node stops working entirely.

## Example
```
An inference fleet running a customer-support agent logs full request and
response payloads (including retrieved context chunks, which can be
several KB each) to local disk before an async job ships them to
long-term storage every 6 hours. The team also keeps the last 5 model
checkpoint versions on each node's local SSD (180GB each) to support
fast rollback.

Over 3 weeks, traffic grows 40% following a product launch, increasing
log volume proportionally. The async log-shipping job, sized for the
original traffic level, starts falling behind and its backlog grows
faster than it drains. Combined with the 900GB of retained checkpoints,
available disk on each 1TB node SSD drops below 5%.

A routine deployment triggers a 6th checkpoint download. It fails midway
with "no space left on device." The deployment rolls back automatically,
but the partially-downloaded checkpoint file isn't cleaned up, consuming
another 60GB. Three nodes cross 100% disk usage over the next 2 hours;
the serving process on each crashes when it can't write its log buffer.

The fleet loses 3 of 20 nodes (15% of capacity) for the 90 minutes it
takes an on-call engineer to diagnose and manually clear old checkpoints
and log backlogs. Remaining nodes absorb the redirected traffic at
higher utilization, and 2 autoscaled replacement nodes are provisioned
unnecessarily before the root cause is found, adding avoidable GPU-hour
cost on top of the capacity already lost.
```

## Statistics
| Finding | Context |
|---------|---------|
| Retained model checkpoint versions without an eviction policy commonly consume 30-50% of local inference-node disk within weeks of frequent deployment cycles | Typical range observed in fast-iterating serving environments |
| Disk-exhaustion-triggered node failures typically take 30-90 minutes to diagnose and resolve when no dedicated disk-usage alerting exists | Estimated range from operational incident response times |
| Fleet capacity loss during a disk-exhaustion incident is commonly 5-20% of nodes, depending on how uniformly the growth sources (logs, checkpoints, cache spill) are distributed across the fleet | Typical range across multi-node inference deployments |

## Mitigations
1. **Automated checkpoint retention policy**: Cap the number of model checkpoint versions retained locally per node (e.g. last 2), with older versions pulled from remote storage on-demand for the rare rollback, instead of keeping every version resident.
2. **Disk-usage-aware autoscaling and health checks**: Add disk usage as an explicit health-check dimension so nodes approaching a disk threshold are proactively drained and marked unhealthy before they crash mid-request, rather than failing ungracefully.
3. **Bounded, rotating log storage with backpressure-aware shipping**: Size the log-shipping pipeline's throughput against realistic peak traffic with headroom, and configure local log retention with hard caps and rotation so a shipping backlog degrades log completeness gracefully instead of consuming unbounded disk.
4. **Cache-spill quotas with eviction, not unbounded growth**: Configure KV-cache/prompt-cache disk-spill mechanisms with an explicit disk quota and LRU eviction, so spill degrades cache hit rate under pressure rather than growing until the disk is full.
5. **Proactive disk-usage monitoring with trend alerting**: Alert on the rate of disk-usage growth over days, not just the absolute threshold, so a slow accumulation is caught and remediated before it reaches the crisis point that takes nodes offline.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| disk_usage_percent | Percentage of local disk used per inference node | Alert if > 80%, page if > 92% |
| disk_usage_growth_rate_daily | Change in disk usage percent per day, rolling average | Alert if trend projects threshold breach within 72 hours |
| checkpoint_versions_retained | Count of model checkpoint versions currently stored locally per node | Alert if exceeds configured retention policy |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Disk usage critical | disk_usage_percent exceeds 92% on any inference node | High | Page on-call, drain node from load balancer, clear old checkpoints/log backlog |
| Disk growth trending toward exhaustion | disk_usage_growth_rate_daily projects a threshold breach within 72 hours | Medium | Investigate growth source (logs, checkpoints, cache spill), schedule proactive cleanup |

## Related Patterns
- [Resource Leak](./resource-leak.md) - shares the slow-accumulation-until-crisis mechanism, but for memory/connections rather than disk
- [Concurrent Request Resource Explosion](./concurrent-request-resource-explosion.md) - a burst-driven capacity loss that can compound with disk exhaustion if log volume spikes alongside request volume
- [Resource Quota Overcommit](./resource-quota-overcommit.md) - both describe infrastructure limits reached through unmanaged growth rather than deliberate provisioning decisions
