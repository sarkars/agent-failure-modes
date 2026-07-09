# Multi-Agent Handoff Drops Partial-Credit-Already-Issued Flag Between Triage and Billing Agent

## Issue: A Triage Agent That Learns During Intake That a Customer Has Already Been Issued a Partial Credit for a Disputed Charge by a Prior Agent Records That Fact Only in Its Own Conversational Summary, and When the Conversation Is Routed to a Downstream Specialized Billing-Dispute Agent That Operates on a Structured Dispute-Case Object Containing Only the Disputed Amount and Category, the Already-Issued Partial Credit Never Crosses the Handoff Boundary -- So the Billing Agent Calculates and Approves a Second, Full-Amount Refund on Top of the Credit the Customer Already Received

**Frequency**: Occasional

**Symptoms**
- The triage agent's transcript explicitly states "customer confirms they already received a $15 partial credit from a prior contact for this charge," but the structured dispute-case object passed to the billing agent contains only `disputed_amount: 60.00` and `category: duplicate_charge`, with no field for prior partial credits
- The billing agent's resolution message offers a full $60 refund with no acknowledgment of, or deduction for, the $15 already credited, because that detail was never represented in the data structure it operates on
- Finance reconciliation discovers the customer received $15 (from the prior contact) plus $60 (from the billing agent's full resolution) against a $60 disputed charge, a $15 overpayment
- The triage agent's own summary, read by a human auditing the case after the fact, contains the missing fact in plain text, confirming the information existed in the conversation but did not survive the structured handoff to the next agent
- Overpayment incidents cluster specifically around disputes that involved a prior partial resolution before being re-escalated or re-opened, rather than disputes resolved in a single agent's conversation

**Example**
```
Customer previously contacted support about a $60 duplicate charge and received a $15 goodwill credit while the full investigation was pending; this is logged in the triage agent's free-text case notes
Customer recontacts a week later asking about the remaining balance of the dispute; triage agent correctly summarizes "customer already has a $15 credit applied, remaining disputed amount under review is $45" in its own conversational reasoning
Triage agent routes the case to the billing-dispute agent by creating a structured case object with fields disputed_amount: 60.00, category: duplicate_charge, status: escalated -- no field exists for "prior_credits_issued," so the $15 fact is dropped
Billing agent, operating only on the structured case object, approves a refund of the full $60.00 disputed amount, unaware that $15 was already issued
Customer receives $60.00 on top of the earlier $15.00, a $15.00 overpayment caught only during a later finance audit
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Agent-environment and multi-agent coordination failure research documents information present in one agent's working context being lost when control passes to a downstream agent operating on a narrower, structured representation of the task | [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504) |
| Failure-mode taxonomies for LLM systems identify multi-agent handoff and state-passing errors as a distinct production failure category, separate from single-agent reasoning errors, arising specifically at the boundary between cooperating agents | [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933) |

**Contributing Factors**
- The structured case object used to hand off from triage to the billing-dispute agent has no field for prior partial credits or partial resolutions, so there is no slot for that fact to occupy even if someone tried to pass it along
- The triage agent's free-text conversational summary is not parsed or required to populate the structured handoff object; the two representations of the same conversation diverge silently
- The billing agent's refund-calculation logic computes the full disputed amount from the case object's `disputed_amount` field alone, with no instruction or tool call to check for prior credits issued against the same dispute or charge ID before finalizing an amount
- No deterministic cross-check queries the credit/refund ledger for prior actions against the same charge ID before a new refund is approved, leaving the only safeguard dependent on information surviving the handoff

---

## Mitigation Strategies

1. **Structured Prior-Resolution Field**: Add an explicit `prior_credits_issued` (amount and date) field to the dispute-case handoff object, and require the triage agent to populate it whenever a prior partial credit is mentioned or discoverable, rather than leaving it to free-text summary alone
2. **Ledger Cross-Check Before Refund Approval**: Require the billing-dispute agent to query the credit/refund ledger directly for the charge ID before calculating a refund amount, rather than relying solely on the handoff object's stated disputed amount
3. **Net-Amount Calculation Enforcement**: Require refund-calculation logic to explicitly compute `disputed_amount - prior_credits_issued` and never approve a refund without first checking whether that subtraction field is populated or queried
4. **Handoff Completeness Audit**: Periodically sample triage-to-billing handoffs and diff the triage agent's free-text summary against the structured case object to detect facts mentioned in conversation but missing from the object passed downstream

### Metrics
- Rate of refund approvals where a prior credit exists in the ledger for the same charge ID but was not reflected in the refund calculation
- Number of fields present in triage free-text summaries but absent from the structured handoff object, sampled per audit cycle
- Dollar amount of overpayments per month attributable to missed prior-credit deductions

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Ledger/handoff mismatch | Credit/refund ledger shows a prior credit for the charge ID that is absent from the billing agent's case object | P1 | Block refund approval; require ledger cross-check before resuming |
| Full-amount refund on re-opened dispute | Billing agent approves a refund equal to the full original disputed amount on a dispute case marked as previously partially resolved | P1 | Auto-flag for finance review before payout |
| Handoff field-drop rate spike | Sampled audits show rising rate of facts present in triage summary but missing from structured case object | P2 | Review and extend the handoff schema; add required-field validation |

---

## References

- [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504)
- [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933)
