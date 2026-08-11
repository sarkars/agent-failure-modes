# Multi-Agent Handoff Drops Jurisdiction-Specific Exception Between Compliance-Review and Filing Agent

## Issue: A Compliance-Review Agent That Determines, in Its Own Narrative Analysis, That a Filing Qualifies for a Jurisdiction-Specific Exception to a General Disclosure Requirement Hands Off to a Filing Agent Through a Structured Checklist That Has No Field for the Exception, So the Filing Agent Applies the General Requirement the Exception Was Meant to Override

**Frequency**: Occasional

**Symptoms**
- The compliance-review agent's analysis correctly identifies that a specific jurisdiction's exception applies and that a standard disclosure should therefore be omitted or modified, but the structured filing checklist it hands off shows the standard disclosure requirement as still active
- The filing agent, which builds the submission solely from the structured checklist, includes the standard disclosure language the exception was meant to override
- Re-reading the compliance-review agent's analysis transcript clearly shows the exception was identified and reasoned through; it simply never reached a structured field the filing agent reads
- Less common jurisdiction-specific exceptions are hit hardest, precisely because the standard filing checklist template has a dedicated checkbox for the exceptions filers see often and none for the long tail it doesn't
- The error surfaces only when a regulator or counterparty flags the filing for including disclosure language inconsistent with the jurisdiction's exception, since the filing itself is internally consistent and well-formed

**Root Cause**
The filing checklist was designed around the exceptions the template's authors anticipated, not around an open-ended representation of "any exception the compliance-review agent might identify." A less common jurisdiction-specific exception therefore has nowhere to go in the schema: it stays in the review agent's narrative analysis, and the filing agent's generation process -- built to drive off the checklist, not to re-derive filing decisions from analysis text -- never has a reason to look for it there.

