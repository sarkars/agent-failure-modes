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

## Mitigation Strategies

### Prevention
1. **Risk-scaled timeout durations with no blanket auto-approve**: Set timeout length and fallback behavior based on the action's risk (amount, reversibility, fraud signals) instead of the same 15-minute/auto-approve default for a $5 and a $5,000 refund — this directly targets the example's root configuration flaw. Trade-off: requires a reliable risk score per action type, and misclassified low-risk actions could face unnecessarily long delays.
2. **Escalation-on-timeout instead of auto-approve-on-timeout**: When the primary approver doesn't respond in time, escalate to a secondary approver rather than defaulting to approval — the manager in the example being in a meeting shouldn't mean the refund silently proceeds; it should mean someone else gets asked. Trade-off: requires maintaining a staffed secondary-approver chain for every approval type, which has real staffing cost.
3. **Fraud/risk-signal override on the timeout fallback**: For requests carrying elevated risk signals (known fraud account, unusual pattern), disable auto-approve-on-timeout entirely regardless of the configured default, forcing either escalation or blocking instead — the example's $500 loss came from a known fraud account being auto-approved by a generic timeout rule that didn't account for account risk. Trade-off: requires risk signals to be available and checked at timeout-evaluation time, not just at request creation.

### Detection & Response
1. **Timeout-rate-by-action-type tracking**: Monitor what fraction of each action type times out and what fallback fires, so a pattern like "refunds routinely time out and auto-approve" surfaces before it becomes a recurring fraud vector.
2. **Auto-approval outcome auditing**: Specifically track outcomes of actions that were auto-approved via timeout (not manually approved) and compare their downstream results (chargebacks, disputes, fraud flags) against manually-approved actions — this would have caught the fraud-account refund pattern before repeat occurrences.
3. **Approver-unavailability correlation**: Cross-reference timeout events against approver calendar/status (in a meeting, out of office) to distinguish systemic timeout misconfiguration from individual approver unavailability, informing whether the fix is timeout tuning or escalation-chain staffing.

### Architecture Patterns
1. **Tiered timeout-and-fallback matrix**: Maintain an explicit action-risk-to-timeout-and-fallback mapping (e.g., low-risk/short-timeout/auto-approve-ok vs. high-risk/short-timeout/escalate-only) rather than a single global default, so risk and timeout behavior are configured together, not independently. Deployment consideration: needs upfront classification work across all approval-gated action types and ongoing maintenance as new action types are added.
2. **Escalation-chain service with SLA tracking**: Build a dedicated escalation service that tracks approval SLAs, automatically routes to the next approver on timeout, and notifies all parties of the escalation — replacing ad hoc per-workflow timeout handling with a shared, auditable mechanism. Deployment consideration: centralizing escalation logic is a larger investment than per-workflow timeout config but avoids the inconsistent handling described in the pattern's symptoms.
3. **Partial/conditional approval for time-sensitive cases**: Support an "approve with conditions" state (e.g., approve up to $100 immediately, escalate anything above) so time-sensitive low-risk portions of a request can proceed while the risky portion still requires review. Deployment consideration: only applicable to actions that can be meaningfully split or capped, and adds complexity to the approval UI/API.

### Metrics
1. **timeout_rate_by_action_type**: % of approval requests that hit timeout rather than receiving a timely decision, broken out by action type; target < 10%; alert if > 30% for any type.
2. **auto_approve_fraud_correlation**: % of timeout-auto-approved actions later flagged as fraudulent/disputed, versus the same rate for manually-approved actions; target: parity or better; alert if timeout-auto-approved rate is 2x+ the manual rate.
3. **escalation_chain_success_rate**: % of timed-out requests successfully escalated to and resolved by a secondary approver (rather than falling through to auto-approve or permanent block); target > 95%; alert if < 80%.
4. **risk_scaled_timeout_coverage**: % of approval-gated action types with a distinct, risk-appropriate timeout/fallback configuration (vs. using the global default); target 100%; alert if < 80%.

### Alerts
1. **Timeout Auto-Approval on Elevated-Risk Account** (P1): Condition — an auto-approve-on-timeout fires for a request flagged with a fraud/risk signal. Action: immediately flag the resulting action for retroactive review and hold any linked disbursement/effect if still reversible.
2. **Escalation Chain Failure** (P1): Condition — escalation_chain_success_rate drops below 80%, indicating timed-out requests aren't reaching a secondary approver. Action: page the workflow owner to fix escalation routing; treat any pending requests as blocked until resolved.
3. **Uniform Timeout Configuration Detected** (P3): Condition — risk_scaled_timeout_coverage falls below 80%, meaning most action types still share one timeout/fallback default. Action: schedule a configuration review to build the risk-scaled timeout matrix for uncovered action types.

## References

- [Braintrust: Agent Observability Guide 2026](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Workflow monitoring
- [Microsoft: Failure Modes in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Human-in-the-loop failures
- [OWASP: AI Agent Security](https://owasp.org/www-project-top-10-for-large-language-model-applications/) - Approval workflow risks
