# Agent State Divergence

## Issue
Two or more agents that are supposed to maintain a shared view of the world — the current status of a task, a customer's conversation context, an inventory count — drift out of sync because their state-synchronization mechanism silently fails or falls behind. Each agent keeps acting confidently on its own local copy, and because no single agent has a global view, the divergence goes undetected until the agents' outputs visibly contradict each other or a downstream system receives conflicting updates.

**Frequency**: Common

**Symptoms**
- Two agents giving different answers about the same entity's status in the same conversation or workflow
- A downstream system receiving conflicting writes for the same record from different agent instances
- State that was supposed to propagate (e.g. "order cancelled") appearing on one agent's view but not another's
- Reconciliation jobs finding growing numbers of mismatches between agents' local state and a source of truth
- Bugs that are hard to reproduce because they depend on which agent instance happened to be stale at the time

## Root Cause
Multi-agent systems commonly optimize for low latency by giving each agent a local cache or copy of shared state rather than requiring a synchronous read from a single source of truth on every decision. Synchronization between that local copy and the canonical state relies on an update mechanism — event propagation, polling, a message bus — that is not guaranteed to be instantaneous or reliable. When an update is delayed, dropped, delivered out of order, or only partially applied (e.g. due to a crash mid-write), the agent's local view silently becomes stale while its confidence in that view remains unchanged. Because agents don't cross-check each other's state by default, the divergence compounds across further actions taken on the stale view.

## Example
```
A travel-booking system uses a Pricing Agent and a Booking Agent, each
holding a local cache of seat availability for flight AA1450 for
performance reasons, refreshed via an event bus.

14:00:00 - Seat count is 3 in the source-of-truth database, and matches
           in both agents' local caches.
14:00:02 - A customer completes a purchase through the Booking Agent,
           which decrements the source of truth to 2 seats and emits an
           "inventory_updated" event.
14:00:02.4 - The event bus experiences a brief partition; the event is
             queued but not yet delivered to the Pricing Agent.
14:00:03 - A second customer asks the Pricing Agent for a quote. The
           Pricing Agent's stale cache still shows 3 seats available and
           quotes the discounted "3+ seats remaining" price.
14:00:05 - The customer attempts to book at that price through the
           Booking Agent, which correctly shows 2 seats left and rejects
           the discount, causing a price mismatch and a support escalation.
14:00:09 - The delayed event finally arrives at the Pricing Agent, and its
           cache catches up -- five seconds after it had already quoted
           the wrong price.
```

## Statistics
| Finding | Context |
|---------|---------|
| State divergence between cooperating agents is implicated in an estimated 15-25% of cross-agent consistency bugs reported in production | Typical range observed in production incident reviews |
| Median divergence-detection lag (time between a state change and a stale agent's cache catching up) is commonly in the low single-digit seconds under normal conditions, but can extend to minutes under partition or backlog | Estimated from instrumented event-propagation logs |
| Adding read-time freshness checks or version stamps reduces divergence-driven incorrect actions by an estimated 50-70% | Reported range across teams that added staleness detection |

## Mitigations
1. **Versioned state with staleness checks**: Attach a version number or timestamp to every piece of shared state, and have agents check freshness before acting on cached data, refusing or re-fetching when a cache is older than an acceptable bound.
2. **Single source of truth for critical decisions**: For high-stakes actions (bookings, payments, irreversible writes), require a synchronous read from the canonical store rather than trusting a local cache, even at some latency cost.
3. **Idempotent, ordered event delivery**: Use an event bus that guarantees ordered, at-least-once delivery with idempotency keys, and have consuming agents detect and recover from gaps or out-of-order delivery rather than silently accepting whatever arrives.
4. **Periodic reconciliation sweeps**: Run a background process that compares each agent's local state against the source of truth on a regular cadence and corrects or alerts on drift before it causes a customer-visible conflict.
5. **Cross-agent consistency checks on shared entities**: Before two agents act on the same entity within a short window, have them cross-validate their views of that entity's state, surfacing a conflict rather than both proceeding independently.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| state_divergence_lag | Time between a canonical state change and all subscribed agents reflecting it | Alert if p95 > 5s |
| cache_staleness_at_read | Age of cached state at the moment an agent makes a decision using it | Alert if > defined freshness bound |
| reconciliation_mismatch_rate | Fraction of entities found mismatched between agent caches and source of truth during sweeps | Alert if > 0.5% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Conflicting agent outputs on same entity | Two agents produce contradictory state for the same entity ID within a short window | High | Page on-call, freeze writes to the entity, run reconciliation |
| Event propagation backlog growing | Event bus consumer lag for state-sync events exceeds threshold | Medium | Investigate bus health, alert dependent agent owners |

## Related Patterns
- [Agent Handoff Race Condition](./agent-handoff-race-condition.md) - a transaction-boundary special case of state divergence occurring specifically during task ownership transfer
- [Byzantine Agent Failure](./byzantine-agent-failure.md) - both require other agents to detect and not blindly trust an inconsistent view, though divergence is unintentional and Byzantine failure may not be
- [Inter-Agent Latency Imbalance](./inter-agent-latency-imbalance.md) - latency differences between agents are a common contributor to how long divergence windows stay open
