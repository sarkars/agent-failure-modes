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

## Mitigation Strategies

### Prevention
1. **Structure-aware chunking**: Split on section/heading boundaries detected from document structure (TOC, headings, page breaks) rather than fixed token counts, so a chunk never cuts through the middle of a clause or table. Trade-off: requires reliable structure detection first, which itself can fail on poorly-formatted documents.
2. **Cross-reference pre-resolution pass**: Before chunking, scan the full document for reference patterns ("see Exhibit B," "per Section 3.2") and build a lookup table mapping each reference to its target location/content, then inject the resolved content inline or as an annotation when that chunk is processed. Trade-off: adds a full-document pre-pass, increasing latency and cost before any chunk-level work begins.
3. **Hierarchical summarize-then-drill-down processing**: First pass extracts document structure and a summary of each major section at low resolution; second pass processes each section in full detail with the summary of other sections available as context, so cross-section relationships aren't lost even though full text isn't in context simultaneously. Trade-off: two-pass processing roughly doubles latency versus naive single-pass chunking.

### Detection & Response
1. **Unresolved-reference tracking**: Instrument the agent to log every cross-reference phrase it encounters ("as defined in...", "per Section...") and whether it was resolved; unresolved references above a threshold per document signal chunking is breaking context.
2. **Chunk-boundary error correlation**: When downstream QA finds errors, check whether the erroneous field sits within one token-length of a chunk boundary; a disproportionate concentration of errors near boundaries confirms chunking (not model quality) is the driver.
3. **Retrieval-augmented fallback for low-confidence extractions**: When a chunk's extraction confidence is low, allow the agent to explicitly query the indexed full document for the specific missing reference rather than guessing from within-chunk context alone.

### Architecture Patterns
1. **Retrieval-augmented document processing**: Index the full document (embeddings + structural metadata) once, then let the agent issue targeted retrieval queries for referenced content on demand instead of relying purely on static chunk boundaries — this decouples "how much fits in context" from "what the agent can access."
2. **Sliding window with overlap**: Chunk with deliberate overlap (e.g., last N tokens of chunk k repeated as the first N tokens of chunk k+1) so references near a boundary have a chance of appearing in both surrounding chunks.
3. **Two-stage map-reduce extraction**: Map stage extracts candidate values per chunk independently; reduce stage reconciles values across chunks using the same conflict-resolution logic as [[conflicting-information]], since chunking artificially creates the same "same field, multiple values" problem within a single document.

### Metrics
1. **unresolved_cross_reference_rate**: Target: < 3% of detected references left unresolved; Alert if > 10%
2. **boundary_adjacent_error_rate**: Target: errors within 1 chunk-boundary should be < 2x errors elsewhere; Alert if > 4x
3. **retrieval_fallback_invocation_rate**: Target: track as baseline; Alert if it spikes > 50% week-over-week (signals a document type poorly served by current chunk size)
4. **extraction_accuracy_long_vs_short_docs**: Target: accuracy gap between docs > 100 pages and < 20 pages should be < 5 percentage points; Alert if gap > 15 points

### Alerts
1. **Boundary Error Concentration** (P2): Condition - boundary-adjacent error rate exceeds 4x the baseline rate for a document source. Action: Reduce chunk size or increase overlap window for that document type, re-run affected extractions.
2. **Long-Document Accuracy Gap** (P1): Condition - accuracy gap between long and short documents exceeds 15 percentage points. Action: Escalate to review chunking/hierarchical processing strategy for documents in that length bracket before processing more.
3. **Cross-Reference Resolution Failure Spike** (P3): Condition - unresolved reference rate exceeds 10% for a document type. Action: Review reference pattern library and add missing patterns specific to that document type.

## References

- [AWS: 3 Agent Failure Modes](https://dev.to/aws/why-ai-agents-fail-3-failure-modes-that-cost-you-tokens-and-time-1flb) - Context overflow patterns
- [Why Frontier Agents Can't Read Documents](https://www.databricks.com/blog/why-frontier-agents-cant-read-documents-and-how-were-fixing-it) - Long document processing
- [Document AI: Next Evolution of IDP](https://www.llamaindex.ai/blog/document-ai-the-next-evolution-of-intelligent-document-processing) - Hierarchical extraction
