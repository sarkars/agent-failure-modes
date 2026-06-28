# Embedding-Retrieval Matches New Supplier to Wrong Certification Template

## Issue: A Supplier-Onboarding Agent's RAG Step, Used to Retrieve the Correct Compliance/Certification Checklist Template for a New Supplier Based on Its Stated Industry and Product Category, Pulls a Lexically Similar but Substantively Different Template Because the New Supplier's Self-Description Text Is Embedding-Similar to a Different Product Category's Template

**Frequency**: Occasional

**Symptoms**
- New supplier is onboarded against a certification checklist (e.g., food-safety vs. food-contact-packaging vs. general-industrial) that does not match their actual product category, discoverable by comparing the applied checklist against the supplier's actual product specification sheet
- The mismatched template shares substantial boilerplate language and category keywords with the correct one, since many certification checklists across adjacent product categories are derived from a common base template with only category-specific clauses differing
- The error concentrates on suppliers in adjacent or overlapping product categories (e.g., a food-contact packaging supplier onboarded against a general-industrial-packaging checklist) where the category boundary is determined by a small number of distinguishing terms easily diluted in embedding space by the surrounding similar boilerplate
- Onboarding audits find required category-specific certifications (e.g., a food-contact migration-testing certificate) missing from a supplier's file, traced back to the wrong checklist template having been applied at intake
- Forcing an explicit category lookup against the supplier's registered product-category code (rather than free-text similarity matching against their self-description) eliminates the mismatch, isolating the retrieval step as the point of failure

**Root Cause**
The onboarding agent's template-selection step retrieves the applicable certification checklist by embedding similarity between the new supplier's free-text self-description and the corpus of category-specific template documents, rather than by a deterministic lookup against the supplier's registered product-category code. Because certification checklists across adjacent categories share extensive common boilerplate with only a few category-determining clauses differing, their embeddings cluster closely together, and a supplier's free-text self-description -- which may not precisely articulate the regulatory category distinction -- can match the wrong template's dominant boilerplate language with high similarity.

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
