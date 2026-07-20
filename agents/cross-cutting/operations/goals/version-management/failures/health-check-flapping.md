# Health Check Flapping

## Issue
An agent instance's health check oscillates rapidly between healthy and unhealthy — not because the instance is genuinely alternating between working and broken, but because the check itself is measuring something noisy near a hard threshold (e.g., LLM inference latency hovering right around a 2-second cutoff, or memory usage from a request-scoped context cache sawtoothing above and below a limit). Each flip triggers the orchestrator to pull the instance from rotation and then add it back, repeatedly, which causes constant partial-capacity loss, connection churn for any in-flight sessions on that instance, and load balancer/service-mesh reconfiguration overhead — all without the instance ever being reliably unhealthy or reliably healthy.

**Frequency**: Common

**Symptoms**
- An instance's rotation status (in/out of load balancer pool) toggles multiple times within a short window, visible as rapid alternation in orchestrator logs
- Aggregate fleet capacity dips and recovers repeatedly with no corresponding change in actual request volume
- Sessions on a flapping instance are intermittently disrupted even though the instance is "healthy" more often than not
- Health check metric (latency, memory, custom readiness signal) sits close to its threshold rather than clearly above or below it
- Autoscaler reacts to the flapping by cycling replacement instances, adding churn without addressing the underlying noisy signal

## Root Cause
Health checks are typically implemented as a single point-in-time measurement compared against a fixed threshold, evaluated on a short interval, with no smoothing or hysteresis between the healthy and unhealthy states. Agent workloads produce especially noisy raw signals for common health-check dimensions — LLM call latency varies run to run with upstream provider load, memory usage swings with the size of the conversation context currently being processed, request queue depth spikes with bursty tool-call fan-out — so a signal that averages comfortably within bounds still crosses a hard threshold on individual samples. Without hysteresis (different thresholds for going unhealthy versus recovering) or a required number of consecutive failing/passing checks before changing state, any threshold set close to the signal's natural noise band will flap, and tightening the threshold to be more "correct" often makes the flapping worse rather than better because it moves the boundary deeper into the noise.

## Example
```
"InferenceGateway" pods run a readiness probe every 5 seconds:
HTTP 200 required within 2000ms from a lightweight /health endpoint
that also checks current request queue depth (< 50 pending).

Under normal-to-moderately-busy traffic, queue depth for a given pod
oscillates between 35 and 55 as tool-call-heavy conversations arrive
in bursts and drain. This puts it right across the 50 threshold on
roughly a third of probe intervals.

12:10:00 - queue depth 47, probe passes, pod stays "Ready."
12:10:05 - queue depth 53, probe fails, orchestrator marks pod
NotReady, load balancer stops sending new sessions to it, and 4
in-flight sessions get their next request routed to a different pod
mid-conversation (breaking any pod-local context cache they had).
12:10:10 - queue depth 41 (partly because it just got pulled from
rotation), probe passes, pod marked Ready again, sessions resume
routing to it.
12:10:15 - queue depth 52, fails again.

Over a 10-minute window, this single pod flaps 34 times. Fleet-wide,
several pods are doing the same thing independently, so effective
serving capacity is undercounted by the load balancer at almost all
times even though aggregate queue depth across the whole fleet is
well within safe bounds.
```

## Statistics
| Finding | Context |
|---------|---------|
| Health check thresholds set within the normal operating noise band of the underlying signal are a common cause of flapping in latency- and queue-depth-based checks | Typical finding across teams reviewing flapping incidents |
| Adding hysteresis (distinct thresholds for marking unhealthy vs. recovering) and requiring multiple consecutive failures substantially reduces flap frequency | Reported range across teams that added consecutive-check requirements |
| Flapping instances are frequently undercounted as "available capacity" by autoscalers, contributing to unnecessary scale-out during otherwise normal load | Estimated from teams correlating flap events with autoscaling activity |

## Mitigations
1. **Hysteresis between unhealthy and healthy thresholds**: Use a stricter threshold to mark an instance unhealthy than to mark it healthy again (e.g., unhealthy at queue depth > 60, healthy again only below 40), so noise near a single boundary can't cause rapid toggling.
2. **Consecutive-check requirements**: Require multiple consecutive failing checks before removing an instance from rotation, and multiple consecutive passing checks before re-adding it, rather than reacting to any single sample.
3. **Smoothed/windowed health signals**: Base the health determination on a rolling average or percentile over a short window rather than the instantaneous value of a single noisy metric.
4. **Separate readiness from liveness semantics**: Distinguish "temporarily busy, don't send new work" (which shouldn't disrupt in-flight sessions) from "genuinely broken, restart me" (which should), so transient load doesn't trigger the same disruptive rotation-pull as an actual failure.
5. **Flap-rate monitoring with automatic threshold review**: Track how often each instance's health state toggles and flag any that flap beyond a reasonable rate for threshold retuning, rather than letting a persistently noisy check keep degrading capacity indefinitely.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| health_state_transitions_per_hour | Count of healthy/unhealthy toggles for a single instance | Alert if > 6 per hour for any instance |
| flapping_instance_count | Number of instances currently exceeding the flap-rate threshold | Alert if > 5% of fleet |
| effective_capacity_loss_from_flapping | Estimated serving capacity unavailable due to instances mid-flap versus genuinely unhealthy | Alert if > 10% of fleet capacity |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Instance flapping detected | health_state_transitions_per_hour exceeds threshold for one or more instances | Medium | Review threshold/hysteresis config for the failing check, inspect underlying signal noise |
| Fleet-wide flap-driven capacity loss | flapping_instance_count and effective_capacity_loss_from_flapping both elevated simultaneously | High | Widen hysteresis or consecutive-check requirement fleet-wide, check for a systemic load pattern driving the noise |

## Related Patterns
- [Circuit Breaker False Positive](./circuit-breaker-false-positive.md) - closely related instability where a threshold-based gate trips on noise rather than genuine sustained failure
- [Canary Deployment Incomplete](./canary-deployment-incomplete.md) - a flapping health signal can be one reason canary promotion metrics never resolve cleanly to a promote or rollback decision
- [Sticky Session Loss](./sticky-session-loss.md) - each flap that pulls an instance from rotation is a concrete mechanism by which in-flight session affinity gets broken
