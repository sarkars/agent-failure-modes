# Recovery Partial Failure

## Issue
A recovery operation spanning multiple components or subsystems completes successfully for some of them but not others, leaving the overall system in a mixed state where part of it is back online with fresh, correct state and another part is still down, still on stale state, or stuck mid-recovery. Unlike cascade-divergent-recovery (where every component recovers but into mutually inconsistent states), this pattern is about recovery simply not finishing everywhere — some components never complete recovery at all, and the system limps along in a half-recovered condition, often without anyone noticing because the components that did recover look healthy.

**Frequency**: Common

**Symptoms**
- A recovery runbook or automated recovery job reports "complete" while a subset of affected components remain in a failed, degraded, or pre-recovery state
- Health dashboards show a mix of green and red/unknown status across components that were all affected by the same original incident
- Functionality that depends on the not-yet-recovered component fails or behaves inconsistently, while functionality depending only on recovered components works fine
- The stuck component is discovered days or weeks later, often by an unrelated investigation, rather than by the recovery process itself flagging incompleteness

## Root Cause
Multi-component recovery is often orchestrated as a set of independent recovery tasks (recover the database, recover the cache, recover the message queue, recover each of N regional replicas) launched together but not tracked as a single atomic unit with a shared success/failure gate. If one of those tasks fails, hangs, or is silently skipped (a script error, a permissions issue on one region, a component that was already in a state the recovery script didn't anticipate), the orchestrator or runbook operator may not have explicit visibility into per-task completion, and can end up marking the overall recovery as done based on the tasks that did report success, especially if there's no automated aggregation of task-level results into a single completion gate.

## Example
```
Setup: A distributed caching layer for a personalization agent has 8
regional shards. An incident takes all 8 offline simultaneously due to
a bad config push. The recovery runbook triggers a parallel
"recover-shard" job across all 8 regions.

16:00:00 - Recovery jobs launched in parallel for shards in
           us-east-1, us-east-2, us-west-1, us-west-2, eu-west-1,
           eu-central-1, ap-south-1, ap-southeast-1.

16:04:30 - 7 of 8 shard recovery jobs complete successfully and report
           green. The ap-southeast-1 job fails silently: it hits an IAM
           permission error trying to re-provision a replaced instance,
           logs the error to a file that nobody is tailing, and the job
           process exits with a non-zero code that the orchestration
           script (written to just check "did most jobs finish") does
           not surface as a blocking failure.

16:05:00 - The recovery runbook, driven by a dashboard showing "7/8
           shards healthy, aggregate cache hit rate at 94% of normal,"
           is marked complete by the on-call engineer, who reasonably
           reads 94% as "basically done, will self-heal."

16:05:00 onward - All personalization requests routed to
           ap-southeast-1 users continue being served with cold-cache
           fallback logic (default, non-personalized recommendations)
           indefinitely, since nothing is actively monitoring for "this
           specific shard never came back," only aggregate health.

3 weeks later - A regional product manager for Southeast Asia notices
           personalization engagement metrics have been flat for three
           weeks and escalates, only then triggering investigation that
           finds the never-recovered shard.
```

## Statistics
| Finding | Context |
|---------|---------|
| Multi-component recovery operations that lack an explicit per-component completion gate leave at least one component unrecovered in a meaningful share of incidents | Estimated from postmortem review of multi-region/multi-shard recovery operations |
| Partial recovery incidents are detected significantly later on average than the original incident, since aggregate health metrics can mask a single failed component | Typical range observed comparing original-incident detection time to partial-recovery detection time |
| Adding automated per-component completion verification is reported to cut partial-recovery detection time substantially | Reported range across teams adding recovery completion gates |

## Mitigations
1. **Explicit per-component completion gate**: Require every recovery orchestration to track and report the status of each individual component task, and define "recovery complete" as all components reporting success, not an aggregate health threshold.
2. **Fail loud, not silent, on individual recovery task failure**: Ensure recovery job failures are surfaced as first-class alerts (not just logged to a file), including the specific component and error, rather than allowing the orchestrator to proceed as if nothing happened.
3. **Aggregate-health dashboards paired with component-level detail**: Never let an aggregate metric (94% healthy) stand in for confirmation that every individual affected component recovered; always pair it with an explicit list of any component still outstanding.
4. **Recovery runbook sign-off requires itemized checklist**: Require the operator closing out a multi-component recovery to check off each component by name, not just observe that overall metrics look acceptable.
5. **Automated stale-state detection independent of the recovery process**: Run a periodic, recovery-independent sweep that flags any component whose state age or health has not changed since a known incident window, catching components the recovery process itself missed.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| recovery_task_completion_rate | Fraction of individual component recovery tasks that report success out of all launched | Alert if < 100% |
| stale_component_state_age | Time since a component's state was last confirmed current, independent of overall system health | Alert if exceeds incident window plus buffer |
| aggregate_vs_component_health_gap | Difference between aggregate system health metric and worst individual component health | Alert if gap exceeds defined threshold |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Incomplete multi-component recovery | recovery_task_completion_rate < 100% at runbook close-out | High | Block recovery sign-off, escalate the specific failed component task |
| Long-stale component detected | A component's stale_component_state_age exceeds threshold post-incident | Medium | Trigger independent investigation regardless of aggregate health status |

## Related Patterns
- [Cascade Divergent Recovery](./cascade-divergent-recovery.md) - both are multi-component recovery failures, one is components recovering to inconsistent states, this is some components never recovering at all
- [Recovery Time Objective Miss](./recovery-time-objective-miss.md) - a component stuck in partial recovery is a severe, often silent, form of RTO miss for that component
- [Single Point of Failure](./single-point-of-failure.md) - a component that never recovers can become a de facto single point of failure for functionality that depended on it
