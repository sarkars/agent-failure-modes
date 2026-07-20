# Sticky Session Loss

## Issue
A multi-turn agent conversation relies on session affinity — the load balancer routing every request in that conversation to the same backend instance, which holds in-memory conversation state, a warm context cache, or an in-progress multi-step tool-calling loop — but a deployment, instance rotation, or connection-pool rebalancing breaks that affinity mid-conversation. The next turn gets routed to a different instance that has no knowledge of what came before, and depending on how the system handles the mismatch, the user either gets a jarring "who are you, what were we talking about" response, silently loses in-progress tool-call context, or triggers a duplicate action because the new instance re-executes a step the original instance had already completed.

**Frequency**: Common

**Symptoms**
- A single conversation's turns show requests landing on different backend instance IDs in access logs, despite session-affinity configuration being present
- Users report the agent "forgetting" recent context mid-conversation, especially right after a known deployment window
- Duplicate tool-call side effects (two calendar events, two support tickets) traced to the same logical action being re-attempted by a second instance that didn't know the first had already handled it
- Session-affinity cookie or routing key is present and valid, but the target instance it points to no longer exists (was terminated during a rollout)
- Affinity-loss incidents cluster tightly around deployment and autoscaling events rather than occurring uniformly throughout the day

## Root Cause
Session affinity is typically implemented as a mapping (cookie, consistent-hash ring, or explicit routing table) from a session identifier to a specific backend instance, which works as long as that instance keeps existing and keeps being a valid, healthy target. Deployments and autoscaling events routinely terminate and replace instances, and unless the affinity mechanism has an explicit rebinding strategy for "the instance this session was pinned to is gone," the default behavior is either to fail the request, silently fall back to a new instance with no session context, or — in consistent-hash setups — reshuffle a disproportionate number of sessions onto new instances all at once when the pool membership changes. Agent workloads are more exposed to this than typical stateless web services because they're more likely to actually depend on instance-local state (an in-memory conversation buffer, a locally-cached embedding, an in-progress tool-call loop) rather than treating every request as independently reconstructable from a shared external store, so the loss of affinity is not just a performance hit but a correctness/continuity break.

## Example
```
"SupportAgent" fleet uses consistent-hash session affinity keyed on
conversation_id, routing all turns of a conversation to the same pod
where a 20-turn rolling context window and a partially-completed
3-step "process refund" tool-call sequence live in local memory
(chosen for latency reasons over round-tripping to a shared store on
every turn).

A routine autoscale-down event removes 15% of pods to match reduced
evening traffic. The consistent-hash ring rebalances, and per the
mechanics of hash-ring rebalancing, roughly 15% of ALL sessions
(not just those that were on the removed pods) get reassigned to a
different pod than before, including a conversation that was
mid-refund: step 1 (verify order) and step 2 (calculate refund
amount) had completed on the original pod, step 3 (issue refund) was
about to run.

The user's next message routes to a new pod with no memory of steps
1-2. The new pod's agent logic, seeing no in-progress refund state,
restarts the flow from step 1: "I'd be happy to help you with a
refund - can you provide your order number?" The user, who had
already provided it two messages ago, is confused and frustrated,
and if the flow isn't idempotency-checked, there's a risk of the
refund being calculated and issued twice if session state had
instead been closer to completion.
```

## Statistics
| Finding | Context |
|---------|---------|
| Consistent-hash rebalancing on pool membership change commonly reshuffles a share of sessions well beyond just those on removed/added instances, unless a bounded-rebalancing scheme is used | Typical characteristic of naive consistent-hash implementations |
| Affinity-loss incidents are disproportionately clustered around deployment and autoscaling events rather than distributed evenly | Estimated from teams correlating session-continuity complaints with infrastructure event timestamps |
| Externalizing session state to a shared store (versus keeping it instance-local) eliminates the correctness impact of affinity loss, though not the latency cost, in teams that have made the change | Reported range across teams that migrated from in-memory to externalized session state |

## Mitigations
1. **Externalize session state**: Store conversation state, in-progress tool-call sequences, and context caches in a shared, fast external store (e.g., a low-latency key-value store) rather than instance-local memory, so any instance can pick up a session with full context regardless of routing.
2. **Bounded-impact rebalancing**: If session affinity must remain, use a rebalancing scheme (e.g., bounded-load consistent hashing) that minimizes the number of sessions reassigned when pool membership changes, rather than one that reshuffles a large fraction of all sessions on any single membership change.
3. **Graceful affinity-loss handling**: Design the application layer to detect when it's receiving a request for a session it has no local context for, and explicitly reconstruct or request the missing state (from an external store or by asking the user to confirm) rather than silently restarting the flow from scratch or duplicating an action.
4. **Idempotent multi-step tool sequences**: Make each step in a multi-step tool-call flow (like a refund process) idempotent and checkable against persisted progress, so a session picked up by a new instance can safely determine what's already been done rather than blindly re-executing it.
5. **Drain-aware affinity migration during planned events**: For deployments and planned scale-downs (as opposed to unplanned failures), proactively migrate session state to the new target instance before removing the old one, rather than letting the next request discover the break reactively.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| session_instance_reassignment_rate | Share of active sessions whose routing target changes within a rolling 10-minute window | Alert if > 5% outside of a planned deployment |
| context_loss_incidents | Count of requests where the serving instance reports no local state for a session ID it should have context for | Alert if > 0.5% of multi-turn sessions |
| duplicate_tool_action_rate | Rate of the same logical tool action being executed more than once for a single session | Alert on any sustained occurrence |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Mass session reassignment during scaling event | session_instance_reassignment_rate spikes correlated with an autoscale or deploy event | Medium | Verify externalized state or graceful migration is functioning, monitor for context-loss reports |
| Duplicate side-effecting tool action detected | duplicate_tool_action_rate registers a nonzero event for a side-effecting tool | High | Manually reconcile the duplicated action, review idempotency guards for the affected tool flow |

## Related Patterns
- [Connection Draining Incomplete](./connection-draining-incomplete.md) - both concern in-flight session continuity breaking during infrastructure changes, one via forced termination and one via routing change
- [Feature Flag Toggle Lag](./feature-flag-toggle-lag.md) - can compound with affinity loss so a single conversation sees both a routing change and a behavior change mid-session
- [Traffic Routing Asymmetry](./traffic-routing-asymmetry.md) - a broader category of routing inconsistency that sticky-session loss is one specific instance of
