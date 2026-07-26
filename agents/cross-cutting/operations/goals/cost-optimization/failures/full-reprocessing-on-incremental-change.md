# Full Reprocessing on Incremental Change

## Issue: A Small Edit to a Source Document Triggers Full Re-Embedding/Re-Analysis of the Entire Document Instead of an Incremental Update to Just the Changed Portion

**Frequency**: Common

**Symptoms**
- Editing one paragraph of a large source document (policy doc, knowledge-base article, codebase file) triggers re-embedding, re-chunking, or re-summarization of the entire document
- Reprocessing cost and latency for a document is the same whether 1% or 100% of its content changed
- No change-detection or diffing step exists between the update pipeline and the full-reprocessing pipeline
- Index/embedding refresh jobs process entire document sets on every source update rather than only the changed documents' changed sections

**Root Cause**
Document ingestion and re-indexing pipelines are often built around a simple "process the whole document" model because it's easier to implement than tracking and reprocessing only what changed. This is a reasonable default for initial ingestion, but when the same full-document pipeline is reused for every subsequent edit, a one-line correction to a 50-page document costs the same as ingesting a brand-new 50-page document, every time. As documents that update frequently (living policy docs, changelogs, product catalogs) accumulate edits, this compounds into a recurring, avoidable cost that scales with document size rather than with the actual size of each edit.

**Example**
```
A company's 40-page product policy document is updated ~3 times/week
(small edits: a price change, a clarified sentence, a new bullet point).

Each update triggers the standard ingestion pipeline: the full document
is re-chunked (into ~80 chunks) and every chunk is re-embedded, even
though a typical edit changes only 1-2 of the 80 chunks.

Per-update reprocessing cost (full document):
  80 chunks x ~150 tokens/chunk = 12,000 tokens re-embedded

Per-update cost if only changed chunks were reprocessed:
  ~2 chunks x 150 tokens = 300 tokens

At 3 updates/week x 52 weeks = 156 updates/year:
  Full-reprocessing total: 156 x 12,000 = 1,872,000 tokens/year
  Incremental-reprocessing total: 156 x 300 = 46,800 tokens/year

Waste: 1,825,200 tokens/year (97.5%) spent re-embedding the 78 chunks
per update that never actually changed.
```

**Contributing Factors**
- No diffing step compares the new document version against the previously-ingested version before deciding what to reprocess
- Chunking/embedding pipeline was designed for initial ingestion and reused unmodified for update-triggered reprocessing
- Change events from the source system (a CMS save, a wiki edit, a file commit) don't carry a diff or changed-section marker, only a "document updated" signal
- No per-chunk versioning or content-hash tracking exists to determine which chunks are actually stale after an edit

---

## Test Scenario & Reproduction

### Scenario Setup
- A document ingestion/re-indexing pipeline that reprocesses (re-chunks and re-embeds) the entire document on every update event
- A representative document that receives frequent small edits (e.g., a policy doc with weekly minor changes)
- No content-hash/versioning mechanism to detect which specific chunks changed between versions

### Trigger Mechanism
1. Ingest a large document and record the full reprocessing cost (chunks re-embedded, tokens spent)
2. Apply a small, localized edit (e.g., change one sentence) and trigger the update pipeline
3. Measure whether the full document is reprocessed again, versus only the changed section

**Example Reproduction Steps:**
```
1. Ingest a 40-page document, chunked into 80 pieces; record total
   embedding tokens for full ingestion
2. Apply a one-sentence edit affecting content within 1-2 of the 80
   chunks
3. Trigger the standard update/re-indexing pipeline
4. Log how many chunks are re-embedded as a result of this single edit
5. Compare against the chunk count that actually changed (1-2) versus
   the chunk count actually reprocessed (expected: all 80)
6. Repeat over a series of 10 small, independent edits and sum total
   reprocessing tokens
7. Compute the waste ratio: tokens spent reprocessing unchanged chunks
   divided by total tokens spent
```

### Expected Failure State
- Every edit, regardless of how localized, triggers re-embedding of all 80 chunks rather than just the 1-2 that actually changed
- Waste ratio (tokens spent on unchanged-chunk reprocessing / total reprocessing tokens) exceeds 90%, consistent with the example's 97.5% waste
- No content-hash or chunk-level versioning exists to distinguish stale from still-valid chunks after an edit
- Reprocessing cost and latency per update are statistically indistinguishable from the cost of ingesting the document from scratch

---

## Mitigation Strategies

