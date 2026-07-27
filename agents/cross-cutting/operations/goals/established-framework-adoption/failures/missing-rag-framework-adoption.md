# Missing RAG Framework Adoption

## Issue: Team builds a bespoke retrieval pipeline (custom chunking, custom vector store glue, custom prompt assembly) from scratch instead of adopting an established RAG framework, missing built-in chunking strategies, retrieval orchestration, and evaluation tooling that ship by default.

**Frequency**: Occasional

**Symptoms**
- Chunking, embedding orchestration, and retrieval-to-prompt assembly are all hand-rolled, with no framework providing tested defaults for any pipeline stage
- Chunk size and overlap were picked once by trial and error early on and never revisited, with no chunking-strategy comparison (fixed-size vs. semantic vs. recursive) ever run
- Retrieval is a single dense-vector similarity search with no hybrid search, re-ranking, or query rewriting, because none of those were built and no framework provided them by default
- Adding a new document type or data source requires writing an entirely new ingestion path from scratch, since there is no shared document-loader abstraction
- There is no built-in evaluation harness for retrieval quality (context precision/recall/faithfulness), so regressions from chunking or embedding-model changes are only caught by user complaints

**Root Cause**
Team builds a bespoke retrieval pipeline from scratch instead of adopting an established RAG framework, missing built-in chunking strategies, retrieval orchestration, and evaluation tooling that ship by default.

**Example**
```
An internal engineering-docs assistant is built by a small platform team who
writes a Python script to split markdown files into 500-character chunks with
no overlap, embeds them with a single call to an embedding API, stores vectors
in a self-managed table, and assembles the top-3 nearest chunks into a prompt
template written by hand.

As the docs corpus grows past a few thousand pages, engineers start noticing
the assistant frequently answers with outdated or only-half-relevant
information. The root cause turns out to be several stacked, unaddressed gaps:
fixed 500-character chunking regularly splits a procedure's steps across chunk
boundaries so only half of a runbook is ever retrieved together; there is no
re-ranking step, so a marginally relevant recent chunk sometimes crowds out a
more precise older one; and there is no evaluation harness at all, so nobody
noticed the degradation until users started complaining in a shared Slack
channel. Rebuilding chunking, retrieval, and evaluation from scratch to fix
each gap individually took the team most of a quarter - all functionality an
established RAG framework would have shipped with tested defaults for out of
the box.
```

**Contributing Factors**
- No evaluation of established RAG frameworks (document processing, embedding orchestration, retrieval, evaluation) was done before building each pipeline stage independently in-house
- The initial prototype ("just embed some docs and do similarity search") worked well enough on a small corpus that nobody revisited the architecture as the corpus and query diversity grew
- Each pipeline stage (chunking, embedding, storage, retrieval) was built by a different engineer at a different time with no shared design review, so there was never a single point to decide "should we adopt a framework instead"
- Framework adoption was seen as a rewrite risk to an already-working system, so the team kept patching the bespoke pipeline incrementally rather than migrating
- No one on the team had hands-on experience with LangChain, LlamaIndex, or Haystack, so the bespoke approach felt like the path of least resistance despite the long-term maintenance cost

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Chunk boundary integrity | A multi-step procedure/runbook document split by the current chunking strategy | All steps of a single procedure retrievable together in one chunk or clearly linked chunks | Steps of a single procedure are split across unrelated chunk boundaries |
| Retrieval quality regression | A fixed benchmark set of query/expected-answer pairs run after an embedding model or chunking change | Context precision/recall/faithfulness scores stay within an acceptable range of baseline | Scores drop significantly after a pipeline change with no automated flag |
| New document type onboarding | A new file format (e.g. PDF with tables) added to the corpus | Existing ingestion abstraction handles the new format via configuration, not a new bespoke loader | A wholly new ingestion script must be written from scratch for the new format |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Context precision/recall (RAGAS-style) | >= 0.8 on a labeled evaluation set | Run an automated RAG evaluation (e.g. RAGAS) against a held-out query/answer benchmark after every pipeline change |
| Retrieval regression detection lag | Detected within 1 release cycle | Track time between a chunking/embedding change and detection of a quality regression |
| New data source onboarding time | < 1 day | Measure engineering time to onboard a new document type/source into the pipeline |

---

## Mitigation Strategies

