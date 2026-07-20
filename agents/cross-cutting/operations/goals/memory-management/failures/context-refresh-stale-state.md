# Context Refresh Stale State

## Issue
Many agent architectures periodically "refresh" a block of context — re-fetching current system state (order status, ticket state, account balance, feature flags) and re-injecting it into the prompt so the agent reasons over up-to-date information rather than what it read at session start. When the refresh mechanism itself reads from a stale source — a lagging read replica, a cache with a long TTL, a materialized view that hasn't recomputed — the agent receives a context block that looks fresh (it was "just refreshed") but actually contains old data, and the agent has no way to distinguish this from a genuine refresh.

**Frequency**: Common

**Symptoms**
- Agent acts on a just-refreshed state block that contradicts what a direct, uncached check would show
- Refresh timestamp in the context looks current, but the underlying value is minutes-to-hours old
- Agent repeats an action already completed because the refreshed status still shows "pending"
- Behavior differs between environments with different cache/replica lag (staging fresh, prod stale)
- Issue is intermittent and correlates with backend replication or cache-invalidation lag, not with the agent's own logic

## Root Cause
"Refresh" is typically implemented as a call to whatever backing store is fastest/cheapest to query — a cache, a read replica, or a denormalized view — rather than the true source of record. These layers trade consistency for latency/cost and can lag the source of record by anywhere from milliseconds to minutes depending on replication configuration or cache invalidation strategy. The refresh mechanism has no way of knowing it read stale data (the query succeeds and returns a value), so it stamps the context block with a fresh timestamp and confidence signal that reflects when the *read* happened, not how current the *underlying data* actually is. The agent, trusting the refresh mechanism's own signal, treats the value as authoritative.

## Example
```
Agent workflow: process a support ticket, refresh ticket status every
3 turns by querying a read-replica-backed ticket API.

Turn 1: refresh -> ticket #8821 status: "open"
        Agent escalates ticket to a human agent, who resolves it
        and marks it "closed" in the primary database at 14:02:03.

Turn 4: refresh -> ticket #8821 status: "open"  (read replica has
        4-minute replication lag; replica catches up at 14:06:00)
        Timestamp shown to agent: "refreshed at 14:03:10" (looks current)

Agent action: escalates the ticket a second time, paging an
on-call human for a ticket that was already resolved one minute
after the first escalation, because the "fresh" refresh actually
returned data that was 3 minutes stale relative to the true close
event despite carrying a current-looking timestamp.
```

## Statistics
| Finding | Context |
|---------|---------|
| Read-replica-backed refresh mechanisms typically carry 1-10 second lag under normal load, spiking to minutes under replication backlog | Typical range for asynchronously replicated data stores |
| An estimated 5-15% of "refresh" reads in cache-backed agent context pipelines return a value older than the cache's nominal TTL due to invalidation delays | Estimated from cache-instrumented agent pipelines |
| Duplicate or redundant agent actions attributable to stale refresh reads are reported in a meaningful minority of escalation/status-check workflows | Reported range across teams operating status-polling agents |

## Mitigations
1. **Read-your-writes routing**: Route refresh reads to the primary/source-of-record (or a replica guaranteed caught-up) for any state the agent itself, or a tightly-coupled human-in-the-loop step, may have just written.
2. **Staleness-aware timestamps**: Stamp refreshed context with the underlying data's last-modified time from the source of record, not the time of the refresh read, so the agent can reason about actual staleness.
3. **Version/etag checks**: Attach a version number or etag to refreshed state and compare against the last version the agent observed; treat an unchanged version after an expected update as a signal to re-query the primary.
4. **Bounded staleness contracts**: Configure caches/replicas used for agent refresh with an explicit maximum staleness SLA, and have the refresh mechanism fail loudly (rather than silently serve stale data) if that SLA is violated.
5. **Idempotent action design**: Where possible, make agent actions like "escalate" or "notify" idempotent or check-before-act, so a stale refresh causes a no-op rather than a duplicate side effect.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| refresh_staleness_seconds | Gap between refreshed value's underlying last-modified time and the refresh read time | Alert if p95 > SLA (e.g. 30s) |
| stale_refresh_action_rate | Fraction of agent actions taken immediately after a refresh that read a value later found to already be outdated | Alert if > 2% |
| duplicate_action_rate | Rate of agent actions (escalate, notify, retry) that duplicate an action already completed per the source of record | Alert if > 1% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Refresh source lag spike | Backing replica/cache lag exceeds configured staleness SLA | High | Failover refresh reads to primary, throttle agent actions until resolved |
| Duplicate action from stale refresh | Agent re-performs an action the source of record shows as already completed | Medium | Log and suppress duplicate, alert workflow owner to review refresh routing |

## Related Patterns
- [Memory Not Updated Stale Retrieval](./memory-not-updated-stale-retrieval.md) - the same read-after-write consistency gap, in the memory store's read path rather than a context-refresh mechanism
- [Context Coherence Loss](./context-coherence-loss.md) - stale refreshed state is one common trigger for the agent's context becoming internally inconsistent
- [Retrieval Temporal Ordering Failure](./retrieval-temporal-ordering-failure.md) - both involve the agent trusting a data-freshness signal that doesn't reflect true recency
