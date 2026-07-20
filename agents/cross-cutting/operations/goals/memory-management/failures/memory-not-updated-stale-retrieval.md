# Memory Not Updated Stale Retrieval

## Issue
A memory write completes and is acknowledged as successful, but the read path the agent actually queries — a separate search index, a cache layer, a denormalized read table — has not yet been updated to reflect it, so the agent's next retrieval for that same fact returns the pre-update value even though the write, from the writer's point of view, already happened. This is a read-after-write consistency gap: the record of the update exists somewhere in the system, but not yet on the path the agent reads from, and neither the write nor the read reports any error.

**Frequency**: Common

**Symptoms**
- Agent retrieves and acts on a fact immediately after updating it, and gets the old value back
- A "confirm your update" step shows the update succeeded, but the very next query in the same session shows the prior state
- Issue is timing-dependent — waiting even a few seconds and re-querying returns the correct, updated value
- Discrepancy is worse under load, when index/cache update pipelines fall further behind the write path
- Affects only reads that go through a secondary index or cache, not reads against the primary store directly

## Root Cause
Memory systems commonly separate the write path (a durable primary store) from the read/retrieval path (a search index or vector index optimized for fast lookup, often updated asynchronously via a background indexing job or event-driven pipeline) for performance reasons — indexing on every write inline would add unacceptable write latency. This means there is an inherent, sometimes variable-length window between "the fact is durably written" and "the fact is discoverable via retrieval." An agent that writes an update and then immediately retrieves to confirm or act on it can land inside that window, especially when the write and the follow-up read happen in the same short-lived turn, and nothing in the architecture signals to the agent that the read path might not yet reflect the write it just made.

## Example
```
Agent updates a user's stored preference:
  write_memory(user_id="u_9910", fact="prefers vegetarian meal options")
  -> write acknowledged, status: "success", written_at: 15:41:02.100

Background indexing job that feeds the retrieval-facing vector
index runs every 5 seconds; the write above will be indexed at
approximately 15:41:05.

Same turn, 15:41:02.400 (300ms after the write):
  retrieve_memory(query="what are this user's dietary preferences")
  -> returns the previous record: "no dietary restrictions noted"
     (the index has not yet picked up the write from 300ms ago)

Agent, trusting the retrieval result over its own just-completed
write, tells the user: "I don't see any dietary restrictions on
file for you" — moments after the agent itself recorded that the
user is vegetarian, because it read from an index that hadn't
caught up to its own write.
```

## Statistics
| Finding | Context |
|---------|---------|
| Asynchronous indexing pipelines feeding retrieval indexes typically lag the primary write path by hundreds of milliseconds to a few seconds under normal load | Typical range for background-indexed memory architectures |
| Immediate write-then-read-in-same-turn patterns are a common trigger for observed stale-retrieval incidents, more so than reads separated by natural conversational delay | Reported pattern across teams instrumenting write-to-read gaps |
| Adding a short-lived write-through cache or read-your-writes override for the acting session removes the large majority of same-turn stale-read incidents | Estimated from teams that added read-your-writes handling |

## Mitigations
1. **Read-your-writes override**: For the same session/agent that just performed a write, route the immediately-following read to the primary store (or a cache populated synchronously on write) instead of the async-indexed retrieval path.
2. **Synchronous critical-path indexing**: For facts the agent is likely to immediately act on (confirmations, safety-relevant updates), index synchronously as part of the write rather than relying solely on the async pipeline.
3. **Write-through session cache**: Maintain a small, short-lived cache of the current session's own recent writes that retrieval checks first, so the agent's own updates are visible to itself even before the backing index catches up.
4. **Indexing lag monitoring**: Track and alert on the actual gap between write time and index-availability time, so degraded indexing pipelines are caught before they cause a burst of stale reads.
5. **Explicit confirmation semantics**: Design write APIs to only report "success" once the fact is confirmed retrievable (or to clearly separate "durably written" from "indexed and retrievable" status) so calling code can wait or branch appropriately.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| write_to_index_lag_seconds | Time between a write's durable commit and its availability via the retrieval path | Alert if p95 > 5s |
| same_turn_stale_read_rate | Rate at which a read immediately following a write in the same turn returns the pre-write value | Alert if > 2% |
| read_your_writes_override_miss_rate | Rate at which the read-your-writes cache fails to catch a same-session stale read | Alert if > 0 |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Same-turn stale read served | An agent's own just-completed write is not reflected in its immediately following retrieval | High | Route to read-your-writes path, investigate indexing pipeline lag |
| Indexing pipeline backlog | write_to_index_lag_seconds exceeds SLA sustained over several minutes | Medium | Scale indexing workers, alert infra team |

## Related Patterns
- [Context Refresh Stale State](./context-refresh-stale-state.md) - the same read-after-write consistency gap, surfacing through a context-refresh mechanism rather than a direct memory retrieval call
- [Memory Inconsistency Between Agents](./memory-inconsistency-between-agents.md) - a multi-agent variant where the stale read is served to a different agent than the one that wrote the update
- [Retrieval Temporal Ordering Failure](./retrieval-temporal-ordering-failure.md) - both can surface an outdated fact ahead of a current one, though this pattern is caused by indexing lag rather than ranking logic
