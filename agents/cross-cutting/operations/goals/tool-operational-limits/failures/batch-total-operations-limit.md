# Batch Total Operations Limit

## Issue
Beyond the size limit on any single batch, many tools also enforce an aggregate cap on total operations across a rolling window — for example, no more than 10,000 record writes per hour regardless of how they're split across individual batch calls. An agent that correctly chunks each batch to stay under the per-call limit can still violate this rolling aggregate cap if it fires many compliant batches in quick succession, because per-call compliance says nothing about cumulative volume over time. The agent's batching strategy solves the wrong constraint and the job fails partway through with no signal that the two limits are independent.

**Frequency**: Common

**Symptoms**
- A job that succeeds for the first several batches and then starts failing with quota/aggregate-limit errors partway through, even though every individual batch is well within the per-call size limit
- Errors referencing a rolling-window quota (e.g., "operations per hour exceeded") distinct from the per-request batch-size error
- Agents that retry the failed batch immediately, without waiting for the rolling window to free up capacity, hitting the same aggregate limit repeatedly
- Successful completion in low-volume test runs, failure in high-volume production runs performing the same per-batch chunking
- Throttling that appears random or load-dependent because it depends on how much other traffic (from the same account/key) has already consumed the rolling window

## Root Cause
Per-call batch-size limits and rolling aggregate quotas are usually enforced by separate mechanisms on the server side — one checks request shape at parse time, the other checks a counter (often per API key or account, in a sliding or fixed time window) independent of any single request. Agents that implement chunking logic keyed only to the documented per-call maximum have no model of the aggregate quota, its window length, or how much of it has already been consumed by prior calls in the same session or by other concurrent processes sharing the same credential. Without tracking cumulative operations against a time-windowed budget, the agent cannot know it is approaching the aggregate ceiling until the server rejects a call that is, by itself, perfectly valid.

## Example
```
A data-sync agent needs to update 45,000 CRM contact records. It correctly
chunks these into batches of 500 (the documented per-call max) and fires
90 sequential batch-update calls. The CRM also enforces an account-level
quota of 20,000 write operations per rolling hour. After the 40th batch
(20,000 records updated), the 41st batch — itself a valid 500-record
request — is rejected with
{"error": "rate_limit_exceeded", "scope": "hourly_write_quota", "reset_in": 1847}.
The agent's retry logic, tuned only for per-call 429s with short
Retry-After values, retries after 30 seconds using its default backoff,
fails again, and repeats this every 30 seconds for the next 30 minutes,
burning through its retry budget and eventually aborting the job with
44,500 of 45,000 records updated and no record of which 500 remain.
```

## Statistics
| Finding | Context |
|---------|---------|
| Rolling-window aggregate quotas (per-hour or per-day) are common on top of per-call batch limits in CRM, messaging, and data-platform APIs | Observed as a second, independent limit layer beyond per-request caps |
| Jobs that fail on aggregate quotas typically do so well into execution (after partial success), making failure detection and recovery harder than a batch rejected immediately at call time | Based on typical rolling-window enforcement patterns |
| Agents lacking session-level operation counters have no way to predict an aggregate-limit failure before it occurs, versus per-call limits which are checkable in advance from batch size alone | Structural property of rolling quotas vs. static per-call limits |

## Mitigations
1. **Track a session-level operation counter against the known rolling quota**: Maintain a running count of operations submitted within the current window and throttle proactively (pause or slow down) before the server-side counter is exhausted.
2. **Read quota-remaining headers when available**: Many APIs expose `X-RateLimit-Remaining` or similar for the aggregate window; poll or check this before firing the next batch rather than discovering exhaustion via a rejected call.
3. **Persist progress with resumable checkpoints**: Record which batches have been confirmed processed so that hitting the aggregate limit mid-job results in a resumable state (pick up at record 40,001) rather than an ambiguous partial failure.
4. **Respect the reset_in / window-reset time on aggregate rejections**: Distinguish aggregate-quota errors from per-call throttling and wait for the full window reset rather than applying a short per-call backoff schedule.
5. **Spread large jobs across the window proactively**: For known large jobs, pace batch submission to stay under the per-window budget throughout, rather than sprinting through per-call-sized batches as fast as possible.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `quota.rolling_window_consumed_pct` | Percentage of the known rolling aggregate quota consumed by the current session/account | Alert when > 80% before job completion |
| `job.aggregate_limit_failures` | Count of failures specifically attributed to rolling/aggregate quota (not per-call size) | Alert if > 0 |
| `job.completion_pct_at_aggregate_failure` | Fraction of total job completed when an aggregate-limit failure occurs | Track to size resumable-checkpoint granularity |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Aggregate quota exhausted mid-job | rolling-window rate-limit error received after prior successful batches | High | Pause job, persist checkpoint, resume after window reset per reset_in |
| Retry loop against exhausted aggregate quota | Same-window retries continue after an aggregate-limit rejection | Critical | Disable short-backoff retry for aggregate errors, switch to window-reset-aware scheduling |

## Related Patterns
- [Batch Size Limit](./batch-size-limit.md) - the per-call limit that correct chunking satisfies but that does nothing to prevent this aggregate limit
- [Backoff Envelope Violation](./backoff-envelope-violation.md) - applying the wrong retry timing to an aggregate-quota rejection compounds the failure
- [Tool Max Retry Limit Enforced](./tool-max-retry-limit-enforced.md) - another server-tracked rolling counter that client-side logic commonly fails to mirror
