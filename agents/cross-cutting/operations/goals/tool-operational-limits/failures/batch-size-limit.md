# Batch Size Limit

## Issue
Bulk-operation tools commonly enforce a maximum number of operations (rows, records, actions) per batch request, distinct from any single-field array cap — for instance a max of 200 records per bulk-import call or 100 messages per batch-send. Agents that build a batch from dynamic upstream data (a database query, a paginated feed, a fan-out from a previous step) often assemble the request first and only discover the limit when the call is rejected outright, because nothing in the agent's planning path checks the batch's total size against the tool's documented ceiling before dispatch.

**Frequency**: Very Common

**Symptoms**
- `400`/`413`/`422` errors referencing a batch or request size limit, occurring only when upstream data volume crosses a threshold
- Agent code that works reliably in testing (small fixtures) and fails unpredictably in production (real data volumes)
- Entire batches rejected atomically, so zero records are processed even though most of the batch was valid
- Repeated identical failures on retry, because the agent resubmits the same oversized batch unchanged
- Manual intervention required to re-chunk and resubmit work that the agent could not complete

## Root Cause
Batch endpoints cap size to bound per-request processing time, transactional scope, and memory footprint on the server. Agents typically construct batches by accumulating results from upstream calls (e.g., "fetch all pending orders, then submit them as one batch") without a pre-flight check against the target tool's max-batch-size, because that limit lives in documentation rather than in a machine-checkable part of the tool's schema. Unlike per-field array limits, batch-size limits often apply to the request as a whole (headers + all fields combined) and can trigger an all-or-nothing rejection rather than partial processing, making the failure mode more disruptive.

## Example
```
An agent processes an end-of-day reconciliation job: it queries a database
for all unsynced transactions (that day: 743 rows) and submits them in a
single call to a payments API's `POST /v2/transactions/batch` endpoint.
The API's documented limit is 250 transactions per batch. The call returns
`413 Payload Too Large` with body
{"error": "batch_size_exceeded", "max": 250, "received": 743}.
The agent's error handler recognizes only network-level failures and
generic 5xx retries; it does not parse the 413 body, so it retries the
identical 743-row batch three times with exponential backoff, failing
identically each time, before giving up and alerting on-call with a
generic "transaction sync failed" message that omits the actual cause.
```

## Statistics
| Finding | Context |
|---------|---------|
| Bulk-operation endpoints commonly cap batches in the 100-1,000 item range | Observed across payments, CRM, and data-import APIs |
| Batch-size failures are disproportionately first discovered in production rather than testing, because test fixtures rarely reach production data volumes | Common gap in agent test coverage |
| All-or-nothing batch rejection (vs. partial processing) is the typical behavior for size-limit violations, as opposed to count-mismatch behavior seen in per-field array limits | Based on typical bulk-API transactional design |

## Mitigations
1. **Chunk against a known limit before dispatch**: Maintain the documented max batch size per tool and split any oversized batch into sequential sub-batches client-side, never relying on the server to reject and inform.
2. **Parse structured error bodies for size violations**: Ensure error-handling logic distinguishes a batch-size-exceeded response from generic failures and reacts by re-chunking rather than blind retry.
3. **Size batches dynamically from actual payload weight, not just item count**: Where the limit is byte-based rather than count-based, estimate serialized size before submission since item count alone can understate true payload size.
4. **Make batch submission idempotent per chunk**: Assign a stable idempotency key per chunk so re-chunking after a failure doesn't risk double-processing records from a chunk that partially succeeded before a later chunk failed.
5. **Alert with the actual limit context, not a generic failure message**: Surface `max` and `received` values from the error response in on-call alerts so the fix (adjust chunk size) is immediately clear.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `batch_call.rejected_size_count` | Count of batch calls rejected specifically for exceeding max batch size | Alert if > 0 in any run |
| `batch_call.avg_items_per_batch` vs configured max | Ratio of typical batch size to the tool's documented limit | Alert when ratio > 0.8 (approaching limit) |
| `batch_call.identical_retry_count` | Number of times the same oversized batch is retried unchanged | Alert if >= 2 (indicates retry logic isn't re-chunking) |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Batch size limit exceeded | 413/422 batch-size error received | High | Halt job, re-chunk using known limit, resubmit |
| Repeated unchanged retry after size rejection | Same batch payload resubmitted 2+ times after a size error | Critical | Disable naive retry path, page on-call to fix chunking logic |

## Related Patterns
- [Array Element Limit](./array-element-limit.md) - a narrower cap on one array field rather than the whole batch/request
- [Batch Total Operations Limit](./batch-total-operations-limit.md) - a rolling aggregate cap across many correctly-sized batches
- [Request Payload Size Limit](./request-payload-size-limit.md) - byte-size ceiling that a large batch can hit even when item count is within limits
