# Array Element Limit

## Issue
Many tool APIs cap the number of elements allowed in a specific array field of a single request — for example a maximum of 500 line items per invoice-creation call, or 1,000 IDs per bulk-lookup request. When an agent assembles this array dynamically (aggregating results from a prior tool call, paginated upstream source, or a loop that accumulates records), it frequently has no visibility into the cap until the call fails or, worse, the API silently truncates the array and returns success. The agent then proceeds as if all elements were processed, producing incomplete work that looks complete.

**Frequency**: Common

**Symptoms**
- A bulk request that "succeeds" but only processes the first N elements of a larger array, with no error surfaced
- Intermittent `400`/`422` errors that appear only on days with unusually high data volume, never in small-scale testing
- Downstream reconciliation jobs showing a fixed shortfall (e.g., always missing items past index 500) that grows proportionally with input size
- Agent logs showing a single tool call with an array field whose length matches the API's undocumented or documented max exactly, followed by no retry for the remainder
- Silent data loss discovered only during audits, not during the agent's own run

## Root Cause
Tool providers impose array-length caps to bound request parsing cost, memory allocation, and downstream fan-out (e.g., one array element may trigger one internal write or notification). Agents typically treat an array-valued parameter as unbounded because the tool schema declares it as `array<T>` without a machine-readable `maxItems`, or the agent's prompt/plan was written against a small test dataset and never exercised the boundary. Because the agent has no chunking logic keyed to the specific field's limit, it hands the full accumulated array to a single call and trusts the response status rather than verifying the processed count against the input count.

## Example
```
An agent aggregates 1,200 support ticket IDs flagged for bulk-close from a
ticketing system's search API (paginated, 100 per page, 12 pages fetched
correctly). It then calls `POST /tickets/bulk-update` with all 1,200 IDs in
the `ticket_ids` array. The bulk-update API silently caps `ticket_ids` at
1,000 elements and processes only the first 1,000, returning HTTP 200 with
`{"updated": 1000}`. The agent reads the 200 status, logs "bulk close
successful," and moves to the next task. 200 tickets remain open. Three days
later a customer escalation reveals tickets that were supposedly closed are
still active, and the agent's run log shows no indication anything went
wrong.
```

## Statistics
| Finding | Context |
|---------|---------|
| Bulk/array-typed endpoints in production agent tool sets commonly cap arrays between 100 and 2,000 elements | Observed across CRM, ticketing, and messaging bulk APIs |
| A large share of array-limit failures are silent (partial success with 2xx) rather than hard errors | Increases risk relative to other operational limits, which usually fail loudly |
| Agents that verify response counts against input counts catch this failure mode close to 100% of the time; agents that check only HTTP status catch it rarely | Based on typical post-call validation patterns |

## Mitigations
1. **Declare and enforce maxItems client-side**: Maintain a per-tool, per-field registry of known array limits and chunk any array exceeding it into multiple calls before dispatch, rather than discovering the limit via a failed or silently truncated call.
2. **Validate response cardinality**: After any bulk call, compare a count field in the response (or the returned array length) against the count of elements submitted; treat a mismatch as a failure requiring remediation, not a success.
3. **Prefer explicit rejection over silent truncation when configurable**: Where the API supports a strict-mode or validation flag, enable it so oversized arrays return a hard error instead of being quietly truncated.
4. **Batch with continuation tracking**: When chunking is required, persist which sub-batches have been submitted and confirmed so a crash mid-loop can resume rather than resubmit or skip elements.
5. **Add integration tests at and beyond the boundary**: Test array-valued calls with N-1, N, and N+1 elements against the known or discovered limit so regressions in chunking logic are caught before production.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `bulk_call.input_count vs response.processed_count delta` | Difference between elements submitted and elements confirmed processed | Alert if delta > 0 on any bulk call |
| `array_field.max_observed_length` | Rolling max length of a given array field sent by the agent | Alert when within 10% of the known/documented limit |
| `bulk_call.silent_truncation_rate` | Share of bulk calls where response count < request count despite 2xx status | Alert if > 0% sustained over 1 hour |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Bulk array truncation detected | processed_count < submitted_count on a 2xx response | High | Page on-call, re-queue unprocessed elements, verify no duplicate side effects |
| Approaching array limit | submitted array length >= 90% of known maxItems for 3 consecutive calls | Medium | Trigger automatic chunking rollout for that tool/field |

## Related Patterns
- [Batch Size Limit](./batch-size-limit.md) - same class of cap but applied to the whole batch/request rather than a single array field
- [Batch Total Operations Limit](./batch-total-operations-limit.md) - aggregate cap across multiple calls that per-call array chunking alone won't satisfy
- [Response Payload Size Limit](./response-payload-size-limit.md) - another silent-truncation failure mode, on the response side instead of the request side
