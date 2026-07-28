# What Are the Most Common Monitoring-and-Alerting Failures in AI Agents?

**Agent systems produce metrics (latency, error rate, resource usage) that indicate system health. Monitoring-and-alerting failures occur when metrics are not collected, thresholds are not configured correctly, or alerts don't fire when they should (or fire too often and are ignored), resulting in failures being discovered too late or being masked by alert fatigue.**

## Key Takeaways

1. **Metrics Are Not Collected at Critical Boundaries**: Agents are instrumented to emit metrics locally, but the metrics that matter for system health (latency between agents, handoff success rate, cascade detection) are not collected or are only collected at coarse granularity.

2. **Thresholds Are Tuned to Historical Data, Not SLAs**: Alert thresholds are set based on "what the system normally looks like" rather than "what the SLA requires." If the normal error rate is 0.1%, and the alert is set at 5%, an increase to 1% (which violates SLA) goes undetected.

3. **Alert Fatigue Causes Critical Alerts to Be Ignored**: Too many alerts (from misconfigured thresholds, from too much instrumentation noise) cause engineers to ignore them. When a critical alert fires, it's lost in the noise.

4. **Alerts Don't Trigger Automatic Mitigation**: An alert fires, but no one is on-call to respond, or the response is manual and slow. Alerts that could trigger automatic remediation (circuit breaker, failover, restart) instead just produce noise.

## Scope

Monitoring-and-alerting concerns cluster into four categories:

- **Metric Collection & Instrumentation**: Agents emit metrics (or fail to emit them) at key decision points and boundaries. Without comprehensive instrumentation, important signals are lost.
- **Threshold Configuration**: Alert thresholds are based on SLAs and business requirements (or are arbitrary and ineffective). Thresholds must be tuned to catch problems while avoiding false positives.
- **Alert Lifecycle Management**: Alerts fire reliably and are acted upon (or are ignored due to fatigue). Alert fatigue is a major cause of incidents going unnoticed.
- **Automatic Remediation**: Alerts can trigger automatic responses (circuit breaker, failover, rate limiting) or just notify humans. Automatic remediation prevents incidents from requiring manual intervention.

## When Monitoring-and-Alerting Matters

1. **On-Call Operations**: Systems where an on-call engineer is responsible for incident response. Alerts are the primary mechanism for notifying on-call when something goes wrong.

2. **High-Availability Services**: Systems where incidents have significant business impact. Early detection and rapid response are critical to meeting SLAs.

3. **Self-Healing Systems**: Systems where automatic remediation can address common problems without human intervention. Monitoring must feed data to automatic remediation logic.

## Cross-Pattern Insight

Monitoring and alerting are fundamentally about **detecting problems before they become critical**. By default, systems operate silently; there's no visibility into whether they're healthy or degraded. But degradation accelerates: a 10% error rate that goes unnoticed for 10 minutes becomes a cascade that brings down the entire system. Robust monitoring and alerting require: (1) comprehensive metric collection at agent boundaries and decision points (latency, error rate, resource usage, custom business metrics); (2) thresholds tuned to SLAs and business requirements (if SLA is 99% availability, alert when error rate exceeds 1%, not when it exceeds 50%); (3) alert routing and de-duplication so critical alerts reach on-call without noise; (4) automatic remediation for common failures (circuit breaker on high error rate, failover on unavailability, rate limiting on cascades); and (5) regular reviews of alert thresholds and remediation logic to ensure they're still appropriate. Without comprehensive metric collection, SLA-tuned thresholds, alert routing, automatic remediation, and regular threshold reviews, monitoring is reactive (understanding what went wrong after the damage is done) instead of proactive (preventing problems before they cascade).

## Frequently Asked Questions

**What metrics should an agent emit to enable monitoring?**
1. Latency (p50, p95, p99) for each operation - how fast is the agent responding?
2. Error rate (% of requests failing) and error type distribution - is the agent healthy?
3. Resource usage (CPU, memory, connections, file handles) - is the agent consuming resources normally?
4. Dependency health (is the agent's dependencies available? what's their latency?)
5. Business metrics (requests processed, transactions approved, data transformed) - is the agent doing productive work?
6. Cache hit rate, queue depth, and other implementation-specific metrics

**How should alert thresholds be set if there's no historical baseline?**
Set thresholds based on the SLA. If the SLA is 99% availability, the error rate must be below 1%; set alert threshold at 0.5% to catch degradation early. If there's latency SLA (p95 latency < 100ms), set threshold at 75ms to detect degradation early. If no SLA exists, create one (what's the business requirement?), then set thresholds to support it.

**What should happen if an alert fires but there's no on-call engineer available?**
Use automatic remediation: if the alert indicates high error rate, open a circuit breaker. If it indicates a dependency is unavailable, failover to a backup. If it indicates cascade, shed load by rejecting new requests. Automatic remediation buys time for on-call to respond. When on-call arrives, the situation has already been partially mitigated.

**How can alert fatigue be reduced?**
1. Set thresholds correctly (not too sensitive, not too loose).
2. De-duplicate alerts (if the same alert fires multiple times in quick succession, send one alert, not many).
3. Combine related alerts into a single high-level alert (if CPU and latency both spike, that's one "resource exhaustion" alert, not two separate alerts).
4. Silence known-benign alerts during expected high-activity periods (maintenance windows, high-traffic events).
5. Regularly review alert configuration and disable alerts that never fire or always fire.

**Can an agent detect anomalies (something is wrong, but I don't have a specific threshold)?**
Use statistical methods: compute baseline metrics (normal latency, error rate) over a time window. Alert if the current metric deviates significantly from the baseline (e.g., 3-sigma rule: alert if the current value is more than 3 standard deviations from the mean). Anomaly detection can catch problems that fixed thresholds would miss.

## Failure Patterns

No specific failure patterns have been documented for monitoring-and-alerting yet. However, poor monitoring and alerting are root causes for late detection of failures in all other goal areas.

**Total: 0 documented patterns**

## Related Goals

- [Logging-and-Tracing](../logging-and-tracing/README.md) — logs provide raw data that monitoring systems analyze
- [Observability-Monitoring](../observability-monitoring/README.md) — complementary; monitoring focuses on metrics and alerting on thresholds
- [Fault-Tolerance](../fault-tolerance/README.md) — rapid detection (via monitoring) is a prerequisite for rapid recovery
- [Explainability-and-Debugging](../explainability-and-debugging/README.md) — alerts can trigger automatic diagnosis and detailed logging
- [Cascading-Failures](../cascading-failures/README.md) — early cascade detection (via monitoring and alerting) is critical to stopping cascades
