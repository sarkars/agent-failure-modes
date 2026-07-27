# What Are the Most Common Retrieval Failures in AI Agents?

**Retrieval fails when the pipeline searches the wrong corpus, returns too few or too many documents, misses content trapped in tables or scanned images, or hands synthesis a set of chunks that are individually correct but collectively stale, contradictory, or poorly assembled.** The 12 retrieval patterns documented here cover the full retrieval pipeline end to end — from picking the right knowledge base, through precision/recall tuning and content-extraction gaps, to how the retrieved chunks get assembled and finally cited in a synthesized answer — and every one shares the same downstream risk: a retrieval-stage error is invisible to the generation model, which has no way to know the corpus, ranking, or extraction step upstream of it already went wrong.

## Key Takeaways

- 12 patterns are documented here, spanning corpus selection, precision/recall tuning, content-extraction blind spots, context assembly, and downstream synthesis/citation.
- Wrong Corpus Retrieval is the most severe of the 12 in a multi-tenant setting: a tenant-boundary violation isn't just a wrong answer, it's a data-isolation security incident, which is why its documented metrics target a strict 0% wrong-corpus and cross-tenant retrieval rate rather than an approximate threshold.
- Low-Precision and Low-Recall Retrieval are two failure directions of the same threshold/top-k tuning decision — a threshold set too low pulls in noise that corrupts synthesis, while a threshold set too high silently drops relevant documents and pushes the model to hallucinate a gap-filling answer instead.
- Table/Figure Blindness and OCR Extraction Error are content-extraction gaps rather than ranking gaps: the relevant value is present in the corpus but trapped in a modality (a table, a chart, a scanned image) the retrieval pipeline's text-only indexing never captured in the first place.

## Scope

- **Corpus and Recall/Precision Fundamentals** — [Wrong Corpus Retrieval](failures/wrong-corpus-retrieval.md), [Low-Precision Retrieval](failures/low-precision-retrieval.md), [Low-Recall Retrieval](failures/low-recall-retrieval.md), [Metadata Filter Error](failures/metadata-filter-error.md). The foundational retrieval-configuration questions — right knowledge base, right similarity threshold, right filter — that determine whether the candidate document set is even in the right neighborhood before ranking or synthesis begins.
- **Content-Extraction Blind Spots** — [OCR Extraction Error](failures/ocr-extraction-error.md), [Table/Figure Blindness](failures/tablefigure-blindness.md). The document was retrieved, but the specific value needed lives in a scanned, smudged, or visually-structured region the text-extraction pipeline doesn't correctly read.
- **Context Assembly** — [Chunk Boundary Failure](failures/chunk-boundary-failure.md), [Context Stuffing Failure](failures/context-stuffing-failure.md). Once relevant content is found, how it's split into chunks and packed into the synthesis context window can still lose or dilute the fact that made retrieval succeed in the first place.
- **Downstream Synthesis and Attribution** — [Answer Synthesis Failure](failures/answer-synthesis-failure.md), [Citation Mismatch](failures/citation-mismatch.md), [Conflicting Source Failure](failures/conflicting-source-failure.md), [Stale Document Use](failures/stale-document-use.md). Correctly retrieved content can still be summarized incorrectly, cited to the wrong source, left unreconciled when sources disagree, or simply be an outdated document that scored well on relevance but not on currency.

## When Retrieval Matters

- A knowledge base serves multiple tenants, products, or business units, where a wrong-corpus retrieval isn't just a quality problem but a data-isolation or compliance incident
- Source documents include scanned faxes, tables, or embedded figures, and the pipeline's indexing was built primarily around clean, born-digital text
- Retrieved documents can span multiple valid versions or time periods (policies, pricing, reports), creating conditions for a stale but well-ranked document to be selected over its current replacement

## Cross-Pattern Insight

The 12 retrieval patterns describe a pipeline where an error at any stage is invisible to every stage after it: a wrong-corpus search looks like a normal retrieval to the ranking step, a poorly-OCR'd document looks like a normal chunk to the context-assembly step, and a stale document looks like a normal citation to the synthesis step. The mitigation that recurs across nearly every pattern here is the same architectural move — add an explicit, independent verification layer at the boundary between stages rather than trusting that a good result at one stage implies a good result at the next: tenant-isolation tests that run independently of the retrieval logic itself, citation-grounding checks that verify a claim against its cited chunk rather than trusting the citation was attached correctly, and staleness/freshness scoring that runs independently of semantic relevance ranking. No single stage's success is a reliable signal that the pipeline as a whole produced a correct, current, and properly-attributed answer.