### Prevention
1. **Content-hash-based chunk diffing**: Store a content hash per chunk at ingestion time; on a document update, re-chunk the new version, compare chunk-level hashes against the prior version, and re-embed only chunks whose hash changed, directly targeting the 78-of-80-chunks waste in the example. Trade-off: re-chunking boundaries can shift even when content is mostly unchanged (e.g., if an early paragraph grows longer, later chunk boundaries may shift), which can cause more chunks to register as "changed" than the edit's actual scope; chunking strategies that are resilient to small insertions (e.g., paragraph-anchored rather than fixed-token-count chunking) reduce this false-positive rate.
2. **Diff-aware update events from the source system**: Where the source system (CMS, wiki, version control) can supply a diff or changed-section marker rather than just a generic "document updated" event, consume that diff directly to identify candidate chunks for reprocessing, rather than re-deriving the diff independently after the fact. Trade-off: requires integration work with each source system to expose diff information, which may not be uniformly available across all document sources.
3. **Chunk-level versioning independent of document-level versioning**: Track version/freshness at the chunk level, not just the document level, so a document-level "updated" flag doesn't force full reprocessing when only a subset of its chunks actually changed. Trade-off: adds bookkeeping overhead (mapping document versions to chunk versions) versus the simplicity of a single document-level timestamp.

### Detection & Response
1. **Reprocessing-scope-versus-actual-change-scope tracking**: For every update-triggered reprocessing event, log both the number of chunks reprocessed and (via post-hoc diffing) the number of chunks that actually differ from the prior version; a persistent large gap between these two numbers is the direct signature of this failure.
2. **Update-cost-versus-ingestion-cost comparison**: Track whether the cost of processing a document update is statistically similar to the cost of processing that same document from scratch; if updates cost nearly as much as full ingestion regardless of edit size, incremental reprocessing isn't happening.
3. **High-churn-document cost audit**: Identify documents with frequent update events and compute their cumulative annual reprocessing cost; documents with both high update frequency and full-reprocessing-per-update are the highest-value targets for incremental-reprocessing fixes.

### Architecture Patterns
1. **Two-phase update pipeline: diff then selective reprocess**: Split the update pipeline into an explicit diffing phase (compare new document against the stored chunk-hash manifest to identify changed chunks) followed by a selective reprocessing phase (re-embed only the identified chunks and patch the index), rather than a single "reprocess everything" pipeline reused unmodified for updates. Deployment consideration: requires maintaining a chunk-hash manifest per document, which itself needs storage and must stay synchronized with the live index.
2. **Content-addressed chunk storage**: Store chunks and their embeddings keyed by content hash rather than by position/index, so that an unchanged chunk (even if its position shifts slightly due to nearby edits) is recognized as already-embedded and skipped, rather than re-embedded simply because its offset within the document changed. Deployment consideration: requires a mapping layer between content-addressed storage and the document's positional/sequential structure for retrieval purposes.
3. **Lightweight verification pass over unchanged chunks**: Rather than fully re-embedding unchanged chunks, run a cheap verification step (e.g., a fast hash comparison, or a lightweight patch-check) confirming they're genuinely unchanged before skipping them, providing a safety net against silent corruption or missed edits without paying the full re-embedding cost. Deployment consideration: the verification step itself must be materially cheaper than full re-embedding, or it erodes the savings this pattern targets.

### Metrics
1. **reprocessing_waste_ratio**: Target < 20% of reprocessing tokens spent on chunks that didn't actually change; Alert if > 70% (approaching the example's 97.5%).
2. **update_cost_to_full_ingestion_cost_ratio**: Target < 15% for a typical small edit; Alert if > 80% (indicating updates cost nearly as much as full re-ingestion).
3. **chunk_hash_manifest_coverage_percent**: Target 100% of frequently-updated documents have a maintained chunk-hash manifest; Alert if < 50%.
4. **high_churn_document_annual_reprocessing_cost**: Track per-document; flag any document whose annual reprocessing cost, driven by update frequency, exceeds its one-time full-ingestion cost by more than 10x without incremental reprocessing in place.

### Alerts
1. **Full-Reprocessing-On-Small-Edit** (P3): Condition - reprocessing_waste_ratio exceeds 70% for a document update event. Action: prioritize implementing chunk-hash diffing for that document's ingestion pipeline.
2. **High-Churn-Document-Cost-Outlier** (P3): Condition - a document's high_churn_document_annual_reprocessing_cost exceeds 10x its one-time ingestion cost. Action: treat as a top candidate for the two-phase diff-then-selective-reprocess pipeline.

## References

- [Zero-Waste Agentic RAG: Designing Caching Architectures to Minimize Latency and LLM Costs at Scale](https://towardsdatascience.com/zero-waste-agentic-rag-designing-caching-architectures-to-minimize-latency-and-llm-costs-at-scale/) - caching and incremental-update architectures for RAG ingestion pipelines to avoid reprocessing unchanged content
- [StepCache: Step-Level Reuse with Lightweight Verification and Selective Patching for LLM Serving](https://arxiv.org/pdf/2603.28795) - step-level reuse with lightweight verification and selective patching, applicable to avoiding full reprocessing when only part of an input changed
- [Related Pattern: Caching Failures](../../cost-efficiency/failures/caching-failures.md) - the broader caching-failure category; this pattern is the specific case of document/index reprocessing rather than LLM response caching
