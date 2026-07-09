# Embedding-Retrieval Match Treats a Lexically Similar but Legally Distinct Substantiation Source as Adequate

## Issue: A Compliance-Review Agent's Retrieval Step Over a Vector Store of Approved Substantiation Documents Returns a Source That Is Embedding-Similar to the Marketing Claim Under Review Because It Discusses the Same Product Category and Uses Closely Related Phrasing, but the Retrieved Source Actually Supports a Narrower, Differently Conditioned, or Already-Expired Claim Than the One the Copy Makes, and the Agent Approves the Claim as Substantiated on the Strength of the Similarity Match Alone

**Frequency**: Occasional

**Symptoms**
- The compliance agent's approval log cites a specific substantiation document by name, and that document is real and does exist in the substantiation database, but a side-by-side read shows it supports a different claim than the one being approved (different population, different time period, different product variant, or a claim the document itself flags as discontinued)
- The retrieved source and the marketing claim share dense surface-level phrasing overlap (same product category terms, same comparative structure) even though the underlying tested condition differs
- Spot audits find the substantiation document's own qualifying language ("results apply only to the 12-ounce formulation" or "valid through Q3 2025 per the original test protocol") is never surfaced in the agent's approval reasoning, even though that qualifier directly disqualifies the broader claim being made
- The same claim, when checked manually against the full substantiation database rather than via similarity retrieval, surfaces no document that actually supports the claim as written
- Approval rates for comparative or superiority claims stay high even as the substantiation database accumulates more narrowly-scoped or superseded documents that are embedding-similar to common claim phrasing

**Example**
```
Marketing copy claims: "Our refill formula lasts 30% longer than leading competitors, in any season"
Compliance agent's substantiation-retrieval step returns a document titled "Comparative Longevity Test -- Refill Formula vs. Competitor X" with high embedding similarity to the claim
Agent approves the claim, citing the retrieved document as adequate substantiation
Manual review finds the retrieved document tested only summer-temperature conditions and only against Competitor X, not "leading competitors" generally, and the document's own conclusion section states "results should not be generalized across seasons or to other competitor products without further testing"
The approved claim's "in any season" and "leading competitors" language is unsupported by the one document the agent's retrieval step actually surfaced
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Surveys of retrieval-augmented generation systems identify embedding-similarity retrieval favoring text with high surface-phrasing overlap over text that is substantively current or applicable as a distinct and recurring error category | [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677) |
| Taxonomies of RAG system errors find that retrieval components frequently surface a superficially similar but substantively mismatched document when source phrasing patterns recur across a document store covering related but legally or technically distinct conditions | [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1) |
| Surveys of hallucination in LLM-based agents note that treating a retrieved document's mere topical relevance as equivalent to its evidentiary sufficiency is a recognized triggering cause of downstream approval errors | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |

**Contributing Factors**
- The substantiation database contains multiple documents covering the same product category with closely related phrasing but materially different scope (population, season, formulation, time validity), producing dense embedding clusters that retrieval cannot distinguish on similarity score alone
- The compliance agent's approval logic treats "a document was retrieved with high similarity score" as equivalent to "a document supports this exact claim," with no separate step that checks the retrieved document's stated scope and qualifiers against the claim's actual wording
- Qualifying language inside substantiation documents (season, product variant, validity window) is often in a conclusions or limitations section that ranks lower in embedding similarity to the claim text than the document's headline finding, making it less likely to be surfaced in the agent's reasoning
- No deterministic scope-matching step cross-references claim attributes (population, time period, product variant, comparison set) against the retrieved document's stated scope independent of similarity ranking

---

## Mitigation Strategies

1. **Scope-Matching Step Before Approval**: After retrieval, run a deterministic check that extracts the claim's stated scope attributes (population, season, product variant, comparison set) and the retrieved document's stated scope attributes, and require an explicit match -- not just topical similarity -- before treating the document as substantiation
2. **Surface Limitations Sections Explicitly**: Re-rank or separately surface a retrieved document's limitations/conclusions section in the agent's context, rather than relying on the headline finding's similarity score alone to represent the document
3. **Reject on Partial Scope Match**: Require the agent to flag claims for human legal review whenever the retrieved substantiation document's scope is narrower than the claim being made, rather than defaulting to approval when any related document is found
4. **Periodic Substantiation-Database Hygiene**: Regularly flag and archive narrowly-scoped or expired substantiation documents that remain embedding-similar to common claim phrasing, reducing the chance they are retrieved as if still generally applicable

### Metrics
- Rate of approved claims where the cited substantiation document's stated scope is narrower than the claim as published
- Number of approvals overturned on manual audit due to scope mismatch between claim and retrieved source
- Percentage of substantiation-retrieval calls that surface a document's limitations section versus only its headline finding

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Scope mismatch on approval | Deterministic scope-matching step finds the claim's attributes exceed the retrieved document's stated scope | P1 | Block approval; route to human legal review before publishing |
| Limitations section not surfaced | Retrieved substantiation document contains a limitations or validity-window section that was not included in the agent's approval reasoning | P2 | Re-run approval with limitations section explicitly injected |
| Rising narrow-scope approval rate | Percentage of approvals citing documents with scope narrower than the claim trends upward over a rolling period | P2 | Audit substantiation database for accumulation of stale or narrowly-scoped documents |

---

## References

- [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677)
- [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1)
- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
