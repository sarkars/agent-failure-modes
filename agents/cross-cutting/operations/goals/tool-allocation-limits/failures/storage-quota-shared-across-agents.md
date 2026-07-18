# Storage Quota Shared Across Agents

## Issue
Multiple instances of an agent (or multiple distinct agents in a fleet) write to the same pooled storage quota — a shared object store bucket, a shared vector database namespace, a shared scratch volume. One agent instance with an unusually heavy workload (large file uploads, verbose logging, an unbounded caching pattern) can silently consume the entire pool, causing unrelated agent instances to fail their own writes with no indication that another agent, not their own behavior, caused the exhaustion.

**Frequency**: Common

**Symptoms**
- An agent instance that has changed nothing about its own behavior starts failing writes
- Storage exhaustion correlates in time with a different agent's deployment or workload spike, not the failing agent's own activity
- Multiple unrelated agents report the same "quota exceeded" error simultaneously
- Investigating the failing agent's own write volume shows it's well within historical norms
- Freeing space (deleting another agent's data) immediately unblocks the failing agent with no code change

## Root Cause
Shared storage pools are provisioned at the account, bucket, or namespace level for cost and operational simplicity, but the tool enforcing the quota has no concept of per-agent fair-share allocation — it just tracks aggregate bytes used against one ceiling. When agent instances are deployed independently (different teams, different release cadences, different scaling behavior), none of them individually monitors or is responsible for the shared pool's total usage, so exhaustion is a "tragedy of the commons" that manifests as an unpredictable failure for whichever agent happens to write next after the ceiling is crossed.

## Example
```
1. Three independent agents (a document-summarizer, a customer-support-transcript-analyzer,
   and a nightly-report-generator) all write intermediate artifacts to the same shared
   "agent-scratch" S3 bucket, provisioned with a 500 GB quota shared across the account.
2. The document-summarizer normally uses ~50 GB steady-state and has been stable for months.
3. The transcript-analyzer is redeployed with a bug that fails to clean up temporary
   audio-transcription files, causing its usage to grow from 100 GB to 440 GB over 3 days.
4. On day 4, the document-summarizer's routine write of a 2 GB batch of summaries fails
   with "507 Insufficient Storage" — the bucket is now at 498 GB against its 500 GB quota.
5. The document-summarizer team, seeing no change in their own usage pattern or code,
   spends an hour debugging their own service before checking the shared bucket's total
   usage and discovering the transcript-analyzer's leak.
6. The nightly-report-generator's scheduled job also fails that night for the same reason,
   doubling the incident's blast radius.
```

## Statistics
| Finding | Context |
|---------|---------|
| Shared-storage-pool incidents typically take 2-4x longer to root-cause than single-consumer storage issues | Because the responding team must first rule out their own service before looking at neighbors |
| A single misbehaving consumer (leak, missing cleanup, retry storm) accounts for the majority of shared-pool exhaustion incidents, commonly cited around 70-80% | Consistent with pooled-resource "noisy neighbor" patterns generally |
| Namespace or prefix-level per-agent quotas, where supported, reduce cross-agent exhaustion incidents by a large majority (often cited 80%+) | By converting a shared failure mode into an isolated one |

## Mitigations
1. **Per-agent namespace or prefix quotas**: Where the storage tool supports sub-quotas (per-prefix, per-namespace, per-bucket), allocate each agent instance its own bounded allocation instead of one shared pool.
2. **Aggregate usage dashboards with per-consumer breakdown**: Instrument the shared pool with tagging (object prefixes, metadata labels) so usage can be attributed per agent, not just tracked in aggregate.
3. **Mandatory TTL/cleanup policies on shared scratch storage**: Enforce lifecycle rules (auto-delete after N days) on any storage pool shared across agents so a single leaking consumer can't accumulate unbounded usage.
4. **Circuit breaker on shared-pool utilization**: Have each agent check aggregate pool utilization before large writes and back off or alert if the shared pool is already near capacity, regardless of the agent's own usage.
5. **Isolate high-risk workloads to dedicated storage**: Route agents with unpredictable or large storage footprints (e.g., anything processing media files) to their own dedicated bucket rather than a pool shared with lightweight agents.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `shared_storage.pool_utilization_pct` | Aggregate usage across all agents sharing the pool, divided by total quota | Alert at 80%, page at 95% |
| `shared_storage.per_agent_usage_delta_24h` | Change in storage usage attributable to each tagged agent over 24 hours | Alert when any single agent's delta exceeds 2x its trailing 7-day average |
| `agent.write_failure_unrelated_to_own_volume` | Write failures on an agent whose own request volume/size is within historical norms | Alert on any occurrence, flag as likely shared-pool exhaustion |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Shared pool near exhaustion | `pool_utilization_pct` > 90% | High | Identify top-growing consumer via per-agent breakdown, throttle or clean up before hard failure |
| Anomalous single-consumer growth | One agent's 24h usage delta exceeds 2x its own baseline | Medium | Investigate for leaked cleanup logic or retry storm in that specific agent |

## Related Patterns
- [Storage Quota Exceeded](./storage-quota-exceeded.md) - the single-consumer version of this same hard-limit failure
- [Storage Quota Soft Limit](./storage-quota-soft-limit.md) - degraded-mode variant that can precede a shared-pool hard exhaustion
- [Api Key Quota Per Account](./api-key-quota-per-account.md) - same "unknown competing consumer" root cause applied to API rate quota instead of storage
