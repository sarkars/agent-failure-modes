# Livelock in Multi-Agent

## Issue
Two or more agents, each trying to politely avoid conflicting with the other, keep changing their behavior in response to each other's changes without ever converging on a state where actual work gets done. Unlike deadlock, none of the agents are blocked or waiting — they are all actively "working," consuming compute and making API calls — but the net forward progress on the task stays at zero because each agent's reaction to the other keeps resetting the situation back to an equivalent unresolved state.

**Frequency**: Occasional

**Symptoms**
- Agents that show high activity (CPU, API calls, message volume) but the task's actual completion percentage never advances
- Two agents repeatedly yielding to each other, retrying, or reversing their own action in direct response to the other's most recent action
- Logs showing a repeating cycle of the same handful of states across agents, with no new state ever reached
- The system eventually resolves only after an external intervention (a random delay, a manual kill, a forced priority) breaks the cycle
- Symptom is often mistaken for normal "in progress" activity until someone checks task completion over a longer time window

## Root Cause
Livelock typically emerges from well-intentioned conflict-avoidance logic: when two agents detect they're both about to act on the same resource or make conflicting decisions, each is designed to defer or retry rather than proceed, to avoid the class of failure described in resource-contention or race-condition patterns. But if both agents use the same (or symmetric) deferral logic — "if I detect a conflict, I'll back off and let the other one go first" — and they detect the conflict at the same moment, they can both back off simultaneously, then both retry simultaneously, forever. The system oscillates between two (or more) states that are each individually "safe" from the conflict they were designed to avoid, but the avoidance mechanism itself has no randomization or escalating priority to break the symmetry.

## Example
```
Two warehouse-routing agents (Agent-North and Agent-South) share a single
narrow conveyor junction and are both designed with identical
"yield-on-conflict" logic: if I detect the junction is about to be needed
by another agent's item at the same time as mine, I'll pause for one
tick and let the other go first.

Tick 1: Agent-North's item and Agent-South's item both arrive at the
        junction's approach sensor simultaneously.
Tick 1: Both agents detect the conflict and, per their identical logic,
        both decide to yield -- neither item enters the junction.
Tick 2: Both items are still waiting at the approach sensor (nothing
        changed), so both agents detect the same conflict again and
        both yield again.
Tick 3-40: The pattern repeats exactly, tick after tick. Both agents
           report "active, awaiting clear junction" in their status
           logs. Throughput on both lines drops to zero for the full
           duration, but no error or timeout fires because neither
           agent considers "yielding" to be a failure state.
Tick 41: A maintenance engineer notices the conveyor hasn't moved in
         over a minute, manually forces Agent-South to proceed, and the
         junction clears immediately.
```

## Statistics
| Finding | Context |
|---------|---------|
| Livelock is reported as materially rarer than deadlock in production multi-agent systems, but harder to detect because standard health checks show agents as active | Typical qualitative finding across reported multi-agent operational reviews |
| Symmetric conflict-avoidance logic without randomized backoff is estimated to produce livelock in a meaningful minority of simultaneous-conflict events under high concurrency | Estimated from instrumented conflict-resolution logs in warehouse/routing style systems |
| Adding randomized backoff or priority tie-breaking is reported to eliminate the large majority of observed livelock cycles | Reported range across teams that added asymmetry to conflict-avoidance logic |

## Mitigations
1. **Randomized backoff on conflict**: When two agents detect a simultaneous conflict, have each choose a random delay before retrying rather than a fixed or symmetric rule, breaking the synchronization that causes repeated identical outcomes.
2. **Deterministic tie-breaking**: Assign each agent a fixed priority or ID and use it to deterministically decide who proceeds on conflict (e.g. lower ID always wins), removing the ambiguity that causes both to defer.
3. **Progress detection with forced escalation**: Track how many consecutive cycles have passed without net progress on a task, and after a threshold, force one agent to proceed unconditionally (or escalate to a human/coordinator) regardless of the conflict-avoidance logic.
4. **Asymmetric roles for shared-resource negotiation**: Where two agents regularly contend for the same resource, give them explicitly asymmetric behavior (one always yields, one always proceeds, or a rotating designated "proceeder") rather than identical logic on both sides.
5. **Livelock-aware monitoring distinct from liveness checks**: Monitor task-completion progress over time, not just agent activity/heartbeat, since livelocked agents pass standard liveness checks while making zero forward progress.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| task_progress_stall_duration | Time since the task's completion percentage last advanced, despite agents showing active status | Alert if > 30s for real-time systems |
| repeated_state_cycle_count | Number of times the same agent-state combination has recurred consecutively | Alert if > 5 |
| conflict_yield_rate | Fraction of conflict detections resulting in both/all agents yielding simultaneously | Alert if > 10% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Livelock suspected | Agents active but task progress stalled beyond threshold | High | Page on-call, force priority tie-break or manual proceed on one agent |
| Repeated symmetric yield cycle | The same conflict-and-yield state recurs beyond threshold count | Medium | Review conflict-avoidance logic for missing randomization/tie-breaking |

## Related Patterns
- [Deadlock in Multi-Agent](./deadlock-in-multi-agent.md) - the counterpart failure where agents are fully blocked rather than actively but unproductively cycling
- [Agent Resource Contention](./agent-resource-contention.md) - livelock frequently emerges from conflict-avoidance logic built to manage resource contention
- [Agent Priority Inversion](./agent-priority-inversion.md) - both can be resolved by introducing an explicit priority or tie-breaking mechanism where none previously existed
