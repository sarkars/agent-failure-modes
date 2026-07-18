# Latency SLA Violation

## Issue
A tool's documented latency SLA (e.g., "p99 under 500ms") is regularly exceeded in actual production traffic, and the agent's own timeout and retry logic — tuned to trust that documented figure — fires prematurely relative to the tool's real behavior, or conversely the agent's own downstream SLA commitment to its users gets breached because it inherited an unrealistic latency assumption from the upstream tool. Either way, the mismatch between advertised and actual latency propagates as a reliability problem that looks like the agent's own bug.

**Frequency**: Common

**Symptoms**
- Timeouts fire on a meaningful fraction of calls to a tool despite the timeout being set generously above the tool's documented SLA
- P99 (or even p95/p50) latency observed in the agent's own telemetry is consistently higher than the vendor's advertised figure, especially during specific time windows (peak hours, specific regions)
- Retry storms triggered by premature timeouts increase load on the tool further, worsening its latency in a feedback loop
- The agent's own downstream SLA to its users is breached specifically during periods correlated with the upstream tool's slow responses
- Vendor's status page shows no incident despite sustained latency well above the documented SLA, since many SLAs are aggregated over long windows (monthly) that mask shorter periods of violation

## Root Cause
Vendor-published latency SLAs are often aspirational or measured under conditions (specific regions, off-peak load, optimal network paths) that don't match the full range of production conditions a given customer actually experiences. SLAs are also frequently defined as long-window aggregates (e.g., "p99 under 500ms measured monthly"), which can mask sustained multi-hour or multi-day windows where actual latency is far worse, since a single bad day gets diluted across a month of otherwise-good performance. Agents that set timeout and retry configuration based on the advertised SLA figure, without empirically validating actual observed latency in their own traffic, end up with thresholds tuned to a number that doesn't reflect reality, causing either excessive premature timeouts or, if timeouts are set loosely to compensate, cascading delays passed on to the agent's own downstream consumers.

## Example
```
1. An agent calls a third-party address-validation API advertised with "p99 latency under
   300ms," and sets its own request timeout at 1 second (a generous 3x margin) as part
   of a real-time checkout flow.
2. During the vendor's own regional peak traffic hours (which happen to overlap with
   the agent's own peak checkout traffic, since both serve the same geographic market),
   actual p99 latency from the vendor regularly reaches 1.2-1.5 seconds, well above
   both the advertised SLA and the agent's configured timeout.
3. Roughly 8% of checkout-flow address-validation calls during peak hours time out at
   the 1-second mark and get retried by the agent's retry logic.
4. The retries add further load to the vendor's already-strained backend during peak
   hours, pushing latency up further and increasing the timeout rate to 12% within
   the same peak window — a feedback loop.
5. The agent's own checkout completion SLA (99% of checkouts completing within 3 seconds)
   is breached during these peak windows, traced initially to "checkout flow bug" before
   engineers realize the root cause is the upstream vendor's latency exceeding its own
   advertised SLA specifically during shared peak-traffic hours.
```

## Statistics
| Finding | Context |
|---------|---------|
| Actual p99 latency for third-party APIs frequently exceeds the vendor's advertised SLA figure during the customer's own peak-traffic windows, since vendor SLAs are usually aggregated across all traffic and regions rather than measured for a specific customer's peak overlap | Consistent with SLA figures being system-wide averages, not customer-specific guarantees |
| Retry storms triggered by premature or overly aggressive timeout settings have been observed to amplify an initial latency problem by a meaningful multiple during sustained periods, compounding the underlying issue | Because retries add load precisely when the upstream system is already under strain |
| Setting timeouts based on empirically observed latency percentiles (from the agent's own traffic) rather than the vendor's advertised SLA figure has been shown to meaningfully reduce premature-timeout-driven retry storms | By calibrating to actual observed conditions instead of a marketing number |

## Mitigations
1. **Calibrate timeouts to empirically observed latency, not the advertised SLA**: Continuously measure actual p50/p95/p99 latency from the agent's own traffic against the specific tool, and set timeouts based on that observed distribution with appropriate margin, revisiting periodically.
2. **Circuit breakers instead of unbounded retries**: When latency or timeout rate crosses a threshold, trip a circuit breaker that stops issuing new requests for a cooldown period rather than retrying into an already-degraded upstream, preventing the retry-storm feedback loop.
3. **Segment latency monitoring by time window and region**: Track latency separately for peak vs. off-peak hours and by region, since aggregate SLA figures can mask sustained violations concentrated in specific windows relevant to the agent's own traffic pattern.
4. **Asynchronous or degraded-mode fallback for latency-sensitive flows**: For user-facing flows with a hard latency budget, design a fallback (cached/approximate result, deferred processing) that activates when the upstream tool's latency exceeds a threshold, rather than blocking the user-facing flow on a slow call.
5. **Hold vendors accountable with observed data**: When negotiating or renewing vendor contracts, bring empirical latency data showing SLA violations during specific windows, since vendor-reported aggregate SLA compliance often doesn't reflect the customer's actual experience.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `tool.observed_p99_latency_vs_sla` | Actual measured p99 latency from agent traffic compared to the vendor's advertised SLA figure | Alert when observed p99 exceeds advertised SLA by more than 50% for 15+ minutes |
| `tool.timeout_rate` | Rate of agent requests to the tool that hit the configured timeout | Alert above 2% sustained over 10 minutes |
| `agent.downstream_sla_breach_correlation` | Correlation between the agent's own downstream SLA breaches and upstream tool latency spikes | Track to confirm root cause during incidents |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Sustained latency SLA violation | `observed_p99_latency_vs_sla` exceeds threshold for 15+ minutes | High | Trip circuit breaker, activate fallback path, notify vendor with observed data |
| Timeout-driven retry storm forming | `timeout_rate` climbs above 5% and continues rising | Critical | Halt retries immediately, fail fast to fallback rather than compounding upstream load |

## Related Patterns
- [Execution Time Quota](../../tool-allocation-limits/failures/execution-time-quota.md) - related but distinct: a hard-enforced cutoff versus a latency SLA that's merely exceeded in practice
- [Degraded Sla Not Communicated](./degraded-sla-not-communicated.md) - latency violations are often one symptom of a broader, uncommunicated vendor-side degradation
- [Sla Availability Not Met](./sla-availability-not-met.md) - severe, sustained latency violations frequently shade into an effective availability failure even if the vendor doesn't classify it as downtime
