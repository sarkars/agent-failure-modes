# Cascade Timeout Interaction

## Issue
Different layers in a call chain are configured with timeout values that were each set reasonably in isolation but interact badly when combined, actively amplifying a cascade instead of bounding it. The classic bad pattern is an upstream timeout that is shorter than or too close to a downstream timeout, so the caller gives up and retries while the original call is still in flight and still consuming resources on the downstream system — doubling load without reducing it. This is a distinct, specific mechanism from general cascade-amplification: the trigger here is specifically the numeric relationship between timeout values at different layers, not retry policy or resilience-mechanism design broadly.

**Frequency**: Common

**Symptoms**
- A caller's timeout fires and it retries or gives up, but the original downstream request keeps running to completion, consuming resources for no benefit
- Nested calls show timeout values that increase in the wrong direction — an inner call's timeout is longer than the outer call's timeout that wraps it
- Load on a struggling downstream service does not decrease despite upstream errors, because "failed" requests upstream are still active downstream
- Incident timelines show total in-flight request count on a downstream service far exceeding the concurrency the upstream caller believes it is sending

## Root Cause
Timeout values are usually set independently at each layer by whichever team owns that layer, calibrated against that layer's own latency expectations, without a shared, enforced rule that outer timeouts must always be strictly greater than the sum of inner timeouts plus their retry budgets. When an inner (downstream) timeout is equal to or longer than an outer (upstream) timeout, the upstream caller times out and moves on — often retrying — while the downstream operation is still consuming a thread, a connection, or CPU, unaware that the caller has already abandoned it. Under normal conditions this mismatch is invisible because everything completes well within all timeouts; it only becomes catastrophic once the downstream service is already somewhat slow, at which point the mismatch turns every upstream timeout into extra, uncancelled downstream load, which slows the downstream service further, which causes more upstream timeouts.

## Example
```
Call chain: API Gateway (5s timeout) -> Orchestration Agent (8s timeout) 
            -> Search Service (10s timeout) -> Vector DB (no timeout set)

Under normal load: Vector DB responds in 200ms, everything completes
well within all four timeout budgets.

16:20:00 - Vector DB index compaction job runs, slowing query latency
           from 200ms to 6s for a subset of shards.

16:20:05 - Search Service, with its 10s timeout, is still waiting.

16:20:05 - Orchestration Agent's 8s timeout has NOT yet fired (6s < 8s),
           so this particular call is still fine. But some queries hit
           slower shards taking 9s.

16:20:09 - For those slower queries, API Gateway's 5s timeout fires
           FIRST (5s < 8s < 10s — the timeouts increase in the wrong
           direction relative to caller-to-callee order). API Gateway
           returns a 504 to the end user and, per its retry policy,
           immediately re-issues the request.

16:20:09 - The ORIGINAL request is still running in Orchestration Agent,
           Search Service, and Vector DB — nothing downstream was told
           to cancel. The retried request starts a second full chain of
           calls, doubling load on Search Service and Vector DB for
           every gateway-level timeout.

16:20:30 - With Vector DB now serving roughly double its normal
           concurrent query load (originals plus retries, none
           cancelled), average query latency crosses 9s for most shards,
           triggering gateway timeouts and retries on nearly all
           traffic. Full outage within 90 seconds of the initial index
           compaction slowdown.
```

## Statistics
| Finding | Context |
|---------|---------|
| A large share of retry-amplification incidents trace back to an outer timeout shorter than an inner timeout somewhere in the call chain | Estimated from postmortem categorization of timeout-related cascades |
| Systems without a hard rule enforcing outer > inner timeout budgets are reported to have measurably higher rates of retry-driven outages | Typical range observed across service-mesh timeout audits |
| Adding request cancellation propagation (so a caller's timeout cancels the downstream call) is reported to substantially cut uncancelled-work load during timeout cascades | Reported range across teams adopting context-based cancellation |

## Mitigations
1. **Strict timeout budget hierarchy**: Enforce as a design/lint rule that every outer-layer timeout must exceed the sum of its inner-layer timeout plus retry budget, never the reverse, across the entire call chain.
2. **Propagate cancellation, not just timeouts**: When an upstream caller times out, actively propagate a cancellation signal downstream (e.g. context cancellation, request abortion) so downstream work stops consuming resources instead of running to completion unobserved.
3. **Deadline propagation instead of independent timeouts**: Pass a single absolute deadline through the whole call chain so every layer computes its remaining budget from the same clock, rather than each layer having an independently-configured, potentially mismatched fixed timeout.
4. **Timeout configuration audits as part of dependency reviews**: Whenever a new service-to-service dependency is added, require an explicit review of the full timeout chain end-to-end, not just the new hop in isolation.
5. **No-timeout dependencies treated as an isolation-failure risk**: Flag any component in the call chain (like the Vector DB in the example) with no timeout configured at all as a specific risk requiring remediation, since it removes the natural backpressure a timeout would otherwise provide.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| timeout_hierarchy_violation_count | Count of configured service pairs where an outer timeout is not strictly greater than inner timeout + retry budget | Alert if > 0 in production config |
| uncancelled_work_ratio | Ratio of downstream requests still in flight after their corresponding upstream caller has timed out | Alert if > 5% during incidents |
| in_flight_request_count_vs_expected | Actual concurrent in-flight requests on a downstream service versus what upstream concurrency limits imply | Alert if actual exceeds expected by > 50% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Timeout hierarchy violation in config | A deploy introduces or contains a timeout chain violating the outer > inner rule | High | Block deploy or require explicit sign-off, flag for immediate remediation |
| Uncancelled work spike | uncancelled_work_ratio crosses threshold during a live incident | High | Trigger downstream load shedding, alert dependency owner to enable cancellation propagation |

## Related Patterns
- [Cascade Amplification](./cascade-amplification.md) - timeout misconfiguration is one of the most common specific triggers for the general amplification pattern
- [Cascade Resilience Failure](./cascade-resilience-failure.md) - describes the broader family of resilience mechanisms (including retries driven by bad timeouts) contributing to cascades
- [Failover Delay Too Long](./failover-delay-too-long.md) - timeout misconfiguration can also directly cause failover to be triggered later than intended, or not at all
