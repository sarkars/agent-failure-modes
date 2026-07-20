# Semantic Drift in Embeddings

## Issue
When the embedding model used to index a memory store is upgraded or swapped — a new model version, a provider change, a fine-tuning update — the vector space it produces shifts: distances and similarity relationships that held under the old model don't hold the same way under the new one, so old embeddings computed with the previous model and new embeddings computed with the current model are no longer meaningfully comparable, even though they're stored in the same index and queried together as if they were. Retrieval quality degrades in a way that has nothing to do with the content of the memories themselves, purely because the "ruler" used to measure similarity changed without the stored data being re-measured against it.

**Frequency**: Occasional

**Symptoms**
- Retrieval quality drops noticeably right after an embedding model upgrade, with no change to the underlying stored content
- Older records (embedded with the previous model) are systematically under- or over-retrieved relative to newer records embedded with the current model
- Similarity scores between a fresh query embedding and old-model record embeddings look arbitrary or uniformly lower than expected
- Re-embedding the entire store with the new model resolves the degradation, confirming the mismatch was the cause
- Issue is easy to miss initially because the index doesn't distinguish which model produced which vector, so the mixed-version state isn't visible without explicit auditing

## Root Cause
Embedding models define a vector space through their training process, and different models — even different versions of the same model family — produce vector spaces with different geometry: what counts as "close" or "far," the effective dimensionality of meaningful variation, and the absolute scale of distances are all specific to a given model. Comparing a vector produced by model A to a vector produced by model B via cosine similarity or dot product is not a well-defined operation in the way comparing two model-A vectors is — the numbers can still be computed and will still produce a score, but that score doesn't correspond to any meaningful semantic relationship, since the two vectors live in spaces that were never aligned to each other. When a memory store upgrades its embedding model for new writes but doesn't re-embed the existing corpus, the index silently becomes a mix of two (or more) incompatible vector spaces being queried and compared as if they were one, with no structural signal indicating which vectors belong to which space.

## Example
```
A memory store has been running on Embedding-Model-v1 for 18
months, accumulating 2.1M records. The team upgrades to
Embedding-Model-v2 for improved quality on new content, but the
migration only applies to new writes going forward — re-embedding
the full 2.1M-record backlog is deferred as a "later" cleanup task
due to cost.

Post-upgrade, incoming queries are embedded with v2. Against the
~2.1M v1-embedded historical records, v2 query vectors produce
similarity scores that are systematically lower and less
semantically meaningful than they were pre-upgrade, because the
v1 vectors were never re-computed in v2's space — the comparison
is happening across two different, unaligned geometries.

Effect: historical records (18 months of accumulated organizational
knowledge) become dramatically harder to retrieve relative to the
small volume of new v2-embedded records, even for queries that are
directly and obviously relevant to that older content. An agent
asked about a well-documented incident from 8 months ago returns
"no relevant information found," not because the information isn't
there, but because its v1 embedding no longer meaningfully compares
against the v2 query embedding now being used to search for it.
```

## Statistics
| Finding | Context |
|---------|---------|
| Similarity scores between embeddings from different model versions are typically not meaningfully comparable, even when both are normalized to the same dimensionality | Typical property of independently-trained embedding models |
| Retrieval recall on historical content commonly drops sharply immediately following an embedding model upgrade when the existing corpus is not re-embedded | Reported pattern across teams upgrading embedding models without full re-indexing |
| Full corpus re-embedding after a model upgrade is a common but frequently deferred remediation, due to the compute/cost of re-processing large historical stores | Typical pattern across teams managing large legacy memory stores |

## Mitigations
1. **Full re-embedding on model upgrade**: Treat an embedding model change as requiring a full re-index of the existing corpus, not just a change applied to new writes going forward, and budget for the compute cost accordingly.
2. **Model-version tagging**: Tag every stored vector with the embedding model/version that produced it, so mixed-version states are visible and queryable, rather than silently indistinguishable.
3. **Dual-index transition period**: During migration, maintain separate indexes per embedding model version and query both (merging results with awareness of the version mismatch) rather than mixing vectors from different models in one index.
4. **Staged rollout with recall monitoring**: Roll out a new embedding model gradually, monitoring retrieval recall specifically on historical content, and halt/rollback if recall on old content degrades before re-embedding completes.
5. **Compatibility validation before adoption**: Before adopting a new embedding model, explicitly test whether it's designed to be comparable with the prior model's vector space (some model families guarantee this, most don't), rather than assuming compatibility.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| mixed_version_index_fraction | Fraction of a queried index composed of vectors from a different embedding model version than the current query embedder | Alert if > 0% sustained beyond a planned migration window |
| historical_content_recall | Retrieval recall specifically on records embedded with a prior model version, measured post-upgrade | Alert if drops > 20% relative to pre-upgrade baseline |
| re_embedding_backlog_size | Count of records still awaiting re-embedding after a model upgrade | Alert if backlog persists beyond the planned migration timeline |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Recall regression after model upgrade | historical_content_recall drops sharply following an embedding model change | High | Prioritize re-embedding backlog, consider temporary dual-index query strategy |
| Unplanned mixed-version index | mixed_version_index_fraction remains nonzero well past the intended migration window | Medium | Schedule and complete full corpus re-embedding |

## Related Patterns
- [Retrieval Index Corruption](./retrieval-index-corruption.md) - both degrade retrieval broadly across the index, though drift is a semantic/geometric mismatch rather than structural damage
- [Retrieval Confidence Miscalibration](./retrieval-confidence-miscalibration.md) - a mixed-version index makes similarity scores even less reliable as a usefulness signal, compounding existing miscalibration
- [Memory Fragmentation](./memory-fragmentation.md) - a deferred full re-embedding, like deferred consolidation, leaves the store in a degraded intermediate state that compounds the longer it's postponed
