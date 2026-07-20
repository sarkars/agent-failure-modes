# Action-Completion Claimed Without Reading the Tool's Status Field

## Issue: Agent Narrates a Tool-Initiated Action as Complete Based on Having Issued the Call, Not on the Call's Actual Returned Status

An agent calls a tool that performs a real-world side effect — disbursing funds, applying a credit, sending a notification — and generates its confirmation to the user or downstream system immediately after issuing the call, without gating that confirmation on the tool's actual response. When the call times out, returns a `pending`/queued status, or fails outright, the agent has already claimed success. This differs from the tool itself lying about its outcome (see [Silent Tool Failures](./silent-failures.md)): here the tool may be behaving correctly and honestly reporting `pending` or `failed`, but nothing in the agent's control flow requires that status to be read before the completion claim is generated.

**Frequency**: Occasional

**Symptoms**
- The agent's tool-call log shows a request sent, but the response object shows `pending`, `failed`, or a timeout, while the agent's user-facing or downstream message asserts the action is done
- Confirmation language is generated immediately after the call is issued, with no intervening step that parses the response body
- The gap concentrates on asynchronous or eventually-consistent backends (billing, payments, verification services) where an immediate acknowledgment is structurally similar to — but distinct from — a completed-action confirmation
- Downstream consumers (customers, reconciliation systems) discover the discrepancy only later, when the promised effect never materializes
- Audit of the tool-call log shows a request ID was generated but the corresponding confirmed/failed status was never re-fetched before the agent's session or turn ended

## Root Cause
Many real-world action tools (payment disbursement, account verification, notification delivery) accept a request synchronously but resolve it asynchronously, returning an immediate acknowledgment (a request ID, an "in progress" status) that is structurally similar to a success response. Nothing in most agent architectures hard-requires the completion-claiming step to be gated on a specific confirmed-status value from the tool; the act of issuing the call and the act of confirming its outcome are treated as effectively the same event because they usually happen close together in the reasoning trace. This is invisible in the common case (the action completes quickly and the eventual status does turn out to be success) and only surfaces when the backend is slow, degraded, or the action genuinely fails — exactly the cases where an accurate confirmation matters most.

## Example
```
A support agent calls apply_account_credit to issue a customer a $25
goodwill credit for a service outage. The billing microservice is
experiencing elevated latency and the call times out after 8 seconds
without returning a definitive success response.

The agent, having already begun composing its reply in parallel with
issuing the call, tells the customer: "I've applied a $25 credit to
your account -- you'll see it reflected within 1-2 billing cycles."
No subsequent check of the tool's actual response (a timeout, not a
success payload) is performed before or after sending that message.

The customer contacts support three weeks later because no credit
appeared. Investigation shows the original credit request was never
completed -- only the transcript claiming it was.
```

### Domain Examples
- **Insurance / claims payment**: a bank-account-verification tool returns an immediate "pending — check back in up to 24 hours" acknowledgment; the agent's payment workflow disburses funds immediately based on the call having been made, not on a confirmed match. The verification later resolves to "unable to verify — account number mismatch," but the $1,400 payout has already gone to the wrong account and is unrecoverable.
- **Customer service / billing**: see the primary Example above.

## Statistics
| Finding | Context |
|---|---|
| Failure-mode taxonomies for LLM systems identify unverified tool invocation — treating a call's issuance as equivalent to its successful completion — as a distinct, recurring production failure category | Cited across both domain instances of this pattern (Failure Modes in LLM Systems, arXiv:2511.19933) |
| Tool-use calibration research finds agents relying on evidence-gathering tool calls without an explicit pass/fail re-check show systematically higher overconfidence in the correctness of the tool's outcome than agents that gate on a confirmed status | The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents, arXiv:2601.07264 |
| The failure concentrates disproportionately on asynchronous or eventually-consistent backends (payments, verification, notification delivery), where an immediate acknowledgment is easiest to mistake for a completion confirmation | Structural to how async APIs are shaped, consistent across both documented domain instances |

## Mitigations
1. **Confirmation-Gated Response Generation**: Require any "this has been done" language to be generated only after parsing an explicit success field in the tool's response, never immediately after issuing the call.
2. **Explicit Status-Value Gating for Irreversible Actions**: For actions with real-world side effects (payments, credits, disbursements), require the executing step to branch on the tool's actual status field (confirmed / pending / failed), not merely on whether the call was logged as made.
3. **Asynchronous Poll-Before-Confirm**: For tools that return an async/pending result, require an automated poll-and-wait step that retrieves the final status before any completion claim is permitted, rather than allowing the session to proceed on the initial acknowledgment.
4. **Independent, Non-LLM Completion Gate**: Insert a deterministic gate between the action tool and any downstream effect (payment execution, customer-facing confirmation) that hard-blocks on anything other than an explicit confirmed status in the system of record.
5. **Explicit Pending-State Language**: When a tool returns pending/queued/timeout, require the agent to communicate that the request is in progress with a verification timeline, rather than claiming immediate completion.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| unconfirmed_completion_claim_rate | Share of agent-claimed-complete actions where the underlying tool response was pending, failed, or timed out | > 0% for financial/irreversible actions |
| action_to_confirmation_latency | Time between an action tool call being issued and its status reaching a terminal (confirmed/failed) state | Confirmation claimed before this resolves |
| post_action_dispute_rate | Rate of customer/downstream disputes citing a promised action that never took effect | Rising trend or > baseline |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Unconfirmed completion claim | Agent's message asserts an action is complete while the tool's response status is pending, failed, or absent | P1 | Auto-flag for review; for financial actions, halt or reverse if not yet settled |
| Confirmation issued before terminal status | A completion claim's timestamp precedes the tool's confirmed/failed status timestamp | P1 | Route to owning team; audit confirmation-gating logic |
| Audit sampling mismatch | Periodic sampling finds a claimed-complete action absent from the system of record | P1 | Escalate for manual remediation |

## Related Patterns
- [Silent Tool Failures](./silent-failures.md) - the tool itself misreports its outcome (returns success when the action didn't complete); this pattern is the case where the tool honestly reports pending/failed but the agent never reads that field before claiming success
- [Stale Tool Confirmation After Revision](./stale-tool-confirmation-after-revision.md) - a related but distinct failure where a confirmation was genuinely read once, but a subsequent change invalidates it without triggering a fresh re-check
- [Tool Output Misinterpretation](./output-misinterpretation.md) - a related but distinct failure where the agent does read the tool's response but extracts the wrong value from it, as opposed to this pattern's case of never reading the response at all
