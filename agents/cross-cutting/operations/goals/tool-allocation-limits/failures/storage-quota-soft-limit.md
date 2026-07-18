# Storage Quota Soft Limit

## Issue
A storage tool enforces a soft limit below its hard quota ceiling — triggering throttled write speeds, forced read-only mode, or reduced replication guarantees once usage crosses a threshold like 85% of provisioned capacity. The agent has no logic to detect this intermediate degraded state; it only recognizes "working" versus "hard error," so when writes start silently slowing down or getting rejected in read-only mode, the agent misattributes the behavior to a bug in the tool, a network issue, or its own code, rather than recognizing an approaching-capacity condition it could act on.

**Frequency**: Occasional

**Symptoms**
- Write latency gradually increases over days/weeks with no corresponding change in payload size or request volume
- Writes begin failing with errors that don't mention quota or capacity (e.g., "read-only filesystem", "operation not permitted") even though the account is technically still under its hard quota
- The degraded behavior resolves itself after data is deleted or archived, even though no code changed
- Retrying failed writes sometimes succeeds intermittently, consistent with throttling rather than a hard block
- Monitoring shows the account has "quota available" per the hard-limit dashboard, contradicting the write failures being observed

## Root Cause
Storage vendors often implement a two-tier enforcement model: a soft threshold that triggers protective degraded behavior (throttling, read-only mode, reduced durability) to prevent accounts from crashing into the hard ceiling, and the hard ceiling itself which rejects writes outright. This soft-limit behavior is frequently underdocumented compared to the hard limit, and the errors it produces are often generic filesystem- or protocol-level errors rather than quota-specific ones, because the degraded mode is implemented at a different layer (e.g., the storage backend) than the quota-accounting system that would produce a clear "approaching quota" error. Agents built against the documented hard-quota API don't know a soft-limit state exists, so they have no branch of logic for it.

## Example
```
1. An agent stores generated report artifacts in a managed file-storage tool provisioned
   with a 1 TB quota. The vendor's (underdocumented) soft limit kicks in at 90% utilization,
   switching the volume to read-only for new large files while still allowing small metadata
   writes.
2. Usage grows steadily from batch report generation, crossing 900 GB (90%) on a Tuesday.
3. Wednesday's batch job attempts to write a 2 GB report artifact; the write fails with
   "EROFS: read-only file system" — a generic POSIX-style error with no mention of quota.
4. The on-call engineer checks the vendor's billing dashboard, which shows "900 GB / 1 TB
   used, hard limit not reached" and concludes the storage tool itself is broken.
5. Two hours are spent restarting the storage mount and filing a vendor support ticket
   before a vendor support engineer explains the undocumented 90% soft-limit read-only
   behavior.
6. The immediate fix (deleting 150 GB of old artifacts) resolves the issue instantly,
   confirming it was capacity-related all along.
```

## Statistics
| Finding | Context |
|---------|---------|
| Soft-limit degraded-mode behavior is frequently underdocumented or entirely undocumented by storage vendors, contributing to longer diagnosis times, often observed as 2-5x longer than hard-limit failures | Because the error class doesn't match the actual cause |
| Typical soft-limit thresholds observed in production storage tools cluster around 85-95% of hard quota | Reasonable vendor-side buffer to avoid crashing into the hard ceiling |
| Proactively monitoring utilization percentage (rather than relying on write-failure signals) reduces soft-limit-related incidents by a large majority, commonly estimated at 70%+ | By acting before the threshold rather than reacting after |

## Mitigations
1. **Monitor utilization percentage directly, not just write success**: Poll actual usage against the hard quota on a schedule and treat crossing 80-85% as an actionable signal, independent of whether writes are currently failing.
2. **Research and document vendor-specific soft-limit thresholds**: Since these are often underdocumented, proactively test or contact vendor support to learn the actual soft-limit percentage and resulting degraded behavior, and encode that knowledge into the agent's error-handling logic.
3. **Classify ambiguous storage errors against current utilization**: When a write fails with a generic filesystem-level error (read-only, permission denied) and utilization is above 80%, treat capacity as the likely cause before investigating other hypotheses.
4. **Automated cleanup triggers at the soft threshold**: Configure retention/archival jobs to run automatically once utilization crosses the known soft-limit threshold, keeping usage below the degraded-mode boundary proactively.
5. **Alert on latency/throughput degradation, not just errors**: Track write latency trends as a leading indicator, since throttling often precedes outright read-only failures.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `storage.utilization_pct` | Current usage divided by hard quota | Alert at 80%, treat 90%+ as likely soft-limit degraded mode |
| `storage.write_latency_p95_ms` | P95 write latency trend, as a leading indicator of throttling | Alert when p95 exceeds 2x the trailing 30-day baseline |
| `storage.generic_fs_error_rate` | Rate of generic (non-quota-labeled) filesystem errors like read-only or permission-denied | Alert on any sustained increase while utilization is above 80% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Approaching known soft-limit threshold | `utilization_pct` crosses 80% | Medium | Trigger cleanup/archival job proactively before degraded mode engages |
| Generic filesystem errors correlated with high utilization | `generic_fs_error_rate` rises while `utilization_pct` > 85% | High | Treat as soft-limit degraded mode, not a tool bug; free space immediately |

## Related Patterns
- [Storage Quota Exceeded](./storage-quota-exceeded.md) - the hard-limit counterpart this soft limit is designed to protect against
- [Storage Quota Shared Across Agents](./storage-quota-shared-across-agents.md) - soft-limit degraded mode can be triggered by a different agent's usage in a shared pool
- [Degraded Sla Not Communicated](../../tool-sla-quality-limits/failures/degraded-sla-not-communicated.md) - same "silent degraded state misread as a bug" pattern applied to SLA quality rather than storage capacity
