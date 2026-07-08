# Chunk Boundary Failure

## Issue: Needed fact is split across chunks and lost.

**Frequency**: Occasional

**Symptoms**
- Answer misses adjacent table/paragraph context.
- [Add more specific symptoms]

**Root Cause**
Needed fact is split across chunks and lost.

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
1. **Hierarchical Parent-Child Chunking**: When chunking documents, maintain hierarchy (document → section → paragraph → sentence). Store parent_id for each chunk. Retrieve chunk + parent/child context together for full semantic understanding.
2. **Overlapping Chunks at Boundaries**: When creating chunks, overlap by 1-2 sentences at boundaries. Ensures context not lost at chunk borders. Example: chunk_1 ends with sentences_A+B, chunk_2 starts with sentences_B+C (overlap on B).
3. **Neighboring Chunk Retrieval**: When retrieving a chunk, also surface neighboring chunks (previous, next) with metadata tags. Include in synthesis context window. Log which chunks are neighbors for traceability.

### Detection & Response
1. **Context Loss Detection**: For queries, retrieve chunk + adjacent chunks. Compare answer quality with and without neighbor context. Flag context loss when quality drops significantly.
2. **Chunk Coherence Scoring**: Compute internal coherence for each retrieved chunk (do sentences flow logically?). Low scores indicate chunk boundary cuts mid-thought. Alert on low coherence chunks.
3. **Fragment Continuation Detection**: Analyze retrieved text for incomplete sentences ('As mentioned in the previous...', 'continued from above...'). Fragments indicate chunk boundary cuts. Flag for context retrieval.

### Architecture Patterns
1. **Hierarchical Chunk Indexing**: Build index with multi-level chunks. Retrieval can start at any level and pull up/down hierarchy. Surface parent/child relationships in results (e.g., show section_header alongside retrieved paragraph).
2. **Chunk Boundary Metadata**: For each chunk store: chunk_id, parent_chunk_id, next_chunk_id, previous_chunk_id, context_window_overlap_percent. Use metadata for intelligent context retrieval.
3. **Semantic Chunking**: Instead of fixed-size chunks, chunk where semantic boundaries occur (topic changes, new section). Use embedding-based or LLM-based detection of boundaries. Reduces mid-fact chunk breaks.

### Metrics
1. **chunk_coherence_score_avg**: Target: > 0.85; Alert threshold: < 0.70
2. **context_window_inclusion_rate_percent**: Target: 95%; Neighboring chunks retrieved with primary chunk
3. **fragment_sentences_in_results_percent**: Target: < 2%; Alert threshold: > 5%
4. **user_feedback_context_loss_rate_percent**: Target: < 3%; Alert threshold: > 8%
5. **chunk_hierarchy_coverage_percent**: Target: 100%; All chunks have parent/child relationships

### Alerts
1. **Chunk Boundary Fragment Detected** (P2 - Warning): Condition - > 5% of chunks have incomplete sentences at boundaries. Action: Review chunking strategy, consider semantic chunking approach, re-chunk corpus.
2. **Context Loss User Feedback** (P2 - Warning): Condition - user marks result as context-incomplete. Action: Log chunk-context pair, analyze chunking strategy at that boundary.
3. **Low Chunk Coherence** (P1 - Critical): Condition - chunk_coherence_score < 0.60. Action: Investigate individual chunks, consider re-chunking document, test semantic chunking.

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
