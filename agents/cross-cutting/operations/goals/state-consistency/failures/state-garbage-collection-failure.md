# State Garbage Collection Failure

## Issue
An agent system accumulates state — completed task records, expired session memory, superseded conversation checkpoints, orphaned lock entries — that should be cleaned up once it's no longer needed, but the cleanup process (a TTL expiry, a reference-counted collector, a scheduled sweep) fails to run, fails silently, or falls behind the rate of new state creation. The stale state isn't just inert; it keeps being scanned, indexed, and loaded, degrading query latency and eventually memory or storage capacity.

**Frequency**: Occasional

**Symptoms**
- Steady, monotonic growth in state-store size or record count with no corresponding growth in active workload
- Query and lookup latency against the state store degrades gradually over days or weeks, not suddenly
- A disproportionate share of stored records have status fields indicating "completed," "expired," or "superseded" but remain queryable
- Restarting or manually running the cleanup job recovers a large fraction of capacity, confirming the automated path had stalled
- Memory or disk alerts fire eventually, but with a long, easily-missed lead-up rather than a sharp spike

## Root Cause
Garbage collection for agent state is usually a background process decoupled from the main read/write path — a cron job, a TTL index, a mark-and-sweep pass — specifically so it doesn't add latency to live requests. That decoupling means its failure mode is also decoupled: if the sweep job crashes, gets misconfigured, loses its schedule, or simply can't keep pace with a spike in state-creation rate, nothing in the live request path notices, because live requests were never depending on collection having happened. Reference-counting schemes have a parallel failure mode: an agent that creates a reference to shared state (e.g. a memory checkpoint two conversation branches point to) but crashes or times out before decrementing the count on the abandoned branch leaves that state permanently un-collectible, since the collector correctly sees a nonzero reference count.

## Example
```
A multi-agent research system checkpoints intermediate reasoning state
to a shared store every time an agent branches into a sub-task, so a
parent agent can resume if a sub-task fails. Checkpoints are supposed
to be garbage-collected 24 hours after the parent task completes, via
a nightly sweep job that deletes checkpoints past their TTL.

Week 1: sweep job runs nightly, deletes ~40,000 expired checkpoints/day,
        store size stable around 300K records.

Week 2: a config change adds a new checkpoint field; the sweep job's
        deserializer throws on records containing the new field and
        the job's error handling silently catches and skips the whole
        run instead of failing loudly.

Week 2-6: sweep job "succeeds" (exits 0, having caught its own
        exception) but deletes 0 records every night. Store grows by
        ~40,000 records/day.

Week 6: store has grown to 1.7M records. Checkpoint lookup queries,
        which scan by parent-task ID, have gone from 15ms p50 to
        800ms p50. Sub-task resume latency becomes a leading complaint
        in support tickets before anyone traces it to the sweep job.
```

## Statistics
| Finding | Context |
|---------|---------|
| 20-35% of state-store performance-degradation incidents trace back to a stalled or silently-failing garbage collection job rather than genuine load growth | Typical range observed in production agent telemetry |
| Reference-counted collectors in multi-agent branching systems leak an estimated 2-10% of created references due to abandoned/crashed branches never decrementing | Estimated from systems with branch-and-merge agent architectures |
| Adding store-size growth-rate alerting catches GC failures a median of 5-10 days earlier than waiting for latency or capacity alerts | Reported range across teams that added dedicated GC health monitoring |

## Mitigations
1. **GC job health as a first-class metric**: Monitor and alert on the collector's own success (records deleted per run, run duration, exceptions caught) independent of downstream capacity or latency symptoms, so a silently-failing sweep is caught immediately.
2. **Fail loud, not quiet**: Ensure the collection job propagates exceptions and fails its run/exits nonzero on unexpected errors rather than catching and swallowing them, so job-scheduler alerting catches the failure the same night it happens.
3. **Reference-count timeouts with forced release**: For reference-counted state, attach an absolute maximum lifetime independent of reference count, so an abandoned reference from a crashed branch can't keep state alive forever.
4. **Store-size growth-rate alerting**: Alert on the rate of state-store growth relative to workload volume, not just absolute size, since a stalled collector shows up as a rate anomaly well before it shows up as a capacity or latency problem.
5. **Idempotent, resumable sweeps**: Design the collection job so a partial or interrupted run can safely resume where it left off rather than needing a clean full pass, reducing the chance that transient errors cause the job to skip an entire cycle.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| gc_records_deleted_per_run | Count of records removed by the most recent collection run | Alert if 0 for 2+ consecutive scheduled runs |
| state_store_growth_rate | Net growth rate of the state store, normalized against active workload volume | Alert if sustained growth with flat/declining workload |
| gc_job_error_rate | Rate of exceptions or non-zero exits from the collection job | Alert if > 0 |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Collection job produced zero deletions | gc_records_deleted_per_run is 0 across consecutive scheduled runs while expired-eligible records exist | High | Page on-call, inspect job logs for silently-caught exceptions, run manual sweep |
| Unbounded store growth | state_store_growth_rate exceeds baseline for 3+ days with no matching workload increase | Medium | Audit collector configuration and reference-count logic, check for abandoned branches |

## Related Patterns
- [State Version Incompatibility](./state-version-incompatibility.md) - a schema change can be exactly what silently breaks the collector's deserializer, as in the worked example above
- [State Replication Lag](./state-replication-lag.md) - both describe background maintenance processes whose failure is invisible from the live request path
- [State Consistency Timeout](./state-consistency-timeout.md) - shares the pattern of a background safeguard failing quietly and only surfacing as a downstream symptom later
