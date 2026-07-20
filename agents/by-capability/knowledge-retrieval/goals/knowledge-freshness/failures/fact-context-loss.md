# Fact Context Loss

## Issue
A retrieval system pulls a fact that is accurate on its own terms, but the qualifying context that makes it correctly applicable — the condition, population, or scope it was originally stated under — is dropped somewhere between the source document and the agent's final answer. The fact survives; the sentence or clause that scoped it does not, usually because chunking, summarization, or context-window truncation separated the fact from its qualifier.

**Frequency**: Very Common

**Symptoms**
- Agent states a fact verbatim-correct but omits an adjacent qualifying clause present in the source
- Errors trace back to a chunk boundary or truncation point that split a fact from its condition
- The same source document, read in full by a human, would not produce the same unqualified claim
- Downstream users apply the fact in cases the original qualifier would have excluded

## Root Cause
Retrieval pipelines commonly split source documents into fixed-size or semantically-bounded chunks for indexing, and a fact and its qualifying clause don't always fall in the same chunk — especially when the qualifier appears in a preceding sentence, a footnote, or a "notes" section physically separated from the fact's primary statement. Once the chunk containing the qualifier isn't retrieved (because it scores lower on relevance to the query than the chunk containing the bare fact), the agent only ever sees the unqualified version and has no way to know a qualifier existed, since nothing marks the retrieved chunk as incomplete.

## Example
```
A source document states, across two separate sentences in a "Dosage"
section: "The standard adult dose is 500mg twice daily." Two paragraphs
later, under a "Renal Considerations" subheading: "Reduce to 250mg once
daily in patients with eGFR below 30."

The document is chunked by paragraph for indexing. A user asks a
medical-reference agent about the standard dose for a patient with
documented kidney impairment. The retrieval system pulls the "Dosage"
chunk (higher semantic match to "standard dose") but not the "Renal
Considerations" chunk, since the query didn't use terms close enough
to trigger a high relevance score for it.

The agent answers "500mg twice daily" — accurate as a general
statement, but the qualifying renal-impairment reduction that applies
directly to this patient was in a chunk that never made it into
context.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 15-25% of chunked source documents split a fact from a qualifying clause that changes its applicability across chunk boundaries | Estimated from chunk-boundary audits of technical/medical/legal source corpora |
| Multi-chunk retrieval (pulling a window around the top-matching chunk) recovers a substantial share of otherwise-dropped qualifiers | Reported range across teams testing context-window retrieval strategies |
| Fact-qualifier separation errors are markedly more common in documents using footnotes, side-notes, or non-adjacent "special cases" sections than in documents stating qualifiers inline | Typical pattern observed in document-structure-aware retrieval evaluation |

## Mitigations
1. **Qualifier-aware chunking**: At ingestion, detect and preserve fact-qualifier relationships (e.g. via sentence-dependency parsing or structural cues like "unless," "in patients with," "except") so a fact and its qualifier are never split across separate retrieval units.
2. **Context-window expansion around retrieved chunks**: Retrieve a window of surrounding content (preceding/following paragraphs) alongside the top-matching chunk by default, rather than the single highest-scoring chunk in isolation.
3. **Structural cross-referencing**: Index cross-references between sections (e.g. "Dosage" and "Renal Considerations" in the same document) so retrieval of one triggers inclusion of linked qualifying sections.
4. **Completeness flagging**: When a fact is retrieved from a chunk that structurally appears to reference other sections (footnote markers, "see Section X"), flag the response as potentially incomplete rather than presenting it as the full picture.
5. **Full-document fallback for high-stakes queries**: For domains where qualifier loss carries high risk, retrieve and pass the full source document (or a much larger context window) rather than relying on chunk-level relevance ranking alone.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| qualifier_recall_rate | Share of retrievals where a known qualifying clause for the retrieved fact is also present in context | Alert if < 90% for documents with tagged fact-qualifier pairs |
| chunk_boundary_split_rate | Rate at which known fact-qualifier pairs fall across separate chunks at ingestion | Track trend; alert on increase after re-chunking |
| unqualified_fact_correction_rate | Rate of expert/user corrections adding a qualifier the agent's answer omitted | Alert if > 5% of fact-based responses in qualifier-heavy domains |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Known qualifier dropped in high-stakes response | Audit confirms a documented qualifier was absent from context for a matching high-stakes query | High | Re-chunk affected document with qualifier-aware boundaries, review recent similar queries |
| Chunk boundary split rate increase | chunk_boundary_split_rate rises after a re-indexing or chunking-strategy change | Medium | Roll back or refine chunking strategy, re-audit affected documents |

## Related Patterns
- [Fact Partial Truth](./fact-partial-truth.md) - the resulting failure mode when a critical qualifier is dropped, presenting a partial truth as complete
- [Domain Context Loss](./domain-context-loss.md) - the same "qualifying context silently dropped" mechanism at the level of a whole session rather than a single fact
- [Knowledge Temporal Context Lost](./knowledge-temporal-context-lost.md) - a specific case of this pattern where the dropped qualifier is temporal ("as of" scoping)
