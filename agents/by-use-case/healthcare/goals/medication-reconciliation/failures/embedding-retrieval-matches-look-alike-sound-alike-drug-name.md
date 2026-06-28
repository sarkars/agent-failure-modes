# Embedding Retrieval Matches Look-Alike/Sound-Alike Drug Name

## Issue: A Medication-Reconciliation Agent Matching a Free-Text or Handwritten Medication Entry Against a Structured Formulary Database Uses Similarity-Based Lookup That Resolves the Entry to a Lexically Similar but Pharmacologically Different Look-Alike/Sound-Alike (LASA) Drug, and the Reconciled Medication List Carries the Wrong Drug Forward Into the Patient's Active List

**Frequency**: Occasional

**Symptoms**
- The reconciled medication list contains a drug that does not match the source document (discharge instructions, home-medication list, handwritten note) when the original entry is independently re-checked
- The substituted drug name is a known LASA pair with the intended drug (e.g., similar spelling, similar phonetic pattern), and the dosage or formulation carried forward is inconsistent with the substituted drug's typical use, a mismatch visible only on close review
- Re-running the same match with the source document's surrounding context (indication, dosage form, prescribing service) included as disambiguating input, rather than the drug-name text alone, resolves to the correct drug, isolating the failure to name-only similarity matching
- The substitution concentrates on drug-name pairs already flagged on standard LASA confusion lists, where lexical similarity is highest and pharmacological difference is most consequential
- The error is caught only if a pharmacist independently cross-checks the reconciled list against the original source document, since the reconciled list reads as internally consistent and well-formatted regardless of the substitution

**Root Cause**
The reconciliation agent resolves a free-text or handwritten medication entry to a formulary database record by similarity matching over the drug-name text, and LASA drug pairs are, by definition, constructed from names that score highly similar under any text-similarity metric (lexical or embedding-based) despite being pharmacologically unrelated. When the matching step does not incorporate available disambiguating context -- indication, dosage form, typical prescribing service -- the similarity score alone cannot distinguish a correct match from a LASA substitution, because the two candidate drugs are specifically close in name-similarity space.

**Example**
```
Source document (handwritten discharge instructions) lists a medication as "hydroxyzine 25mg," intended for the patient's documented anxiety/itching indication
Reconciliation agent's similarity-based lookup against the formulary database resolves the entry to "hydralazine 25mg," a LASA match with high name-similarity to "hydroxyzine" but an entirely different pharmacological class (an antihypertensive, not an antihistamine)
Reconciled medication list now carries "hydralazine 25mg" forward as part of the patient's active medication list, with no flag indicating this resolution was a similarity match rather than an exact one
Patient's blood pressure drops unexpectedly after the substituted antihypertensive is administered for an indication it was never prescribed for, and the error is traced back to the LASA substitution during reconciliation
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Polypharmacy and drug-name resolution research documents that name-similarity-based matching is a known source of substitution error distinct from dosing or interaction-checking failures | [Polypharmacy & Drug-Drug Interactions](https://arxiv.org/abs/2005.01742) |
| Surveys of LLM-based agents in medicine identify medication-list reconciliation against free-text or handwritten source documents as a distinct reliability challenge requiring disambiguating context beyond name matching alone | [A Survey of LLM-based Agents in Medicine: How far are we from Baymax?](https://arxiv.org/html/2502.11211v1) |
| Tiered oversight frameworks for healthcare AI agents specifically call for independent verification of any medication-list entry resolved by automated matching before it is carried into the active list | [Tiered Agentic Oversight: A Hierarchical Multi-Agent System for Healthcare Safety](https://arxiv.org/pdf/2506.12482) |

**Contributing Factors**
- Matching step resolves the source-document drug name to the formulary database using name-similarity alone, without incorporating available disambiguating context such as indication or dosage form
- LASA drug pairs are specifically constructed to be highly similar in spelling or pronunciation, making name-only similarity matching maximally unreliable exactly where the consequence of error is highest
- No automated flag distinguishes an exact-name match from a similarity-based match in the reconciled medication list, so a pharmacist reviewing the list has no signal indicating which entries warrant closer scrutiny

---

## Mitigation Strategies

1. **Disambiguating-Context Matching**: Require the matching step to incorporate available disambiguating context (documented indication, dosage form, prescribing service) alongside name similarity, rather than resolving solely on drug-name text
2. **Known LASA-Pair Flagging**: Maintain a standard list of known look-alike/sound-alike drug pairs, and require any match resolving to a drug on this list to be flagged for mandatory pharmacist review before being carried into the active medication list
3. **Match-Confidence Labeling on Reconciled Entries**: Require every reconciled medication-list entry to carry a visible label distinguishing an exact-name match from a similarity-based match, so pharmacist review can prioritize lower-confidence resolutions
4. **Indication-Consistency Check**: Automatically cross-check the resolved drug's typical indications against the patient's documented diagnoses or reason for the medication, flagging a mismatch (e.g., an antihypertensive resolved against an anxiety/itching indication) for review before reconciliation completes

### Metrics
- Rate of reconciled medication-list entries resolved by similarity match that are later corrected on pharmacist review
- Percentage of similarity-based matches resolving to a drug on the known LASA-pair list
- Rate of indication-consistency mismatches flagged between a resolved drug and the patient's documented diagnosis

### Alerts
- A reconciled medication-list entry resolves to a known LASA-pair drug with no pharmacist review flag → P1
- An indication-consistency check finds a resolved drug inconsistent with the patient's documented diagnosis and the entry proceeds into the active list without resolution → P1
- Similarity-based (non-exact) match rate across reconciliations exceeds baseline for two consecutive reporting periods → P3

---

## References

- [Polypharmacy & Drug-Drug Interactions](https://arxiv.org/abs/2005.01742)
- [A Survey of LLM-based Agents in Medicine: How far are we from Baymax?](https://arxiv.org/html/2502.11211v1)
- [Tiered Agentic Oversight: A Hierarchical Multi-Agent System for Healthcare Safety](https://arxiv.org/pdf/2506.12482)
