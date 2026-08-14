# Embedding-Retrieval Matches New Supplier to Wrong Certification Template

## Issue: A Supplier-Onboarding Agent's RAG Step, Used to Retrieve the Correct Compliance/Certification Checklist Template for a New Supplier Based on Its Stated Industry and Product Category, Pulls a Lexically Similar but Substantively Different Template Because the New Supplier's Self-Description Text Is Embedding-Similar to a Different Product Category's Template

**Frequency**: Occasional

**Symptoms**
- A supplier's onboarding file passes intake review while missing a category-specific certification (e.g., a food-contact migration-testing certificate) that their actual product line requires, invisible until someone compares the checklist against the supplier's own product spec sheet
- The supplier's self-description text was never wrong -- "packaging manufacturer serving consumer goods and food brands" is an accurate description -- but it is also accurate enough to score high similarity against a checklist template for a category the supplier doesn't actually fall into
- Because certification templates are typically written by cloning the nearest existing category's document and editing only the clauses that differ, the resulting corpus is structurally biased toward near-duplicate boilerplate, which is exactly the condition embedding retrieval handles worst
- The category-distinguishing clauses in any given template (migration testing, material-contact certification, etc.) are a small minority of that document's total token count, so they contribute proportionally little to the document's embedding relative to the shared boilerplate
- The gap is typically caught not by the onboarding process itself but by an unrelated downstream audit -- a customer-driven supply-chain review months later -- since nothing in the onboarding flow ever re-validates the checklist choice against the supplier's registered category

**Root Cause**
Template selection was implemented as a similarity search over supplier self-description text because, at the time it was built, the certification-template library did not yet have a machine-readable category taxonomy to key a deterministic lookup against -- similarity search was the fastest way to route an open-text description to a document. That shortcut becomes a liability specifically because certification templates are maintained by cloning: each new category's checklist starts as a copy of the closest existing one, so the corpus embedding retrieval searches over is dense with near-duplicates whose only real differences are a handful of category-determining clauses, which is the one thing embedding similarity is least sensitive to detecting.

**Example**
```
New supplier onboarding describes themselves as a "packaging manufacturer serving consumer goods and food brands"
Onboarding agent's RAG step retrieves the general-industrial-packaging certification checklist as the top similarity match, since its boilerplate language overlaps heavily with "packaging manufacturer" and "consumer goods," while the food-contact-packaging checklist's distinguishing clauses (migration testing, food-contact material certification) are a smaller fraction of that template's overall text
Supplier is onboarded against the general checklist and never asked to provide the food-contact migration-testing certificate their actual product category requires
Gap is discovered six months later during a customer-driven supply-chain audit, requiring the supplier relationship to be retroactively re-certified before shipments can continue
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Most-similar retrieved documents are not necessarily the most relevant for the decision being made, a structural limitation of similarity-ranked retrieval that does not account for category-determining details represented by only a small fraction of the document's text | [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1) |
| Standard embedding models lack domain-specific structure and routinely overlook the few critical variables that distinguish near-identical boilerplate documents from one another | [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677) |
| LLM-based supply-chain agents are evaluated specifically on their ability to handle multi-agent consensus and category-sensitive decisions correctly, since misclassification at intake propagates into downstream compliance and risk-management failures | [Agentic LLMs in the Supply Chain: Towards Autonomous Multi-Agent Consensus-Seeking](https://arxiv.org/pdf/2411.10184) |

**Contributing Factors**
- Template-selection step relies on free-text embedding similarity against the supplier's self-description rather than a deterministic lookup against a registered product-category code
- Certification checklist templates across adjacent categories share extensive common boilerplate, with category-determining clauses making up only a small fraction of the document's overall text and embedding signature
- No automated cross-check compares the applied checklist's category against the supplier's actual product specification sheet before onboarding is finalized

---

## Mitigation Strategies

1. **Deterministic Category-Code Lookup Before Similarity Ranking**: Require suppliers to be classified by a registered, deterministic product-category code (e.g., an industry-standard classification) before template selection, and use that code -- not free-text similarity -- to select the certification checklist
2. **Category-Determining Clause Weighting**: When similarity search is used at all, weight the category-determining clauses (not the shared boilerplate) more heavily in the embedding or retrieval ranking, so adjacent-category templates are correctly distinguished
3. **Specification-Sheet Cross-Check Gate**: Require an automated, non-LLM verification step that the applied checklist's category matches the supplier's submitted product specification sheet before onboarding can be marked complete
4. **Near-Duplicate Template Audit**: Periodically scan the certification-template library for template pairs with near-identical embeddings but differing category-specific clauses, and flag those pairs for mandatory deterministic-lookup routing rather than similarity search

### Metrics
- Rate of onboarded suppliers whose applied certification checklist category does not match their product specification sheet, sampled via audit
- Count of near-duplicate certification-template clusters in the library with no deterministic-lookup override in place
- Time between onboarding and detection of a wrong-template mismatch, by detection method (audit-driven vs. customer-driven)

### Alerts
- Supplier onboarding finalized with a checklist category that fails the specification-sheet cross-check → P1
- Audit sampling finds wrong-template-category rate above baseline for a given product-category pair → P2
- New certification template added to the library creates a near-duplicate cluster with an existing template without a deterministic-lookup rule added → P3

---

## References

- [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1)
- [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677)
- [Agentic LLMs in the Supply Chain: Towards Autonomous Multi-Agent Consensus-Seeking](https://arxiv.org/pdf/2411.10184)
