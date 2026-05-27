# Context Window Limits

## Issue: Context Window Limitations

**Frequency**: Common

**Symptoms**
- Agent loses track of earlier content
- Cross-references not resolved
- Summary extraction misses details from truncated sections

**Root Cause**
Documents exceeding context window require chunking, but naive chunking breaks cross-references, tables spanning pages, and contextual understanding.

**Example**
```
Input: 200-page contract

Chunk 1 (pages 1-50): "Payment terms defined in Exhibit B"
Chunk 2 (pages 51-100): [Exhibit B is here]
Chunk 3 (pages 101-150): "Per payment terms in Section 3.2..."

Agent processing Chunk 1: Cannot resolve Exhibit B reference
Agent processing Chunk 3: Lost context about what payment terms were
```

**Mitigation Strategies**
1. **Smart chunking**: Respect document structure (sections, pages)
2. **Overlap windows**: Include context from adjacent chunks
3. **Cross-reference resolution**: Pre-process to resolve references
4. **Hierarchical processing**: Extract structure first, then details
5. **Retrieval augmentation**: Index document, retrieve relevant chunks on demand

## References

- [AWS: 3 Agent Failure Modes](https://dev.to/aws/why-ai-agents-fail-3-failure-modes-that-cost-you-tokens-and-time-1flb) - Context overflow patterns
- [Why Frontier Agents Can't Read Documents](https://www.databricks.com/blog/why-frontier-agents-cant-read-documents-and-how-were-fixing-it) - Long document processing
- [Document AI: Next Evolution of IDP](https://www.llamaindex.ai/blog/document-ai-the-next-evolution-of-intelligent-document-processing) - Hierarchical extraction
