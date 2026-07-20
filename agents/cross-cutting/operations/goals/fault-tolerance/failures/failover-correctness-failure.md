# Failover Correctness Failure

## Issue
A failover mechanism does exactly what it's supposed to on the surface — it detects the primary's failure, promotes a standby, and traffic resumes flowing within the expected time — but the standby produces incorrect results once it's live. This is distinct from failover being slow (failover-delay-too-long) or losing data in flight (failover-data-loss): here the mechanics of the switch itself work, but the standby was running different code, stale configuration, an outdated model version, or an incomplete replica of reference data, so it silently serves wrong answers with full apparent availability.

**Frequency**: Occasional

**Symptoms**
- Availability and latency metrics look completely healthy immediately after failover, masking the problem
- Correctness-sensitive downstream metrics (order accuracy, fraud false-positive rate, agent recommendation quality) degrade only after failover, with no corresponding infrastructure alert
- The standby is later found to be running an older application version, an outdated model checkpoint, or a stale configuration snapshot than the primary had
- Customer complaints or manual review are often the first signal, arriving well after automated monitoring reported a "successful" failover

## Root Cause
Failover automation is usually built and tested against the question "does traffic reach a healthy-looking replica," which is answerable with basic health checks (process up, port open, returns 200). It's rarely built or tested against the question "does the replica compute the same answer as the primary would have," because that requires functional/semantic testing, not just liveness testing. Standby instances drift from the primary over time — a config change, a model retrain, a feature-flag update, or a schema migration gets applied to the primary and, due to a gap in the deployment pipeline, never reaches the standby — and because the standby is rarely serving live traffic, this drift goes unnoticed until an actual failover event promotes it.

## Example
```
Setup: PricingAgent runs as primary in us-east-1 and standby in
us-west-2, with automated failover triggered on primary health-check
failure.

Week -3: A pricing-logic bugfix (correcting a currency-rounding error
          for orders over $10,000) is deployed to us-east-1 primary via
          the standard rolling-deploy pipeline. The standby deploy step
          for us-west-2, which only runs when explicitly triggered
          because it receives no live traffic, is skipped because no one
          remembers to trigger it for a passive standby.

Week 0, 03:14:00 - us-east-1 primary experiences a hardware fault.
          Health checks fail 3 consecutive times; automated failover
          promotes us-west-2 standby. DNS and load balancer cut over
          within 45 seconds, well inside the 60-second RTO target.
          Failover dashboard shows green: "Failover completed
          successfully."

03:14:45 - us-west-2, now serving 100% of traffic, is running the
          pricing logic from 3 weeks ago — the currency-rounding bug is
          back. Every order over $10,000 processed in the next 6 hours
          (until an engineer manually notices and redeploys) is
          mispriced by a small but consistent margin.

09:30:00 - Finance flags a reconciliation discrepancy across ~340
          high-value orders placed overnight. Root cause traced to the
          stale standby, not the original hardware fault.
```

## Statistics
| Finding | Context |
|---------|---------|
| A meaningful share of automated failovers promote a standby running a different application version, config, or model than the primary | Estimated from configuration-drift audits in active-passive deployments |
| Correctness-impacting failover incidents are typically detected significantly later than availability-impacting ones, often hours rather than minutes | Typical range observed where health checks are liveness-only |
| Adding deployment-parity checks as part of the failover health check is reported to catch most version-drift issues before they reach production traffic | Reported range across teams that added version/config parity gates |

## Mitigations
1. **Deployment parity enforcement**: Treat standby instances as first-class deploy targets in the same pipeline as the primary, not an optional or manually-triggered secondary step, so version and config drift cannot occur.
2. **Semantic health checks, not just liveness checks**: Extend failover health checks to include a canary request whose expected output is known, verifying the standby produces correct results, not just that it responds.
3. **Pre-promotion parity verification**: Before completing a failover, automatically compare the standby's deployed version, config hash, and model checksum against the primary's last-known-good values, and block promotion (or page a human) on mismatch.
4. **Regular failover drills with correctness checks**: Periodically failover to the standby under controlled conditions and run a full correctness test suite against it, not just an availability check.
5. **Post-failover correctness monitoring window**: Automatically elevate correctness-sensitive monitoring (business-logic metrics, not just infra metrics) for a defined window after any failover event, since this is exactly when drift-caused errors surface.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| standby_primary_version_drift | Difference in deployed version/config hash between standby and primary | Alert if any drift detected |
| post_failover_correctness_delta | Change in business-logic correctness metrics (e.g. order accuracy) in the window following a failover event | Alert if delta exceeds normal variance |
| canary_check_mismatch_rate | Rate of known-answer canary requests returning incorrect results from a standby | Alert if > 0% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Standby drift detected pre-failover | Version/config parity check fails during routine standby health monitoring | High | Block automatic promotion, trigger standby redeploy, alert on-call |
| Correctness regression post-failover | post_failover_correctness_delta exceeds threshold within monitoring window | High | Treat as a live incident even though availability metrics are green; investigate standby parity |

## Related Patterns
- [Failover Delay Too Long](./failover-delay-too-long.md) - both are failover-quality failures, one about timing, this one about correctness of the result
- [Failover State Corruption](./failover-state-corruption.md) - a related but distinct mechanism where the standby's state itself is corrupted during transfer rather than merely stale
- [Recovery Divergence](./recovery-divergence.md) - shares the theme of a recovered/promoted instance ending up in a state inconsistent with what preceded it
