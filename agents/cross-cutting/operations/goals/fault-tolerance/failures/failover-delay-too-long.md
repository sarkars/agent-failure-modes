# Failover Delay Too Long

## Issue
The failover mechanism eventually works — the standby is correct, no data is lost, no state is corrupted — but it takes materially longer to complete than the service's defined SLA or failover-time objective, extending customer-visible downtime well beyond what was promised or designed for. This is purely a timing failure: every other part of the failover (detection, promotion, correctness) can be functioning as designed, but the accumulated latency across detection, decision, and cutover steps blows through the target window.

**Frequency**: Common

**Symptoms**
- Actual failover completion time, measured from first failure symptom to full traffic cutover, consistently exceeds the documented failover SLA
- Post-incident timelines show delay concentrated in specific stages — health-check confirmation, DNS propagation, connection draining, manual approval gates — rather than one obvious bottleneck
- Failover time varies widely between drills (fast) and real incidents (slow), suggesting the drill doesn't exercise the same conditions as a real failure
- Customers or downstream SLAs are breached specifically because of the failover window, not the root outage itself

## Root Cause
Total failover time is the sum of several sequential stages — fault detection (waiting for enough consecutive failed health checks to avoid false positives), decision (automated or manual approval that the failure is real and failover is warranted), promotion (standby transitioning to primary role, often including cache warmup or connection re-establishment), and propagation (DNS TTL expiry, load balancer re-registration, client-side connection pool refresh) — and each stage is usually tuned independently for its own tradeoff (e.g. longer health-check confirmation windows reduce false-positive failovers but add delay). Nobody typically adds up the worst-case total across all stages and compares it to the actual SLA; each stage's owner considers their own piece "fast enough." Under a real incident, several of these stages hit their worst case simultaneously (conservative health-check thresholds, a manual approval step waiting on a paged human, a DNS TTL that hasn't been lowered since a previous, since-forgotten incident), and the sum exceeds the target even though no single stage was individually broken.

## Example
```
SLA: Failover must complete within 60 seconds of primary failure.

Actual failover time budget (as configured, nobody had added it up):
- Health check: 5 consecutive failed checks at 10s intervals = 50s to
  confirm the primary is actually down (tuned conservatively after a
  prior false-positive-failover incident).
- Decision: automated for infra failures, but this incident triggers an
  ambiguous "degraded but responding" state that requires a paged
  human's manual approval = average 90s from page to click-confirm.
- Promotion: standby requires a 15s cache warmup before it reports
  itself healthy and can be added back to the load balancer pool.
- Propagation: DNS record TTL is 300s (5 minutes), left over from a
  config template nobody had customized down for this service.

09:40:00 - Primary begins failing. Health-check clock starts.
09:40:50 - 5th consecutive failed check confirms primary down (50s).
09:40:50 - Ambiguous state triggers manual approval gate; page fires.
09:42:35 - On-call engineer, mid-standup, sees the page and approves
           failover (105s after page fired).
09:42:50 - Standby promotion begins; cache warmup completes (15s).
09:47:50 - DNS TTL of 300s means clients caching the old primary's IP
           don't fully cut over until up to 5 minutes after the DNS
           record updates.

Total observed failover time: approximately 7 minutes 50 seconds against
a 60-second SLA — a 680% overrun, with no single stage being obviously
"broken" in isolation.
```

## Statistics
| Finding | Context |
|---------|---------|
| Real-incident failover times commonly run several times longer than tabletop-drill failover times for the same system | Typical range observed comparing drilled vs. live failover durations |
| DNS TTL and manual-approval gates are among the most common individually-overlooked contributors to failover SLA overruns | Estimated from postmortem stage-by-stage timing breakdowns |
| Removing or automating manual approval gates for well-understood failure classes is reported to cut total failover time substantially | Reported range across teams that moved from manual to automated failover decisions |

## Mitigations
1. **End-to-end failover time budget**: Explicitly sum the worst-case duration of every stage (detection, decision, promotion, propagation) against the SLA, and treat any stage whose worst case alone threatens the budget as a required fix, not an acceptable local tradeoff.
2. **Automate ambiguous-state decisions where possible**: Replace manual approval gates for well-characterized failure signatures with automated decision logic, reserving human approval only for genuinely novel or ambiguous scenarios.
3. **Aggressively low DNS/client-side TTLs on failover-critical records**: Set TTLs as low as operationally reasonable for any DNS record involved in failover cutover, and prefer client-side service discovery with fast refresh over long-TTL DNS where possible.
4. **Drill under realistic conditions, including paging**: Run failover drills that include the actual paging and human-approval path (not just the automated technical steps) so the measured drill time reflects real incident timing, not an idealized one.
5. **Stage-level timing instrumentation**: Instrument and dashboard the duration of each individual failover stage on every real incident and drill, so slow stages are visible and attributable rather than hidden inside a single end-to-end number.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| failover_stage_duration | Duration of each individual failover stage (detection, decision, promotion, propagation) | Alert if any stage exceeds its allocated budget |
| total_failover_duration | End-to-end time from first failure symptom to full traffic cutover | Alert if > defined SLA |
| manual_approval_wait_time | Time from page fired to human approval for failover decisions requiring one | Alert if > 60s |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Failover SLA breach | total_failover_duration exceeds defined SLA on a real incident | High | Post-incident review with stage-by-stage timing breakdown, identify and fix the slowest stage |
| Manual approval bottleneck | manual_approval_wait_time exceeds threshold | Medium | Evaluate automating the decision for this failure signature |

## Related Patterns
- [Recovery Time Objective Miss](./recovery-time-objective-miss.md) - failover delay is frequently the dominant contributor to an overall RTO miss
- [Cascade Timeout Interaction](./cascade-timeout-interaction.md) - misconfigured timeouts at intermediate layers can independently add to total failover delay
- [Failover Data Loss](./failover-data-loss.md) - a longer failover delay generally widens the window in which in-flight data loss can occur
