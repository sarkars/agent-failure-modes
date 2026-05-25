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

**Mitigation Strategies**
1. **Hybrid search**: Combine vector search with keyword/BM25
2. **Query expansion**: Add synonyms and related terms
3. **Document enrichment**: Index with multiple phrasings
4. **Domain-specific embeddings**: Fine-tune on domain vocabulary
5. **Hypothetical document embeddings (HyDE)**: Generate hypothetical answer, embed that
6. **Multiple query reformulations**: Try several query versions

**Detection**
- Track queries with no/low-quality retrievals
- Monitor retrieval scores distribution
- Compare user language to document language
- A/B test retrieval strategies

## References

- [Medium: 7 RAG Hallucination Root Causes](https://medium.com/@umesh382.kushwaha/why-your-rag-pipeline-hallucinates-7-root-causes-and-how-to-fix-them-1a04a84be7f5) - Query-document mismatch
- [FloTorch: 2026 RAG Performance Landscape](https://www.flotorch.ai/blogs/the-2026-rag-performance-landscape-what-every-enterprise-leader-needs-to-know) - Retrieval challenges