## Frequently Asked Questions

### How much does a wrong-corpus retrieval matter compared to an ordinary low-relevance result?
Considerably more in a multi-tenant or multi-product system — per [Wrong Corpus Retrieval](failures/wrong-corpus-retrieval.md), retrieving from the wrong corpus can mean surfacing one customer's or one product line's documents to a different customer's query, a tenant-isolation violation and potential security/compliance incident rather than merely a quality miss. The pattern's documented target is 0% cross-tenant leakage, treated as a P1 incident on any nonzero occurrence.

### What is the difference between low-precision and low-recall retrieval?
[Low-Precision Retrieval](failures/low-precision-retrieval.md) means the retrieved set contains irrelevant chunks (the threshold or top-k is too permissive), corrupting synthesis with noise. [Low-Recall Retrieval](failures/low-recall-retrieval.md) means relevant chunks exist in the corpus but weren't retrieved (the threshold is too strict), which typically manifests as an incorrect "I don't have information about that" or a hallucinated answer filling the gap retrieval should have filled.

### How do you catch a citation that doesn't actually support its claim?
Per [Citation Mismatch](failures/citation-mismatch.md), run an NLI (natural language inference) entailment check between the generated claim and the retrieved chunk it cites before the answer is finalized, and block or flag any claim whose cited source doesn't actually entail it — a naive check that only confirms the citation exists will miss a claim-source mismatch entirely.

### Can better OCR alone fix table and figure blindness?
No — [Table/Figure Blindness](failures/tablefigure-blindness.md) and [OCR Extraction Error](failures/ocr-extraction-error.md) are related but distinct: OCR failures are about misread text, while table/figure blindness is about structurally-formatted data (rows, columns, chart values) that text-only extraction never captures as queryable content regardless of OCR accuracy. The fix requires a separate table/figure extraction pipeline (structure detection plus table-specific OCR into a queryable representation), not just a better general-purpose OCR engine.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Answer Synthesis Failure](failures/answer-synthesis-failure.md) | Correctly retrieved information is summarized or paraphrased incorrectly during synthesis |
| [Chunk Boundary Failure](failures/chunk-boundary-failure.md) | A fact needed to answer the query is split across two chunks and never assembled together |
| [Citation Mismatch](failures/citation-mismatch.md) | Agent cites a retrieved source that doesn't actually support the claim attached to it |
| [Conflicting Source Failure](failures/conflicting-source-failure.md) | Two retrieved documents disagree and the agent picks one without reconciling or disclosing the conflict |
| [Context Stuffing Failure](failures/context-stuffing-failure.md) | Too many retrieved chunks dilute the synthesis context, burying the one that actually answers the query |
| [Low-Precision Retrieval](failures/low-precision-retrieval.md) | Retrieval threshold or top-k too permissive, pulling in irrelevant chunks that corrupt the synthesized answer |
| [Low-Recall Retrieval](failures/low-recall-retrieval.md) | Retrieval threshold or top-k too strict, missing relevant documents that exist in the corpus |
| [Metadata Filter Error](failures/metadata-filter-error.md) | Wrong or overly strict date, version, region, or role filter excludes a document that should have matched |
| [OCR Extraction Error](failures/ocr-extraction-error.md) | Agent misreads scanned, smudged, rotated, or low-quality source text |
| [Stale Document Use](failures/stale-document-use.md) | Agent retrieves and relies on an outdated policy, document, or version instead of its current replacement |
| [Table/Figure Blindness](failures/tablefigure-blindness.md) | Agent misses data embedded in tables, charts, images, or PDFs that text-only extraction never captured |
| [Wrong Corpus Retrieval](failures/wrong-corpus-retrieval.md) | Agent searches the wrong knowledge base or tenant corpus entirely |

**Total: 12 patterns**

## Related Goals

- [Retrieval Quality](../retrieval-quality/) — a complementary set of ranking, embedding, and freshness failures at a finer level of granularity than retrieval's pipeline-stage view
- [Citation Accuracy](../citation-accuracy/) — a deeper treatment of the citation-grounding failures Citation Mismatch and Answer Synthesis Failure touch on here
- [Answer Synthesis](../answer-synthesis/) — the full set of generation-stage failures that occur once retrieval has already handed off its (possibly flawed) result set
