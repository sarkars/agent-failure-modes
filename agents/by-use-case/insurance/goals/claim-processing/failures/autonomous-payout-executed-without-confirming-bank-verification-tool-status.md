# Autonomous Payout Executed Without Confirming Bank-Verification Tool's Actual Status

## Issue: A Claims-Payment Agent Authorized to Autonomously Disburse Funds Once Payee Bank Details Are Verified Initiates and Completes the Disbursement Step Without Re-Checking the Actual Return Status of the Bank-Account-Verification Tool Call, Treating the Mere Fact That a Verification Call Was Made as Equivalent to the Call Having Returned a Successful Confirmation, So Payments Proceed Against Unverified or Failed Verification Results

**Frequency**: Occasional

**Symptoms**
- The agent's payment narrative states that payee bank details were "verified" and proceeds to disburse funds, while the actual logged response from the bank-verification tool shows a "pending," "unable to verify," or error status rather than a confirmed match
- Disbursements occur within seconds of a verification call being initiated, in cases where the verification service's actual response was asynchronous or required a follow-up poll the agent never performed
- Payments sent to an unverified account are later returned, rejected by the receiving bank, or flagged by the payee as never received, only surfacing the gap after funds have left the carrier's account
- Audit of the agent's tool-call log shows the verification API was called and a request ID was generated, but the corresponding confirmation-status check (the actual pass/fail result) was never retrieved before the disbursement instruction was issued
- The failure concentrates on payees with newly added or recently changed bank details, since first-time or changed account verification is more likely to return a non-immediate "pending" status that the agent treats as equivalent to "verified"

**Example**
```
A claims-payment agent processes an approved auto-glass claim with a $1,400 payout; the payee recently switched banks and provided new account details for direct deposit
The agent calls the bank-account-verification tool, which returns an immediate acknowledgment with a request ID and a status of "pending -- verification in progress, check back in up to 24 hours"
The agent's payment workflow proceeds to disburse the $1,400 immediately, with its summary stating "payee bank details verified, payment issued," based on having made the verification call rather than on the call's actual pending status
Eighteen hours later the verification tool's asynchronous result resolves to "unable to verify -- account number does not match name on file," but by then the payment has already been sent and the funds are unrecoverable from the mismatched account
Finance reconciliation flags the payment as unrecovered three weeks later when the payee calls to ask why their direct deposit never arrived, despite the carrier's system showing the claim as paid
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Survey work on LLM-agent provenance finds that trustworthy tool use requires tracing not just that a tool was called but the actual reliability and content of its returned result, since a call having been made is frequently conflated with the call having succeeded | [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1) |
| Research on detecting and correcting tool-use errors in agent and dialogue systems finds that agents frequently fail to distinguish a tool call that returned a pending, partial, or error response from one that returned a successful, actionable result, and proceed as though the call succeeded | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Tool-use calibration research finds that agents relying on evidence-gathering tool calls without a verification or confirmation step show systematically higher overconfidence in the correctness of the tool's outcome than agents using tools that ground reasoning with an explicit pass/fail check | [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264) |

**Contributing Factors**
- The bank-verification tool's API returns an immediate acknowledgment response (call accepted, request ID issued) that is structurally similar to a success response, and the agent's prompt does not explicitly distinguish "call accepted" from "verification confirmed"
- The disbursement step is authorized to proceed autonomously once verification is "initiated" in the workflow logic, rather than being gated on a specific confirmed-status value retrieved from the tool
- Asynchronous verification results that resolve minutes or hours after the initial call are not re-checked before the payment instruction executes, since the agent's session ends once the disbursement step completes
- No automated, independent gate sits between the verification tool and the payment-execution step that hard-blocks disbursement on any status other than an explicit confirmed match

---

## Mitigation Strategies

1. **Explicit Status-Value Gating**: Require the payment-execution step to read and branch on the verification tool's actual status field (confirmed / pending / failed), not merely on whether a verification call was logged as having been made
2. **Asynchronous Poll-Before-Pay**: For verification tools that return an asynchronous or pending result, require an automated poll-and-wait step that retrieves the final status before disbursement is permitted, rather than allowing the agent's session to proceed on the initial acknowledgment
3. **Independent Disbursement Gate**: Insert a non-LLM, deterministic gate between verification and payment execution that hard-blocks any disbursement lacking a confirmed-match status in the verification system of record
4. **Post-Call Provenance Logging**: Log the verification tool's full status-transition history (pending to confirmed/failed) against each payment, and flag any payment issued before a confirmed-status timestamp exists

### Metrics
- Number of disbursements issued before the corresponding bank-verification call reached a confirmed (non-pending) status
- Rate of payments later returned, rejected, or reported as unreceived, broken out by whether verification was confirmed before disbursement
- Average time between verification-call initiation and disbursement, for payees with newly added or changed bank details

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Payment issued on pending verification | Disbursement instruction executes while the linked bank-verification call's status is pending or unresolved | P1 | Halt disbursement if not yet settled; if already sent, immediately initiate recall/reversal and flag for finance review |
| Verification failure post-payment | A verification call resolves to failed or mismatched status after a linked payment has already disbursed | P1 | Initiate fund-recovery process and route payee account for manual re-verification |
| Disbursement-to-verification latency anomaly | Time between verification-call initiation and disbursement falls below the minimum time the verification service requires to return a confirmed result | P2 | Audit the payment workflow for missing poll-and-wait logic |

---

## References

- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264)
