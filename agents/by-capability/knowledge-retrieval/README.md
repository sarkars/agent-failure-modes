# What Are the Most Common Knowledge Retrieval Failures in AI Agents?

**Knowledge retrieval failures happen at every stage of a RAG pipeline independently — a query gets misunderstood before search even runs, the wrong or poorly-ranked documents get retrieved, a synthesized answer drifts from or hallucinates beyond correct context, a citation points at a source that doesn't actually support its claim, and a fact that's individually true gets applied at the wrong time, scope, or level of domain nuance.** None of the five stages named above reliably catches an error made at an earlier stage: a synthesis model has no way to know retrieval already searched the wrong corpus, and a citation-verification step has no way to know the cited fact was true a year ago but isn't anymore. That gap is what makes knowledge retrieval a category of parallel, independently-failing concerns rather than a single pipeline with one point of failure.

## Key Takeaways

- 7 goals and 74 patterns are documented here, spanning query understanding, retrieval and retrieval quality, answer synthesis, citation accuracy, retrieval relevance, and knowledge freshness.
- Knowledge Freshness is the largest goal at 22 patterns — nearly a third of the category — because it spans three distinct levels of the same problem: domain-level judgment gaps, single-fact distortions, and system-level architecture gaps like missing expiration mechanisms.
- Retrieval and Retrieval Quality together document 25 patterns spanning the same underlying pipeline stage at two levels of granularity — corpus/precision/recall/extraction fundamentals in Retrieval, and ranking/embedding/index-infrastructure nuance in Retrieval Quality.
- Legal RAG tools are cited at a documented 17-33% hallucination rate even with retrieval augmentation (Stanford Legal RAG Hallucinations study) — retrieval augmentation reduces but does not eliminate hallucination, a finding that recurs across Answer Synthesis, Citation Accuracy, and Knowledge Freshness patterns alike.

## Knowledge Retrieval Goals

| Goal | Covers | Patterns |
|------|--------|----------|
| [Answer Synthesis](goals/answer-synthesis/) | Generation-stage failures after retrieval succeeds — context ignored, hallucination despite context, cherry-picking, source contradiction, confidence miscalibration | 11 |
| [Citation Accuracy](goals/citation-accuracy/) | Citations that exist but don't do the job a citation is supposed to do — fabricated, misgrounded, wrong source, wrong granularity, broken links | 7 |
| [Knowledge Freshness](goals/knowledge-freshness/) | Facts and domain knowledge applied at the wrong time, scope, or level of domain nuance, plus the architecture gaps that make misapplication more likely | 22 |
| [Query Understanding](goals/query-understanding/) | Misreading what a user actually wants before retrieval ever runs — ambiguity, false premises, scope, multi-part fragmentation | 8 |
| [Retrieval](goals/retrieval/) | Pipeline-stage retrieval failures — wrong corpus, precision/recall tuning, content-extraction blind spots, context assembly, downstream synthesis/attribution | 12 |
| [Retrieval Quality](goals/retrieval-quality/) | Ranking, embedding, temporal/jurisdictional validity, and index-infrastructure failures at a finer level of granularity than Retrieval | 13 |
| [Retrieval Relevance](goals/retrieval-relevance/) | Structural-attribute mismatch hiding behind high textual similarity in comparable-item retrieval | 1 |

**Total: 74 patterns**

## How the Goals Relate

The 7 goals in knowledge retrieval are mostly parallel concerns rather than a strict pipeline, because a RAG system can fail at any one of the stages below independently of whether the others succeeded. Query Understanding failures happen before search runs at all. Retrieval and Retrieval Quality failures happen during search, at two levels of granularity — Retrieval covers corpus selection, precision/recall tuning, and content-extraction gaps; Retrieval Quality covers ranking, embedding-model health, and temporal/jurisdictional validity within an already-selected corpus. Retrieval Relevance is a narrow, single-pattern special case of retrieval matching on the wrong signal (text similarity instead of structural attributes). Answer Synthesis and Citation Accuracy both happen after retrieval succeeds — a correctly-retrieved set of documents can still be synthesized or cited incorrectly. Knowledge Freshness cuts across every other goal listed above: a fact can be retrieved correctly, synthesized faithfully, and cited accurately, and still be wrong because it's stale, out of scope, or missing domain nuance that a generic pipeline never encoded. To localize an incident by symptom: the agent answers the wrong question entirely → **Query Understanding**; the wrong documents (or too many/too few) come back from search → **Retrieval** or **Retrieval Quality**; the right documents come back but the generated answer doesn't reflect that content faithfully → **Answer Synthesis**; the answer cites a source that doesn't actually support its claim → **Citation Accuracy**; every individual fact and citation checks out but the answer is still wrong for the moment or scope it's needed in → **Knowledge Freshness**.

## Frequently Asked Questions

### Which goal should be checked first when a RAG agent gives a wrong answer?
Work backward through the pipeline: first confirm [Query Understanding](goals/query-understanding/) correctly parsed the actual question, then check whether [Retrieval](goals/retrieval/) or [Retrieval Quality](goals/retrieval-quality/) found the right documents, then check whether [Answer Synthesis](goals/answer-synthesis/) faithfully used what was retrieved. If every stage checks out and the answer is still wrong, the fact itself was likely stale or misapplied — check [Knowledge Freshness](goals/knowledge-freshness/).

### Do the 7 goals form a strict pipeline where fixing an earlier stage fixes everything downstream?
No. Because each goal documents an independent failure surface, a RAG system can have perfect query understanding, perfect retrieval, and still fail at synthesis or citation — or have flawless synthesis of a document that was itself stale. Fixing one goal's patterns doesn't guarantee the remaining goals are covered; a production-grade pipeline needs monitoring across all 7 simultaneously.

### What is the difference between Retrieval and Retrieval Quality?
[Retrieval](goals/retrieval/) takes a pipeline-stage view — corpus selection, precision/recall threshold tuning, content-extraction blind spots (OCR, tables), context assembly, and downstream synthesis/citation. [Retrieval Quality](goals/retrieval-quality/) covers a complementary, finer-grained set of concerns within an already-correctly-scoped search — ranking errors, reranker degradation, embedding-model version drift, and temporal/jurisdictional validity of otherwise well-matched documents.

### Can retrieval augmentation alone eliminate hallucination?
No — the Stanford Legal RAG Hallucinations study documents a 17-33% hallucination rate even in retrieval-augmented legal tools, a finding echoed across [Answer Synthesis](goals/answer-synthesis/)'s Hallucination Despite Context pattern and [Citation Accuracy](goals/citation-accuracy/)'s Misgrounded Citation pattern. Retrieval reduces hallucination risk relative to a closed-book model, but doesn't eliminate the model's tendency to fill gaps or misapply retrieved content with confidence.

## Related Categories

- [Document Processing](../document-processing/) — what happens before content ever reaches a retrieval index, including OCR, layout preservation, and classification failures that determine what's available to retrieve
- [Reasoning and Thought](../reasoning-and-thought/) — model-behavior and model-versioning failures that compound with knowledge-retrieval issues whenever the underlying model itself is degrading or has changed
