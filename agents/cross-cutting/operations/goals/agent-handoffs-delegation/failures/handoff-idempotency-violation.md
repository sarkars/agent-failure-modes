# Handoff Idempotency Violation

## Issue
A handed-off task gets executed more than once because the handoff mechanism retries on a suspected failure (timeout, dropped acknowledgment, transient network error) without any way to detect that the receiving agent already processed the original attempt. The receiving agent has no concept of "I've seen this task ID before" and treats each retry as a fresh, independent instruction, resulting in duplicate side effects — a second email sent, a second charge issued, a second record created.

**Frequency**: Common

**Symptoms**
- Duplicate downstream side effects (two emails, two calendar invites, two database records) traced back to a single logical task
- Handoff logs showing the same task ID or payload sent to the receiving agent more than once
- Receiving agent's own logs showing successful completion on both the original and retried attempt, with no error on either
- Retry logic present at the orchestration layer with no corresponding deduplication logic at the receiving agent

## Root Cause
Retries exist to handle the ambiguity of network and system failures: when a handoff acknowledgment doesn't arrive within a timeout, the sender cannot distinguish "the receiver never got it" from "the receiver got it, processed it, and only the acknowledgment was lost." The safe default is to retry, because failing to retry risks losing the task entirely. But retrying safely requires the receiving agent to be idempotent — to recognize a repeated task ID and skip re-execution — and idempotency has to be deliberately engineered per action type (an email send is not naturally idempotent; a "set status to X" write often is). When the receiving agent's action isn't idempotent and no deduplication layer sits between the retry and the action, every retry is a full re-execution.

## Example
```
An order-fulfillment agent hands off "charge customer $89.99 for order
#55201" to a payment-processing agent. The handoff transport is an
HTTP call with a 5-second timeout; the payment agent successfully
charges the card and returns a 200 response, but the response is lost
to a transient network blip on the way back to the fulfillment agent.

The fulfillment agent's retry policy treats "no response within timeout"
as "assume failure, retry" and resends the identical handoff message
30 seconds later. The payment-processing agent, which has no
deduplication check against a task or idempotency key, processes it as
a new charge request and bills the customer's card a second time for
$89.99.

The duplicate charge is only caught four days later when the customer
disputes the second line item with their bank, well after both agents'
individual logs show "success" for their respective attempts.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 1-3% of retried agent-to-agent handoffs result in duplicate execution when no idempotency key is enforced | Typical range observed in systems with retry-on-timeout handoff policies |
| Adding idempotency keys to handoff payloads typically eliminates the large majority of duplicate-execution incidents | Reported range across teams introducing dedup layers |
| Financial and communication actions (charges, emails, notifications) account for a disproportionate share of duplicate-execution incidents relative to their share of total handoffs | Estimated from incident classification in agent orchestration postmortems |

## Mitigations
1. **Idempotency keys on every handoff**: Attach a unique, stable idempotency key to each logical task, and require the receiving agent to check a dedup store before executing any side-effecting action, skipping (and returning the original result) if the key was already processed.
2. **Exactly-once semantics via dedup store**: Maintain a durable store of processed task IDs with a TTL long enough to cover realistic retry windows, and reject or short-circuit any handoff matching an already-processed ID.
3. **Distinguish acknowledgment loss from processing failure**: Where possible, have the receiving agent persist "processing started" before executing, so a retry can check that state and either wait for the in-flight attempt or safely resume rather than blindly re-executing.
4. **Non-idempotent action isolation**: Identify actions that are inherently non-idempotent (charges, sends, external API calls with side effects) and route them through a dedicated idempotency-enforcing wrapper rather than relying on general-purpose retry logic.
5. **Retry-safe handoff design review**: When adding a new handoff-triggered action, explicitly document and test its idempotency behavior under retry before deploying, treating it as a required property rather than an incidental one.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| duplicate_task_execution_count | Count of task IDs processed more than once by a receiving agent | Alert if > 0 for non-idempotent action types |
| handoff_retry_rate | Rate of handoffs that trigger a retry due to timeout or missing acknowledgment | Alert if > 5% |
| idempotency_key_coverage | Share of handoff payloads carrying a valid idempotency key | Alert if < 100% for side-effecting task types |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Duplicate side effect detected | Two executions of the same task ID both completed a side-effecting action | High | Trigger compensating action (refund, cancellation), page on-call |
| Missing idempotency key on retryable handoff | A handoff to a side-effecting agent is sent without an idempotency key | Medium | Block the handoff, require key before dispatch |

## Related Patterns
- [Handoff Timing Mismatch](./handoff-timing-mismatch.md) - the timeout-driven retries that trigger idempotency violations are a direct consequence of timing mismatches between sender and receiver
- [Handoff Rollback Failure](./handoff-rollback-failure.md) - duplicate executions are especially damaging when the resulting side effects cannot be cleanly rolled back
- [Handoff State Loss](./handoff-state-loss.md) - loss of "already processed" state is one specific mechanism by which idempotency checks fail to catch a retry
