# Integration Error Handling Mismatch

## Issue
Different systems an agent integrates with signal failure through incompatible conventions — one returns HTTP error status codes, another embeds an error object inside a 200 OK response body, a third throws a language-level exception that a client SDK translates inconsistently, and a fourth simply omits expected fields on failure with no explicit error marker at all. Integration code written to detect failure one way (checking status codes) silently misses failures signaled another way (a 200 with an error payload), treating a failed operation as successful and proceeding as if it worked.

**Frequency**: Very Common

**Symptoms**
- A downstream action proceeds (a record is created, a notification is sent) based on an upstream call the agent believed succeeded, but which actually failed
- Error-handling code has visible gaps: a try/catch around one integration's exception-based errors, but no equivalent check for another integration's status-code-based errors used in the same workflow
- Logs show the raw response body containing an error message, but the code path that would have surfaced it as a failure never triggered because it only checked the status code
- A single workflow spanning three integrations has three different error-handling styles, increasing the chance any given failure mode is missed
- Post-incident review finds the failure was visible in the response payload the whole time, just not in the field the code was checking

## Root Cause
There is no universal standard for how an API signals failure, and different providers, frameworks, and even different endpoints within the same provider's API choose different conventions based on their own history and design philosophy — REST purists use status codes, some GraphQL and RPC-style APIs return 200 with an errors field regardless of outcome, some SDKs translate all of this into exceptions while others return error objects the caller must explicitly check. When an agent's workflow chains calls to multiple systems, the integration code for each call is often written by looking at that system's own documentation and examples in isolation, without a unifying error-handling abstraction that normalizes all these conventions into one consistent internal representation, so gaps between conventions become gaps in the code's failure detection.

## Example
```
A procurement agent completes a purchase workflow across three systems: (1)
a vendor-catalog API that raises an HTTP 4xx/5xx status code on failure, (2)
an internal approval-routing service that returns 200 OK always, embedding
"status": "approved" or "status": "rejected" inside the body, and (3) a
payment-processing SDK that raises a language-level exception on failure but
returns a plain success object with no exception on partial failures like
"payment pending manual review."

The agent's workflow code wraps the vendor-catalog call and the payment SDK
call in error handling (status-code check for the first, try/catch for the
second), but treats the approval-routing call as successful whenever the
HTTP request itself completes without a network error, since a 200 status
code is, by that call's own convention, always returned.

A purchase request is rejected by the approval-routing service due to
exceeding a spending threshold, returned as {"status": "rejected", "reason":
"exceeds department budget"} inside a 200 OK response. The agent's code
never inspects the body's "status" field, treats the 200 as approval, and
proceeds to trigger the payment SDK call, which itself succeeds without
exception (submitting the payment for processing) but actually returns
"payment pending manual review" rather than "completed" -- a distinction the
agent also doesn't check. The purchase is initiated despite being rejected
by approval routing, and the mismatch is discovered only when finance
reconciles unauthorized spend at month-end.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 25-35% of multi-integration workflows contain at least one call whose failure signaling convention differs from the others in the same workflow and isn't uniformly checked | Typical range observed in integration code review |
| Silent failure-as-success incidents (a failed call proceeding as if successful) are disproportionately concentrated in workflows spanning 3+ distinct integrations | Estimated from incident classification by workflow complexity |
| Normalizing all integration responses into a single internal success/failure representation at the integration boundary reduces missed-failure incidents by an estimated 60-75% | Reported range across teams adopting a unified error-handling abstraction layer |

## Mitigations
1. **Unified internal error representation**: Normalize every integration's response, regardless of its native error-signaling convention, into a single consistent internal result type (e.g., a Result/Either type with explicit success/failure) at the integration boundary, so downstream workflow logic never has to know each system's native convention.
2. **Per-integration error-convention documentation and testing**: Explicitly document how each integrated system signals failure (status code, body field, exception, silent omission) and write tests that specifically exercise each system's failure path to verify it's correctly detected.
3. **Full-body inspection even on "successful" status codes**: For any integration known to embed error semantics in the response body regardless of status code, always inspect the body's success/failure indicator rather than trusting the HTTP status code alone.
4. **End-to-end workflow failure injection testing**: Test each step of a multi-integration workflow with simulated failures using that step's actual native failure convention, verifying the workflow correctly halts or compensates rather than only testing the happy path.
5. **Fail-closed default for ambiguous responses**: When a response doesn't clearly match either a known success or known failure pattern, default to treating it as a failure requiring review, rather than defaulting to proceed.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| unchecked_error_field_rate | Rate of integration responses containing a body-level error/status field that the calling code doesn't inspect | Alert if > 0 for known dual-convention integrations |
| workflow_proceeded_after_upstream_failure_count | Count of workflow instances that proceeded to a subsequent step despite an earlier step's response indicating failure | Alert if > 0 |
| per_integration_failure_detection_coverage | Fraction of an integration's documented failure modes covered by an explicit test | Alert if < 100% for integrations used in multi-step workflows |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Workflow proceeded despite embedded failure signal | A downstream step executes after an upstream response's body indicates rejection/failure, regardless of status code | High | Halt the workflow, reverse any downstream side effects already taken, add explicit body check |
| New integration lacks normalized error handling | A newly added integration bypasses the unified error-representation layer | Medium | Require refactor before the integration is used in a multi-step workflow |

## Related Patterns
- [Integration API Contract Violation](./integration-api-contract-violation.md) - a mismatch between documented and actual error signaling is a specific case of a broader contract violation
- [Integration Data Consistency](./integration-data-consistency.md) - silently missed failures are a common root cause of two systems ending up in disagreeing states
- [Data Pipeline Replay Idempotency](./data-pipeline-replay-idempotency.md) - retries triggered by a misread error state can produce the same duplicate-action risk idempotency failures cause
