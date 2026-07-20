# Memory Inconsistency Between Agents

## Issue
When multiple agent instances or agent types share a common memory store — a customer-service agent and a billing agent both reading/writing facts about the same account, or multiple parallel worker agents in a fleet — they can each see a different view of "current" memory state at the same moment, because of replica lag, per-connection caching, or eventual-consistency propagation delays in the shared store. There is no single moment-in-time snapshot all agents agree on, so two agents acting concurrently on the same entity can make decisions based on genuinely different, both-locally-valid-but-mutually-inconsistent memory states.

**Frequency**: Common

**Symptoms**
- Two agents give different answers about the same entity's state within the same time window
- An agent acts on a fact another agent already updated moments earlier, as if the update never happened
- Inconsistencies resolve themselves after a delay with no code change, indicating a propagation-lag root cause
- Behavior differs depending on which replica/region/cache an agent instance happens to be connected to
- Post-incident review shows both agents were "correct" relative to the version of memory each one read

## Root Cause
Shared memory stores at any meaningful scale trade strict consistency for availability and latency — reads may be served from local caches, regional replicas, or read-optimized indexes that are updated asynchronously relative to the write path. Each individual agent's read is internally consistent (it gets *a* valid snapshot), but different agents connected to different cache/replica instances, or reading at different points in a propagation window, see different snapshots of the same underlying data. Because agents don't typically coordinate a shared transaction or locking protocol before acting — they're designed to operate independently for latency and scalability reasons — there is no mechanism forcing them to agree on a single current state before both proceed, so concurrent action based on divergent views is structurally possible rather than a rare edge case.

## Example
```
Shared memory store (eventually consistent, ~2s regional propagation)
holds account #7734's status: "active".

Agent A (billing, region us-east) processes a chargeback at 09:14:00,
updates account status to "suspended" in us-east primary.

Agent B (support, region us-west, reading from a us-west replica
that hasn't yet received the update) handles an inbound chat at
09:14:01: reads account status "active" from its local replica,
tells the customer "Your account is fully active, let me help
you upgrade your plan," and initiates an upgrade billing charge.

By 09:14:03 the us-west replica catches up and shows "suspended,"
but Agent B's action has already been taken based on the stale
"active" view it legitimately read one moment earlier — both
agents were internally consistent with what they read, but the
two actions taken 1 second apart contradict each other.
```

## Statistics
| Finding | Context |
|---------|---------|
| Regionally-replicated shared stores typically propagate updates within 1-5 seconds under normal load, with tail latency reaching much higher during backlog | Typical range for cross-region eventually-consistent replication |
| Multi-agent fleets sharing a common memory store without a coordination/locking layer show a measurable rate of conflicting-action incidents proportional to concurrent-agent count and update frequency on shared entities | Reported pattern across teams operating multi-agent fleets on shared state |
| Introducing a single-writer or locking protocol for high-conflict entities reduces observed cross-agent inconsistency incidents substantially in comparative deployments | Estimated from before/after comparisons in coordinated vs. uncoordinated fleets |

## Mitigations
1. **Single-writer entities**: For entities with high conflict risk (account status, balances), route all writes through a single authoritative writer or a locking mechanism so only one agent can mutate the entity's state at a time.
2. **Read-committed guarantees for hot entities**: For entities under active dual-agent access, force reads to the primary or a fully-caught-up replica rather than allowing eventually-consistent reads.
3. **Version/conflict detection**: Attach a version number to shared records and have agents check-and-set on write, so a write based on a stale read is rejected rather than silently overwriting or contradicting a concurrent update.
4. **Cross-agent event broadcasting**: Emit an event when a shared entity changes so other active agents holding that entity in their working context can be notified and refresh, rather than relying solely on passive re-read propagation.
5. **Conflict monitoring by entity**: Track and alert on entities that receive near-simultaneous writes/reads from multiple agents with divergent results, to identify hot-conflict entities that need stronger consistency guarantees.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| cross_agent_read_divergence_rate | Rate at which two agents reading the same entity within a short window see different values | Alert if > 1% for high-conflict entity types |
| replication_lag_seconds | Propagation delay between primary write and replica read-availability | Alert if p95 > 3s |
| conflicting_action_count | Count of detected pairs of agent actions on the same entity based on divergent memory reads | Alert if > 0 for critical entity types (billing, account status) |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Conflicting concurrent actions detected | Two agents take contradictory actions on the same entity within a short window | High | Roll back or reconcile the later action, escalate to on-call, review consistency guarantees for the entity type |
| Replication lag spike | replication_lag_seconds exceeds SLA for a shared memory store | Medium | Route high-conflict entity reads to primary, notify infra team |

## Related Patterns
- [Memory Not Updated Stale Retrieval](./memory-not-updated-stale-retrieval.md) - the single-agent version of the same read-after-write consistency gap
- [Memory Interleaving Corruption](./memory-interleaving-corruption.md) - a more severe outcome of concurrent multi-agent access where writes actually corrupt a record rather than just diverge in reads
- [Context Coherence Loss](./context-coherence-loss.md) - the within-agent analogue: no single authoritative current-state view, here across agents rather than across turns
