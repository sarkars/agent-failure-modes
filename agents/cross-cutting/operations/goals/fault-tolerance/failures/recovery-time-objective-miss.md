# Recovery Time Objective Miss

## Issue
The organization has a defined Recovery Time Objective (RTO) — the maximum acceptable duration of an outage, e.g. "service must be restored within 30 minutes" — and an actual incident's total recovery time exceeds it. This pattern is specifically about the RTO commitment being broken, as a measurable, reportable event distinct from general slowness: it requires a documented target and an actual, measured overrun against that target, and is the aggregate/governance-level counterpart to specific timing failures like failover-delay-too-long (which describes the mechanics of why failover itself is slow).

**Frequency**: Common

**Symptoms**
- Post-incident timeline shows total time-to-restore exceeding the documented RTO for the affected service or tier
- RTO misses cluster around specific incident types (e.g. always fine for infra-only failures, always missed for incidents requiring cross-team coordination) rather than being evenly distributed
- The gap between committed RTO and actual recovery time grows over time as the system's scale or complexity increases, even though the RTO documentation hasn't been revisited
- Stakeholders (customers, internal SLA holders, compliance) learn about the RTO miss from the incident report rather than having any earlier signal that RTO was at risk

## Root Cause
RTO is typically set once, during initial architecture or compliance planning, based on an idealized model of what recovery should take — often the sum of a few key automated steps without accounting for detection time, human decision/approval time, coordination overhead across teams, or the specific failure mode actually encountered. As the system grows (more data to restore, more services to coordinate, more complex dependency chains) the real recovery time trends upward, but the RTO commitment, having been treated as a fixed, one-time architectural decision rather than a continuously re-validated operational target, doesn't get revised to match. RTO misses are also disproportionately caused by failure modes that weren't the ones originally used to derive the RTO — e.g. RTO was validated against a clean single-node failure, but the real incident involves a more complex multi-component failure that the original RTO calculation never modeled.

## Example
```
Documented RTO for the OrderProcessing platform: 30 minutes, set two
years ago based on a drill simulating a single database node failure
with automated failover.

Current reality: the platform has grown from 1 database cluster to 3
(sharded by region), added a message-queue dependency for async order
events, and added a fraud-scoring agent in the critical path — none of
which were part of the original RTO's failure model.

10:00:00 - A configuration error during a routine deploy causes the
           fraud-scoring agent to become unresponsive across all
           regions simultaneously (not the single-node database
           failure the RTO was designed around).

10:00:00-10:12:00 - Detection takes 12 minutes because monitoring for
           the fraud-scoring agent was added after the original RTO
           was set and was never included in the RTO's alerting-latency
           budget.

10:12:00-10:25:00 - The automated failover mechanism, built for
           database failures, doesn't apply to this failure mode at
           all; a human must diagnose that fraud-scoring specifically
           is the culprit and manually decide whether to fail open
           (skip fraud checks) or fail closed (block all orders) —
           a decision the original runbook doesn't address, requiring
           escalation to a product-policy owner (13 minutes).

10:25:00-10:52:00 - Once the fail-open decision is made, rolling
           restart of the fraud-scoring agent across 3 regions takes
           27 minutes, longer than expected because rollout tooling
           was built for single-region deploys and only later extended
           (without re-timing) to 3 regions.

Total time to restore: 52 minutes against a 30-minute RTO — a 73%
overrun, for a failure mode the original RTO was never designed to
cover.
```

## Statistics
| Finding | Context |
|---------|---------|
| A meaningful share of real incidents exceed their documented RTO, disproportionately for failure modes not represented in the original RTO validation drill | Estimated from post-incident RTO-compliance review |
| Detection and human-decision time (not automated remediation time) is commonly the largest single contributor to RTO overruns | Typical range observed in RTO-miss postmortem timing breakdowns |
| Organizations that re-validate RTO against evolving architecture on a regular cadence report substantially fewer RTO misses than those that set RTO once at design time | Reported range across DR-maturity comparisons |

## Mitigations
1. **Model multiple failure types when setting RTO, not just one**: Validate RTO against a representative range of failure modes (single-node, multi-component, human-decision-required, cross-region) rather than a single idealized scenario, since real incidents rarely match the easiest case.
2. **Re-validate RTO whenever architecture changes materially**: Treat the addition of new critical-path dependencies (a new service, a new region, a new agent in the pipeline) as a trigger to re-assess whether the existing RTO commitment is still achievable.
3. **Budget detection and decision time explicitly, not just remediation time**: Include human detection, diagnosis, and approval time in the RTO calculation, since these are frequently the dominant contributors to overruns, not the automated remediation steps.
4. **Track RTO performance as an ongoing metric, not just a design-time target**: Measure and trend actual recovery time against committed RTO across every real incident, surfacing systemic drift before it becomes a compliance or customer-facing surprise.
5. **Pre-authorize ambiguous-decision paths**: For failure modes requiring a judgment call (like fail-open vs. fail-closed), pre-define and pre-authorize the decision criteria during calm periods so a live incident doesn't need to escalate to find a decision-maker.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| actual_recovery_time_vs_rto | Measured total recovery time for each incident compared to the documented RTO | Alert if actual exceeds RTO |
| rto_validation_failure_mode_coverage | Number/variety of failure modes the current RTO has been validated against via drill | Alert if < defined minimum coverage |
| rto_last_revalidated_age | Time since the RTO was last re-validated against current architecture | Alert if > 6 months or after major architecture change |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| RTO breach confirmed | actual_recovery_time_vs_rto shows overrun on a real incident | High | Formal SLA/compliance review, root-cause the specific stage(s) responsible for the overrun |
| RTO validation stale after architecture change | A new critical-path dependency is added without a corresponding RTO re-validation | Medium | Require re-validation drill before the change is considered fully rolled out |

## Related Patterns
- [Failover Delay Too Long](./failover-delay-too-long.md) - describes the stage-by-stage mechanics that most commonly cause an aggregate RTO miss
- [Recovery Point Objective Miss](./recovery-point-objective-miss.md) - the data-loss-axis counterpart; both are commitment-vs-reality gaps in disaster-recovery objectives
- [Recovery Procedure Untested](./recovery-procedure-untested.md) - an untested procedure is one of the most common root causes of an RTO miss, since its time estimate was never empirically validated
