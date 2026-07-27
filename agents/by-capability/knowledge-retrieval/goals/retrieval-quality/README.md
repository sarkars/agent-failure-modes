# What Are the Most Common Retrieval Quality Failures in AI Agents?

**Retrieval quality fails when the pipeline finds documents that are topically plausible but wrong along a dimension similarity search doesn't measure — outdated, jurisdictionally inapplicable, poorly ranked relative to a better match sitting a few positions lower, diluted by too much or too little context, or compromised by an embedding-model version mismatch or a poisoned document nobody vetted.** All 13 patterns share the same root limitation: semantic similarity is the one signal nearly every retrieval pipeline optimizes for by default, and every pattern here documents a case where similarity and correctness diverge — a textually-similar document that is stale, jurisdictionally wrong, structurally split, or simply outranked by a better match the system never surfaced.

## Key Takeaways

- 13 patterns are documented here, covering ranking and volume tuning, temporal and jurisdictional validity, structural chunk integrity, and index/embedding infrastructure health.
- Chunk Boundary Issues is rated "Very Common" and Semantic Mismatch is rated "Very Common" — both are default production behavior in any pipeline using fixed-size chunking or off-the-shelf embeddings without domain tuning, not edge cases.
- Reranking Degradation documents a measured -27% Context Precision drop in one example: a cross-encoder reranker, tuned on general web prose, demoted a terse-but-correct technical spec sheet from rank 1 to rank 5 in favor of more fluent but less useful marketing copy — rerankers can make retrieval measurably worse, not just fail to help.
- Temporal Relevance and Jurisdictional Mismatch both trace to the same gap: embedding similarity has no built-in concept of legal currency or jurisdictional applicability, so a semantically on-topic but overruled precedent or wrong-state statute can outrank the actually-correct source.

## Scope

- **Ranking and Volume Tuning** — [Over-Retrieval](failures/over-retrieval.md), [Under-Retrieval](failures/under-retrieval.md), [Retrieval Ranking Errors](failures/retrieval-ranking-errors.md), [Reranking Degradation](failures/reranking-degradation.md), [Query Expansion Noise](failures/query-expansion-noise.md). The core precision/recall/ordering tuning surface — too many documents, too few, the right documents ranked too low, a reranker actively making ranking worse, or a query-expansion step introducing off-topic terms.
- **Temporal and Jurisdictional Validity** — [Temporal Relevance](failures/temporal-relevance.md), [Jurisdictional Mismatch](failures/jurisdictional-mismatch.md), [Index Staleness](failures/index-staleness.md). Content that is semantically on-topic but no longer valid — overruled, out of jurisdiction, or superseded by an update the index hasn't caught up to.
- **Structural and Semantic Gaps** — [Chunk Boundary](failures/chunk-boundary.md), [Semantic Mismatch](failures/semantic-mismatch.md), [Metadata Filtering](failures/metadata-filtering.md). Content that's present in the corpus but not correctly surfaced because a chunk split apart related information, the user's phrasing doesn't match the document's vocabulary, or a metadata filter's schema or type mismatch silently excludes a valid match.
- **Index and Model Infrastructure** — [Embedding Drift](failures/embedding-drift.md), [Knowledge Base Poisoning](failures/knowledge-base-poisoning.md). Failures in the underlying infrastructure retrieval depends on — an incompatible embedding-model version change, or malicious content injected into a knowledge base that retrieval trusts by default.

## When Retrieval Quality Matters

- The domain has meaningful temporal or jurisdictional validity constraints — law, medicine, tax, policy — where a semantically similar but superseded or wrong-jurisdiction source is worse than no source at all
- The corpus mixes short technical/structured content (spec sheets, tables) with long-form prose, since rerankers and embeddings tuned on general web text systematically favor the latter regardless of which actually answers the query
- The knowledge base accepts contributions from multiple sources of varying trust (official documents alongside wikis, forums, or user-generated content), creating both a poisoning attack surface and an unweighted-reliability gap

## Cross-Pattern Insight

Every pattern in retrieval quality documents a case where semantic similarity was treated as a sufficient proxy for correctness, when it measures only topical resemblance — not currency, not jurisdiction, not structural completeness, not reliability, and not immunity from malicious injection. The mitigation that recurs across nearly all 13 patterns is to add an explicit, non-similarity signal as a first-class ranking or filtering input rather than layering it on as an afterthought: recency/validity metadata that gates or downweights results independent of similarity score, jurisdiction and source-reliability tags enforced at the schema level, hybrid dense-plus-sparse retrieval so vocabulary mismatch doesn't rely on embeddings alone, and content-validation pipelines that scan for injected instructions before a document ever becomes retrievable. The consistent finding is that similarity search and correctness are two different axes, and a retrieval pipeline that only tunes the first axis will keep hitting failures on the second no matter how good its embedding model becomes.

