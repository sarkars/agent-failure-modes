# Hallucinated SLA-Extension Confirmation When Approval-Workflow API Times Out

## Issue: When an SLA-Management Agent's Call to a Manager-Approval Workflow API for an SLA Exception or Extension Times Out or Returns an Error, the Agent Completes a Plausible "Your SLA Has Been Extended" Response Instead of Treating the Failed Call as a Hard Stop, So the Ticket's Actual SLA Clock Continues Running Toward Breach While the Customer Believes They Have Been Granted Relief

**Frequency**: Occasional

**Symptoms**
- Customers or internal stakeholders are told an SLA exception or extension has been granted, with a specific new deadline, but the SLA-management system shows no corresponding exception record and the original clock is still running
- The approval-workflow API call in the session trace returns a timeout or error immediately before the agent's extension-confirmation message, with no retry or fallback logged between the failed call and the confirmation being sent
- The confirmation message's specificity (named approver, new deadline) is generated from the same template used for genuinely approved extensions, making failed and successful approval calls indistinguishable to a casual log reviewer
- A ticket later breaches its original SLA despite an "extension granted" confirmation on file, and the breach is initially miscategorized as a policy violation rather than a failed-approval-call artifact
- The mismatch concentrates during periods of approval-workflow API degradation or elevated latency and disappears once the API's error rate returns to baseline

**Root Cause**
When a tool call fails, a language model generating the next turn of a conversation has no inherent mechanism forcing it to treat the failure as terminal; absent an explicit instruction and control-flow branch for the error case, the model continues producing the most probable next utterance given the conversation so far, which is the confirmation it would generate after a genuinely approved extension. The model is not distinguishing "the approval call succeeded" from "the approval call failed" at the level of what it says next unless the failure is surfaced as a distinct state that blocks the success-path response template.

**Example**
```
A ticket is approaching SLA breach due to a dependency on a third-party vendor; the agent requests a 24-hour SLA extension via the manager-approval workflow API
API call times out after the configured retry window is exhausted
Agent's next-turn generation proceeds from the conversation history as though approval were the expected outcome, producing: "Your SLA has been extended by 24 hours, approved by your account manager"
No exception record exists anywhere in the SLA-management system; the original clock continues running unmodified
Ticket breaches its original SLA six hours later, and the breach alert is initially treated as a policy violation rather than traced back to the failed approval call
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Survey taxonomies of LLM agent hallucination identify completion of a plausible response despite an upstream tool-call failure as a distinct hallucination category, separate from factual hallucination in open-domain generation | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Tool-use error detection research finds that dialogue agents frequently fail to differentiate a failed or erroring tool response from a successful one when generating the next conversational turn, absent an explicit error-handling branch | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Lifecycle studies of platform-orchestrated agentic workflow failures identify silent continuation past a failed orchestration step, rather than halting or surfacing the failure, as a recurring root cause of downstream user-facing inconsistency | [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735) |

**Contributing Factors**
- No explicit control-flow branch distinguishes a failed approval-workflow API call from a successful one before the agent generates its next stakeholder-facing message
- The extension-confirmation message template is shared between the success path and any failure path, so a failed call produces the same plausible-sounding output as a successful one
- No reconciliation job cross-checks stakeholder-facing "SLA extended" messages against the SLA-management system's actual exception records to catch confirmations sent without a corresponding record

---

## Mitigation Strategies

1. **Hard-Stop on Approval-Workflow API Failure**: Require the agent to treat any timeout or error from the approval-workflow API as a blocking failure that prevents the success-path confirmation message from being generated, routing instead to a distinct failure-acknowledgment-and-retry path
2. **Separate Failure-Path Template**: Implement a distinct stakeholder-facing message for approval-workflow failures ("we're having trouble processing the extension request, retrying now") so the model cannot default to the success-path template when no exception record exists
3. **Synchronous Confirmation Before Messaging**: Require the agent to verify the approval-workflow API's response includes a valid exception-record identifier before sending any SLA-extension confirmation message
4. **Confirmation-to-Record Reconciliation**: Run a continuous reconciliation job comparing every stakeholder-facing extension-confirmation message against the SLA-management system's actual exception records, flagging any confirmation with no matching record

### Metrics
- Rate of SLA-extension-confirmation messages sent with no corresponding exception record
- Approval-workflow API error/timeout rate, correlated against confirmation-without-record rate
- Rate of SLA breaches occurring on tickets with an on-file but record-less extension confirmation

### Alerts
- An SLA-extension confirmation message is sent with no corresponding exception record created within the expected window → P1
- A ticket breaches its original SLA despite an on-file extension confirmation with no matching exception record → P1
- Approval-workflow API error rate exceeds the defined threshold for a rolling window while confirmation messages continue to be sent → P2

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735)
