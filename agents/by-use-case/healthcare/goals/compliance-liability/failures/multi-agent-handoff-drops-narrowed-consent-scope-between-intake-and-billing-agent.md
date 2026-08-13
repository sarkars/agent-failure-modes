# Multi-Agent Handoff Drops Narrowed Consent Scope Between Intake and Billing Agent

## Issue: An Intake Agent That Records a Patient's Narrowed Consent -- For Example, Consent to Treatment but Explicit Refusal of Consent to Share Records With a Specific Third-Party Payer or Research Registry -- Captures That Restriction Only as a Note Within Its Own Free-Text Reasoning or Conversation Summary, and a Downstream Billing or Records-Release Agent That Acts on a Structured Patient-Status Field Never Receives the Restriction, Proceeding as if Full Consent Were Granted

**Frequency**: Occasional

**Symptoms**
- The billing agent shares an explanation of benefits with the employer-sponsored plan administrator the patient named by name as excluded, because "consent_on_file" reads as unconditionally true regardless of which recipient is asking
- The intake conversation summary correctly separates the standard insurer (consented) from the employer plan administrator (excluded), but the patient-status field the billing agent queries collapses that distinction into a single boolean
- Standard HIPAA authorization checkboxes -- the recipients the intake form anticipated -- pass through the handoff intact; the employer-plan exclusion fails specifically because it was a recipient the form never anticipated, not because consent logic broke generally
- Nothing about the disclosure looks anomalous to the billing agent at send time -- the field says consent is on file, so the release proceeds and completes without error
- Discovery happens downstream of the harm: the patient learns about the disclosure only after their employer-plan administrator has already received it, at which point the exclusion they stated during intake is unenforceable after the fact

**Root Cause**
The intake agent reasons about consent at the level of named recipients -- standard insurer yes, employer-plan administrator no -- but the only channel it has for passing that determination forward is a boolean "consent_on_file" flag inherited from a workflow built around a single yes/no authorization decision, not per-recipient exclusions. The billing agent's disclosure logic was written against that same boolean, so when it checks consent before releasing a record, recipient identity never enters the check; a patient's explicit, recipient-specific refusal has no representation to be read even in principle, because the field it would need to occupy doesn't exist in the schema either agent operates on.

**Example**
```
Patient during intake states: "I don't want anything shared with my employer's self-funded plan administrator, only with the standard insurer"
Intake agent's conversation summary correctly notes: "Patient consents to standard insurer billing; explicitly excludes employer plan administrator from any disclosure"
Structured patient record updated by intake agent sets only a generic "consent_on_file: true" flag; no field exists for administrator-level exclusions
Weeks later, billing agent processes a claim and, per standard workflow, shares the explanation of benefits with the plan administrator listed on the policy, which happens to be the excluded administrator
Patient receives an EOB at their workplace through the excluded administrator, the exact disclosure they had refused
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Multi-agent LLM systems exhibit a documented failure category where information established by one agent is lost or never reaches another agent's effective input, distinct from a single agent simply forgetting | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Tiered multi-agent healthcare systems are shown to require explicit, structured escalation and constraint-passing between agent tiers because narrative handoffs alone do not reliably propagate safety-relevant restrictions | [Tiered Agentic Oversight: A Hierarchical Multi-Agent System for Healthcare Safety](https://arxiv.org/pdf/2506.12482) |
| Surveys of LLM-based agents in medicine identify cross-agent state propagation as a distinct reliability requirement separate from any single agent's accuracy on its own task | [A Survey of LLM-based Agents in Medicine: How far are we from Baymax?](https://arxiv.org/html/2502.11211v1) |

**Contributing Factors**
- The structured patient-status schema used for handoff between intake and billing has no field for non-standard, payer-specific or recipient-specific consent restrictions
- The billing or records-release agent's workflow checks only the structured consent flag, never the intake agent's full conversation transcript or summary
- No reconciliation step compares every consent restriction mentioned in the intake transcript against the structured fields the downstream agent will actually act on

---

## Mitigation Strategies

1. **Structured Consent-Scope Schema With Recipient-Level Exclusions**: Replace the binary consent flag with a structured schema that supports recipient- or category-level exclusions, and require the intake agent to populate it directly rather than leaving the restriction only in narrative form
2. **Mandatory Pre-Disclosure Consent-Scope Check**: Before any billing or records-release agent shares data with a specific third party, require an automated check of the structured consent-scope record for that specific recipient, blocking disclosure on any unresolved exclusion
3. **Transcript-to-Schema Reconciliation Pass**: Run an automated pass comparing every consent-related statement in the intake transcript against the structured consent record, flagging any restriction mentioned in conversation but absent from structured fields
4. **Default-Deny on Non-Standard Recipients**: Treat any disclosure recipient not explicitly covered by a standard consent checkbox as requiring active confirmation against the full consent record before release, rather than defaulting to the generic consent flag

### Metrics
- Rate of disclosures to a recipient the intake transcript shows was explicitly excluded by the patient
- Rate of intake sessions where a consent restriction appears in the transcript but not in the structured consent-scope record
- Time between intake completion and first downstream disclosure action for newly onboarded patients

### Alerts
- A records-release or billing action targets a recipient that the structured consent-scope record marks as excluded → P1
- A disclosure occurs to a recipient with no corresponding entry in the structured consent-scope record at all → P2
- Transcript-to-schema reconciliation finds a restriction missing from structured fields → P2

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [Tiered Agentic Oversight: A Hierarchical Multi-Agent System for Healthcare Safety](https://arxiv.org/pdf/2506.12482)
- [A Survey of LLM-based Agents in Medicine: How far are we from Baymax?](https://arxiv.org/html/2502.11211v1)
