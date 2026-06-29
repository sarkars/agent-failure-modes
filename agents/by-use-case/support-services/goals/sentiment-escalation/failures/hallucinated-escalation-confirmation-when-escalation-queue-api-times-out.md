# Hallucinated Escalation-Confirmation When Escalation-Queue API Times Out

## Issue: When the Sentiment-Escalation Agent's Call to the Human-Escalation Queue API Times Out or Returns an Error, the Agent Completes a Plausible "You've Been Escalated to a Specialist" Response to the Customer Instead of Treating the Failed Call as a Hard Stop, So No Escalation Record Is Ever Created

**Frequency**: Occasional

**Symptoms**
- Customers are told their conversation has been escalated to a human specialist, with a specific queue name or estimated wait time, but no corresponding ticket or queue entry exists in the escalation system
- The escalation-queue API call in the trace returns a timeout or 5xx error immediately before the agent's escalation-confirmation message, with no retry or fallback logged between the failed call and the confirmation being sent
- The confirmation message's specificity (named queue, ETA) is generated from the same template used for genuinely successful escalations, making failed and successful escalations indistinguishable to the customer and to a casual log reviewer
- Customers who were told they were escalated re-contact support later, frustrated that no specialist ever reached out, and the second contact is logged as a new issue rather than as a failed-escalation follow-up
- The mismatch concentrates during periods of escalation-queue API degradation or elevated latency, and disappears once the API's error rate returns to baseline

**Root Cause**
When a tool call fails, a language model completing the next turn of a conversation has no inherent mechanism that forces it to treat the failure as terminal; absent an explicit instruction and control-flow branch for the error case, the model continues generating the most probable next utterance given the conversation so far, which is the confirmation message it would produce after a successful escalation. The model is not distinguishing "the call succeeded" from "the call failed" at the level of what it says next unless the failure is surfaced to it as a distinct state that blocks the success-path response template.

**Example**
```
Customer's message is classified as highly negative sentiment, triggering an automatic escalation to a human specialist
Agent calls the escalation-queue API to create a queue entry and route the conversation to a specialist
API call times out after the configured retry window is exhausted
Agent's next-turn generation proceeds from the conversation history as though escalation were the expected outcome, producing: "You've been escalated to our specialist team, expect a callback within 30 minutes"
No queue entry, ticket, or routing record exists anywhere in the escalation system
Customer waits, receives no callback, and re-contacts support six hours later visibly more frustrated than the original contact
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Survey taxonomies of LLM agent hallucination identify completion of a plausible response despite an upstream tool-call failure as a distinct hallucination category, separate from factual hallucination in open-domain generation | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Tool-use error detection research finds that dialogue agents frequently fail to differentiate a failed or erroring tool response from a successful one when generating the next conversational turn, absent an explicit error-handling branch | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Lifecycle studies of platform-orchestrated agentic workflow failures identify silent continuation past a failed orchestration step, rather than halting or surfacing the failure, as a recurring root cause of downstream user-facing inconsistency | [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735) |

**Contributing Factors**
- No explicit control-flow branch distinguishes a failed escalation-queue API call from a successful one before the agent generates its next customer-facing message
- The escalation-confirmation message template is shared between the success path and any failure path, so a failed call produces the same plausible-sounding output as a successful one
- No reconciliation job cross-checks customer-facing "you've been escalated" messages against actual queue-entry records to catch confirmations sent without a corresponding ticket

---

## Mitigation Strategies

1. **Hard-Stop on Escalation API Failure**: Require the agent to treat any timeout or error from the escalation-queue API as a blocking failure that prevents the success-path confirmation message from being generated, routing instead to a distinct failure-acknowledgment-and-retry path
2. **Separate Failure-Path Template**: Implement a distinct customer-facing message for escalation-queue failures ("we're having trouble connecting you to a specialist, retrying now") so the model cannot default to the success-path template when no escalation record exists
3. **Synchronous Confirmation Before Messaging**: Require the agent to verify the escalation-queue API's response includes a valid ticket or queue-entry identifier before sending any escalation-confirmation message to the customer
4. **Confirmation-to-Record Reconciliation**: Run a continuous reconciliation job comparing every customer-facing escalation-confirmation message against the escalation system's actual queue-entry records, flagging any confirmation with no matching record

### Metrics
- Rate of escalation-confirmation messages sent with no corresponding queue-entry record
- Escalation-queue API error/timeout rate, correlated against confirmation-without-record rate
- Re-contact rate within a defined window following an unconfirmed (record-less) escalation

### Alerts
- An escalation-confirmation message is sent with no corresponding queue-entry record created within the expected window → P1
- Escalation-queue API error rate exceeds the defined threshold for a rolling window while confirmation messages continue to be sent → P1
- A customer re-contacts support describing a prior escalation that has no matching queue-entry record → P2

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735)
