# Feature Flag Toggle Lag

## Issue
An operator flips a feature flag controlling agent behavior — for example, disabling a newly-launched tool that's producing bad outputs, or switching the active system-prompt variant — expecting the change to take effect immediately across the fleet. In reality, flag state propagates to running agent instances on a delay: some instances poll the flag service on an interval, some cache the value in memory for a TTL, some read it only once at process startup. For anywhere from tens of seconds to several minutes, different agent instances (and sometimes different requests within the same instance) are operating on inconsistent flag state, so some users get the old behavior and some get the new one simultaneously, and an emergency kill-switch doesn't actually stop the behavior it was meant to stop right away.

**Frequency**: Very Common

**Symptoms**
- Flag dashboard shows the new value as "active" but a meaningful share of live requests still exhibit old-value behavior
- An emergency flag flip intended to immediately disable a misbehaving tool/prompt doesn't stop the bad behavior for a noticeable window
- Different concurrent sessions from the same user, or the same session's sequential turns, get inconsistent behavior depending on which instance handled the request
- Support/on-call assumes a flag flip "didn't work" and takes further escalatory action (e.g., a full redeploy) that was unnecessary and just needed time
- Flag propagation delay is not documented or known by the people who rely on flags for incident response

## Root Cause
Feature flag systems trade consistency for scalability by default: rather than pushing every toggle to every instance synchronously (which would create a thundering-herd load on the flag service at flip time and a single point of failure), most implementations have each instance pull or long-poll flag state on its own interval, often with local in-memory caching to avoid a network round-trip on every request. This is a reasonable design for gradual feature rollouts where a few minutes of inconsistency is harmless, but it is silently reused for kill-switch and incident-response use cases where the whole point is immediate, uniform effect. Nobody has separately modeled "this flag is a safety kill-switch and needs sub-second propagation" versus "this flag is a slow rollout dial and a few minutes of skew is fine" — both go through the same polling/caching path with the same default TTL.

## Example
```
"ToolPolicyAgent" fleet (140 instances) uses a feature flag,
"enable_web_search_tool", read from a flag service with a 60-second
client-side cache TTL per instance, refreshed on a background poll.

14:02:00 - the web-search tool starts returning malformed results
that cause the agent to hallucinate citations. On-call flips
enable_web_search_tool to false via the flag dashboard.

14:02:00 - flag dashboard immediately shows "false" and the person
who flipped it moves on to the next incident-response step,
believing the tool is now disabled fleet-wide.

14:02:00-14:03:00 - each of the 140 instances is at a different
point in its 60-second cache cycle. Instances that last polled at
14:01:50 won't re-poll until 14:02:50. During this window, roughly
half the fleet still has web search enabled and continues generating
hallucinated-citation responses.

14:02:40 - on-call, seeing continued reports of bad citations,
concludes the flag flip "isn't working" and starts a full
emergency redeploy with the tool hardcoded off - a much slower,
riskier action than just waiting 20 more seconds for the caches to
naturally expire, and one that itself introduces a new deployment
during an active incident.
```

## Statistics
| Finding | Context |
|---------|---------|
| Client-side flag cache TTLs in the tens-of-seconds-to-minutes range are a common default across teams that haven't distinguished kill-switch flags from rollout-dial flags | Typical pattern reported across teams using off-the-shelf flag services |
| Incident responders frequently escalate to a redeploy or other heavier remediation before flag propagation alone would have resolved the issue | Estimated from post-incident reviews involving flag-based mitigations |
| Push-based or short-TTL kill-switch flags reduce propagation time from minutes to low seconds in teams that have implemented a separate fast path | Reported range across teams maintaining a distinct kill-switch flag class |

## Mitigations
1. **Separate fast-path kill-switches from rollout dials**: Classify flags explicitly as "kill-switch" (push-based, sub-second propagation, no caching) versus "rollout dial" (poll-based, cache-tolerant) at creation time, and route them through different propagation mechanisms.
2. **Push-based propagation for critical flags**: For flags used in incident response, use a push mechanism (webhook, streaming connection, pub/sub) that notifies instances immediately rather than relying on the next poll interval.
3. **Document and surface known propagation delay**: Make the expected propagation time for each flag visible in the flag dashboard itself, so on-call knows to wait out a known delay rather than assuming a flip failed and escalating unnecessarily.
4. **Propagation confirmation telemetry**: Emit a metric showing what fraction of the live fleet has actually picked up the latest value of a given flag, so operators can watch propagation complete in real time instead of guessing.
5. **Reduce or eliminate caching for safety-critical flags**: For the small subset of flags used as kill-switches, accept the added read load and query the flag service directly per-request (or with a very short TTL, e.g., 1-2 seconds) rather than using the same longer TTL applied to non-critical flags.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| flag_propagation_lag_p99 | Time between a flag value change and the last fleet instance observing it | Alert if > 60s for flags tagged "kill-switch" |
| flag_value_skew_fleet_share | Percentage of fleet instances holding a stale flag value at a given moment | Alert if > 10% more than 2 minutes after a change |
| kill_switch_ineffective_window | Duration between a kill-switch flip and the monitored bad behavior actually stopping | Alert if > 30s |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Kill-switch propagation delayed | kill_switch_ineffective_window exceeds threshold after an emergency flag flip | High | Confirm propagation status per instance, avoid escalating to redeploy until propagation window elapses, investigate cache/poll config |
| Persistent flag skew | flag_value_skew_fleet_share stays elevated well past expected TTL | Medium | Check flag service health, verify instances are polling successfully, investigate stuck instances |

## Related Patterns
- [Traffic Routing Asymmetry](./traffic-routing-asymmetry.md) - both produce inconsistent behavior across concurrent requests due to state that hasn't uniformly propagated
- [Sticky Session Loss](./sticky-session-loss.md) - flag skew combined with session routing can compound into a single user seeing wildly different behavior turn to turn
- [Canary Deployment Incomplete](./canary-deployment-incomplete.md) - flags are sometimes used as a lighter-weight substitute for canary rollout, and share the same "believed complete but actually partial" failure shape
