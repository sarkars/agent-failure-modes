# Circuit Breaker False Positive

## Issue
A circuit breaker sitting in front of an agent's backend (the LLM inference endpoint, a tool API, or an internal microservice the agent calls) trips open in response to a short burst of transient errors — a brief upstream GC pause, a single overloaded pod, a momentary network blip — rather than a genuine sustained outage. Once open, the breaker rejects all subsequent calls for its full cooldown period regardless of whether the underlying service has already recovered, so a two-second blip turns into a 30-60 second window where every agent session fails over to a degraded fallback or errors outright, even though the dependency was healthy again within a couple of retries.

**Frequency**: Common

**Symptoms**
- Circuit breaker opens and closes repeatedly within a short window even though the upstream service's own health checks show it as continuously healthy
- Agent sessions receive fallback responses or hard failures immediately after a very brief upstream latency spike (well under the breaker's configured error-rate window)
- Breaker cooldown period is consistently longer than the actual outage duration, so recovery lags real service health by tens of seconds
- Error budget consumption attributed to "dependency unavailable" spikes even though the dependency's own dashboards show no sustained degradation
- Manually re-testing the "failed" dependency immediately after a trip succeeds on the first try

## Root Cause
Circuit breakers are typically configured with a fixed error-rate or consecutive-failure threshold over a short rolling window (e.g., "open if 5 of the last 10 calls failed"), tuned for a worst case of sustained upstream failure. Agent workloads amplify the sensitivity of this design in two ways: LLM inference calls have naturally higher per-call latency variance than typical microservice calls, so a handful of slow responses under load can look identical to a handful of failed responses if timeouts are counted as failures; and agent traffic is often bursty (many tool calls fan out from a single orchestration step), so a transient blip affects a disproportionate share of the breaker's rolling window all at once. When the threshold window is short and the failure definition doesn't distinguish "slow" from "actually failed," a brief, self-resolving blip crosses the trip threshold before the underlying issue would have resolved on its own, and the fixed cooldown then holds the breaker open well past the point of actual recovery.

## Example
```
"ToolOrchestrator" agent calls the internal "PricingService" API as
part of a checkout-assistant flow. Circuit breaker: opens after 5
failures in a rolling 10-call window, 45-second cooldown, 3-second
per-call timeout counted as failure.

12:04:01 - PricingService pod undergoes a routine JVM GC pause,
adding ~2.5s of latency to in-flight requests for about 4 seconds.

12:04:01-12:04:05 - 6 of the orchestrator's concurrent tool-call
fan-outs (triggered by a single busy user session issuing several
sub-queries at once) hit PricingService during the pause. 5 exceed
the 3-second timeout and are counted as failures.

12:04:05 - breaker trips open. All PricingService calls for the next
45 seconds are short-circuited to the fallback ("price unavailable,
please check back shortly").

12:04:09 - PricingService's own health check confirms latency is
back to normal (p99 220ms). The dependency has been fully healthy
for 41 of the 45 seconds the breaker stays open.

12:04:50 - breaker half-opens, test call succeeds, breaker closes.
Total user-facing degraded window: 49 seconds, of which roughly 4
seconds corresponded to an actual upstream issue.
```

## Statistics
| Finding | Context |
|---------|---------|
| A substantial share of circuit breaker trips against LLM and tool-call dependencies are estimated to resolve within a few seconds if probed immediately, well inside the typical fixed cooldown window | Estimated from teams comparing breaker cooldown duration to actual upstream recovery time |
| Counting request timeout as failure without separating "slow" from "errored" is a common contributor to over-sensitive breakers in high-latency-variance workloads | Typical finding across incident reviews of agent-adjacent circuit breakers |
| Adaptive/exponential half-open probing (versus fixed cooldown) reduces mean unnecessary-degradation duration substantially in teams that have adopted it | Reported range across teams that moved from fixed to adaptive cooldowns |

## Mitigations
1. **Separate latency from failure in trip criteria**: Distinguish slow-but-successful calls from actual errors when computing the breaker's failure rate, and size the per-call timeout to reflect realistic LLM/tool latency percentiles (e.g., p99) rather than a generic microservice default.
2. **Widen the evaluation window relative to burst size**: Use a rolling window sized to absorb a single fan-out burst without tripping on it alone (e.g., minimum call-count floor before evaluating error rate, not just a raw ratio over the last N calls).
3. **Fast, adaptive half-open probing**: Replace a fixed cooldown with exponential or fast-retry half-open probing that re-tests the dependency within a few seconds of tripping, so recovery is detected close to when it actually happens rather than after a flat 30-60s wait.
4. **Correlate breaker trips with upstream health telemetry**: Automatically cross-check a trip against the upstream service's own health/latency dashboards, and flag trips that don't correspond to any sustained upstream degradation as likely false positives for tuning review.
5. **Per-dependency threshold tuning from observed variance**: Calibrate trip thresholds per dependency using its actual historical latency and error distribution rather than applying one global default across every agent tool and backend call.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| breaker_trip_to_upstream_recovery_gap | Time between a breaker opening and the upstream service's own health check reporting healthy | Alert if median gap > 10s over a rolling day |
| breaker_flap_count | Number of open/close transitions for a given breaker within a rolling hour | Alert if > 3 per hour for the same breaker |
| fallback_traffic_share_during_healthy_upstream | Percentage of requests served by fallback while upstream health checks report green | Alert if > 2% sustained over 5 minutes |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Breaker flapping | breaker_flap_count exceeds threshold for a single dependency | Medium | Review recent trip windows against upstream telemetry, consider widening evaluation window or timeout |
| Sustained false-positive fallback | fallback_traffic_share_during_healthy_upstream stays elevated while upstream is reporting healthy | High | Manually reset/tune breaker, notify dependency owner, audit user impact during the window |

## Related Patterns
- [Health Check Flapping](./health-check-flapping.md) - a closely related instability pattern where the underlying health signal itself oscillates, often co-occurring with breaker false positives
- [Traffic Overflow Cascade](./traffic-overflow-cascade.md) - describes what happens downstream when a breaker's fallback path itself gets overwhelmed by the traffic it absorbs
- [Deployment Validation Skipped](./deployment-validation-skipped.md) - untested breaker threshold changes are a common way overly sensitive configurations reach production
