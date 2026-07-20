# Data Pipeline Replay Idempotency

## Issue
When a pipeline stage fails partway through, gets redeployed, or a consumer's offset is reset for recovery, the standard remedy is to replay events from a checkpoint. If the agent's downstream processing logic performs side effects (sending a notification, charging a payment, incrementing a counter, calling an external API) without checking whether that specific event was already processed, replaying the event log causes those side effects to happen again, producing duplicate charges, duplicate notifications, or double-counted metrics.

**Frequency**: Common

**Symptoms**
- Customers report receiving the same notification, email, or charge multiple times after an incident or deployment
- Aggregate counters or balances drift upward over time, correlating with consumer restarts or offset resets
- A "just replay from the last known-good checkpoint" recovery procedure is treated as universally safe when it is only safe for read-only or naturally idempotent stages
- Duplicate records appear in downstream systems with different generated IDs but identical business content
- Incident postmortems show the recovery action (the replay) caused a second, distinct incident (duplicate side effects)

## Root Cause
Idempotency is a property that must be deliberately engineered into a consumer — checking "have I already applied this specific event" before acting — and it is easy to skip when a stage is first built because replay is a recovery-time concern, not a normal-operation concern, so it doesn't show up in day-to-day testing. Many external side-effecting calls (payment APIs, email providers, webhooks) do not natively deduplicate by the caller's event ID unless the caller explicitly passes an idempotency key, so even a well-intentioned retry or replay silently becomes a duplicate action unless every side-effecting step in the chain independently implements dedup logic keyed off a stable, unique event identifier.

## Example
```
A billing agent consumes a "subscription-renewal" event stream and, for each
event, calls the payment provider's charge API and then sends a "your
subscription renewed" email via a transactional email service. Neither call
passes an idempotency key; both APIs treat each call as a brand-new charge or
send.

During a deploy, the consumer crashes after processing 340 of a batch of 500
renewal events but before committing its offset checkpoint, which was still
pointing to the start of the batch. On restart, the orchestration system
does what it's designed to do: it replays the batch from the last committed
offset, reprocessing all 500 events, including the 340 already charged and
emailed.

340 customers are charged twice for the same billing cycle and receive two
renewal emails within the same hour. Support tickets and refund requests
follow. The recovery procedure (replay from checkpoint) was correct pipeline
behavior; the consumer's lack of idempotent side effects turned a routine
crash-recovery into a billing incident.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 25-35% of pipeline crash-recovery incidents that involve side-effecting consumers produce at least one duplicate action | Typical range observed in incident postmortems involving replay-based recovery |
| Adding idempotency keys to all side-effecting external calls reduces replay-induced duplicates by an estimated 90%+ | Reported range across teams that retrofitted idempotency keys |
| Non-idempotent consumers are disproportionately represented among "recovery made it worse" incident classifications | Estimated from postmortem tagging in teams tracking this category |

## Mitigations
1. **Idempotency keys on every side-effecting call**: Derive a stable idempotency key from the source event's unique ID and pass it to every external API call (payment, email, webhook) that supports idempotent request handling, so provider-side dedup catches replays even if internal dedup is missed.
2. **Processed-event ledger**: Maintain a durable record of event IDs already fully processed (including all their side effects) and check it before acting on any event, skipping ones already marked complete.
3. **Exactly-once or effectively-once consumer patterns**: Use transactional outbox patterns or consumer frameworks with effectively-once semantics that atomically commit offset advancement together with the side effect's completion record, rather than committing offsets independently of action success.
4. **Replay-safe recovery runbooks**: Explicitly classify each pipeline stage as idempotent or non-idempotent in its operational runbook, and require non-idempotent stages to use a targeted, deduplicated replay procedure rather than a blanket "replay from checkpoint."
5. **Chaos-test replay scenarios**: Regularly test crash-and-replay recovery in staging for every side-effecting consumer, verifying no duplicate external calls occur, rather than only discovering the gap during a real production incident.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| duplicate_side_effect_rate | Rate of external API calls (charges, emails, webhooks) sharing an idempotency key or source event ID with a prior successful call | Alert if > 0 for keyed calls |
| event_replay_count | Count of events reprocessed due to offset reset or replay, cross-referenced against processed-event ledger hits | Alert if replayed events lack ledger coverage |
| checkpoint_commit_lag | Gap between event processing completion and offset checkpoint commit | Alert if lag allows large uncommitted batches to accumulate |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Duplicate external side effect detected | Same idempotency key or event ID triggers two successful external calls | High | Halt further replay, reconcile duplicate charges/notifications, notify affected customers |
| Non-idempotent consumer restarted with offset reset | A consumer without a processed-event ledger has its offset reset | High | Block automatic replay, require manual dedup review before reprocessing |

## Related Patterns
- [Data Pipeline Ordering Change](./data-pipeline-ordering-change.md) - both are consumer-side assumptions about delivery guarantees (order and exactly-once) that the transport layer does not actually promise
- [Data Pipeline Backpressure Unhandled](./data-pipeline-backpressure-unhandled.md) - crash-and-replay recovery from a backpressure-induced crash is a common trigger for idempotency failures
- [Integration Error Handling Mismatch](./integration-error-handling-mismatch.md) - retries triggered by mismatched error handling across integrated systems can cause the same non-idempotent duplicate-action problem
