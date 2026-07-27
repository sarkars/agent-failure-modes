# What Are the Most Common Medication-Reconciliation Failures in AI Agents?

**Medication-reconciliation failures happen when an agent matches a medication from one source (discharge instructions, home-medication list) to a formulary or reference database without grounding that match in the requesting context, or when an interaction flag identified during reconciliation exists only in narrative form and disappears at a handoff boundary, or when a discharge list is generated from the hospital's medication-administration record without reconciling against pre-admission home medications.** A reconciled medication list that looks complete and correct can silently carry a wrong drug substituted by similarity matching, or omit a home chronic medication that was never re-entered during a hospital stay.

## Scope

The 3 medication-reconciliation patterns split into distinct failure mechanisms: name-similarity-driven drug substitution (matching without disambiguating context), multi-agent handoff information loss (a structured schema gap), and reconciliation completeness (a workflow gap where hospital-only medications are carried to discharge without explicit rationale). Each represents an independent failure point in the reconciliation pipeline.

## When Medication Reconciliation Matters

- Admission medication reconciliation where free-text or handwritten entries must be normalized to a structured formulary
- Discharge medication lists where both pre-admission home medications and inpatient-initiated medications must be explicitly reconciled
- Multi-agent workflows where a reconciliation agent identifies a risk (interaction, look-alike/sound-alike substitution) and hands off to a downstream review agent

## Cross-Pattern Insight

All three medication-reconciliation patterns reflect a gap between what an agent can detect or reason through and what actually reaches downstream decision-makers. A reconciliation agent can identify an interaction but only in its own reasoning; downstream pharmacy review sees only the structured list. A similarity-based match can substitute a wrong drug and the reconciled list reads as complete. A home medication can be silently omitted because the hospital's MAR never captured it. The recurring mitigation is explicit verification and structured handoff: require exact-identifier matching with flagged fallbacks; carry risk flags through structured schema fields, not narrative form; and mandate three-column reconciliation (home/inpatient/discharge) with explicit disposition for every medication.

## Frequently Asked Questions

### How do you catch look-alike/sound-alike drug substitutions during reconciliation?
Require matching to use disambiguating context (indication, dosage form, patient diagnosis) alongside name similarity; maintain a known LASA-pair list and flag any resolution to a drug on that list for mandatory pharmacist review; label every reconciled entry as exact-match or similarity-match so reviewers can prioritize verification of lower-confidence resolutions.

### How do medication omissions happen at discharge?
The discharge list is generated from the inpatient medication-administration record (MAR), which only reflects what was ordered during the stay. A home medication that was simply not re-entered during hospitalization is silently omitted. Mitigate with mandatory three-column reconciliation (home medications vs. inpatient MAR vs. discharge list) with explicit disposition (continue/stop/change/new) for every home medication.

### How do you ensure a flagged interaction doesn't disappear at agent handoff?
Include a structured risk-flag field in the handoff payload that is separate from and cannot be silently dropped from the medication list itself; require the downstream agent to explicitly acknowledge or resolve any flag before completing its review; run an automated reconciliation check comparing upstream reasoning against downstream schema fields.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Discharge Medication Reconciliation Gap](failures/discharge-medication-reconciliation-gap.md) | Discharge list generated from inpatient MAR without reconciling pre-admission home medications; omissions and duplications not caught |
| [Embedding Retrieval Matches Look-Alike/Sound-Alike Drug Name](failures/embedding-retrieval-matches-look-alike-sound-alike-drug-name.md) | Similarity-based match resolves medication to a LASA drug with high name-similarity but different pharmacology |
| [Multi-Agent Handoff Drops Flagged Interaction Between Reconciliation and Pharmacy-Review Agent](failures/multi-agent-handoff-drops-flagged-interaction-between-reconciliation-and-pharmacy-review-agent.md) | Interaction flag identified by reconciliation agent exists only in narrative; structured list passed to pharmacy review carries no flag |

**Total: 3 patterns**

## Related Goals

- [Adverse Drug Interaction](../adverse-drug-interaction/) — interaction detection at reconciliation-time complements ongoing interaction checking; shares LASA confusion mechanism with adverse-drug-interaction retrieval mismatches
- [Compliance & Liability](../compliance-liability/) — shares the multi-agent handoff information-loss mechanism with consent-scope dropping