**Example**
```
Compliance-review agent analyzes a cross-border filing and determines: "Jurisdiction B's local-disclosure exception applies here because the counterparty qualifies as an exempt institutional investor under its registration framework; standard retail disclosure language should be omitted"
Review agent's structured checklist handoff to the filing agent has a checkbox for "standard disclosure required: yes/no" which remains set to "yes" because no field exists for exception-driven overrides
Filing agent generates the submission including the full standard retail disclosure language, exactly the language the identified exception was meant to remove
Counterparty's compliance team flags the inconsistency, since institutional-exempt counterparties receiving full retail disclosure language is itself a recognized red flag under Jurisdiction B's framework
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Multi-agent LLM systems exhibit a documented failure category where a determination established by one agent is lost or never reaches a downstream agent's effective input, distinct from either agent reasoning incorrectly on its own | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Evaluations of large language models in legal applications identify handoff fidelity between analysis and downstream document-generation steps as a distinct reliability gap from analytical accuracy itself | [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267) |
| Multi-agent system failure taxonomies identify rigid, schema-constrained inter-agent communication as a recurring driver of information loss between agents performing sequential steps of a single task | [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://arxiv.org/abs/2411.04468) |

**Contributing Factors**
- The filing checklist schema includes fields only for commonly applied exceptions, with no general-purpose field for less common, jurisdiction-specific overrides
- The filing agent's generation process consults only the structured checklist, never the compliance-review agent's full analysis transcript
- No reconciliation step compares exception language in the review agent's analysis against what the structured checklist actually encodes before filing

---

## Mitigation Strategies

### Prevention

1. **Mandatory general-purpose exception-override field in filing checklist with required population**: Extend filing checklist schema to include dedicated "Jurisdiction-Specific Overrides" field (free-text, required to populate). Before compliance-review agent hands off to filing agent, it must: (a) scan its own analysis for any exception/override determinations, (b) for each found, write explicit override statement into field: "Jurisdiction B institutional-investor exception applies — omit standard retail disclosure language", (c) mark standard fields affected by override. Fail-safe: filing checklist with populated override field must be reviewed by human compliance officer before filing agent generation begins. Root cause mitigation: Prevents exceptions from existing only in narrative analysis by forcing structured capture and mandatory field population.

2. **Pre-filing exception reconciliation pass with full-analysis context embedding**: Before filing agent generates submission, run automated reconciliation: (a) extract exception language from compliance-review agent's full analysis (use semantic search for "except", "override", "exempt", "not applicable"), (b) compare extracted exceptions against checklist field values, (c) if mismatch detected (analysis says "exempt", checklist says "required"), flag for human review, (d) provide filing agent with direct access to compliance-review agent's full analysis, not just checklist, for any filing with flagged mismatches. Filing agent must read exception rationale and apply it. Root cause: Makes full reasoning visible to downstream agent, not just structured checklist output.

3. **Jurisdiction-exception registry with pre-submission validation gate**: Maintain structured registry: {jurisdiction, exception_type, applicability_conditions, required_field_modifications}. Before any filing, query registry: "Does filing's jurisdiction have recognized exceptions? [Yes → list]. Do any apply to this filing? [Check conditions against filing metadata]." For each applicable exception, cross-check checklist: is exception captured? If not, flag for human review. Require filing to pass registry validation before submission. Root cause: Creates independent verification layer (registry) that catches handoff gaps missed by agents.

### Detection & Response

1. **Multi-agent handoff audit logging with exception reconciliation tracking**: For every filing, log: (a) compliance-review agent's analysis (full text searchable), (b) exceptions/overrides identified in analysis, (c) filing checklist values, (d) reconciliation result (match/mismatch), (e) exceptions captured in override field, (f) whether filing passed registry validation, (g) human approval before filing generation. Run automated sampling: for each filed submission, verify exception reconciliation was performed and approved. Measure: exception_capture_rate_in_checklist, analysis_checklist_mismatch_detection_rate, handoff_fidelity_rate.

2. **Retroactive exception audit on post-submission compliance flag**: When counterparty or regulator flags filing for disclosure inconsistency, re-analyze original filing's compliance-review agent analysis and checklist. Did agent identify exception? Did exception reach filing agent? Where did handoff fail? Update processes based on failure root cause (missing registry entry, checklist schema gap, reconciliation step skipped).

### Architecture Patterns

1. **Exception-Aware Checklist Schema**: Enhanced checklist includes (1) standard fields (disclosure required: yes/no), (2) dedicated "Override & Exceptions" field (mandatory free-text), (3) metadata about exception source (registry / agent analysis), (4) cross-reference to applicable jurisdiction regulations.

2. **Compliance-Review to Filing Reconciliation Engine**: (1) Extracts compliance-review agent's analysis, (2) Scans for exception/override language, (3) Compares against checklist field values, (4) Flags mismatches, (5) Requires human review before filing generation proceeds.

3. **Jurisdiction-Exception Registry**: Indexed by {jurisdiction → [exceptions]}. Each exception includes conditions for applicability, required field modifications, citations to regulations. Pre-filing validation checks: is filing's jurisdiction in registry? Do applicable exceptions apply? Are they captured in checklist?

### Key Metrics

| Metric | Target | Alert Threshold | Measurement Method |
|--------|--------|-----------------|-------------------|
| Exception Capture Rate in Checklist | 100% | <98% | # of exceptions identified in compliance-review analysis captured in filing checklist / total exceptions identified |
| Analysis-Checklist Mismatch Detection Rate | 100% | <99% | # of analysis-checklist mismatches detected by reconciliation pass / total mismatches present (validation: post-hoc audit) |
| Reconciliation Pass Execution Rate | 100% | <99% | # of filings with pre-filing reconciliation pass completed before filing generation / total filings |
| Registry Validation Accuracy | >98% | <95% | # of exceptions correctly identified as applicable/inapplicable by registry check / total registry checks (validated by legal review) |
| Handoff Fidelity Rate | 100% | <98% | # of compliance-review determinations reaching filing agent correctly / total determinations made by compliance-review agent |
| Post-Submission Compliance Flags | 0 | >0 | # of filings flagged by counterparty/regulator for disclosure inconsistency due to missed exceptions / total filings |
| Override Field Completion Rate | 100% | <99% | # of filings with Override & Exceptions field populated (if exceptions present) / total filings with exceptions identified |

### Alerts & Escalation

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Exception Identified in Analysis But Not in Checklist | Compliance-review agent's analysis identifies jurisdiction-specific exception, but exception not captured in filing checklist's override field | CRITICAL | Block filing generation; require compliance officer review; populate override field with exception details; verify filing agent will apply override |
| Analysis-Checklist Mismatch Detected | Reconciliation pass finds mismatch between analysis exceptions and checklist field values | CRITICAL | Escalate to compliance team; do not proceed to filing generation; resolve mismatch and document resolution; repeat reconciliation |
| Registry Exception Not Captured | Filing's jurisdiction has recognized exception in registry, applicable to filing, but checklist does not reflect exception | HIGH | Escalate to filing agent; provide exception details from registry; require filing agent to acknowledge and apply exception |
| Filing Generated Despite Unresolved Exception Mismatch | Filing submitted to generation despite flagged analysis-checklist mismatch not being resolved | CRITICAL | Halt filing generation; re-analyze; escalate to legal/compliance; file cannot proceed until mismatch resolved |
| Post-Submission Exception Flag | Counterparty or regulator flags filing for including disclosure language inconsistent with an applicable jurisdiction exception | CRITICAL | Investigate root cause (missed exception, handoff failure, or registry gap); assess filing impact; may require amendment/resubmission; audit all active filings for same exception pattern |

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267)
- [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://arxiv.org/abs/2411.04468)
