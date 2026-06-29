# Multi-Agent Handoff Drops Beneficial-Ownership Discrepancy Before Onboarding Approval

## Issue: A Document-Review Agent Flags in Free-Text Notes That a Supplier's Listed Beneficial Owner Does Not Match Across Two Submitted Documents, but the Structured Pass/Fail Checklist Handed Off to the Onboarding-Approval Agent Has No Field for an Unresolved Ownership Discrepancy, So the Supplier Is Approved

**Frequency**: Occasional

**Symptoms**
- A supplier is approved for onboarding despite a document-review agent's own notes flagging that the beneficial owner named in the corporate registration document does not match the beneficial owner named in the bank-account verification document
- The structured checklist handed off to the onboarding-approval agent shows all required documents as "received" and "verified" with no field capturing an unresolved cross-document discrepancy, even when the document-review agent's free-text notes describe one
- Onboarding-approval agents operating purely from the structured checklist show a materially higher approval rate on suppliers with an unresolved ownership discrepancy than approval agents given the full document-review transcript alongside the checklist
- The discrepancy is discovered only during a later compliance audit or a sanctions-screening re-run, by which point the supplier relationship and payment terms are already active
- The mismatch concentrates on suppliers whose onboarding documents come from jurisdictions where beneficial-ownership registries are not directly queried by the approval agent's own structured data sources, relying instead on the document-review agent's manual cross-document comparison

**Root Cause**
The onboarding-approval agent's decision logic consumes only the structured checklist produced by the document-review stage, and that checklist was built to track whether each required document was received and individually verified, not whether the document-review agent's comparison across documents surfaced a discrepancy. Because a beneficial-ownership mismatch is identified through free-text cross-document reasoning rather than a per-document pass/fail check, it has no corresponding field in the checklist schema and is therefore invisible to the approval agent, even though the same model, given the document-review transcript, would readily flag it.

**Example**
```
Document-review agent compares a new supplier's corporate registration document against its bank-account verification document and notes in free text: "Beneficial owner listed differs between registration filing and bank verification -- requires resolution before approval"
Document-review agent marks each individual document as "received" and "verified" in the structured checklist, since each document independently passes its own format and completeness check
Structured checklist handed off to the onboarding-approval agent shows all required documents as verified, with no field for the cross-document discrepancy
Onboarding-approval agent, working only from the structured checklist, approves the supplier and activates payment terms
Discrepancy surfaces three months later during a routine sanctions-screening re-run, triggering an emergency compliance review of an already-active supplier relationship
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Surveys of multi-agent LLM system failures identify narrow handoff interfaces between staged agents, where a downstream agent's structured input omits a finding an upstream agent's free-text reasoning surfaced, as a distinct and recurring failure category | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Platform-orchestrated agentic workflow failure studies find that narrowing the interface between orchestrated stages to a fixed pass/fail schema is a primary mechanism by which a cross-document or cross-record finding present upstream fails to reach a downstream approval stage | [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735) |
| Agentic LLM research in supply-chain contexts identifies the absence of a shared, continuously synced structured state between sequential verification and approval agents as a distinct reliability gap from either agent's individual document-verification accuracy | [Agentic LLMs in the Supply Chain: Towards Autonomous Multi-Agent Consensus-Seeking](https://arxiv.org/pdf/2411.10184) |

**Contributing Factors**
- Structured checklist schema tracks only per-document receipt and individual verification status, with no field for a cross-document discrepancy finding
- Document-review agent's cross-document comparison output is recorded only in free-text notes, with no structured escalation path into the approval-stage checklist
- No mandatory hold or block is triggered in the approval workflow when the document-review agent's free-text notes contain discrepancy language, since the approval agent's logic does not parse those notes

---

## Mitigation Strategies

1. **Add a Cross-Document Discrepancy Field to the Checklist Schema**: Require the document-review agent to record any cross-document discrepancy finding (beneficial-owner mismatch, address mismatch, signatory mismatch) in a dedicated structured field that blocks approval until resolved, rather than leaving it only in free-text notes
2. **Approval Agent Cross-Checks Review Transcript for Discrepancy Language**: Require the onboarding-approval agent to scan the document-review agent's free-text notes for discrepancy or mismatch language before finalizing approval, not just the per-document checklist
3. **Mandatory Hold on Unresolved Discrepancy**: Automatically place a supplier's onboarding in a hold state, blocking approval, whenever the document-review stage's output contains an unresolved cross-document discrepancy, regardless of individual document verification status
4. **Track Discrepancy-Field-Absent Approval Rate**: Continuously measure how often a supplier with a document-review discrepancy noted in free text is nonetheless approved when the checklist schema lacked a discrepancy field

### Metrics
- Rate of supplier approvals where the document-review transcript contains unresolved discrepancy language not reflected in the structured checklist
- Time between an onboarding approval and a later-discovered beneficial-ownership or identity discrepancy for the same supplier
- Approval rate for suppliers with a document-review discrepancy, segmented by presence vs. absence of a structured discrepancy field

### Alerts
- A supplier is approved for onboarding while the document-review transcript contains unresolved beneficial-ownership or identity discrepancy language → P1
- A supplier already onboarded is found via later audit or sanctions re-screening to have had an unresolved discrepancy at approval time → P1
- Discrepancy-field-absent approval rate across a rolling window exceeds the defined threshold → P2

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735)
- [Agentic LLMs in the Supply Chain: Towards Autonomous Multi-Agent Consensus-Seeking](https://arxiv.org/pdf/2411.10184)
