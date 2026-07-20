# Recovery Point Objective Miss

## Issue
The organization has a defined Recovery Point Objective (RPO) — the maximum acceptable amount of data loss measured in time, e.g. "no more than 5 minutes of data may be lost in any failure" — and an actual incident loses more data than that objective allows. This is a measurement-and-commitment failure specifically about the RPO number itself: the system's actual replication/backup cadence, under real failure conditions, produces a larger data-loss window than what was promised to stakeholders, discovered only when a real failure exposes the gap between designed and actual RPO.

**Frequency**: Occasional

**Symptoms**
- Post-incident data-loss analysis shows a loss window larger than the documented RPO for the affected system
- The gap between actual and target RPO correlates with a specific factor never accounted for in the original RPO calculation — backup job runtime, replication lag under load, a batch-oriented backup schedule mismatched to a continuous-operation expectation
- RPO was set based on best-case or average-case replication/backup timing, not worst-case or under-load timing
- Compliance or SLA reporting cites the target RPO as if it were the actual, tested, guaranteed figure, without recent verification

## Root Cause
RPO is a target, not a physical guarantee, and it can only be as good as the underlying replication or backup mechanism's actual behavior under real failure conditions — which is frequently worse than the conditions used to originally justify the number. Common gaps include: backups taken on a fixed schedule (e.g. every 15 minutes) where the RPO was quoted as "15 minutes" without accounting for the fact that a failure occurring right before the next scheduled backup completes means up to a full interval, not half, could be lost; replication that assumes steady-state lag figures which balloon under the exact high-load conditions that often accompany or cause an incident; or an RPO that was set once at system design time and never re-validated as data volume, write rate, or architecture changed. Because RPO misses are inherently discovered after the fact — you only learn your replication couldn't keep its promise once a real failure tests it — organizations rarely have early warning unless they proactively measure actual data-loss exposure on an ongoing basis, not just once at design time.

## Example
```
Documented RPO for the CustomerProfileStore: 5 minutes, based on
async replication configured with what the original design doc
described as "typically sub-second lag."

Reality 18 months later: write volume has grown 4x since the original
design, and replication lag under peak load (which the original
measurement never tested) now regularly reaches 90-120 seconds during
peak hours, though it still shows sub-second lag during the off-peak
hours when the RPO was last spot-checked.

14:00:00 - Primary database suffers a disk failure during peak
           afternoon traffic. Replication lag at the moment of failure,
           per monitoring (which existed but had no alert threshold
           tied to the RPO commitment), was 4 minutes 40 seconds —
           already close to the RPO limit even before accounting for
           the failure detection and failover time itself.

14:00:00 - 14:04:40 - All writes in this window exist only on the now-
           dead primary and are unrecoverable; the standby's last
           replicated state is from 13:55:20.

14:05:00 - Failover completes; standby promoted. Actual data loss
           window: 4 minutes 40 seconds of writes — technically inside
           the 5-minute RPO for THIS incident, but a near-miss that
           reveals the replication lag has quietly grown to consume
           nearly the entire RPO budget under normal peak load, with no
           margin left for the failure-detection and failover-decision
           time that should also count against the RPO clock.

14:30:00 - A second incident 25 minutes later, under even heavier
           load from users retrying failed requests from the first
           incident, sees replication lag spike to 7 minutes 15 seconds
           at time of a secondary component failure — a clear RPO
           breach, losing over 2 minutes more data than the documented
           commitment allowed.
```

## Statistics
| Finding | Context |
|---------|---------|
| Documented RPOs are commonly based on steady-state or best-case replication lag rather than worst-case/peak-load figures | Typical gap identified in RPO validation audits |
| A meaningful share of RPO commitments have not been re-validated since original system design despite significant subsequent growth in write volume | Estimated from infrastructure audit findings |
| Continuous RPO-exposure monitoring (alerting when live replication lag approaches the committed RPO, not just after an incident) is reported to catch the majority of RPO risk before an actual data-loss incident | Reported range across teams adopting proactive RPO monitoring |

## Mitigations
1. **Continuous RPO-exposure monitoring**: Alert proactively whenever live replication lag or backup age approaches a defined fraction of the committed RPO (e.g. 70%), rather than only discovering RPO risk after a real data-loss incident.
2. **Worst-case, not average-case, RPO validation**: Re-validate RPO commitments under realistic peak-load conditions and against realistic failure-detection/failover timing, not just steady-state replication lag measured during quiet periods.
3. **Include detection and decision time in the RPO clock**: Count the time from the actual last-replicated point to the moment failover completes, not just the raw replication lag, since failure detection and decision time also consume the data-loss window.
4. **Periodic RPO re-certification**: Schedule regular (e.g. quarterly) re-validation of RPO commitments against current write volume, replication architecture, and load patterns, treating growth as a standing risk to previously-valid commitments.
5. **RPO-aware architecture changes as volume grows**: Trigger an explicit architecture review (e.g. moving from async to semi-sync replication, increasing backup frequency) when monitored replication lag trends suggest the committed RPO is becoming unachievable under current load.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| replication_lag_vs_rpo_ratio | Current replication lag as a fraction of the committed RPO | Alert if > 70% of RPO budget |
| actual_data_loss_window_per_incident | Measured data-loss window for each real failover/recovery incident | Alert if exceeds committed RPO |
| rpo_last_validated_age | Time since the committed RPO was last validated under realistic peak-load conditions | Alert if > 6 months |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| RPO budget consumption high | replication_lag_vs_rpo_ratio exceeds 70% sustained | High | Investigate replication bottleneck, consider architecture changes before an actual failure tests the limit |
| RPO breach confirmed | actual_data_loss_window_per_incident exceeds committed RPO on a real incident | High | Formal SLA/compliance incident, root-cause the replication gap, revise RPO commitment or architecture |

## Related Patterns
- [Failover Data Loss](./failover-data-loss.md) - the concrete per-incident mechanism; RPO miss is the aggregate/statistical pattern of that mechanism exceeding its committed bound
- [Recovery Time Objective Miss](./recovery-time-objective-miss.md) - the time-axis counterpart; both are commitment-vs-reality gaps in disaster-recovery objectives
- [Recovery Procedure Untested](./recovery-procedure-untested.md) - an untested recovery procedure is one of the ways an RPO commitment goes unvalidated until a real incident exposes it
