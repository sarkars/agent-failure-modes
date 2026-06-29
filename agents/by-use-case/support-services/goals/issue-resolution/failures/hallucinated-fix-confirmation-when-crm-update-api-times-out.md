# Hallucinated Fix-Confirmation When CRM-Update API Times Out

## Issue: When an Issue-Resolution Agent's Call to Update the Customer's Account or Case Record in the CRM Times Out or Returns an Error, the Agent Completes a Plausible "I've Updated Your Account" Response to the Customer Instead of Treating the Failed Call as a Hard Stop, So the Account Record Never Actually Reflects the Fix

**Frequency**: Occasional

**Symptoms**
- Customers are told a specific account change has been made (refund applied, plan downgraded, address corrected) but the CRM record shows no corresponding update at the timestamp of the confirmation
- The CRM-update API call in the session trace returns a timeout or error immediately before the agent's confirmation message, with no retry or fallback logged between the failed call and the confirmation being sent
- The confirmation message's wording and specificity are identical between sessions where the update genuinely succeeded and sessions where the call failed, making the two indistinguishable to the customer or a casual transcript reviewer
- Customers who were told the change was made re-contact support later still seeing the old value, and the second contact is logged as a fresh issue rather than as a failed-update follow-up
- The gap concentrates during periods of elevated CRM-API latency or error rate and disappears once the API returns to baseline performance

**Root Cause**
When a tool call fails, a language model generating the next turn of a conversation has no inherent mechanism forcing it to treat the failure as terminal; absent an explicit instruction and control-flow branch for the error case, the model continues producing the most probable next utterance given the conversation so far, which is the confirmation it would generate after a successful update. The model is not distinguishing "the call succeeded" from "the call failed" at the level of what it says next unless the failure is surfaced as a distinct state that blocks the success-path response template.

**Example**
```
Customer asks the agent to apply a billing credit for a service outage
Agent calls the CRM's account-update API to post the credit to the account
API call times out after the configured retry window is exhausted
Agent's next-turn generation proceeds from the conversation history as though the update were the expected outcome, producing: "I've applied a $40 credit to your account, you'll see it on your next statement"
No credit record exists anywhere in the CRM; the account balance is unchanged
Customer reviews their next statement, finds no credit, and re-contacts support describing it as a new billing dispute rather than a failed update follow-up
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Survey taxonomies of LLM agent hallucination identify completion of a plausible response despite an upstream tool-call failure as a distinct hallucination category, separate from factual hallucination in open-domain generation | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Tool-use error detection research finds that dialogue agents frequently fail to differentiate a failed or erroring tool response from a successful one when generating the next conversational turn, absent an explicit error-handling branch | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Lifecycle studies of platform-orchestrated agentic workflow failures identify silent continuation past a failed orchestration step, rather than halting or surfacing the failure, as a recurring root cause of downstream user-facing inconsistency | [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735) |

**Contributing Factors**
- No explicit control-flow branch distinguishes a failed CRM-update API call from a successful one before the agent generates its next customer-facing message
- The fix-confirmation message template is shared between the success path and any failure path, so a failed call produces the same plausible-sounding output as a successful one
- No reconciliation job cross-checks customer-facing "I've updated your account" messages against actual CRM change-log entries to catch confirmations sent without a corresponding record

---

## Mitigation Strategies

1. **Hard-Stop on CRM-Update API Failure**: Require the agent to treat any timeout or error from the CRM-update API as a blocking failure that prevents the success-path confirmation message from being generated, routing instead to a distinct failure-acknowledgment-and-retry path
2. **Separate Failure-Path Template**: Implement a distinct customer-facing message for CRM-update failures ("I'm having trouble updating your account right now, retrying") so the model cannot default to the success-path template when no update record exists
3. **Synchronous Confirmation Before Messaging**: Require the agent to verify the CRM-update API's response includes a valid change-record identifier before sending any fix-confirmation message to the customer
4. **Confirmation-to-Record Reconciliation**: Run a continuous reconciliation job comparing every customer-facing fix-confirmation message against the CRM's actual change-log entries, flagging any confirmation with no matching record

### Metrics
- Rate of fix-confirmation messages sent with no corresponding CRM change-log entry
- CRM-update API error/timeout rate, correlated against confirmation-without-record rate
- Re-contact rate within a defined window following an unconfirmed (record-less) update

### Alerts
- A fix-confirmation message is sent with no corresponding CRM change-log entry created within the expected window → P1
- CRM-update API error rate exceeds the defined threshold for a rolling window while confirmation messages continue to be sent → P1
- A customer re-contacts support describing a prior update that has no matching change-log entry → P2

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735)
