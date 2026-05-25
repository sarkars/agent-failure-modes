# Approval Timeout Mishandling

## Issue: Agent Behaves Incorrectly When Human Approval Times Out

**Frequency**: Common

**Symptoms**
- Actions auto-approved after timeout without review
- Tasks permanently stuck waiting for approval
- Timeout triggers wrong fallback behavior
- Users unaware approval expired
- Inconsistent timeout handling across actions

**Root Cause**
Approval workflows must handle the case where humans don't respond in time. Poor timeout handling leads to two failure modes: auto-approval (proceeds without actual review) or permanent blocking (task never completes). Both are problematic—auto-approval defeats the purpose of human oversight, while permanent blocking causes operational failures. Timeout durations often don't match the urgency or complexity of the action being approved.

**Example**
```
Scenario: Customer service agent requesting refund approval

Workflow:
  Agent: "Customer requesting $500 refund. Approve?"
  Timeout: 15 minutes (default)
  Fallback: Auto-approve if no response
  
What happened:
  10:00 - Approval request sent to manager
  10:00 - Manager in meeting, notification missed
  10:15 - Timeout reached, auto-approved
  10:30 - Manager sees notification, already processed
  
Investigation:
  - Customer was known fraud account
  - Manager would have denied
  - Refund was for item never purchased
  - Fraud loss: $500
  
Configuration issues found:
  - Same 15-minute timeout for $5 and $5,000 refunds
  - Auto-approve fallback regardless of amount
  - No escalation to secondary approver
  - No notification that approval timed out
```

**Key Statistics**
From Workflow Research (2026):
- 40% of approval-required actions can't safely wait
- Average approval latency: 4 hours for human reviewers
- 35% of organizations use auto-approve on timeout
- 23% have no timeout at all (tasks stuck indefinitely)
- 67% use same timeout for all action types

**Timeout Failure Modes**
| Mode | Description | Risk |
|------|-------------|------|
| Auto-approve | Proceeds after timeout | Defeats oversight |
| Auto-deny | Rejects after timeout | False negatives |
| Permanent block | Never proceeds | Operational failure |
| Silent expiry | Request disappears | Work lost |
| Retry storm | Re-requests repeatedly | Approval fatigue |

**Contributing Factors**
- One-size-fits-all timeout durations
- No secondary approver escalation
- Silent timeout without notification
- Auto-approve as default fallback
- No timeout based on action risk level

**Mitigation Strategies**
1. **Risk-based timeouts**: Higher risk = longer timeout, no auto-approve
2. **Escalation chain**: Timeout escalates to next approver, not auto-approve
3. **Timeout notification**: Alert requester and approver on timeout
4. **Explicit timeout action**: Require human to choose timeout behavior
5. **Approval SLAs**: Track and alert on approaching timeouts
6. **Partial approval**: Allow "approve with conditions" for time-sensitive cases

**Detection**
- Track approval timeout rates by action type
- Monitor auto-approval outcomes
- Alert on repeated timeouts for same approver
- Compare timeout rates to incident rates
- Survey approvers on timeout appropriateness

## References

- [Braintrust: Agent Observability Guide 2026](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Workflow monitoring
- [Microsoft: Failure Modes in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Human-in-the-loop failures
- [OWASP: AI Agent Security](https://owasp.org/www-project-top-10-for-large-language-model-applications/) - Approval workflow risks
