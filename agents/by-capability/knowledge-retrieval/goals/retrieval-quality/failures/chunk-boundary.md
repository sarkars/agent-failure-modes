# Chunk Boundary Issues

## Issue: Relevant Information Split Across Chunks

**Frequency**: Very Common

**Symptoms**
- Answer requires information from multiple chunks
- Retrieved chunk lacks necessary context
- Tables or lists broken across chunks
- Cause in one chunk, effect in another

**Root Cause**
Documents are split into chunks for indexing, but these splits don't respect semantic boundaries. Information that belongs together gets separated.

**Example**
```
Original document:
"The contract value is $500,000. Payment terms are Net 30. 
[page break]
The late payment penalty is 2% per month."

Chunk 1: "The contract value is $500,000. Payment terms are Net 30."
Chunk 2: "The late payment penalty is 2% per month."

Query: "What happens if I pay late?"
Retrieved: Chunk 2 only

Missing context: User doesn't know the payment terms (Net 30)
```

## Mitigation Strategies

### Prevention
1. **Semantic/Structure-Aware Chunking**: Split at paragraph, section, and heading boundaries detected via a document structure parser instead of a fixed token count, so related clauses (payment terms and the late-payment penalty) stay together. Trade-off: variable chunk sizes complicate downstream batching and cost estimation.
2. **Overlapping Sliding-Window Chunks**: Chunk with 15-20% overlap so boundary-adjacent content appears in both neighboring chunks. Trade-off: increases index size and introduces duplicate content that must be deduplicated at retrieval time.
3. **Parent-Document Retrieval**: Index small chunks for precise matching, but retrieve and pass the parent section or full paragraph to the LLM, guaranteeing surrounding context (like the Net-30 terms) is included even when the matched chunk itself is narrow.

### Detection & Response
1. **Cross-Chunk Answer Requirement Tracking**: Tag eval questions that require information from 2+ source chunks and monitor their pass rate as a distinct eval slice from single-chunk questions, since aggregate accuracy hides this failure mode.
2. **Boundary-Loss Regression Testing**: Maintain a golden set of known split-sensitive documents (contracts, tables) and rerun it after any change to chunk size or overlap settings, alerting on regression.
3. **"Incomplete Context" Feedback Tagging**: Classify negative feedback mentioning missing context or details, and correlate it with how close the retrieved chunk sits to a document boundary.

### Architecture Patterns
1. **Hierarchical/Multi-Granularity Indexing**: Index at sentence, paragraph, and document level simultaneously; use the small chunk for retrieval matching and the larger chunk for context assembly at generation time.
2. **Sentence-Window Retrieval**: Retrieve the matching sentence, then programmatically expand to include N sentences before and after, rather than relying on the original chunk boundary to have captured enough context.
3. **Table/List-Aware Chunkers**: Use format-specific splitters that never break a table row or list item across a chunk boundary, since structural loss compounds with the content loss shown in the example.

### Metrics
1. **multi_chunk_answer_pass_rate**: Target: > 85%; Alert threshold: < 70%
2. **context_completeness_score**: Target: > 0.9; Alert threshold: < 0.75
3. **boundary_adjacent_retrieval_rate**: Target: < 10%; Alert threshold: > 20%
4. **table_list_integrity_rate**: Target: 100%; Alert threshold: any violation

### Alerts
1. **Context Fragmentation Regression** (P2): Condition - multi_chunk_answer_pass_rate drops > 10% after a chunking configuration change. Action: roll back the chunk size/overlap change, re-run the golden set before redeploying.
2. **Structural Split Violation** (P2): Condition - a table or list is detected split across a chunk boundary in production retrieval. Action: reprocess the document with the format-aware chunker.
3. **Repeated Incomplete-Context Feedback** (P3): Condition - more than 3 user reports of missing context for the same document within a week. Action: manually inspect that document's chunking, add overlap or a parent-retrieval override.

## References

- [Medium: 7 RAG Hallucination Root Causes](https://medium.com/@umesh382.kushwaha/why-your-rag-pipeline-hallucinates-7-root-causes-and-how-to-fix-them-1a04a84be7f5) - Chunking issues
- [Mindee: RAG Hallucinations Explained](https://www.mindee.com/blog/rag-hallucinations-explained) - Context fragmentation
