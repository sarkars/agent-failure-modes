# Storage Quota Exceeded

## Issue
An agent writes data through a tool — uploading files, storing generated embeddings, persisting logs or artifacts — and the underlying account or bucket has a fixed storage quota that the agent has no visibility into until it's already been exceeded. The write fails at the moment of the overage, often mid-batch, with no prior warning that the quota was approaching, leaving the agent with a partially-written dataset and no clean way to know which records succeeded.

**Frequency**: Very Common

**Symptoms**
- Writes that succeeded reliably for weeks suddenly start failing with "quota exceeded" or "insufficient storage" errors
- Failures cluster in the middle of a batch operation, leaving some records written and others not, with no transactional rollback
- No warning or degraded-mode signal preceded the failure — it goes from fully working to fully blocked
- Retrying the identical write fails identically since the underlying quota condition hasn't changed
- Downstream consumers of the storage (search indexes, retrieval pipelines) show gaps corresponding to the failed writes

## Root Cause
Storage quotas are typically enforced as a hard account-level or bucket-level ceiling with no proactive push notification to API consumers — the tool only reports the condition reactively, as an error on the write call that crosses the line. Agents that treat storage as an unbounded sink (a common assumption when a tool has historically had "enough" capacity) have no logic to check remaining capacity before writing, and most tool APIs don't offer a lightweight "how much quota do I have left" check that's cheap enough to call before every write. The result is that the first signal of a capacity problem is a failed write, not a warning.

## Example
```
1. An agent generates and stores document embeddings in a vector-store tool's namespace,
   which has a provisioned storage quota of 50 GB.
2. Over several weeks of steady ingestion, usage climbs from 10 GB to 49.6 GB without
   any alert being configured on the account.
3. A batch job processes 10,000 new documents in one run, writing embeddings in batches
   of 500.
4. The first 18 batches (9,000 documents) write successfully, pushing usage past 50 GB
   partway through batch 19.
5. Batch 19's write call fails with "403 storage quota exceeded"; the agent's batch loop
   has no per-record rollback, so 250 of the 500 records in that batch are written and
   250 are not, with no marker distinguishing which.
6. The remaining 1,000 documents in batches 20 and beyond never get attempted.
7. Two days later, a search-quality regression is traced back to the missing embeddings,
   and reconciling exactly which documents are missing takes longer than the original job.
```

## Statistics
| Finding | Context |
|---------|---------|
| Storage-quota-exceeded failures are frequently first noticed via a downstream symptom (missing data, search gaps) rather than the write-time error itself, in an estimated 30-50% of incidents | Consistent with alerts not being wired to the write-path error |
| Batch jobs without per-record idempotency/checkpointing take 2-5x longer to recover from a mid-batch quota failure than checkpointed jobs | Because the full batch must be re-diffed against what actually persisted |
| Proactive quota-usage monitoring (polling remaining capacity before large writes) has been observed to prevent the large majority of mid-batch quota failures | By deferring or chunking writes before the hard ceiling is hit |

## Mitigations
1. **Proactive quota monitoring**: Poll the tool's usage/quota-status endpoint (where available) on a schedule, and alert well before the ceiling — e.g., at 80% utilization — rather than waiting for a write to fail.
2. **Idempotent, checkpointed batch writes**: Track per-record write status so a mid-batch quota failure leaves a clear, resumable boundary instead of an ambiguous partial state.
3. **Pre-write size estimation**: Estimate the storage footprint of a pending batch (record count times average size) against known remaining quota before starting the batch, and defer or split if it would exceed capacity.
4. **Automatic quota expansion or overflow routing**: Where the tool supports it, configure auto-scaling storage tiers or route overflow writes to a secondary namespace/bucket rather than failing outright.
5. **Retention and cleanup policies**: Implement TTL or archival rules on the stored data so stale records are pruned automatically, preventing quota exhaustion from being a one-way ratchet.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `storage.quota_utilization_pct` | Current storage usage divided by provisioned quota | Alert at 80%, page at 95% |
| `batch_write.partial_failure_count` | Count of batch write operations that failed partway through, leaving mixed success/failure state | Alert on any occurrence |
| `storage.days_to_exhaustion` | Projected days until quota exhaustion based on trailing 7-day growth rate | Alert when projection falls below 7 days |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Storage quota near exhaustion | `quota_utilization_pct` > 90% | High | Pause non-critical write jobs, request quota increase or trigger cleanup policy |
| Mid-batch write failure due to quota | Write batch fails with quota-exceeded error and partial success | High | Halt remaining batches, reconcile which records persisted before resuming |

## Related Patterns
- [Storage Quota Shared Across Agents](./storage-quota-shared-across-agents.md) - same failure mode compounded by multiple consumers drawing from one pool
- [Storage Quota Soft Limit](./storage-quota-soft-limit.md) - the degraded-mode-before-hard-failure variant of this same quota category
- [Memory Quota Per Operation](./memory-quota-per-operation.md) - related resource-ceiling failure at the per-operation rather than persistent-storage level
