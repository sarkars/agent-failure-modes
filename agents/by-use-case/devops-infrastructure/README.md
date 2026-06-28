# DevOps & Infrastructure

Agents managing auto-scaling, incident response, deployments, and capacity planning face challenges around threshold miscalibration, cascading failures, and compliance drift.

## Goals

| Goal | Description | Patterns |
|------|-------------|----------|
| [Auto-Scaling](goals/auto-scaling/) | Thrashing, overshooting, under-provisioning | In progress |
| [Incident Response](goals/incident-response/) | Severity miscalibration, cascading failures, alert noise | In progress |
| [Deployment Safety](goals/deployment-safety/) | Rollback failures, quota violations, safety checks | In progress |
| [Capacity Planning](goals/capacity-planning/) | Forecast misses, resource exhaustion, quota tracking | In progress |

**Status**: ~35 patterns planned

## Key Challenges

1. **Threshold Volatility**: Scaling thresholds too sensitive; oscillation
2. **Cascading Failures**: Remediation attempts worsen outage
3. **Metric Staleness**: Actions based on old data
4. **Quota Blindness**: Allocation exceeds hard limits
5. **Compliance Drift**: Changes violate security/compliance rules
