# What Are the Most Common Adverse Drug Interaction Failures in AI Agents?

**Adverse drug interaction failures happen when an interaction-checking pipeline is scoped narrower than the patient's actual regimen — pairwise drug-drug pairs only, structured prescriptions only, name-similarity lookups instead of exact identifiers — so an agent can pass every check it actually runs while missing the interaction that matters.** The checks themselves are not wrong; the boundary drawn around what gets checked is too small, whether that boundary excludes supplements, excludes lab-value and condition context, excludes three-way combinations, or substitutes a lexically similar drug's profile for the one actually prescribed. Because the output still reads as a confident, fully-resolved interaction determination, a clinician has no visible signal that the check ran against an incomplete or wrong input.

## Key Takeaways

- 7 patterns are documented, splitting into interaction-check scope gaps (4 patterns), retrieval identity mismatch (1 pattern), and individualization/causal-reasoning gaps (2 patterns).
- Polypharmacy pushes the combination space out of reach of pairwise checking alone: 10 concurrent drugs produce 120 pairwise combinations and thousands of three-way combinations, and known three-way interactions make up under 5% of the total interaction space that pairwise databases document.
- A large share of patients on prescription medication also take herbal or dietary supplements, and most do not disclose that use unless a clinician asks directly — supplements reported as free text are routinely excluded from structured interaction checks that key off RxNorm/DDI identifiers.
- Similarity-search retrieval over drug names reliably confuses same-family, different-class drugs (different macrolides, different statins, different SSRIs) because the distinguishing pharmacological detail is exactly what a textual-similarity ranking does not weight.

## Scope

- **Interaction-check scope gaps** — [Contraindication Omission](failures/contraindication-omission.md), [Drug Interaction Misses & Contraindication Blindness](failures/drug-interaction-misses.md), [Herbal & Supplement Interaction Blindness](failures/herbal-supplement-interaction-blindness.md), [Polypharmacy Cascade Failures](failures/polypharmacy-cascade-failures.md). Every pattern in the cluster shares one root cause: the interaction-checking pipeline is scoped to a narrower slice of the patient's actual regimen and clinical picture than what's relevant — condition/lab/allergy context excluded from a DDI-only check, prescriptions checked while supplements are ignored, or pairwise combinations checked while three-way and four-way synergy is not.
- **Retrieval identity mismatch** — [Embedding Retrieval Matches Structurally Similar, Different-Class Drug](failures/embedding-retrieval-matches-structurally-similar-different-class-drug-for-interaction-check.md). A similarity-search lookup over drug names resolves to a name- or structure-adjacent but pharmacologically distinct drug's interaction profile instead of the profile for the drug actually prescribed, and the resulting determination gives no indication it came from a similarity match rather than an exact one.
- **Individualization and causal-reasoning gaps** — [Dosage Renal/Hepatic Adjustment Failure](failures/dosage-renal-hepatic-adjustment-failure.md), [Spurious Causal Narrative from Temporally Coincident Medication](failures/spurious-causal-narrative-from-temporally-coincident-medication-in-adverse-event-attribution.md). Both patterns default to a generic answer — standard-label adult dosing, or "the most recently started drug caused it" — instead of grounding the recommendation or attribution in the patient- or mechanism-specific fact that would change it: organ-function lab values in one case, pharmacological mechanism and latency-to-onset in the other.

## When Adverse Drug Interaction Matters

- Prescribing to polypharmacy patients on five or more concurrent medications, where pairwise-only checking structurally cannot represent three-way or four-way synergistic risk
- Intake or medication-reconciliation workflows for patients taking herbal products or supplements they haven't volunteered unless specifically asked
- Adverse-event review where an agent is asked to name a likely causative medication from a patient's chart, and a wrong attribution could lead to discontinuing the wrong drug

## Cross-Pattern Insight

Every adverse-drug-interaction pattern documented here traces back to a checking pipeline that is internally consistent and passes its own logic while missing the part of the clinical picture its designers never scoped it to see. A DDI-only checker correctly clears a pairwise combination it was built to clear; a similarity-search lookup correctly returns the most textually similar entry it was built to return; a recency-driven attribution correctly names the newest drug on the list. Such behaviors are not model errors in the sense of getting a well-posed question wrong — they are architecture errors in what question got posed. The recurring mitigation is the same across the goal: widen the check's input to the full regimen (meds, supplements, labs, conditions), require exact-identifier matching before falling back to similarity search, and gate high-stakes conclusions (a three-way synergy, a causal attribution) behind a mandatory pharmacist or structured-framework review rather than trusting a single automated pass.

