# Semantic Mismatch

## Issue: Query Doesn't Match Document Language

**Frequency**: Very Common

**Symptoms**
- Relevant documents not retrieved
- User phrasing differs from document terminology
- Synonyms and paraphrases not matched
- Domain jargon vs. plain language gaps

**Root Cause**
Embedding models may not capture semantic equivalence between different phrasings of the same concept. The user asks in their language; documents are written in domain-specific or formal language.

**Example**
```
User query: "How do I cancel my subscription?"

Relevant document: "Membership termination procedures"
Content: "To discontinue your membership, navigate to account settings..."

Embedding similarity: 0.61 (below threshold of 0.7)

Result: Document not retrieved, user gets wrong answer or "I don't know"
```

**Common Mismatch Types**
- Synonyms: "cancel" vs. "terminate" vs. "discontinue"
- Abstraction levels: "fix the bug" vs. "resolve the defect"
- User vs. expert language: "stomach ache" vs. "abdominal discomfort"
- Abbreviations: "ROI" vs. "return on investment"

## Mitigation Strategies

### Prevention
1. **Hybrid Dense+Sparse Retrieval**: Combine vector search with BM25/keyword search so that even when embeddings miss the semantic link between "cancel" and "membership termination," lexical overlap on shared terms can still surface the match. Trade-off: added infrastructure complexity for combining and normalizing two scoring systems.
2. **Document Phrasing Enrichment at Indexing Time**: Augment each document's index entry with common user-language paraphrases (add "cancel", "stop", "end" alongside "terminate", "discontinue") generated once at ingestion, rather than relying on runtime query expansion alone.
3. **Domain-Tuned Embedding Fine-Tuning**: Fine-tune the embedding model on domain-specific query-document pairs (support tickets mapped to help docs) so the vector space itself learns that "cancel subscription" and "membership termination procedures" are close, addressing the root cause directly rather than compensating downstream.

### Detection & Response
1. **Low-Similarity Query Logging**: Log all queries where the best-match similarity score falls below the retrieval threshold (0.61 in the example, below the 0.7 cutoff); these are the clearest signal of semantic mismatch and should be reviewed for missing paraphrase coverage.
2. **Zero/Low-Quality Retrieval Correlation With Support Escalations**: Correlate "I don't know" or low-confidence responses with subsequent user rephrasing or support ticket creation, to find systemic vocabulary gaps.
3. **Query-vs-Document Vocabulary Gap Analysis**: Periodically sample user queries and compare their vocabulary against the terminology actually used in top documents, quantifying the user-language-vs-domain-language gap per topic area.

### Architecture Patterns
1. **HyDE (Hypothetical Document Embeddings)**: Generate a hypothetical answer document from the user's query phrasing and embed that instead of the raw query, bridging the gap between casual user phrasing ("cancel my subscription") and formal document language ("membership termination procedures").
2. **Multi-Representation Indexing**: Index each document under multiple embeddings (original text, a summary, and generated user-style paraphrases), retrieving if any representation matches, rather than relying on a single canonical embedding per document.
3. **Reformulation-and-Fusion Retrieval**: Generate several reformulations of the user's query at multiple abstraction levels (plain-language and domain-jargon versions) and fuse retrieval results across all of them.

### Metrics
1. **below_threshold_query_rate**: Target: < 10%; Alert threshold: > 20%
2. **vocabulary_gap_score**: Target: < 0.2; Alert threshold: > 0.35
3. **hyde_lift_on_low_similarity_queries**: Target: > 15% recall improvement on flagged queries; Alert threshold: < 5%
4. **paraphrase_coverage_percent**: Target: > 90% of high-traffic docs; Alert threshold: < 75%

### Alerts
1. **Semantic Gap Spike** (P2): Condition - below_threshold_query_rate exceeds 20% for a topic area over 7 days. Action: prioritize paraphrase enrichment or hybrid search rollout for that topic.
2. **Domain Fine-Tuning Drift** (P3): Condition - vocabulary_gap_score exceeds 0.35 for a growing topic area (e.g., new product line). Action: schedule an embedding fine-tuning refresh with updated query-document pairs.
3. **Low Paraphrase Coverage on High-Traffic Docs** (P3): Condition - paraphrase_coverage_percent falls below 75% for the top-100 most-queried documents. Action: prioritize the enrichment backlog for those documents.

## References

- [Medium: 7 RAG Hallucination Root Causes](https://medium.com/@umesh382.kushwaha/why-your-rag-pipeline-hallucinates-7-root-causes-and-how-to-fix-them-1a04a84be7f5) - Query-document mismatch
- [FloTorch: 2026 RAG Performance Landscape](https://www.flotorch.ai/blogs/the-2026-rag-performance-landscape-what-every-enterprise-leader-needs-to-know) - Retrieval challenges