### Prevention
1. **Adopt LlamaIndex or LangChain for pipeline orchestration**: Use tested document loaders, chunking strategies (semantic, recursive, sentence-window), and retrieval orchestration instead of hand-rolling each stage; LlamaIndex for document-centric RAG, LangChain for broader agent/tool integration.
2. **Adopt RAGAS (or DeepEval) for retrieval evaluation**: Get objective context precision/recall/faithfulness/relevancy metrics and automatic test-dataset generation instead of relying on manual spot-checks of answer quality.
3. **Run a build-vs-buy evaluation before extending the bespoke pipeline further**: Before writing another custom loader or chunker, compare the effort against adopting a framework's existing implementation of that stage.

### Detection & Response
1. **Scheduled retrieval-quality benchmarking**: Run the evaluation framework against a fixed benchmark set on every embedding model, chunking, or retrieval-logic change, not just at initial launch.
2. **Chunk-boundary spot audits**: Periodically sample retrieved chunks against source documents to check whether logical units (steps, sections) are being split inappropriately.
3. **User feedback loop wired to eval set**: Feed user-reported bad answers back into the evaluation benchmark as new test cases, closing the loop that manual pipelines typically lack.

### Architecture Patterns
1. **Framework-native pipeline stages**: Use the chosen framework's document loader, node parser/chunker, retriever, and query engine abstractions end-to-end rather than mixing bespoke code with framework pieces.
2. **Hybrid search + re-ranking**: Adopt the framework's built-in hybrid (dense + sparse) search and re-ranking support rather than single-vector similarity search alone.
3. **Evaluation-in-the-loop CI**: Wire the RAG evaluation framework into CI so retrieval quality is checked automatically before any pipeline change ships, mirroring how code tests gate deploys.

### Metrics
1. **context_precision_recall_score**: Target: >= 0.8; Alert threshold: < 0.65
2. **retrieval_regression_detection_lag_days**: Target: < 3 days; Alert threshold: > 14 days
3. **new_source_onboarding_hours**: Target: < 8 hours; Alert threshold: > 40 hours

### Alerts
1. **Retrieval Quality Regression Detected** (P2 - Warning): Condition - context precision/recall on the benchmark set drops below threshold after a pipeline change. Action: notify pipeline owner, consider rollback of the change.
2. **Chunk Boundary Audit Failure** (P3 - Info): Condition - sampled audit finds a logical unit (procedure/section) split across unrelated chunks at a high rate. Action: notify team to revisit chunking strategy.
3. **New Source Onboarding Delay** (P3 - Info): Condition - onboarding a new document type takes significantly longer than target. Action: flag for review of whether a framework's loader abstraction should be adopted.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| context_precision_recall_score | < 0.65 |
| retrieval_regression_detection_lag_days | > 14 days |
| new_source_onboarding_hours | > 40 hours |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Retrieval quality regression | Context precision/recall benchmark score drops below threshold after a change | Medium |
| Chunk boundary audit failure | Sampled audit finds frequent splitting of logical procedure/section units | Low |
| New source onboarding delay | Onboarding a new document type exceeds target engineering time | Low |

---

## Related Patterns

- [Chunk Boundary Failure](../../../../../by-capability/knowledge-retrieval/goals/retrieval/failures/chunk-boundary-failure.md) - a downstream symptom this pattern's missing framework (with tested chunking strategies) would help prevent
- [Low Recall Retrieval](../../../../../by-capability/knowledge-retrieval/goals/retrieval/failures/low-recall-retrieval.md) - a related downstream symptom; hybrid search and re-ranking (missing here) are exactly the kind of tested defaults an established framework provides out of the box

## References

- [15 Best Open-Source RAG Frameworks in 2026](https://www.firecrawl.dev/blog/best-open-source-rag-frameworks) - survey of mature RAG frameworks and their pipeline coverage
- [Best RAG Framework 2026: LangChain vs LlamaIndex vs DSPy](https://iternal.ai/blockify-rag-frameworks) - LangChain for rapid prototyping, LlamaIndex for document-centric RAG, Haystack for enterprise-grade production pipelines with built-in evaluation tooling
- [RAGAS evaluation](https://www.olostep.com/blog/open-source-rag-frameworks) - RAGAS provides objective context precision/recall/faithfulness/relevancy metrics and automatic test-dataset generation, usable across any RAG framework
