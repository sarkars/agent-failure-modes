# Multi-Agent Handoff Drops Jurisdiction Flag Between Account-Opening and Compliance-Screening Agents

## Issue: An Account-Opening Agent Notes in Free Text That a New Client's Stated Residency and the Jurisdiction Implied by Their Funding Source Do Not Match, but the Structured Client Profile Handed Off to the Compliance-Screening Agent Has No Field for a Jurisdiction Conflict, So the Client Is Screened Only Under Their Stated Residency's Rules

**Frequency**: Occasional

**Symptoms**
- A client account is approved and screened under a single jurisdiction's regulatory rules, even though the account-opening agent's own notes flagged that the client's stated residency and their funding source's jurisdiction do not match
- The structured client profile handed off to the compliance-screening agent contains the stated residency field used to select applicable rules, with no field capturing the funding-source jurisdiction mismatch the account-opening agent's notes raised
- Compliance-screening agents operating purely from the structured profile show a materially lower rate of applying the additional jurisdiction's rules to clients with a noted funding-source mismatch than screening agents given the account-opening agent's full intake transcript
- The jurisdiction conflict surfaces only during a later regulatory examination or a cross-border transaction review, by which point the account has been open and active under a single jurisdiction's rule set
- The mismatch concentrates on clients whose funding source is a different jurisdiction's institution than their stated residence, since those are the cases where a second jurisdiction's rules may also apply and the account-opening agent's note is the only place that distinction is captured

**Root Cause**
The compliance-screening agent's rule-selection logic operates on the structured client profile's fixed schema, and that schema was built to capture a single stated residency used to select the applicable jurisdiction's rules, not a funding-source jurisdiction that might differ from it. Because a jurisdiction mismatch is identified through the account-opening agent's free-text intake reasoning rather than a structured multi-jurisdiction field, it has no corresponding place in the handoff schema and is therefore invisible to the screening agent, even though the same model, given the intake transcript, would readily flag the conflict.

**Example**
```
Account-opening agent processes a new client whose stated residency is Country A, but whose funding source is a bank account domiciled in Country B, and notes in free text: "Funding source jurisdiction (Country B) does not match stated residency (Country A) -- may require dual-jurisdiction screening"
Account-opening agent records the client's stated residency in the structured profile field used for rule selection, with no field for the funding-source jurisdiction mismatch
Structured profile handed off to the compliance-screening agent shows only Country A as the applicable jurisdiction
Compliance-screening agent screens the client only against Country A's rules and approves the account
Country B's stricter source-of-funds documentation requirement, which would have applied given the funding source, is never triggered, and the gap surfaces during a cross-border transaction review eighteen months later
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Surveys of multi-agent LLM system failures identify narrow handoff interfaces between staged agents, where a downstream agent's structured input omits a finding an upstream agent's free-text reasoning surfaced, as a distinct and recurring failure category | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Platform-orchestrated agentic workflow failure studies find that narrowing the interface between orchestrated stages to a fixed single-value schema is a primary mechanism by which a multi-jurisdiction or cross-record finding present upstream fails to reach a downstream screening stage | [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735) |
| Research on agentic AI applied to financial-services modeling and model-risk-management tasks identifies the absence of a shared, continuously synced structured state between sequential intake and screening agents as a distinct reliability gap from either agent's individual screening accuracy | [Agentic AI Systems Applied to tasks in Financial Services: Modeling and model risk management crews](https://arxiv.org/abs/2502.05439) |

**Contributing Factors**
- Structured client-profile schema captures a single stated-residency field used for rule selection, with no field for a funding-source jurisdiction or other jurisdiction-conflict signal
- Account-opening agent's jurisdiction-mismatch reasoning is recorded only in free-text intake notes, with no structured escalation path into the compliance-screening agent's input
- No mandatory dual-jurisdiction screening trigger fires when the account-opening agent's free-text notes contain jurisdiction-mismatch language, since the screening agent's logic does not parse those notes

---

## Mitigation Strategies

1. **Add a Jurisdiction-Conflict Field to the Client-Profile Schema**: Require the account-opening agent to record any funding-source or other jurisdiction-conflict finding in a dedicated structured field that triggers multi-jurisdiction screening, rather than leaving it only in free-text intake notes
2. **Screening Agent Cross-Checks Intake Transcript for Jurisdiction-Mismatch Language**: Require the compliance-screening agent to scan the account-opening agent's free-text notes for jurisdiction-mismatch language before finalizing single-jurisdiction screening, not just the structured stated-residency field
3. **Mandatory Dual-Jurisdiction Screening on Unresolved Conflict**: Automatically trigger screening under both the stated-residency jurisdiction and any flagged funding-source jurisdiction whenever the account-opening stage's output contains an unresolved jurisdiction-conflict finding
4. **Track Conflict-Field-Absent Approval Rate**: Continuously measure how often a client with an account-opening jurisdiction-conflict note is nonetheless screened under only their stated residency when the profile schema lacked a conflict field

### Metrics
- Rate of account approvals where the account-opening transcript contains unresolved jurisdiction-mismatch language not reflected in the structured client profile
- Time between an account approval and a later-discovered jurisdiction-conflict gap for the same client
- Dual-jurisdiction screening rate for clients with a noted funding-source mismatch, segmented by presence vs. absence of a structured conflict field

### Alerts
- A client account is approved while the account-opening transcript contains unresolved jurisdiction-mismatch language → P1
- A client already onboarded is found via later examination or transaction review to have had an unresolved jurisdiction conflict at approval time → P1
- Conflict-field-absent approval rate across a rolling window exceeds the defined threshold → P2

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735)
- [Agentic AI Systems Applied to tasks in Financial Services: Modeling and model risk management crews](https://arxiv.org/abs/2502.05439)
