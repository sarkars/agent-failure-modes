# Tool Idempotency Assumption Failure

## Issue
An agent retries a tool call after a timeout, an ambiguous error, or a crash-and-resume, assuming that calling it again is safe because "retrying is always safe." Some tools are not idempotent — calling them twice with the same arguments produces two distinct side effects (two charges, two emails, two created records) rather than converging to the same end state. The agent's retry logic doesn't distinguish between tools where a duplicate call is harmless and tools where it corrupts state or produces a real-world duplicate action.

**Frequency**: Common

**Symptoms**
- Duplicate emails, notifications, or messages sent to the same recipient for what the user experiences as a single request
- Duplicate charges, orders, or database records with near-identical timestamps a few seconds apart
- Customer complaints about receiving the same communication or being charged twice, tracing back to a logged retry after a timeout
- Retry logs show the retried call "succeeded" both times, with no error on either attempt — the original call had actually succeeded too, just slow to respond
- The issue is intermittent and clusters around periods of elevated latency or transient network issues, exactly when retries are most likely to fire

## Root Cause
Retry-on-failure is a reasonable default for transient errors, but it silently assumes the failed call didn't actually complete its side effect before the error was raised or the timeout fired — an assumption that's false whenever the failure is a response-delivery problem rather than a request-processing problem (the server processed the charge but the response was lost due to a network blip, so the client sees a timeout even though the action succeeded). Agent frameworks that implement generic retry wrappers around "any tool call" without per-tool idempotency metadata treat every tool identically, when in reality idempotency is a property of the specific operation (a GET or a status check is naturally safe to repeat; a POST that creates a new resource or charges a payment method is not, unless the tool or downstream API explicitly supports an idempotency key).

## Example
```
An agent handling a customer refund request calls a "process_refund"
tool that hits a payments API. The API call is sent, the payment
processor successfully issues the refund, but the HTTP response
carrying the success confirmation is delayed past the agent's 5-second
timeout due to a transient network issue.

t=0.0s   Agent calls process_refund(order_id="ORD-88231", amount=42.00)
t=5.0s   Agent's tool call times out with no response received;
         agent's retry policy treats this as "call may not have
         succeeded, retry once"
t=5.1s   Agent calls process_refund(order_id="ORD-88231", amount=42.00)
         again
t=5.4s   Second call succeeds and returns quickly (processor is no
         longer under the load that caused the first delay)
t=5.5s   Agent reports "refund processed successfully" to the user

Result: the customer is refunded $84.00 instead of $42.00 - the first
call had actually succeeded server-side, and the retry, made without
an idempotency key, was processed as an independent second refund.
The duplicate isn't caught until the merchant's daily reconciliation
flags the account balance discrepancy.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 20-40% of tool-call timeouts under load are response-delivery failures where the underlying action actually completed | Typical range observed in production API telemetry involving retries |
| Blind retry-on-any-error policies are estimated to produce a duplicate side effect in 2-8% of retried calls against non-idempotent tools | Estimated from incident data across teams without idempotency-key coverage |
| Adding idempotency-key support to write-type tool calls reduces duplicate-action incidents by an estimated 90%+ | Reported range across teams that added this control |

## Mitigations
1. **Per-tool idempotency classification**: Explicitly tag each tool as safe-to-retry (read-only, naturally idempotent) or unsafe-to-retry-without-a-key (creates/charges/sends), and have the retry wrapper consult this classification rather than treating all tools uniformly.
2. **Idempotency keys on write operations**: For tools that support it, generate and pass a stable idempotency key (derived from the original request, not regenerated per retry) so the downstream API can recognize and deduplicate a retried request server-side.
3. **Query-before-retry for unsafe tools**: Before retrying a non-idempotent call, first query whether the original action already succeeded (e.g. check order/refund status) rather than assuming failure from a timeout alone.
4. **Exactly-once semantics via outbox pattern**: For critical write actions, record the intent to act durably before calling the tool, and check that record on any retry path so a crash-and-resume doesn't re-issue an action whose intent was already fulfilled.
5. **Timeout tuning and response confirmation**: Distinguish "no response received" from "response received but indicated failure," and treat the former with more caution (query-first) than the latter (safe to retry, since the server explicitly rejected the request).

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| duplicate_side_effect_rate | Rate of detected duplicate records/charges/messages traced to a retried tool call | Alert if > 0 for financial or communication tools |
| retry_without_idempotency_key_count | Count of retries issued against write-type tools that lack an idempotency key | Alert if > 0 |
| timeout_then_query_mismatch_rate | Fraction of timeout-triggered retries where a pre-retry status check would have found the original call already succeeded | Track as leading indicator |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Duplicate financial action detected | Reconciliation finds two charges/refunds/orders from what should have been a single request | High | Page on-call, reverse the duplicate, audit the retry path for missing idempotency key |
| Retry issued against unclassified tool | A retry fires against a tool with no idempotency classification on record | Medium | Block the retry pending classification, notify the tool's owning team |

## Related Patterns
- [Tool State Dependency Violation](./tool-state-dependency-violation.md) - both involve incorrect assumptions about what state a prior call actually established
- [Tool Invocation Ordering Dependency](./tool-invocation-ordering-dependency.md) - a retried call can also violate an ordering constraint if other calls happened in between the original attempt and the retry
- [Tool Mutation State Leak](./tool-mutation-state-leak.md) - a non-idempotent retry is one specific mechanism by which a tool's mutation can unexpectedly affect later processing
