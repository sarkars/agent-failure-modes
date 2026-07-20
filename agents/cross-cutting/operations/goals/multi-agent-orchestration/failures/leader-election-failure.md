# Leader Election Failure

## Issue
A multi-agent system that relies on one agent being designated "leader" or "coordinator" (to assign work, break ties, or serialize decisions) fails to establish or maintain a single clear leader. Either no agent successfully claims leadership, multiple agents each believe themselves to be leader simultaneously (split-brain), or leadership flaps rapidly between candidates, leaving the system without the coordination guarantee the architecture depends on.

**Frequency**: Occasional

**Symptoms**
- Two or more agent instances simultaneously acting as if they hold exclusive leader responsibilities
- Work being assigned twice by two different "leaders," or not assigned at all because each assumes another leader will handle it
- Frequent leadership handoff events in logs, with no stable leader holding the role for more than a few seconds
- Followers that stop receiving heartbeats from a leader but also can't confirm a new leader was elected, so they stall
- Split-brain symptoms appearing specifically after network partitions, deployments, or scaling events

## Root Cause
Leader election requires a mechanism (a consensus protocol like Raft/Paxos, a distributed lock with a lease, or a designated external coordinator) that guarantees at most one agent holds the leader role at any given time, even under network partitions or process crashes. Common failure sources are: using a leader-election primitive that doesn't handle partitions correctly (e.g. a simple "first to write a flag" approach with no fencing token, vulnerable to two agents writing during a partition and both believing they won); leases that expire without the old leader knowing to step down, so it keeps acting as leader after a new one has already been elected; or election storms triggered by transient heartbeat misses, where multiple agents simultaneously detect a (false) leader absence and simultaneously try to become the new leader, causing repeated re-elections that never stabilize.

## Example
```
A distributed task-scheduling system elects a leader agent to assign
work batches to a pool of 12 worker agents, using a simple
"write-a-flag-in-shared-storage" leader election with a 10-second lease
and no fencing token.

14:00:00 - Agent-7 holds the leader lease, renewing it every 3 seconds.
14:00:41 - A network partition isolates Agent-7 from the shared storage
           for 12 seconds (longer than the 10s lease), though Agent-7
           itself keeps running and believes it is still leader.
14:00:51 - The lease expires. Agent-3, watching for lease expiry,
           acquires the lease and becomes the new leader, starting to
           assign work batches.
14:00:53 - The network partition heals. Agent-7, unaware its lease
           expired, successfully renews what it believes is its own
           lease (overwriting Agent-3's claim, since there was no
           fencing token to detect the stale writer).
14:00:54 - Both Agent-3 and Agent-7 now believe they are leader. Each
           independently assigns work batch #4471 to two different
           workers, who both process the same batch, doubling the
           compute cost and producing two conflicting result sets.
14:01:10 - A downstream consolidation job detects the duplicate batch
           results and pages on-call.
```

## Statistics
| Finding | Context |
|---------|---------|
| Split-brain leader states are estimated to occur in a small fraction of leader-election cycles, but disproportionately during network partitions and deployments | Typical qualitative finding across reported distributed-systems incident writeups |
| Election implementations without fencing tokens are estimated to be several times more likely to produce a split-brain window during a partition-then-heal event than implementations with them | Estimated from reviews of leader-election incident postmortems |
| Adopting a proven consensus protocol (Raft/Paxos-based) with fencing tokens is reported to reduce split-brain incidents by the large majority compared to ad hoc flag-based election | Reported range across teams migrating from custom to standard consensus implementations |

## Mitigations
1. **Fencing tokens on every leader action**: Have the leader attach a monotonically increasing token to every action it takes, and have all downstream consumers reject actions from a token lower than the highest one they've already seen, so a stale leader's actions after losing leadership are ignored.
2. **Proven consensus protocol**: Use an established consensus implementation (Raft, Paxos, or a managed equivalent) for leader election rather than a custom flag-in-storage approach, since these protocols are specifically designed to handle partition-and-heal scenarios correctly.
3. **Leader self-demotion on lease expiry**: Require the leader itself to actively check its own lease validity before every leadership action and immediately step down if it can't confirm the lease is current, rather than assuming it's still leader until told otherwise.
4. **Election hysteresis / backoff**: Add randomized delay and confirmation steps before a candidate declares itself leader, and require sustained (not momentary) evidence of leader absence before triggering a new election, to prevent election storms from transient heartbeat misses.
5. **Split-brain detection and reconciliation**: Continuously monitor for the case where two agents are both acting as leader (e.g. via periodic cross-checks against shared storage) and have an automatic or paged reconciliation path to force one to step down.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| concurrent_leader_claims | Number of agent instances simultaneously believing they hold leadership | Alert if > 1 |
| leadership_change_rate | Number of leader handoffs per unit time | Alert if > 3 in 5 min |
| stale_leader_action_count | Actions taken by a leader after its fencing token was superseded | Alert if > 0 |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Split-brain leadership detected | Two or more agents observed acting as leader concurrently | High | Page on-call, force step-down of stale leader via fencing, audit duplicated actions |
| Election storm | Leadership changes exceed threshold within a short window with no stable leader | High | Investigate heartbeat/network health, apply election backoff |

## Related Patterns
- [Byzantine Agent Failure](./byzantine-agent-failure.md) - Byzantine fault tolerance in consensus protocols directly addresses election correctness under arbitrary or adversarial agent behavior
- [Agent State Divergence](./agent-state-divergence.md) - split-brain leadership is a specific and severe form of state divergence about who is authoritative
- [Deadlock in Multi-Agent](./deadlock-in-multi-agent.md) - a failed election that leaves no leader can leave follower agents waiting indefinitely, structurally similar to a deadlocked wait
