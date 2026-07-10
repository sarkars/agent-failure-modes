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

## Mitigation Strategies

### Prevention
1. **Metadata Schema Enforcement at Ingestion**: Define a strict, validated schema (enum values, fixed types) for filterable fields like category and quarter, and reject or auto-correct documents at ingestion that don't conform. This directly prevents the "reports" vs. "sales" and integer-vs-string quarter mismatches shown in the example.
2. **Canonical Value Normalization Pipeline**: Run all metadata values through a normalization step (e.g., quarter always stored as integer 1-4, category mapped through a controlled taxonomy with synonyms) before indexing, rather than trusting free-text tags entered by different teams.
3. **Multi-Label Categorization**: Allow documents to carry multiple category tags (e.g., both "sales" and "reports") instead of one exclusive category, so a document isn't excluded just because it was tagged from one team's perspective. Trade-off: requires filter logic to handle set-membership rather than equality.

### Detection & Response
1. **Zero-Result Filter Monitoring**: Log every query where the applied metadata filter returns zero or near-zero results — a direct signal of over-restrictive or mismatched filtering — and auto-trigger the fallback path while alerting if the rate rises.
2. **Filtered-vs-Unfiltered Recall Comparison**: Periodically run the same query with and without metadata filters and compare result overlap; a large gap indicates filters are excluding documents that are otherwise good semantic matches, as with the Q3 2024 sales report example.
3. **Metadata Consistency Audit**: Run scheduled jobs that scan the corpus for field-value drift (quarter stored as both string and integer, category taxonomy divergence) and report an inconsistency rate per field.

### Architecture Patterns
1. **Fallback-on-Empty Retrieval**: If the filtered query returns no or very few results, automatically re-run without filters (or with progressively relaxed filters) and log the relaxation for review, rather than silently returning nothing to the user.
2. **Fuzzy/Soft Filtering With Score Penalty**: Instead of hard-excluding non-matching metadata, apply a ranking penalty for mismatched filters so near-matches (like "reports" vs. "sales") can still surface, especially when strict matches are sparse.
3. **Filter Debug Logging in the Retrieval Pipeline**: Instrument the retrieval layer to log exactly which filter clause excluded each candidate document, so failures like this are diagnosable from logs rather than requiring manual reproduction.

### Metrics
1. **zero_result_filtered_query_rate**: Target: < 2%; Alert threshold: > 5%
2. **filtered_vs_unfiltered_recall_gap**: Target: < 10%; Alert threshold: > 25%
3. **metadata_field_consistency_rate**: Target: > 98%; Alert threshold: < 95%
4. **fallback_trigger_rate**: Target: < 3% of queries; Alert threshold: sustained upward trend

### Alerts
1. **Filter Starvation** (P2): Condition - zero_result_filtered_query_rate exceeds 5% for a given filter combination over 24h. Action: investigate metadata tagging for the affected category/field, trigger the fallback retrieval path.
2. **Metadata Drift Detected** (P3): Condition - the scheduled audit finds a field's consistency rate below 95%. Action: run a normalization backfill job for the affected field.
3. **Recall Gap Widening** (P2): Condition - filtered_vs_unfiltered_recall_gap exceeds 25% for a query category. Action: review filter strictness and schema, consider a soft-filtering rollout for that category.

## References

- [Medium: 7 RAG Hallucination Root Causes](https://medium.com/@umesh382.kushwaha/why-your-rag-pipeline-hallucinates-7-root-causes-and-how-to-fix-them-1a04a84be7f5) - Metadata issues
- [CMARix: RAG & AI Trust Statistics 2026](https://www.cmarix.com/blog/rag-ai-statistics/) - Enterprise filtering challenges
