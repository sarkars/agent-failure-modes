# Recovery Procedure Untested

## Issue
A documented recovery or disaster-recovery procedure exists — a runbook, an automated failover script, a restore-from-backup process — but has never actually been executed end-to-end against a real or realistic failure. When a real failure finally occurs and the procedure is invoked for the first time, it fails: a step references infrastructure that no longer exists, a credential has expired, a script depends on a manual precondition nobody remembers to satisfy, or the procedure simply takes far longer than anyone expected because nobody had a real timing baseline. The defining feature of this pattern is that the failure is discovered at the worst possible time — during an actual outage — rather than during a drill.

**Frequency**: Common

**Symptoms**
- The recovery runbook was last executed (even in a drill) longer ago than any reasonable staleness window, or has never been executed at all since it was written
- The procedure references specific hostnames, credentials, IAM roles, or infrastructure that has since been renamed, rotated, decommissioned, or migrated
- During the real incident, engineers discover mid-procedure that a prerequisite step (a permission grant, a config value, a manual approval workflow) isn't where the documentation says it is
- Actual recovery time during the real incident wildly exceeds any previously-stated estimate, because the estimate was never empirically measured
- The runbook's author or primary maintainer has left the team, and no one currently on-call has ever run it

## Root Cause
Recovery procedures are typically written once, during initial system design or immediately after a prior incident, and then left largely unmaintained because running them has a real cost (time, risk of disrupting production if the drill isn't suffiently isolated) and no natural forcing function requires re-running them regularly. Meanwhile the surrounding infrastructure keeps changing — credentials rotate, IAM policies tighten, services get renamed or migrated to new hosting, dependencies get replaced — and none of these changes are cross-checked against the dormant runbook, because nothing in the normal change-management process touches it. The runbook silently drifts out of sync with reality, and because it's only ever needed during an actual emergency, the drift is invisible until the worst possible moment reveals it.

## Example
```
Runbook: "DR-07: Restore Primary Database from Cross-Region Backup,"
last verified via drill 14 months ago. Since that drill:

- The backup storage bucket was migrated from a legacy AWS account to
  a new consolidated account as part of an unrelated cost-optimization
  project 9 months ago. The runbook still references the old bucket
  ARN.
- The IAM role the restore script assumes (DR-Restore-Role) had its
  trust policy tightened 5 months ago as part of a security audit,
  and no longer permits assumption from the on-call engineer's current
  federated identity group (the group was renamed during an SSO
  migration).
- The restore script itself was last tested against a database roughly
  1/3 the current size; nobody has validated how long restore actually
  takes at current data volume.

02:14:00 - Primary database suffers unrecoverable corruption. On-call
           engineer, following DR-07 for the first time in a real
           incident, runs step 3: "assume DR-Restore-Role." Access
           denied — the trust policy no longer permits it.

02:22:00 - After escalating to a second engineer with broader IAM
           permissions, the role is assumed manually (bypassing the
           documented automated step). Step 5 references the legacy
           bucket ARN, which returns "bucket does not exist." 20
           minutes lost tracing the bucket's actual current location
           through Slack history and tribal knowledge.

02:55:00 - Restore finally begins from the correct bucket. It takes
           3 hours 40 minutes — the runbook's stated estimate was
           "approximately 45 minutes," based on the 14-month-old
           smaller dataset, never updated.

06:35:00 - Recovery completes, roughly 4 hours after the original
           failure, against a runbook whose documented steps and time
           estimate bore little resemblance to what the incident
           actually required.
```

## Statistics
| Finding | Context |
|---------|---------|
| A significant share of documented recovery/DR runbooks have not been executed, even in drill form, within the prior 12 months | Typical range observed in DR-readiness audits |
| Real-incident execution of an untested runbook commonly takes several times longer than the runbook's stated time estimate | Typical range observed comparing drilled vs. never-drilled recovery durations |
| Organizations that run quarterly recovery drills report substantially fewer runbook-blocking surprises during real incidents than those that drill annually or never | Reported range across DR-maturity self-assessments |

## Mitigations
1. **Scheduled, mandatory recovery drills**: Require every critical recovery procedure to be executed end-to-end (in an isolated environment if production disruption risk is a concern) on a fixed cadence, e.g. quarterly, with no exceptions for "we're too busy this quarter."
2. **Runbook staleness tracking as a first-class metric**: Track and surface, for every documented recovery procedure, the time since it was last successfully executed, and treat procedures past a staleness threshold as a known risk requiring remediation, not just documentation debt.
3. **Change-management cross-check for DR-referenced infrastructure**: When infrastructure referenced by a recovery runbook changes (credentials rotated, resources renamed/migrated, IAM policies updated), require an explicit check of whether any dormant runbook references the old configuration.
4. **Drill in conditions resembling a real incident**: Run drills with the actual on-call rotation, actual current credentials, and actual current infrastructure, not with the original author using privileged access that a real on-call engineer wouldn't have.
5. **Update time estimates from measured drill data**: Replace estimated recovery-time figures in runbooks with figures actually measured during the most recent drill, and re-measure whenever data volume or architecture changes materially.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| runbook_last_execution_age | Time since a given recovery procedure was last successfully executed (drill or real) | Alert if > defined staleness threshold (e.g. 90 days) |
| runbook_infrastructure_drift_count | Count of infrastructure changes affecting resources referenced by a dormant runbook since its last execution | Alert if > 0 |
| drill_vs_documented_time_variance | Difference between actual drill execution time and the runbook's documented estimate | Alert if variance exceeds a defined percentage |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Runbook overdue for drill | runbook_last_execution_age exceeds staleness threshold | Medium | Schedule a drill before the next audit cycle, flag as at-risk in DR readiness reporting |
| Infrastructure drift affecting dormant runbook | A change-management event touches a resource referenced by an unexecuted-in-90-days runbook | High | Require runbook update and re-verification before the change is considered complete |

## Related Patterns
- [Recovery Time Objective Miss](./recovery-time-objective-miss.md) - an untested procedure's real execution time is frequently the direct cause of an RTO miss
- [Recovery Point Objective Miss](./recovery-point-objective-miss.md) - untested procedures also commonly fail to deliver their assumed data-loss bound, not just their assumed timing
- [Failover Delay Too Long](./failover-delay-too-long.md) - untested procedures are one of the primary root causes behind failover taking longer than expected in a real incident
