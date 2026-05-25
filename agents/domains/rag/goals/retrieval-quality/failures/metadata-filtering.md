# Metadata Filtering Errors

## Issue: Filters Exclude Relevant Documents

**Frequency**: Common

**Symptoms**
- Documents exist but aren't retrieved due to filter mismatch
- User permissions incorrectly applied
- Date/category filters too restrictive
- Metadata inconsistently applied across documents

**Root Cause**
Pre-retrieval filters based on metadata (permissions, dates, categories) exclude relevant documents due to incorrect metadata or overly strict filters.

**Example**
```
Query: "Q3 2024 sales report"
Filter: category = "sales" AND year = 2024 AND quarter = "Q3"

Relevant document exists:
- Title: "Sales Performance Q3 2024"
- Metadata: { category: "reports", year: 2024, quarter: 3 }

Filter mismatch:
- category: "reports" ≠ "sales"
- quarter: 3 ≠ "Q3" (integer vs string)

Result: Document filtered out despite being exactly what user wants
```

**Mitigation Strategies**
1. **Metadata normalization**: Consistent formats across documents
2. **Fuzzy filtering**: Allow partial matches
3. **Fallback retrieval**: If filtered results empty, try without filters
4. **Filter validation**: Verify filters before applying
5. **Multi-value fields**: Allow documents in multiple categories
6. **Filter debugging**: Log why documents were filtered

**Detection**
- Track filter-caused empty results
- Monitor filter strictness vs. recall
- Audit metadata consistency across corpus
- Compare filtered vs. unfiltered retrieval

## References

- [Medium: 7 RAG Hallucination Root Causes](https://medium.com/@umesh382.kushwaha/why-your-rag-pipeline-hallucinates-7-root-causes-and-how-to-fix-them-1a04a84be7f5) - Metadata issues
- [CMARix: RAG & AI Trust Statistics 2026](https://www.cmarix.com/blog/rag-ai-statistics/) - Enterprise filtering challenges
