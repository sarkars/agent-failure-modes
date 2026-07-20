# Cascade Amplification

## Issue
An agentic system experiences a small, low-severity failure in one component — a single slow dependency, a handful of dropped requests, a brief queue backup — and instead of staying proportionate, the failure grows in magnitude as it propagates through downstream components. Each hop adds retries, duplicate work, or overcorrection, so a fault that started as a 2% error rate in one service arrives at the edge of the system as a full outage. The agent-specific twist is that autonomous retry loops and multi-step planning amplify faster than in traditional systems, because an agent facing a transient tool failure often retries the entire multi-step plan rather than the single failed call.

**Frequency**: Common

**Symptoms**
- Error or latency magnitude grows at each hop in a call graph rather than staying flat or decaying
- A root-cause incident rated low-severity in its origin service produces a high-severity incident several services downstream
- Retry storms coincide with the amplification, with request volume rising well above baseline at each successive layer
- Postmortems show the triggering event was minor (single-digit percent error rate or a few seconds of added latency) but the customer-facing impact was total unavailability

## Root Cause
Amplification happens when each layer in a dependency chain reacts to a failure by doing more work than the failure itself caused — retrying with the same or larger payload, re-running an entire agent plan instead of the one failed step, or fanning a single failed call out to multiple compensating calls. Because each layer's retry/compensation policy is set independently, without visibility into how many layers are already retrying upstream or downstream, the multiplicative effect compounds silently. Agents make this worse because a plan-level retry re-issues every tool call in a step sequence when only the last one failed, multiplying load by the length of the plan rather than by 1.

## Example
```
Service graph: Agent Orchestrator -> Planning Service -> Inventory API -> 
Warehouse DB (read replica).

10:02:00 - Warehouse read replica experiences a 3-second GC pause. 
           Query latency briefly rises from 40ms to 3,000ms for ~1,800 queries.

10:02:03 - Inventory API's client has a 1s timeout with an internal retry of 2x
           per call. Those 1,800 slow queries become 3,600 requests as the
           API retries each once.

10:02:05 - Planning Service calls Inventory API for 6 line items per plan.
           When any one of the 6 sub-calls times out, Planning Service retries
           the FULL 6-call batch rather than the single failed sub-call.
           Effective load on Inventory API roughly doubles again.

10:02:08 - Agent Orchestrator's plan executor sees the Planning Service call
           exceed its 5s SLA and re-runs the entire 12-step agent plan for
           the affected sessions, re-issuing Planning Service calls that had
           already succeeded.

10:02:20 - Inventory API, now receiving ~15x its normal load, exhausts its
           connection pool and returns 503s to ALL callers, not just the
           ones affected by the original replica pause.

10:04:00 - Full outage declared. Root cause: a 3-second GC pause on one
           read replica.
```

## Statistics
| Finding | Context |
|---------|---------|
| A single-digit-percent upstream error rate can translate into 5-15x downstream load within 2-3 hops when each layer retries independently | Typical range observed in multi-tier agent call graphs with uncoordinated retry policies |
| Plan-level (whole-plan) retries amplify load by a factor roughly equal to plan step count, versus 1x for step-level retries | Estimated from agent orchestration postmortems |
| Systems with per-hop retry budgets or amplification caps see 60-80% smaller blast radius for equivalent origin faults | Reported range across teams that added amplification guards |

## Mitigations
1. **Retry budgets, not per-call retries**: Enforce a global retry budget per request chain (e.g. no more than 10% of traffic may be retries) so each layer's independent retry policy cannot multiply unboundedly.
2. **Step-level, not plan-level, retry**: Design agent plan executors to retry only the specific failed tool call, with the results of already-succeeded steps cached and reused, rather than re-running the whole plan.
3. **Deadline propagation**: Pass a single end-to-end deadline down the call chain so downstream layers know how much time is left and shed load or fail fast instead of independently retrying against an already-exhausted budget.
4. **Amplification-aware circuit breakers**: Trip a breaker not just on absolute error count but on the ratio of observed load to expected load, catching amplification before it saturates the next layer.
5. **Load shedding at the edge**: When a service detects it is receiving more retried/duplicate traffic than normal, shed the excess rather than passing the full amplified volume to its own dependencies.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| retry_amplification_ratio | Ratio of actual request volume to expected baseline volume at each hop | Alert if > 2x baseline |
| plan_level_retry_count | Count of full agent-plan re-executions triggered by a single downstream failure | Alert if > 5/min |
| cross_hop_error_rate_delta | Difference between origin-service error rate and edge-service error rate for the same incident | Alert if edge rate > 3x origin rate |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Amplification ratio spike | retry_amplification_ratio exceeds 2x for any service in the chain | High | Engage incident commander, enable emergency retry budget cap |
| Full-plan retry storm | plan_level_retry_count exceeds threshold within a 1-minute window | Medium | Disable plan-level retry fallback, force step-level retry only |

## Related Patterns
- [Cascade Branching](./cascade-branching.md) - amplification grows a single cascade's magnitude, branching spreads it across independent subsystems
- [Cascade Resilience Failure](./cascade-resilience-failure.md) - describes how the retry/circuit-breaker mechanisms meant to help are frequently the amplification mechanism itself
- [Cascade Timeout Interaction](./cascade-timeout-interaction.md) - mismatched timeouts across layers are one of the primary triggers for amplification
