# Integration Timeout Mismatch

## Issue
An agent calls an external integration with a timeout shorter than the operation actually needs to complete on the far side, gives up and treats the call as failed, and then acts on that failure assumption — retrying, falling back, or notifying a user that the action didn't happen — while the original call is, in fact, still running to completion on the downstream system. When the downstream operation succeeds after the agent has already moved on, the agent's decision was made on stale information: it may issue a duplicate request (double-charging a payment, double-booking a resource), or it may leave the user with an incorrect "this failed" outcome for an action that actually succeeded. This is a correctness/state-consistency failure specific to one integration point, distinct from the broader dynamic where mismatched timeouts across a call chain amplify load system-wide.

**Frequency**: Common

**Symptoms**
- A downstream system's audit log shows a call completing successfully after the calling agent had already timed it out and taken a fallback or retry action
- Duplicate side effects appear for actions the agent treats as idempotent-by-retry (two charges, two shipment records, two calendar entries) traceable to a timeout-then-retry against an operation that actually succeeded on the first attempt
- Users are told an action failed ("we couldn't process your request") for a request that downstream records show did in fact complete
- The agent's configured timeout for a given integration is set to a round, convenient number (5s, 10s) that doesn't correspond to any measured p99 latency for that specific downstream operation
- Timeout-triggered fallback logic fires more often during downstream load spikes — exactly when the operation is slow but not actually failing — compounding load on a system that was already under pressure

## Root Cause
A timeout is a bet that "no response within N seconds" reliably indicates failure, but for many integrations that bet is wrong under exactly the conditions most likely to trigger it: elevated load, which slows the downstream system without breaking it. The agent's timeout value is typically chosen based on a rough guess or a generic default rather than the operation's actual, measured latency distribution, and the agent's response to a timeout is usually written as if a timeout definitively means "did not happen," when for many operations (especially ones that mutate state, like payments or bookings) a timeout only means "the response didn't arrive in time" — the operation itself may have already been accepted and is proceeding independently of whether the caller is still listening. Without a way to check the downstream system's actual outcome after a timeout (rather than assuming failure and acting immediately), the agent's fallback logic operates on an assumption that is frequently false precisely when it matters most.

## Example
```
A checkout agent calls a payment-authorization API with a 4-second
timeout, chosen as a reasonable-sounding default when the integration
was first built. The payment provider's own documented p99 latency is
3.8 seconds under normal load - already uncomfortably close to the
agent's timeout - and can exceed 6 seconds during the provider's own
periodic settlement batch jobs.

During one such batch window, a customer's payment authorization call
takes 5.2 seconds. The agent's 4-second timeout fires first; the agent
marks the payment as failed, shows the customer an error, and - per
its retry policy - automatically resubmits the authorization request.

The original authorization was not actually rejected. It completes
successfully on the payment provider's side at the 5.2-second mark,
authorizing the customer's card for the full order amount. The agent's
automatic retry, submitted moments later, authorizes the same card a
second time for the same amount, since the agent has no mechanism to
check whether the first attempt actually completed before resubmitting.

The customer sees two pending authorizations on their card and an error
message claiming the payment "failed," and contacts support confused
about why they were charged for something the agent told them didn't
go through.
```

## Statistics
| Finding | Context |
|---|---|
| A meaningful share of payment/booking-style duplicate-side-effect incidents trace back to a timeout-then-retry against an operation that had actually already succeeded | Estimated from postmortems of duplicate-charge and duplicate-booking incidents |
| Integration timeouts set without reference to the downstream operation's own measured latency distribution are disproportionately likely to trigger during the downstream system's own load spikes | Typical pattern observed where timeout values are chosen as convenient defaults rather than derived from p99/p999 latency data |
| Adding a post-timeout status-check step before acting on a presumed failure eliminates a large share of duplicate-side-effect incidents for idempotency-sensitive operations | Reported range across teams that added reconciliation checks after timeout events |

## Mitigations
1. **Set timeouts from the downstream operation's measured latency distribution, not a convenient default**: Derive the timeout value from the actual p99/p999 latency of the specific downstream operation, with margin, rather than reusing a generic timeout value across unrelated integrations with very different latency characteristics.
2. **Check actual outcome after a timeout, before acting on presumed failure**: For any state-mutating integration call, query the downstream system's own status/idempotency-key lookup after a timeout to determine what actually happened, rather than immediately treating "no response in time" as "did not happen."
3. **Use idempotency keys on every state-mutating call**: Attach a client-generated idempotency key to calls that mutate state (payments, bookings, provisioning), so that even if a retry does fire after a timeout, the downstream system can recognize and deduplicate the repeated request instead of executing it twice.
4. **Distinguish "timed out" from "failed" in the agent's own state model**: Represent a timeout as its own explicit outcome state (unknown/pending-verification) rather than collapsing it into the same "failed" state as an explicit error response, so downstream fallback logic doesn't treat the two as equivalent.
5. **Coordinate timeout budgets explicitly across a call chain**: Where an integration call is itself part of a longer chain, ensure the calling agent's timeout leaves enough margin for the callee's own documented timeout and processing time, rather than setting timeouts independently at each layer with no shared budget.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| post_timeout_success_rate | Rate at which calls the agent timed out are later found to have succeeded on the downstream system | Alert if rate is materially above zero for idempotency-sensitive integrations |
| duplicate_side_effect_count | Count of duplicate mutating actions (charges, bookings, records) attributable to timeout-triggered retries | Alert on any nonzero count for financial or irreversible actions |
| timeout_rate_vs_downstream_p99 | Agent-observed timeout rate compared against the downstream system's own reported p99 latency | Alert if timeout rate rises in lockstep with downstream latency rather than with genuine errors |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Post-timeout success detected for a mutating call | post_timeout_success_rate nonzero on a payment/booking/provisioning integration | Critical | Reconcile the duplicated action immediately, add idempotency-key enforcement, review timeout value against measured latency |
| Timeout rate tracking downstream load | timeout_rate_vs_downstream_p99 shows correlation during a downstream load event | Medium | Widen timeout margin or add a post-timeout status check before the next load event recurs |

## Related Patterns
- [Cascade Timeout Interaction](../../fault-tolerance/failures/cascade-timeout-interaction.md) - covers timeout values interacting across a call chain to amplify system-wide load via retries; this pattern is the narrower, single-integration correctness failure (duplicate/incorrect side effects) that a timeout-then-retry produces even without a broader cascade
- [Integration Order Dependency](./integration-order-dependency.md) - both involve an agent acting on an incomplete or incorrect picture of a downstream call's true completion state
- [Recovery Data Corruption](../../fault-tolerance/failures/recovery-data-corruption.md) - shares the underlying "acted before the true outcome was known" mechanism, applied to failure-recovery replay rather than to normal-path timeout handling
