# Embedding Retrieval Matches Structurally Similar, Different-Class Drug for Interaction Check

## Issue: An Agent Checking a Medication List for Drug-Drug Interactions, Using Semantic Similarity Search Over an Interaction Knowledge Base to Find the Relevant Interaction Profile for a Given Drug, Retrieves the Profile for a Structurally or Name-Similar but Pharmacologically Distinct Drug, and Clears or Flags the Combination Based on the Wrong Drug's Interaction Data

**Frequency**: Occasional

**Symptoms**
- The interaction check's cited rationale references an interaction profile that belongs to a different drug than the one actually on the patient's medication list, distinguishable only by checking the drug's exact name or RxNorm identifier against the retrieved profile's identifier
- The retrieved drug and the actual prescribed drug share a similar name root or are in structurally related but pharmacologically distinct subclasses, such that their interaction profiles differ in clinically meaningful ways
- Querying the interaction knowledge base by the medication's exact RxNorm or NDC identifier, rather than by name similarity, returns a different, correct interaction profile than what the agent used
- The mismatch concentrates on drug families with multiple subclass members that share a name stem (e.g., different statins, different SSRIs, different generation cephalosporins), where similarity search ranks subclass siblings closely together
- The check's output reads as a fully resolved, confidently stated interaction determination with no indication that the underlying profile came from a similarity match rather than an exact identifier match

**Root Cause**
An interaction-profile lookup implemented as embedding or lexical similarity search over drug names optimizes for retrieving the most textually or structurally similar entry, not the entry for the exact drug actually prescribed. When two drugs in the same family share a name stem or structural class but differ in the specific interaction risks that matter clinically, the similarity signal driving retrieval does not reliably distinguish between them, since the distinguishing pharmacological detail is not what the similarity ranking optimizes for.

**Example**
```
Patient's medication list includes clarithromycin, prescribed for a respiratory infection
Interaction-checking agent queries its interaction knowledge base via semantic similarity using the drug name, intending to check it against the patient's existing simvastatin prescription
Similarity search returns the interaction profile associated with azithromycin (a different macrolide, frequently co-occurring in similar contexts in the underlying training and reference data) rather than clarithromycin's own profile
Azithromycin's interaction profile with simvastatin carries a lower-severity warning than clarithromycin's; the agent clears the combination based on the wrong drug's profile
Clarithromycin in fact carries a well-documented, clinically significant interaction with simvastatin via CYP3A4 inhibition that the agent's check never surfaced
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Retrieval-augmented systems are documented to surface a taxonomy of retrieval errors distinct from generation errors, including retrieving a topically or structurally similar but substantively wrong record when similarity search is used in place of exact-identifier lookup | [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1) |
| Knowledge-oriented retrieval-augmented generation surveys identify exact-match retrieval over structured identifiers as a distinct reliability requirement from semantic-similarity retrieval over free text in domains where small lexical or structural differences carry large clinical weight | [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677) |
| Surveys of LLM-based agents in medicine identify drug-interaction lookup as a distinct reliability challenge requiring structured rather than similarity-based matching | [A Survey of LLM-based Agents in Medicine: How far are we from Baymax?](https://arxiv.org/html/2502.11211v1) |

**Contributing Factors**
- Interaction-profile lookup is implemented over drug names via similarity search rather than over the medication's structured RxNorm or NDC identifier
- No validation step confirms the retrieved interaction profile's associated drug identifier matches the actual prescribed medication's identifier before the interaction check proceeds
- Drug families with closely related subclass members sharing a name stem are not flagged for mandatory exact-identifier lookup, so similarity search is applied uniformly regardless of name-collision risk

---

## Mitigation Strategies

1. **Exact Identifier Lookup as Primary Path**: Require interaction-profile retrieval to match on the medication's structured RxNorm or NDC identifier first, falling back to similarity search only when no exact identifier match exists, and flagging that fallback explicitly
2. **Identifier Match Verification Before Clearing or Flagging**: Before using a retrieved interaction profile, automatically verify that its associated drug identifier matches the actual prescribed medication's identifier, blocking the interaction determination on any mismatch
3. **Name-Collision Family Flagging**: Maintain an explicit list of drug families with closely related, easily confused subclass members, and require any interaction lookup within those families to undergo mandatory human or secondary-system verification
4. **Surface Retrieval Method in Output**: Require the interaction-check output to indicate whether the profile was retrieved by exact identifier match or by similarity search, so reviewers can prioritize verification of similarity-matched results

### Metrics
- Rate of interaction checks where the retrieved profile's drug identifier does not match the actual prescribed medication's identifier
- Rate of interaction-profile lookups falling back to similarity search due to no exact identifier match
- Rate of interaction-severity discrepancies between exact-match and similarity-match lookups on the same medication pair, sampled for audit

### Alerts
- A finalized interaction check used a profile whose drug identifier does not match the prescribed medication's identifier → P1
- A flagged name-collision drug family triggers a similarity-search fallback instead of exact identifier match → P2
- Similarity-search fallback rate for interaction-profile lookups exceeds the defined threshold for a rolling window → P3

---

## References

- [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1)
- [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677)
- [A Survey of LLM-based Agents in Medicine: How far are we from Baymax?](https://arxiv.org/html/2502.11211v1)
