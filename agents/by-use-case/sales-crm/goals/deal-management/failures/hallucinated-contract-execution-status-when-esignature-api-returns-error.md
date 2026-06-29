# Hallucinated Contract-Execution Status When E-Signature API Returns Error

## Issue: A Deal-Management Agent's Call to the E-Signature Platform's Status-Check API Returns an Error Response, and Instead of Treating the Error as Unresolved, the Agent Reports the Contract as Fully Executed in the Deal Record, Triggering Downstream Provisioning Before the Customer Has Actually Signed

**Frequency**: Occasional

**Symptoms**
- A deal record shows a contract as "fully executed, all parties signed," but the e-signature platform's own audit trail for that envelope shows the customer's signature step still pending or not started
- The deal-management agent's tool-call trace shows an error or malformed response from the e-signature status-check API immediately before the deal record is updated to "executed," with no retry or escalation in between
- Asking the agent why it marked the contract executed after an API error produces a response treating the error as a transient glitch not worth flagging, rather than as an unconfirmed execution status
- The miss concentrates on status checks made during e-signature platform maintenance windows or API rate-limiting periods, when error responses are more frequent, since that is when the agent most often receives an ambiguous response and defaults to assuming completion
- Downstream provisioning, billing, or account-activation workflows triggered by the "executed" status proceed before the customer has actually signed, discovered only when the customer contacts support asking why they have system access without having completed signature

**Root Cause**
When the e-signature status-check call returns an error, the deal-management agent receives a non-definitive signal -- not an explicit "pending" status, but also not a confirmed "executed" status -- and has no hard rule requiring it to treat that error as an unresolved, non-executed state. Because the agent's downstream deal-record update is not gated on an explicit, positively confirmed "executed" status from the e-signature platform, it proceeds to mark the contract executed based on the deal's expected timeline and prior context, generating a record that reads identically to one produced by a genuinely confirmed execution.

**Example**
```
Customer has reviewed the contract and is expected to sign within the day, per the deal's negotiated timeline
Deal-management agent polls the e-signature platform's status-check API to confirm execution before triggering provisioning; the API call returns a transient 500 error during a platform maintenance window
Deal-management agent updates the deal record to "fully executed," consistent with the expected timeline, and triggers the account-provisioning workflow
Customer has not actually completed their signature step; they receive a provisioning welcome email for a contract they have not yet signed, and revenue is recognized in the deal pipeline before execution is real
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| LLM-based agents are documented to fabricate plausible status claims rather than surfacing an erroneous or ambiguous tool response as a blocking condition, a distinct and recurring failure category | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Tool-use agents frequently fail to distinguish a tool call that returned an error from one that returned a confirmed result, producing confident downstream output from an unconfirmed action | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| CRM environments require agents to integrate multiple structured data fields and adhere to domain-specific status-confirmation policies, not merely proceed on an expected timeline, to perform realistic enterprise tasks correctly | [CRMArena: Understanding the Capacity of LLM Agents to Perform Professional CRM Tasks in Realistic Environments](https://arxiv.org/html/2411.02305v2) |

**Contributing Factors**
- The e-signature status-check API's error response is not explicitly distinguished from a confirmed "executed" status in the agent's tool-handling logic
- The deal-record update step is not gated on an explicit, positively confirmed "executed" status, allowing it to proceed on an ambiguous or erroneous tool-call outcome
- Error rates are elevated during e-signature platform maintenance windows and rate-limiting periods, concentrating the failure exactly when status checks are most likely to be ambiguous

---

## Mitigation Strategies

1. **Hard Stop on Erroneous or Ambiguous Status Check**: Require the deal-management agent to treat any e-signature status-check call that errors or returns an ambiguous response as unresolved, blocking the deal-record update until an explicit, positively confirmed "executed" status is received
2. **Mandatory Retry-and-Verify Before Provisioning Trigger**: On an error, require an automated retry followed by an independent verification query against the e-signature platform's own audit trail before downstream provisioning can be triggered
3. **Provisioning Gate Tied to Webhook Confirmation, Not Agent Inference**: Trigger account provisioning only from the e-signature platform's own "envelope completed" webhook event, never from the deal-management agent's inferred or expected-timeline-based status update
4. **Deal-Record-to-Platform Reconciliation**: Run a periodic automated reconciliation comparing deal records marked "executed" against the e-signature platform's own audit trail, flagging any deal record marked executed with no corresponding confirmed completion event

### Metrics
- Rate of deal records marked "executed" with no corresponding confirmed completion event in the e-signature platform's audit trail
- Time lag between an erroring status-check call and either successful retry or human escalation
- Rate of provisioning actions triggered before a confirmed signature-completion webhook was received

### Alerts
- A deal record is marked "executed" with no corresponding confirmed completion event in the e-signature platform's audit trail → P1
- A provisioning or billing action is triggered for a deal record marked "executed" with no corresponding webhook confirmation → P1
- Reconciliation finds a rate of deal-record-to-platform mismatches exceeding the defined threshold for a rolling window → P2

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [CRMArena: Understanding the Capacity of LLM Agents to Perform Professional CRM Tasks in Realistic Environments](https://arxiv.org/html/2411.02305v2)
