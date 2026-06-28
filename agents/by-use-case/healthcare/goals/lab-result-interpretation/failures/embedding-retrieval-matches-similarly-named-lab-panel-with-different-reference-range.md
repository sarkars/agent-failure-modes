# Embedding Retrieval Matches Similarly Named Lab Panel With Different Reference Range

## Issue: An Agent Interpreting a Lab Result That Looks Up the Applicable Reference Range Via Semantic Search Over a Reference-Range Knowledge Base, Rather Than an Exact Assay-Code Match, Retrieves the Range for a Differently Named but Textually Similar Test -- Such as Confusing "Vitamin D, 25-Hydroxy" With "Vitamin D, 1,25-Dihydroxy" -- and Flags or Clears the Result Against the Wrong Range

**Frequency**: Occasional

**Symptoms**
- The agent's interpretation cites a reference range that belongs to a different, similarly named assay than the one actually ordered and reported on the lab result
- The retrieved range and the correct range for the actual assay differ enough that the same numeric result is flagged as abnormal under one and normal under the other
- Querying the reference-range knowledge base with the lab result's exact assay code (rather than its display name) returns the correct range, isolating the cause to the semantic-similarity lookup rather than a missing entry
- The confusion concentrates on assay families with multiple closely related variants -- vitamin metabolites, hormone subtypes, free versus total measurements -- where the display names differ by only a qualifying word
- The result reads as a fully resolved, confidently stated interpretation with no indication that the reference range came from a similarity match rather than an exact one

**Root Cause**
A reference-range lookup implemented as embedding or lexical similarity search over assay names optimizes for retrieving the most textually similar entry, not the entry for the exact assay actually performed. When two assays in the same family share most of their name and differ only in a qualifying term that carries the entire clinical and numeric distinction -- such as "25-hydroxy" versus "1,25-dihydroxy" -- the similarity signal that drives retrieval does not weight that qualifying term heavily enough to prevent the wrong range from outranking the correct one.

**Example**
```
Lab result reported as "Vitamin D, 25-Hydroxy: 18 ng/mL" with assay code VITD25
Interpretation agent queries its reference-range knowledge base with the result's display text via semantic search rather than the assay code
Top-ranked match returned is the reference range for "Vitamin D, 1,25-Dihydroxy" (assay code VITD125), a structurally similar name but a clinically distinct active-metabolite assay with a different normal range
Agent interprets 18 ng/mL against the 1,25-dihydroxy range, where it falls within normal limits, and reports the result as not requiring follow-up
Correct interpretation against the 25-hydroxy range would have flagged 18 ng/mL as deficient, requiring clinical follow-up
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Retrieval-augmented systems are documented to surface a taxonomy of retrieval errors distinct from generation errors, including retrieving a topically similar but substantively wrong record when similarity search is used in place of exact-key lookup | [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1) |
| Knowledge-oriented retrieval-augmented generation surveys identify exact-match retrieval over structured identifiers as a distinct reliability requirement from semantic-similarity retrieval over free text in domains where small lexical differences carry large semantic weight | [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677) |
| Surveys of LLM-based agents in medicine identify result-to-reference-range matching as a distinct reliability challenge requiring structured rather than similarity-based lookup | [A Survey of LLM-based Agents in Medicine: How far are we from Baymax?](https://arxiv.org/html/2502.11211v1) |

**Contributing Factors**
- The reference-range lookup is implemented over assay display names via similarity search rather than over the lab result's structured assay code
- No validation step confirms that the retrieved reference-range entry's assay code matches the lab result's reported assay code before interpretation proceeds
- Assay families with closely related variants are not flagged for mandatory exact-match lookup, so similarity search is applied uniformly regardless of name-collision risk

---

## Mitigation Strategies

1. **Exact Assay-Code Lookup as Primary Path**: Require reference-range retrieval to match on the lab result's structured assay code first, falling back to similarity search only when no exact code match exists, and flagging that fallback explicitly
2. **Assay-Code Match Verification Before Interpretation**: Before using a retrieved reference range, automatically verify that its associated assay code matches the lab result's reported assay code, blocking interpretation on any mismatch
3. **Name-Collision Family Flagging**: Maintain an explicit list of assay families with closely related, easily confused variants, and require any reference-range lookup within those families to undergo mandatory human or secondary-system verification
4. **Surface Retrieval Method in Output**: Require the interpretation output to indicate whether the reference range was retrieved by exact assay-code match or by similarity search, so reviewers can prioritize verification of similarity-matched results

### Metrics
- Rate of lab interpretations where the retrieved reference range's assay code does not match the result's reported assay code
- Rate of reference-range lookups falling back to similarity search due to no exact code match
- Rate of interpretation discrepancies (normal vs. abnormal classification) between exact-match and similarity-match lookups on the same result, sampled for audit

### Alerts
- A finalized lab interpretation used a reference range whose assay code does not match the result's assay code → P1
- A flagged name-collision assay family triggers a similarity-search fallback instead of exact match → P2
- Similarity-search fallback rate for reference-range lookups exceeds the defined threshold for a rolling window → P3

---

## References

- [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1)
- [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677)
- [A Survey of LLM-based Agents in Medicine: How far are we from Baymax?](https://arxiv.org/html/2502.11211v1)
