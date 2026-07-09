# Document-Level Retrieval Mismatch Pulls Wrong Billing-Dispute Template

## Issue: A Billing-Dispute Agent That Retrieves a Dispute-Handling Template or Policy Article From a Knowledge Base Via Embedding Similarity to the Customer's Complaint Wording Pulls an Entire Document That Is Topically and Lexically Close -- Covering a Structurally Similar but Different Dispute Type, Product Tier, or Region -- Rather Than the Document That Actually Governs the Customer's Account, and Applies That Wrong Document's Resolution Steps and Dollar Thresholds Confidently

**Frequency**: Common

**Symptoms**
- The agent cites a specific refund threshold, cooling-off period, or required documentation that comes verbatim from a retrieved knowledge-base article, but that article is for a different product line, region, or account tier than the customer's own
- Two customers with near-identical complaint wording but different account tiers (e.g., consumer versus business billing) receive resolution steps from the same retrieved document, because the retriever matched on complaint phrasing rather than the document's actual applicability scope
- The retrieved document is not the single best lexical match for an isolated sentence but rather a different, structurally similar document overall -- the failure is at the whole-document level, not a misread paragraph within the correct document
- Audit of retrieval logs shows the correct, account-applicable dispute article was present in the knowledge base and ranked closely behind the wrong one, with only a small embedding-similarity gap separating the two
- Customer escalation rate rises specifically for dispute types that have multiple near-duplicate articles in the knowledge base differing only by region, tier, or product version

**Example**
```
A business-tier customer disputes a recurring subscription charge using wording very similar to a common consumer-tier complaint: "I was charged again after I thought I cancelled"
The agent's retrieval step pulls the consumer-tier cancellation-dispute article, which states a 14-day refund window and a $0 documentation requirement, because that article's embedding is closest to the customer's phrasing
The business-tier account is actually governed by a separate dispute article requiring a signed cancellation confirmation and offering only a pro-rated refund, not a full 14-day window -- that article existed in the same knowledge base but ranked second
Agent tells the business customer they qualify for a full refund with no documentation, based on the wrong article's terms
Finance later reverses the refund decision upon discovering the business-tier contract terms were never consulted, creating a contradicted promise the customer received in writing
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Retrieval research on large, structurally similar document sets identifies "Document-Level Retrieval Mismatch," where the retriever selects an entirely incorrect source document due to embedding-based similarity matching on local phrasing rather than the document's actual scope of applicability | [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1) |
| Failure-mode taxonomies for LLM systems identify retrieval and knowledge-grounding errors as a distinct class of production failure separate from generation-level hallucination, arising when the retrieved source itself is wrong rather than the model's use of a correct source | [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933) |

**Contributing Factors**
- The knowledge base contains multiple dispute-handling articles that are structurally and lexically similar (same complaint patterns, similar resolution-step language) but differ in applicability by account tier, product, or region
- Retrieval ranks purely on embedding similarity to the customer's complaint text, with no hard filter or boost based on the account's actual tier, product, or region metadata before ranking
- The near-duplicate articles' applicability scope is stated in metadata or a header line rather than woven into the body text the embedding model weights most heavily, making tier/region distinctions easy for similarity search to under-weight
- No verification step cross-checks the retrieved article's stated applicability scope against the customer's actual account attributes before its resolution terms are applied

---

## Mitigation Strategies

1. **Metadata-Filtered Retrieval**: Apply a hard pre-filter on account tier, product, and region metadata before embedding-similarity ranking, so the retriever only ranks among documents that are actually applicable to the customer's account, rather than ranking the full corpus on text similarity alone
2. **Document-Level Summary Augmentation**: Prepend each knowledge-base article with a synthetic summary that states its applicability scope in plain terms, injecting that global context into the chunk embeddings to reduce confusion between structurally similar near-duplicate documents
3. **Applicability Cross-Check Before Application**: Before citing a retrieved article's terms to the customer, require an explicit check that the article's stated scope (tier/region/product) matches the customer's actual account attributes, blocking the response if it does not
4. **Near-Duplicate Article Consolidation**: Periodically audit the knowledge base for clusters of near-duplicate dispute articles differing only by tier/region/product and consolidate or restructure them to reduce the retrieval-mismatch surface area

### Metrics
- Rate of agent replies citing a knowledge-base article whose applicability metadata does not match the customer's account tier/region/product
- Embedding-similarity score gap between the top-ranked retrieved article and the actually-applicable article, for known mismatch cases
- Number of finance-reversed refund/resolution decisions per month attributable to a wrong-article citation

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Applicability mismatch | Retrieved article's tier/region/product metadata does not match the customer's account attributes | P1 | Block citation; re-retrieve with metadata filter applied or escalate to a human agent |
| Close-ranking near-duplicate | Top two retrieved articles differ in applicability scope but are within a small similarity-score margin of each other | P2 | Flag for knowledge-base consolidation review |
| Reversed resolution decision | Finance or a supervisor reverses a refund/resolution decision due to a wrong-article citation | P1 | Audit the originating retrieval call and correct customer communication |

---

## References

- [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1)
- [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933)
