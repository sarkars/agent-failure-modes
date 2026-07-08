# Semantic Mismatch

## Issue: Query wording fails to match the relevant content.

**Frequency**: Occasional

**Symptoms**
- Search misses content due to synonyms/acronyms.
- [Add more specific symptoms]

**Root Cause**
Query wording fails to match the relevant content.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- [List factors that make this failure more likely]

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| [Test name] | [Input] | [Expected output] | [What indicates failure] |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |

---

## Mitigation Strategies

### Prevention
1. **Domain-Specific Synonym Dictionary**: Build comprehensive synonym mappings for domain (financial: 'interest_rate'=['APR','yield','coupon'], legal: 'plaintiff'=['claimant','complainant']). Pre-retrieval, expand query with synonyms. Post-indexing, inject synonyms into documents.
2. **Query Rewriting with LLM**: Use LLM to rewrite query into multiple phrasings capturing intent. Example: 'How much interest do I earn?' → ['interest_rate','APY','earnings on deposit','account_yield']. Run all phrasings through retrieval, merge results.
3. **Embedding Domain Fine-Tuning**: Fine-tune embedding model on domain-specific query-document pairs. Example: legal domain fine-tune on case_law precedent pairs. Improves semantic matching for domain-specific vocabulary.

### Detection & Response
1. **Semantic Gap Analysis**: Compute semantic similarity between query and top-k results. Flag queries with low average similarity (< 0.60 threshold). Indicates semantic mismatch signal.
2. **Expert Synonym Audit**: Periodically audit synonym dictionary (monthly). Domain experts review: are common synonyms covered? Missing synonyms? Update dictionary based on feedback.
3. **Query-Result Pair Analysis**: When user marks result as irrelevant despite semantic similarity, log as semantic mismatch pattern. Analyze: is it domain terminology gap? Acronym confusion? Use to improve synonym dictionary.

### Architecture Patterns
1. **Multi-Embedding Strategy**: Use multiple embedding models: general-purpose + domain-specific. Retrieve from both, re-rank merged results using ensemble scoring. Increases coverage for domain-specific terminology.
2. **Synonym Injection Pipeline**: Before indexing, expand documents with synonyms. Before querying, expand query with synonyms. Both directions increase semantic overlap chance.
3. **LLM-Based Semantic Re-Ranker**: After initial retrieval, use LLM to re-rank results by semantic relevance to original query intent (not just lexical similarity). Slower but captures semantic relationships better.

### Metrics
1. **semantic_similarity_avg_top_10_results**: Target: > 0.75; Alert threshold: < 0.65
2. **semantic_mismatch_rate_percent**: Target: < 5%; Alert threshold: > 10%
3. **domain_synonym_coverage_percent**: Target: > 90%; Track synonym dictionary completeness
4. **expert_agreement_rate_on_semantics_percent**: Target: > 85%; Experts agree on semantic relevance
5. **query_rewriting_expansion_factor**: Target: 2.5-4.0x synonyms per query

### Alerts
1. **Semantic Mismatch Detected** (P2 - Warning): Condition - semantic_similarity_avg < 0.60 for query. Action: Log query-result pair, flag for offline analysis, consider query expansion.
2. **Synonym Coverage Gap** (P2 - Warning): Condition - synonym_coverage drops < 85%. Action: Audit synonym dictionary, identify missing terms, prioritize updates.
3. **Embedding Model Drift** (P1 - Critical): Condition - semantic_similarity scores degrade > 10% over 1 month. Action: Investigate embedding model performance, potential domain re-fine-tune.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Medium |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
