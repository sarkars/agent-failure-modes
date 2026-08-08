# Low-Recall Retrieval

## Issue: Agent misses relevant documents.

**Frequency**: Common

**Symptoms**
- User/source shows answer existed but was not retrieved.
- A document later confirmed to contain the answer never appears in the retrieved top-k for that query.
- Query using different terminology than the source document returns 0 or near-0 results despite a relevant document existing in the corpus.
- Recall@10 for a specific query category (e.g., acronym-heavy or long-tail queries) is measurably lower than the overall baseline.

**Root Cause**
Retrieval relies on a single method — dense-only or sparse-only — so documents that the other method would have surfaced are structurally invisible to the search regardless of relevance, and with no query expansion or reformulation step to bridge vocabulary mismatch, a query phrased differently than its source document (a synonym, an acronym, domain-specific shorthand) can return zero results even when a relevant document exists. This is compounded when the embedding model hasn't been fine-tuned on domain vocabulary, so domain-specific terms don't cluster near their synonyms in vector space, and by index gaps — documents never ingested, chunked incorrectly, or filtered out upstream — that remove candidates from the pool before search ever runs.

**Example**
```
Query: "Can I expense a conference badge?"
The relevant policy document uses the phrase "registration fee reimbursement" and never
says "conference badge" or "expense." Pure dense vector search ranks the correct document
outside the top-20 because embedding similarity between the query and the differently-
worded passage is too low, and no lexical/BM25 fallback exists to catch the exact keyword
mismatch. The agent responds "I don't have information on this," even though a directly
relevant document exists in the corpus.
```

**Contributing Factors**
- Single-method retrieval (dense-only or sparse-only) misses documents the other method would have caught.
- No query expansion/reformulation step to handle synonyms, acronyms, or vocabulary mismatch between query and source phrasing.
- Embedding model not fine-tuned on domain vocabulary, so domain-specific terms don't cluster near their synonyms in vector space.
- Index gaps — documents not ingested, chunked incorrectly, or excluded by an overly aggressive pre-filter — remove candidates before search even runs.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Vocabulary mismatch | Query phrased with different words than the source document uses for the same concept (e.g., "badge" vs "registration fee") | Relevant document appears in top-10 results | Relevant document is absent from top-20 despite existing in the corpus |
| Zero-result query | Query using domain jargon or an acronym not present verbatim in any indexed document | Query expansion surfaces the relevant document under its full-term phrasing | Query returns zero or irrelevant results |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| recall_at_10_percent | > 85% | Run eval set with known ground-truth relevant documents per query, measure % where the ground-truth doc appears in top-10 |

---

## Mitigation Strategies

### Prevention
1. **Hybrid Search Strategy**: Combine dense vector search (semantic similarity) with sparse lexical search (BM25/TF-IDF). Execute both in parallel, merge results using reciprocal rank fusion (RRF). Catches documents missed by either method alone.
2. **Query Expansion and Reformulation**: Automatically expand queries with: synonyms, related terms, acronyms, spelling variations. Example: 'CEO' expands to ['chief executive officer', 'president', 'c-suite']. Implement multi-query retrieval: run expanded queries, merge top results.
3. **Recall-Focused Eval Dataset**: Build eval set with queries where ground-truth relevant documents are known. Measure recall@k metrics (recall@10, recall@100). Set recall targets per domain (legal: 98%+, customer service: 95%+). Run evals regularly.

### Detection & Response
1. **Recall Metric Monitoring**: Estimate recall@k in production via user feedback (clicks, marks_relevant). Track recall trends. Alert if recall@10 drops > 5% month-over-month. Baseline per query type.
2. **Zero-Result Query Analysis**: Monitor queries returning 0 results. These are recall failures. Analyze: query type, vocabulary mismatch, missing documents. Use patterns to improve query expansion or index content.
3. **User Feedback False Negatives**: When user provides correct document not in retrieved set, mark as false negative. Track false negative rate. Alert if rate exceeds baseline.

### Architecture Patterns
1. **Multi-Index Architecture**: Maintain parallel indices: dense (embeddings), sparse (keywords), multi-modal (tables/figures). Query all indices, re-rank merged results using learning-to-rank model. Increases recall coverage.
2. **Query Understanding Pipeline**: Before retrieval, classify query intent, detect key entities, identify domain. Route to specialized retrieval strategy (legal queries → legal index, technical queries → code index). Improves recall by matching query to right corpus.
3. **Iterative Query Refinement**: If initial retrieval recall low (< 50% coverage), automatically rewrite query using synonyms/expansion, retry retrieval. Continue iterations up to max_iterations. Log all refinements for learning.

### Metrics
1. **recall_at_10_percent**: Target: > 85%; Alert threshold: < 80%
2. **recall_at_100_percent**: Target: > 95%; Alert threshold: < 90%
3. **zero_result_queries_percent**: Target: < 2%; Alert threshold: > 5%
4. **false_negative_rate_per_1000_queries**: Target: < 20; Alert threshold: > 50
5. **recall_consistency_across_domains_percent**: Target: > 90%; Variance < 10%

### Alerts
1. **Recall Degradation** (P1 - Critical): Condition - recall@10 drops > 10% month-over-month. Action: Investigate index staleness, embedding model drift, query distribution shift, potential index rebuild.
2. **Zero-Result Query Spike** (P2 - Warning): Condition - zero_result_queries_percent > 5%. Action: Analyze query patterns, add query expansion rules, update stop words/synonyms.
3. **High False-Negative Rate** (P1 - Critical): Condition - false_negative_rate > 50 per 1000 queries. Action: Audit retrieval pipeline, consider hybrid search tuning, ranking model retraining.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| recall_at_10_percent | < 80% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Recall Degradation | recall_at_10_percent drops more than 10% month-over-month on eval benchmark | High |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
