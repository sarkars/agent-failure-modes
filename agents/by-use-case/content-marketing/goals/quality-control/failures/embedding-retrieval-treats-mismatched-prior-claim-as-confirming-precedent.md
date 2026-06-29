# Embedding Retrieval Treats Mismatched Prior Claim as Confirming Precedent

## Issue: A Quality-Control Agent's Self-Check Retrieves a Previously Approved Statistical Claim via Embedding Similarity to "Confirm" That a New Claim Is Accurate, but the Retrieved Precedent Is for a Different Year, Population, or Methodology, So the Confirmation Is Not Actually Evidence the New Claim Is Correct

**Frequency**: Occasional

**Symptoms**
- A new statistical claim ("adoption grew 40% year over year") is approved as accurate because the quality-control agent retrieved a previously approved claim with nearly identical wording, but the retrieved precedent was about a different year's data and a different underlying population
- The retrieved precedent and the new claim share almost identical phrasing and claim structure, which is exactly the pattern that produces a high embedding-similarity score despite referring to substantively different underlying data
- Asking the quality-control agent to explain its approval shows it cites the similarity to the previously approved claim as confirmation, without checking that the retrieved precedent's underlying data actually applies to the new claim
- The miss concentrates on recurring claim templates (year-over-year growth statements, comparative benchmarks) where the phrasing is reused across reporting periods but the underlying numbers are not
- Manually checking the new claim's underlying source data against the new claim, rather than against the retrieved precedent, surfaces a discrepancy the embedding-based check missed

**Root Cause**
The quality-control agent's self-check retrieves the most similar previously approved claim by embedding similarity and treats that match as evidence the new claim is accurate, but claim phrasing similarity is not the same as the underlying data being current or applicable; recurring claim templates produce near-identical embeddings across reporting periods specifically because the wording is reused, while the numbers underneath change. The check confirms that a similarly worded claim was approved before, not that the current claim's specific numbers are grounded in current source data.

**Example**
```
Marketing drafts: "Adoption among enterprise customers grew 40% year over year in Q2"
Quality-control agent's self-check retrieves a previously approved claim via embedding similarity: "Adoption among enterprise customers grew 38% year over year in Q1," approved last quarter
Agent treats the high similarity to a previously approved claim as confirmation that the new claim's structure and magnitude are reasonable, and approves it without checking the new claim's underlying Q2 data
The actual Q2 enterprise adoption figure, pulled from the source data, shows 22% growth -- the 40% figure was a drafting error carried over from a different segment's number
Published content states an inflated growth figure that the embedding-based precedent check did not catch, because it never compared the new claim against its own source data
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Surveys of retrieval-augmented generation systems identify embedding-similarity retrieval favoring text with high surface-phrasing overlap over text that is substantively current or applicable as a distinct and recurring error category | [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677) |
| Taxonomies of RAG system errors find that retrieval components frequently surface a superficially similar but substantively outdated or mismatched precedent when claim templates are reused across reporting periods | [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1) |
| Surveys of LLM agent hallucination and self-verification note that confirmation derived from similarity to a prior approved instance, rather than from the current claim's own source data, produces false confidence in accuracy checks | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |

**Contributing Factors**
- Recurring claim templates (year-over-year growth statements) produce near-identical embeddings across reporting periods because the wording is reused while the underlying numbers change
- The quality-control agent's approval logic treats a high-similarity match to a previously approved claim as confirming evidence, rather than requiring an independent check of the new claim's number against its own current source data
- No rule distinguishes "structurally similar to a previously approved claim" from "verified against current source data" in how the approval is logged

---

## Mitigation Strategies

1. **Mandatory Source-Data Check Independent of Precedent Retrieval**: Require every statistical claim to be checked against its own current source data before approval, regardless of whether a similar claim was previously approved; precedent retrieval should inform formatting and structure, not numerical accuracy
2. **Distinguish Structural Precedent From Data Verification in Approval Logging**: Log whether an approval was based on independent source-data verification or only on similarity to a previously approved claim, so gaps in verification coverage can be audited
3. **Recurring-Template Flagging for Stricter Verification**: Identify claim templates that recur across reporting periods (year-over-year statements, comparative benchmarks) and route them through a stricter source-data check given their higher risk of carrying over outdated or wrong numbers
4. **Numerical Diff Against Retrieved Precedent**: When a precedent claim is retrieved, surface the numerical difference between the new claim and the precedent explicitly, rather than treating similarity alone as confirmation, to prompt a closer look at any unexplained jump

### Metrics
- Rate of approved statistical claims later found, on audit, to contain a numerical error not caught by the precedent-similarity check
- Rate of approvals based on source-data verification versus precedent-similarity confirmation alone, for recurring claim templates
- Average magnitude of unexplained numerical deviation between a new claim and its retrieved precedent, for claims later found to be wrong

### Alerts
- A statistical claim is approved based on precedent similarity alone with no independent source-data verification logged → P2
- A published claim is found, on audit, to deviate materially from its underlying source data despite having been approved via precedent-similarity check → P1
- Rate of precedent-similarity-only approvals for recurring claim templates exceeds the defined threshold for a rolling window → P3

---

## References

- [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677)
- [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1)
- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
