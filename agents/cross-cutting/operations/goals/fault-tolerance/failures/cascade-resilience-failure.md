# Cascade Resilience Failure

## Issue
The very mechanisms deployed to make a system resilient — retries, circuit breakers, health-check-triggered auto-restarts, failover — become active contributors to a cascading failure instead of containing it. A retry policy that seemed reasonable in isolation adds load to an already-struggling dependency; a circuit breaker's half-open probe traffic re-triggers the failure it just tripped on; an auto-restart policy cycles a struggling instance in a tight loop that never lets it recover. This pattern is specifically about resilience infrastructure making things worse, distinct from cascade-amplification (which is about magnitude growth generally) and cascade-timeout-interaction (which is about timeout settings specifically).

**Frequency**: Common

**Symptoms**
- Enabling or leaving on a resilience feature (retry, breaker, auto-restart) correlates with a longer or worse outage than would be expected from the underlying fault alone
- Circuit breakers repeatedly flip open/half-open/open without ever staying closed, each half-open probe re-triggering the failure
- Auto-healing/auto-restart systems cycle the same instances repeatedly, visible as a sawtooth pattern in instance uptime
- Disabling retries or breakers manually during an incident measurably improves recovery time
- Load on a struggling dependency does not decrease even after callers report errors, because retries continue regardless

## Root Cause
Resilience mechanisms are typically designed and tuned in isolation against an assumed failure model — for example, a retry policy assumes failures are transient and independent, and a circuit breaker assumes a brief cool-down is enough for the dependency to recover. When the actual failure is a resource-exhaustion cascade (e.g. the dependency is saturated, not merely flaky), these assumptions break: retries add load to an already-saturated resource instead of waiting it out, and a circuit breaker's automatic half-open probes reintroduce just enough load to keep the dependency saturated forever, preventing the natural recovery the breaker was designed to allow. Because these mechanisms operate automatically and locally, without visibility into the dependency's actual saturation state, they keep "helping" in a way that is actively harmful.

## Example
```
15:00:00 - The recommendation-embeddings service begins running near CPU
           saturation due to a sudden 3x traffic spike from a marketing
           campaign. Latency rises from 50ms to 800ms; a small fraction
           of requests start timing out.

15:00:30 - Every caller's client library has a 3-retry policy with no
           jitter, so each of those timeouts becomes 4 requests instead
           of 1. Load on the embeddings service rises further, latency
           climbs past 2s, and timeout rate rises further.

15:01:15 - Circuit breakers on ~40 caller instances trip to "open" after
           crossing a 50% error-rate threshold, correctly stopping new
           requests. Good — load starts to drop.

15:01:45 - All 40 breakers were configured with the same fixed 30-second
           cool-down and no jitter, so they all transition to "half-open"
           within the same 2-second window and simultaneously send probe
           traffic. The synchronized probe burst re-saturates the
           embeddings service instantly, which is still recovering from
           the earlier spike, and all 40 breakers re-open together.

15:02:15 - This 30-second open/half-open/re-open cycle repeats 6 times.
           The embeddings service never gets a sustained quiet period
           long enough to actually recover, extending an incident that
           the original traffic spike alone would have resolved within
           minutes once the campaign's initial burst subsided.
```

## Statistics
| Finding | Context |
|---------|---------|
| A notable share of cascading incidents are extended in duration specifically by retry or breaker behavior rather than the original fault | Estimated from postmortem root-cause tagging in resilience-heavy architectures |
| Synchronized circuit-breaker cool-downs without jitter produce repeated re-trip cycles in a substantial fraction of multi-instance deployments during saturation incidents | Typical range observed where breaker configs are copied uniformly across instances |
| Adding jitter and exponential backoff to retries and breaker cool-downs is reported to cut cascade duration meaningfully compared to fixed-interval configurations | Reported range across teams that added jitter after a resilience-caused incident |

## Mitigations
1. **Jittered backoff and cool-downs everywhere**: Add randomized jitter to every retry interval and circuit-breaker cool-down so that many callers don't retry or probe in lockstep and re-saturate a recovering dependency.
2. **Saturation-aware retry suppression**: Have clients check for an explicit "I am saturated, do not retry" signal (e.g. a specific error code or Retry-After header) from the dependency and honor it by suspending retries entirely, rather than retrying blindly on any failure.
3. **Gradual, load-limited half-open probing**: Configure circuit breakers to admit a small, capped percentage of traffic during half-open rather than a full burst, and require multiple consecutive successful probe windows before fully closing.
4. **Resilience mechanism load testing under saturation**: Explicitly test retry and breaker configurations against a saturated (not just flaky) dependency in chaos exercises, since the two failure modes require different tuning.
5. **Centralized visibility into aggregate retry/probe load**: Give resilience mechanisms (or an adjacent control system) visibility into total aggregate retry and probe traffic across all callers, not just their own local view, so decisions account for the herd effect.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| retry_amplification_factor | Ratio of actual requests reaching a dependency to unique logical requests attempted | Alert if > 1.5x during degraded periods |
| breaker_flap_rate | Number of open/half-open/open transitions per breaker per minute | Alert if > 3 transitions/min sustained |
| synchronized_probe_burst_size | Count of half-open probe requests arriving within the same 1-second window from different caller instances | Alert if > 10 simultaneous probes |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Breaker flapping detected | breaker_flap_rate exceeds threshold for any dependency | High | Manually force breakers open for an extended cool-down, disable automatic half-open probing temporarily |
| Retry amplification spike | retry_amplification_factor exceeds 1.5x during a degraded dependency incident | High | Disable non-critical retries, notify dependency owner of aggregate retry load |

## Related Patterns
- [Cascade Amplification](./cascade-amplification.md) - resilience-caused amplification is one specific, common mechanism behind the general amplification pattern
- [Cascade Timeout Interaction](./cascade-timeout-interaction.md) - mismatched timeout settings are a frequent root cause of the retry/breaker misbehavior described here
- [Cascade Isolation Failure](./cascade-isolation-failure.md) - both involve a resilience mechanism failing at its one job, isolation vs. containment/backoff