## Frequently Asked Questions

### What causes an agent to miss a drug interaction between a patient's current medications?
Most misses trace to scope, not model capability: the interaction check queries a pairwise drug-drug database and never sees condition-based contraindications, lab-value-triggered risks, herbal/supplement interactions, or three-way-plus combinations, because the checking pipeline was built to answer a narrower question than "is this regimen safe." See [Contraindication Omission](failures/contraindication-omission.md) and [Polypharmacy Cascade Failures](failures/polypharmacy-cascade-failures.md).

### How do you catch interaction misses caused by polypharmacy?
Add a mandatory pharmacist gate whenever a recommendation would bring a patient to five or more concurrent drugs, and run a mechanism-based higher-order analyzer (shared metabolic pathway, shared target) alongside pairwise checks, since three-way interactions are too sparse and too varied for a pairwise database to cover.

### Can herbal supplements really cause dangerous drug interactions that an agent would miss?
Yes — St. John's Wort, ginkgo, garlic, and ginseng all carry documented clinically significant herb-drug interactions, but supplements are reported as unstructured free text far more often than as a coded medication, so a structured interaction check that queries only the medication list silently excludes supplements from the check entirely. See [Herbal & Supplement Interaction Blindness](failures/herbal-supplement-interaction-blindness.md).

### Does a better language model fix embedding-retrieval interaction mismatches?
No. The mismatch happens because look-alike drug names in the same family (different macrolides, different statins) score as highly similar under any text-similarity metric, and a more capable model doing the same similarity-based lookup still retrieves the wrong profile. The fix is architectural: match on the exact RxNorm/NDC identifier first, and treat similarity search as a flagged fallback, not the primary path.

### What causes a spurious drug attribution during adverse-event review?
An agent naming "the most recently started drug" as the likely cause without applying a structured causality framework (Naranjo, WHO-UMC) or checking for a plausible pharmacological mechanism — recency alone, not clinical evidence, drives the narrative. See [Spurious Causal Narrative from Temporally Coincident Medication](failures/spurious-causal-narrative-from-temporally-coincident-medication-in-adverse-event-attribution.md).

## Patterns

| Pattern | Mechanism |
|---|---|
| [Contraindication Omission](failures/contraindication-omission.md) | Interaction check scoped to drug-drug pairs only, missing condition/lab/allergy/demographic contraindications |
| [Dosage Renal/Hepatic Adjustment Failure](failures/dosage-renal-hepatic-adjustment-failure.md) | Standard adult dosing recommended without adjusting for chart-documented renal or hepatic impairment |
| [Drug Interaction Misses & Contraindication Blindness](failures/drug-interaction-misses.md) | Recommends a drug combination without flagging a known dangerous interaction due to statistical rather than rule-based reasoning |
| [Embedding Retrieval Matches Structurally Similar, Different-Class Drug](failures/embedding-retrieval-matches-structurally-similar-different-class-drug-for-interaction-check.md) | Similarity search over drug names retrieves a name-adjacent but pharmacologically distinct drug's interaction profile |
| [Herbal & Supplement Interaction Blindness](failures/herbal-supplement-interaction-blindness.md) | Free-text supplement/herb mentions excluded from the structured interaction check entirely |
| [Polypharmacy Cascade Failures](failures/polypharmacy-cascade-failures.md) | Pairwise-only interaction checking misses three-way or four-way synergistic risk in 5+ drug regimens |
| [Spurious Causal Narrative from Temporally Coincident Medication](failures/spurious-causal-narrative-from-temporally-coincident-medication-in-adverse-event-attribution.md) | Adverse-event attribution driven by recency of prescription rather than pharmacological mechanism |

**Total: 7 patterns**

## Related Goals

- [Medication Reconciliation](../medication-reconciliation/) — covers the parallel look-alike/sound-alike drug-name confusion that happens during list reconciliation rather than interaction checking
- [Treatment Planning](../treatment-planning/) — covers comorbidity and guideline-conflict failures in the broader care plan, one level up from a single interaction check
- [Lab Result Interpretation](../lab-result-interpretation/) — shares the same embedding-retrieval-identity-mismatch mechanism, applied to reference ranges instead of drug interaction profiles
