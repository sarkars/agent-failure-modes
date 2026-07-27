# What Are the Most Common Compliance & Liability Failures in AI Agents?

**Compliance and liability failures happen when an agent generates a high-stakes output — a de-identified dataset, an informed-consent summary, a consent-scope record — without an explicit verification gate that confirms the output meets the regulatory or clinical standard it claims to meet, so a structurally well-formed output can fail the safety or regulatory test it was designed to pass.** A de-identified dataset still contains re-identifying quasi-identifiers that escape a checklist-based Safe Harbor removal; an informed-consent note overstates what was actually discussed; or a structured consent-scope record drops a narrowed consent restriction that was captured in an intake transcript but never made it to the field the downstream agent actually reads.

## Key Takeaways

- 3 patterns are documented: de-identification failures rooted in combinatorial quasi-identifier risk that checklists do not catch; informed-consent documentation gaps where template language inflates what was actually discussed; and multi-agent handoff drops where consent restrictions established upstream never reach the structured field downstream agents act on.
- De-identification failures concentrate on small-population or rare-condition data where a conjunction of non-unique quasi-identifiers (rare diagnosis, location, age-range, gender) uniquely identifies individuals despite Safe Harbor removal of direct identifiers, a problem re-identification research has repeatedly demonstrated but that checklist-based removal strategies consistently miss.
- Informed-consent documentation disputes are a recurring category in malpractice claims where chart language and patient recollection diverge, and AI-generated documentation that optimizes for complete-sounding notes makes the divergence more likely, not less.
- Multi-agent handoff failures in consent tracking reflect a structural problem: intake agents capture restrictions in free-text reasoning or conversation summaries; downstream agents act on structured, narrower fields; and the restriction never reaches the field the downstream agent's logic actually consults.

## Scope

The 3 compliance-liability patterns split into distinct failure mechanisms: de-identification as a statistical re-identification risk problem that checklists fail to address; informed-consent documentation as a source-fidelity problem where agents optimize for narrative completeness over grounding; and multi-agent handoff as a structured-field-propagation problem where non-standard consent restrictions exist only in narrative form and disappear at agent boundaries.

## When Compliance & Liability Matters

- De-identified data release to research partners, analytics platforms, or public dashboards, where re-identification would violate HIPAA and breach notification obligations follow
- Informed-consent documentation for procedures where the chart's record of what was discussed could be the deciding evidence in a dispute
- Consent-scope restrictions that are not standard checkboxes but patient-specific narrowed permissions (e.g., "do not share with employer plan administrator")

## Cross-Pattern Insight

All three compliance-liability patterns reflect a gap between what an agent can convincingly produce and what regulatory or clinical rigor actually requires. A de-identified dataset can read as complete and de-identified while still carrying re-identifying quasi-identifier combinations. An informed-consent note can read as thorough while overstating what was discussed. A consent-scope record can read as complete while dropping a restriction that was captured upstream. The recurring mitigation is a verification gate that explicitly confirms the output meets its stated standard — k-anonymity verification for de-identification, transcript grounding for consent documentation, structured field propagation across agent handoffs — rather than relying on the output's internal plausibility.

## Frequently Asked Questions

### Can you de-identify a dataset using just Safe Harbor checklist removal?
Not safely for small-population or rare-condition data. Safe Harbor removes 18 direct identifier categories but leaves quasi-identifiers (age, rare condition, location, gender) intact. Small-population data where a conjunction of quasi-identifiers uniquely identifies individuals requires Expert Determination and k-anonymity verification, not a checklist.

### How do you catch inflated informed-consent documentation?
Require every consent-documentation claim to cite a corresponding transcript timestamp or structured form field rather than inferring from templates. Implement a mandatory clinician attestation step confirming the drafted consent matches what was actually discussed. Compare agent-generated fidelity scores against independent clinician review.

### How do consent restrictions get lost between intake and billing agents?
The intake agent captures a narrowed consent (e.g., "do not share with employer plan") in conversational reasoning or free text; the billing agent reads only a structured consent-on-file flag with no field for recipient-level exclusions. The restriction never crosses the handoff because the handoff schema has no field to carry it. See [Multi-Agent Handoff Drops Narrowed Consent Scope](failures/multi-agent-handoff-drops-narrowed-consent-scope-between-intake-and-billing-agent.md).

## Patterns

| Pattern | Mechanism |
|---|---|
| [HIPAA De-Identification Failure](failures/hipaa-deidentification-failure.md) | Checklist-based Safe Harbor removal leaves quasi-identifier combinations that re-identify individuals in small populations |
| [Informed-Consent Documentation Gap](failures/informed-consent-documentation-gap.md) | AI-generated note includes detailed risk/benefit discussion not actually covered in the encounter |
| [Multi-Agent Handoff Drops Narrowed Consent Scope](failures/multi-agent-handoff-drops-narrowed-consent-scope-between-intake-and-billing-agent.md) | Narrowed consent restriction captured by intake agent exists only in free text and is invisible to downstream billing/records-release agent |

**Total: 3 patterns**

## Related Goals

- [Clinical Documentation](../clinical-documentation/) — shares root cause of unverified source-fidelity gaps in agent-generated output
- [Medication Reconciliation](../medication-reconciliation/) — shares the multi-agent handoff information-loss mechanism with consent-scope dropping