## Frequently Asked Questions

### How is a reranker able to make retrieval quality worse instead of better?
Per [Reranking Degradation](failures/reranking-degradation.md), a cross-encoder or LLM-based reranker trained on general web data learns biases toward fluency, length, and typical document formatting that don't track actual task relevance — the documented example shows a reranker demoting a terse, correct technical spec sheet below a well-written but useless marketing document, a -27% Context Precision drop. The fix is to require a reranker to beat a baseline on a domain benchmark before deployment, not just deploy it and assume reranking helps by default.

### What is the difference between temporal relevance and index staleness?
[Temporal Relevance](failures/temporal-relevance.md) is about retrieval finding a document that was once correct but has since been superseded (an overruled legal precedent, a repealed statute) with no supersession-awareness in the ranking. [Index Staleness](failures/index-staleness.md) is the systems-level cause behind many such cases — the index simply hasn't been re-synced with the source-of-truth system, so an outdated version is what's available to retrieve at all.

### Can a better embedding model fix semantic mismatch on its own?
Partially — [Semantic Mismatch](failures/semantic-mismatch.md) recommends fine-tuning embeddings on domain-specific query-document pairs, but the documented mitigation set also includes hybrid dense-plus-sparse retrieval and HyDE (hypothetical document embeddings) precisely because no single embedding model fully closes the gap between casual user phrasing and formal document language — the fix is architectural (multiple retrieval signals), not just a model swap.

### Does adding a reranker or query expansion always improve retrieval quality?
No — both [Reranking Degradation](failures/reranking-degradation.md) and [Query Expansion Noise](failures/query-expansion-noise.md) document cases where the added step actively hurts: reranking can demote correct-but-terse results, and query expansion can introduce wrong-sense terms (like "Mercury" the planet when the query meant the element) that pull in off-topic documents. Both patterns recommend baseline-guarded rollout — proving the addition helps on a domain benchmark before trusting it in production.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Chunk Boundary](failures/chunk-boundary.md) | Document splits don't respect semantic boundaries, separating a fact from the context it needs |
| [Embedding Drift](failures/embedding-drift.md) | An embedding model version change creates incompatible vector spaces between queries and previously-indexed documents |
| [Index Staleness](failures/index-staleness.md) | Index isn't updated when source documents change, so superseded versions remain retrievable |
| [Jurisdictional Mismatch](failures/jurisdictional-mismatch.md) | Text similarity retrieves content from the wrong jurisdiction, since embeddings can't distinguish governing law by topic alone |
| [Knowledge Base Poisoning](failures/knowledge-base-poisoning.md) | Malicious or manipulated content is injected into a knowledge base and retrieved with the same trust as legitimate content |
| [Metadata Filtering](failures/metadata-filtering.md) | Pre-retrieval filters exclude relevant documents due to schema mismatches (type, taxonomy) between filter and metadata |
| [Over-Retrieval](failures/over-retrieval.md) | Too many marginally-relevant documents dilute the context and bury the genuinely relevant ones |
| [Query Expansion Noise](failures/query-expansion-noise.md) | Synonym/LLM-based query expansion introduces off-topic terms that shift the query's meaning |
| [Reranking Degradation](failures/reranking-degradation.md) | A reranker trained on general data demotes correct-but-terse results in favor of fluent but less relevant ones |
| [Retrieval Ranking Errors](failures/retrieval-ranking-errors.md) | Relevant documents are retrieved but ranked too low for a fixed top-k cutoff to capture |
| [Semantic Mismatch](failures/semantic-mismatch.md) | User phrasing and document vocabulary diverge enough that embedding similarity falls below the retrieval threshold |
| [Temporal Relevance](failures/temporal-relevance.md) | Retrieval finds a document that was accurate at indexing time but has since been superseded or overruled |
| [Under-Retrieval](failures/under-retrieval.md) | Threshold or top-k too strict, dropping true positives that sit just below the cutoff |

**Total: 13 patterns**

## Related Goals

- [Retrieval](../retrieval/) — a pipeline-stage view of retrieval covering corpus selection and content-extraction gaps that complement retrieval quality's ranking/validity focus
- [Knowledge Freshness](../knowledge-freshness/) — Temporal Relevance and Index Staleness share the underlying update-lag and expiration mechanisms documented in depth there
- [Answer Synthesis](../answer-synthesis/) — what happens to a synthesized answer once retrieval quality has already determined which chunks reach the generation step
