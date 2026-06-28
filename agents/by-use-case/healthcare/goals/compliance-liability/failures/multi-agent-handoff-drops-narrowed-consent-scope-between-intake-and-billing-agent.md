# Multi-Agent Handoff Drops Narrowed Consent Scope Between Intake and Billing Agent

## Issue: An Intake Agent That Records a Patient's Narrowed Consent -- For Example, Consent to Treatment but Explicit Refusal of Consent to Share Records With a Specific Third-Party Payer or Research Registry -- Captures That Restriction Only as a Note Within Its Own Free-Text Reasoning or Conversation Summary, and a Downstream Billing or Records-Release Agent That Acts on a Structured Patient-Status Field Never Receives the Restriction, Proceeding as if Full Consent Were Granted

**Frequency**: Occasional

**Symptoms**
- A records-release or billing agent submits a claim or shares a record with a third party the patient explicitly excluded during intake, even though the intake transcript shows the restriction was captured
- Asking the intake agent to summarize the patient's consent status correctly states the narrowed scope, but the downstream agent's structured consent field shows "consent on file" with no scope qualifier
- The restriction exists nowhere in the structured patient record the billing agent actually queries -- it is recoverable only by re-reading the intake agent's full conversation transcript
- The gap is most common for less common consent restrictions (e.g., "do not share with employer-sponsored plan") that have no dedicated structured field in the intake form, unlike standard HIPAA authorization checkboxes
- The violation is caught only when the patient complains after receiving an explanation of benefits or notice from the excluded third party, since the release itself completes without any system-level error

**Root Cause**
The intake agent and the billing or records-release agent operate as separate steps that communicate through a structured patient-status handoff rather than a shared, complete representation of consent. When a consent restriction is non-standard enough that it was captured only in the intake agent's narrative reasoning or conversational summary rather than as a structured field the downstream agent's prompt or query explicitly checks, the restriction is invisible to the agent that actually executes the disclosure, regardless of how clearly it was stated during intake.

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
