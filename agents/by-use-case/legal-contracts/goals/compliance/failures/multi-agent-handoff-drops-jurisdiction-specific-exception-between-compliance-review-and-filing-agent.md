# Multi-Agent Handoff Drops Jurisdiction-Specific Exception Between Compliance-Review and Filing Agent

## Issue: A Compliance-Review Agent That Determines, in Its Own Narrative Analysis, That a Filing Qualifies for a Jurisdiction-Specific Exception to a General Disclosure Requirement Hands Off to a Filing Agent Through a Structured Checklist That Has No Field for the Exception, So the Filing Agent Applies the General Requirement the Exception Was Meant to Override

**Frequency**: Occasional

**Symptoms**
- The compliance-review agent's analysis correctly identifies that a specific jurisdiction's exception applies and that a standard disclosure should therefore be omitted or modified, but the structured filing checklist it hands off shows the standard disclosure requirement as still active
- The filing agent, which builds the submission solely from the structured checklist, includes the standard disclosure language the exception was meant to override
- Re-reading the compliance-review agent's analysis transcript clearly shows the exception was identified and reasoned through; it simply never reached a structured field the filing agent reads
- The gap concentrates on less common jurisdiction-specific exceptions that have no dedicated checkbox in the standard filing checklist template, unlike commonly used exceptions that do
- The error surfaces only when a regulator or counterparty flags the filing for including disclosure language inconsistent with the jurisdiction's exception, since the filing itself is internally consistent and well-formed

**Root Cause**
The compliance-review agent and the filing agent communicate through a fixed checklist schema rather than the review agent's full analysis, so any exception determination that does not map onto an existing checklist field exists only in narrative form and is invisible to the filing agent's checklist-driven generation process. The filing agent has no mechanism to discover the exception because it never consults the review agent's underlying reasoning, only the structured output the schema permits.

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

1. **General-Purpose Override Field in Filing Checklist**: Add a structured, mandatory-to-populate field for any exception-driven override to standard disclosure requirements, requiring the compliance-review agent to write its specific determination directly into that field rather than leaving it in narrative analysis only
2. **Pre-Filing Exception Reconciliation Pass**: Before a filing agent generates a submission, automatically scan the compliance-review agent's analysis for exception or override language and flag any mismatch against the structured checklist's current field values
3. **Filing Agent Access to Full Review Rationale**: Require the filing agent's generation step to have direct access to the compliance-review agent's full analysis, not only the structured checklist, for any filing flagged as involving a non-standard jurisdiction
4. **Jurisdiction-Exception Registry Cross-Check**: Maintain a structured registry of recognized jurisdiction-specific exceptions and require any filing in a covered jurisdiction to be checked against it before submission, independent of whether the review agent's checklist handoff captured the exception

### Metrics
- Rate of filings where the compliance-review agent's analysis contains exception language not reflected in the structured filing checklist
- Rate of filings flagged post-submission for disclosure language inconsistent with an applicable jurisdiction exception
- Time between exception determination and filing checklist field population

### Alerts
- A filing is generated despite the compliance-review analysis identifying an applicable exception not reflected in the structured checklist → P1
- A counterparty or regulator flags a filing for disclosure language inconsistent with a known applicable exception → P1
- Exception-reconciliation mismatch rate exceeds the defined threshold for a rolling window → P2

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267)
- [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://arxiv.org/abs/2411.04468)
