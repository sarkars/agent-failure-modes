# Retrieval Deduplication Failure

## Issue
A memory store accumulates near-duplicate entries — the same fact stated slightly differently across multiple writes, or the same document ingested more than once — and the retrieval layer has no deduplication step, so a single query returns several near-identical results occupying multiple slots in a limited top-k result set. Instead of surfacing k genuinely distinct, useful pieces of information, the agent receives k-minus-several redundant restatements of the same one or two facts, wasting context budget and pushing genuinely different, useful candidates below the cutoff.

**Frequency**: Common

**Symptoms**
- Top-k retrieval results contain multiple near-identical entries differing only in phrasing or timestamp
- Effective information diversity in a retrieval result is much lower than the requested top-k count suggests
- A genuinely distinct, relevant fact is missing from results because near-duplicates of a more frequently-restated fact crowded it out of the cutoff
- Context budget is spent re-stating the same fact multiple times rather than covering the query's full information need
- Increasing top-k doesn't proportionally increase useful information, because additional slots are filled with more duplicates rather than new facts

## Root Cause
Deduplication requires an explicit similarity-clustering step at write time or query time — recognizing that two differently-phrased records refer to the same underlying fact is a nontrivial judgment call (how similar is similar enough to count as a duplicate versus a meaningfully distinct update), and most retrieval pipelines skip it because a simple top-k-by-similarity-score query is far simpler to implement and by default returns whatever the k nearest vectors happen to be — which, when a fact has been restated many times, are disproportionately likely to be near-duplicates of each other rather than a diverse set of the k most useful distinct facts. Without an explicit diversity or novelty constraint applied after initial candidate retrieval, the ranking function optimizes purely for individual-result relevance and has no mechanism to penalize redundancy across the result set as a whole.

## Example
```
Memory store contains, among others:
  "User is based in the Pacific timezone" (stored month 1)
  "User confirmed PST timezone for scheduling" (stored month 3)
  "User's timezone: Pacific (PST/PDT)" (stored month 5)
  "User mentioned they're in California, PT" (stored month 6)
  "User's actual dietary restriction: gluten-free, diagnosed
   celiac" (stored month 2, the only mention of this fact)

Query: "What do we know about this user that's relevant to
scheduling a meeting and planning catering?"

Top-5 retrieval by raw similarity (no deduplication) returns all
four timezone-related restatements (all score similarly high
against a scheduling-flavored query) and drops the gluten-free/
celiac record entirely, since it scores lower on the scheduling-
flavored query embedding despite being highly relevant to the
catering half of the question.

Agent response covers timezone thoroughly (redundantly) and
recommends a generic catering menu, missing the celiac dietary
restriction entirely — not because the fact wasn't in memory,
but because four near-duplicate restatements of a less relevant
fact occupied 4 of the 5 available result slots.
```

## Statistics
| Finding | Context |
|---------|---------|
| Memory stores without deduplication typically show top-k retrieval results containing a meaningful fraction of near-duplicate entries once a store has accumulated months of incremental writes about the same entities | Typical pattern in long-lived, non-deduplicated stores |
| Effective information diversity (distinct facts per k results) in non-deduplicated retrieval commonly falls well short of the nominal k, especially for frequently-restated facts | Reported pattern across teams measuring retrieval result diversity |
| Adding a diversity-aware reranking or clustering step after initial candidate retrieval measurably increases the count of genuinely distinct facts surfaced per query, in comparative evaluation | Estimated from before/after adoption of dedup-aware reranking |

## Mitigations
1. **Write-time deduplication/merge**: Before inserting a new memory entry, check for a highly similar existing entry and merge into it rather than inserting a new near-duplicate record.
2. **Diversity-aware reranking (MMR-style)**: After initial candidate retrieval, apply a diversity-promoting reranking step (e.g. maximal marginal relevance) that penalizes near-duplicate results relative to what's already selected, rather than ranking purely by individual relevance score.
3. **Cluster-then-sample retrieval**: Cluster candidate results by semantic similarity and sample the top result from each cluster, rather than taking the raw top-k, so distinct clusters of information are represented instead of one cluster dominating.
4. **Canonical fact consolidation**: For frequently-updated facts (preferences, status), maintain a single canonical record that overwrites on update, rather than allowing indefinite accumulation of restatements.
5. **Redundancy monitoring**: Periodically measure the duplicate rate within top-k results for representative queries, and treat a rising rate as a signal to run a consolidation/deduplication pass.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| result_set_duplicate_rate | Fraction of top-k retrieval results that are near-duplicates of another result in the same set | Alert if > 20% |
| distinct_fact_coverage | Count of genuinely distinct facts represented in a top-k result set, relative to k | Alert if consistently < 60% of k |
| crowded_out_relevant_rate | Rate at which a genuinely relevant, distinct fact falls below the retrieval cutoff due to duplicate entries occupying higher-ranked slots | Alert if > 5% on sampled queries |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| High duplicate rate in results | result_set_duplicate_rate exceeds threshold for a given namespace | Medium | Trigger consolidation/dedup pass, review write-time merge logic |
| Relevant fact crowded out | A known-relevant fact for a benchmark query falls below cutoff due to duplicate entries ranking above it | Medium | Add diversity-aware reranking, consolidate the crowding duplicates |

## Related Patterns
- [Memory Fragmentation](./memory-fragmentation.md) - the broader storage-level pattern (many small overlapping records) that produces the duplicate candidates this pattern fails to filter out at retrieval time
- [Retrieval Confidence Miscalibration](./retrieval-confidence-miscalibration.md) - duplicate high-scoring results compound miscalibration by making the score distribution even less informative about true usefulness
- [Memory Summarization Lossy](./memory-summarization-lossy.md) - consolidating duplicates via summarization risks trading one failure (redundancy) for another (dropped detail) if not done carefully
