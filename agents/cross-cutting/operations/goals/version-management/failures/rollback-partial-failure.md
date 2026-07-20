# Rollback Partial Failure

## Issue
An emergency rollback of an agent service is triggered to undo a bad release, but the rollback itself fails to complete across the whole fleet — some instances revert to the prior version successfully while others fail to redeploy, get stuck mid-restart, or silently keep running the bad version because the rollback pipeline hit an error partway through and stopped without either finishing or reverting its own progress. The system ends up in a worse state than before the rollback started: a mixed fleet running both the broken version and the reverted version simultaneously, with no clear record of which instances are in which state, during what is already an active incident.

**Frequency**: Occasional

**Symptoms**
- Rollback pipeline reports a failure or timeout partway through, with no automatic retry or completion
- Version-distribution dashboard shows three states instead of two during an active rollback: old-broken, new-broken (pre-rollback), and reverted, in unpredictable proportions
- The specific symptom the rollback was meant to fix continues for a subset of traffic even though the rollback was "triggered"
- On-call has to manually enumerate instance-by-instance state to figure out what actually happened, extending incident duration
- A second, uncoordinated rollback attempt is triggered on top of the first partial one, compounding the inconsistency

## Root Cause
Rollback is often implemented as the same rolling-update mechanism used for forward deploys — replace instances in batches, waiting for each batch to report healthy before proceeding — which assumes a calm, non-incident context where transient batch failures can be retried at leisure. During an active incident, the underlying cause of instability (the reason the rollback was triggered in the first place) is often still actively degrading the environment: capacity is constrained, dependent services are also unhealthy, or the same infrastructure issue that caused the original problem interferes with the rollback's own health checks. A rolling rollback that fails a health check on batch 3 of 10 typically just halts, because the pipeline has no special-cased "this is an emergency rollback, prioritize completing over careful health verification" mode — it applies the same cautious, pausable logic that's appropriate for a routine deploy but actively harmful when the goal is to get off a known-bad version as fast as possible.

## Example
```
"AgentRouter" fleet (80 instances) is on v27, which has a memory
leak causing OOM kills under sustained load. On-call triggers an
emergency rollback to v26 via the standard rolling-update pipeline:
10% batches, wait for each batch to pass health checks before
proceeding to the next.

Batch 1 (8 instances): rollback succeeds, instances healthy on v26.
Batch 2 (8 instances): rollback succeeds.
Batch 3 (8 instances): the underlying memory pressure from v27's
leak (still running on the remaining 64 instances) has pushed
cluster-wide node memory utilization high enough that new v26 pods
in this batch fail to schedule - insufficient allocatable memory on
available nodes. The batch fails its readiness check after a 5-minute
timeout. The pipeline halts, per its default "pause on batch
failure" behavior, waiting for manual intervention.

Result: 16 instances on v26, 64 instances still on the leaking v27,
and the rollback pipeline sitting paused rather than either
completing or retrying. On-call, focused on capacity issues, doesn't
notice the pipeline is paused (not failed - no alert fired) for
another 25 minutes, during which the leak continues degrading the
64 v27 instances further.
```

## Statistics
| Finding | Context |
|---------|---------|
| A meaningful share of emergency rollbacks under active incident conditions fail to complete without manual intervention | Estimated from post-incident reviews of emergency rollback events |
| Rollback pipelines that default to "pause on failure" (versus "retry aggressively" or "alert loudly") are more likely to leave a fleet in a stuck mixed state for an extended period | Typical pattern reported across teams using generic rolling-update tooling for rollback |
| Dedicated emergency-rollback pipelines (as opposed to reusing the forward-deploy pipeline) complete successfully at a meaningfully higher rate under incident conditions | Reported range across teams that built a distinct fast-rollback path |

## Mitigations
1. **Dedicated emergency rollback pipeline**: Build a separate, simpler rollback path optimized for speed and completion under degraded conditions (e.g., larger batch sizes, relaxed health-check strictness, aggressive retry) rather than reusing the cautious forward-deploy pipeline.
2. **Loud alerting on stalled rollback**: Ensure a paused or stalled rollback pipeline pages on-call immediately and prominently — a stuck rollback during an active incident is itself a high-severity event, not a background pipeline status.
3. **Capacity headroom reserved for rollback**: Maintain enough spare cluster capacity that a rollback isn't competing for scheduling room with the still-running bad version, especially when the bad version's own failure mode (like a memory leak) is consuming resources.
4. **Idempotent, resumable rollback execution**: Design the rollback mechanism so it can be safely re-triggered or resumed from wherever it stopped, rather than requiring a full restart or manual cleanup of partial state before retrying.
5. **Rollback completion verification, not just initiation**: Track and explicitly confirm 100% fleet reversion as the definition of "rollback complete," and treat anything less as an ongoing incident state requiring active response, rather than considering the rollback done once it's been triggered.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| rollback_completion_percentage | Share of target fleet successfully reverted since a rollback was triggered | Alert if stalled below 100% for more than 5 minutes |
| mixed_version_fleet_duration | Time spent with more than one version live during an active rollback | Alert if > 10 minutes during an emergency rollback |
| rollback_pipeline_pause_events | Count of rollback pipeline executions that halted on a batch failure | Alert on any occurrence during an emergency rollback |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Rollback stalled mid-fleet | rollback_completion_percentage stops progressing before reaching 100% | High | Page on-call immediately, investigate blocking batch failure, manually force completion or retry |
| Rollback capacity contention | Rollback batch failures correlate with cluster resource pressure from the still-running bad version | High | Free capacity (scale cluster or forcibly terminate excess bad-version instances), retry rollback |

## Related Patterns
- [Rollback Data Consistency](./rollback-data-consistency.md) - both concern rollback leaving the system in a worse state, one via data shape mismatch and one via incomplete execution
- [Connection Draining Incomplete](./connection-draining-incomplete.md) - a stalled rollback often compounds with forced termination of in-flight sessions on the instances stuck mid-transition
- [Deployment Validation Skipped](./deployment-validation-skipped.md) - skipped validation is a common trigger for the bad release that then requires a rollback in the first place
