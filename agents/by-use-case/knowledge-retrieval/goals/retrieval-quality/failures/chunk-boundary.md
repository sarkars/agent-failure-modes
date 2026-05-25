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

**Mitigation Strategies**
1. **Overlapping chunks**: Include context from adjacent chunks
2. **Semantic chunking**: Split at paragraph/section boundaries
3. **Hierarchical indexing**: Index at multiple granularities
4. **Parent-child retrieval**: Retrieve chunk, include parent context
5. **Sentence window retrieval**: Retrieve sentence, expand to paragraph
6. **Document structure awareness**: Respect headers, lists, tables

**Detection**
- Track multi-chunk answer requirements
- Monitor "incomplete context" feedback
- Analyze where answers span chunk boundaries
- Compare answer quality vs. chunk overlap settings

## References

- [Medium: 7 RAG Hallucination Root Causes](https://medium.com/@umesh382.kushwaha/why-your-rag-pipeline-hallucinates-7-root-causes-and-how-to-fix-them-1a04a84be7f5) - Chunking issues
- [Mindee: RAG Hallucinations Explained](https://www.mindee.com/blog/rag-hallucinations-explained) - Context fragmentation
