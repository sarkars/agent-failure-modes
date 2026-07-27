# What Are the Most Common Retrieval Relevance Failures in AI Agents?

**Retrieval relevance fails when an agent selects a comparable or reference item using text-embedding similarity alone, and the selected item matches on language but not on the structured attributes (category, jurisdiction, tier, part specification) that actually determine whether it's a valid comparison.** The single documented pattern here, semantic-similarity-retrieval-misses-structural-attributes, shows the mismatch concentrating on items with generic or sparse text descriptions, since a thin description gives the embedding little signal beyond surface topic match — exactly the cases where structural verification matters most and is least likely to happen.

## Key Takeaways

- 1 pattern is documented here: [Semantic Similarity Retrieval Misses Structural Attributes](failures/semantic-similarity-retrieval-misses-structural-attributes.md), covering financial pricing benchmarks, drug interaction lookups, legal precedent retrieval, and supply-chain parts matching as domain instances of the same mechanism.
- The failure is not a ranking-quality problem — the retrieved item can have the single highest embedding similarity score in the corpus and still be structurally incompatible with what the query actually needs.
- Downstream systems that assume retrieval implies compatibility (a valuation model, a drug-safety check, a legal remedy recommendation, a parts-ordering system) inherit the mismatch silently, since nothing in a similarity score signals "structurally unrelated."
- The documented fix is a two-step retrieval order: match on structured attributes first, and fall back to text similarity only when structured matching is unavailable, rather than using similarity as the primary or sole signal.

## Scope

The single pattern here spans four illustrated domains — financial reference-instrument selection, drug-interaction lookup, legal precedent retrieval, and supply-chain parts matching — but all four are one mechanism: embedding similarity optimizes for textual resemblance, and textual resemblance is not the same signal as structural compatibility. A "revenue bond" description that resembles another "revenue bond" description in wording can still differ in duration and credit tier; an "Ibuprofen-analog compound" can share vocabulary with "Ibuprofen" while having zero actual safety data in common. No sub-clustering is needed for a single pattern.

## When Retrieval Relevance Matters

- A pipeline retrieves a comparable or reference item (a financial instrument, a legal precedent, a replacement part) and a downstream process assumes structural compatibility without an explicit verification step
- The corpus contains items with generic or sparse text descriptions, since that's exactly where the embedding signal has the least power to distinguish truly comparable items from superficially similar ones
- A domain has meaningful structured attributes — jurisdiction, category, tier, specification — that determine validity of a comparison but aren't reliably captured in the free-text description an embedding model reads

## Cross-Pattern Insight

The core lesson from the single documented pattern generalizes past its four illustrated domains: whenever a retrieval system's real correctness criterion is a structured attribute (jurisdiction, tier, specification, category) rather than the topic a passage discusses, similarity search should be treated as a fallback signal, not the primary match, and any similarity-based selection should be flagged for mandatory attribute verification before a downstream system treats it as compatible.

## Frequently Asked Questions

### What is the difference between retrieval relevance and retrieval quality failures?
[Retrieval Relevance](.) is specifically about structural-attribute mismatch hiding behind high textual similarity — the retrieved item is topically on point but structurally wrong. [Retrieval Quality](../retrieval-quality/) covers a broader set of ranking, chunking, and index-freshness failures where the retrieved item may be topically wrong, outdated, or poorly ranked for reasons unrelated to structural attributes.

### How do you detect a structural-attribute mismatch that a similarity score won't reveal?
Per [Semantic Similarity Retrieval Misses Structural Attributes](failures/semantic-similarity-retrieval-misses-structural-attributes.md), require items selected via similarity search to pass an explicit attribute-verification check (category, jurisdiction, tier match) before being used downstream, and flag items with sparse or generic descriptions for mandatory verification since they carry the least distinguishing signal.

### Can improving the embedding model fix structural-attribute mismatches?
No — a better embedding model still optimizes for textual resemblance, not structural correctness. The fix documented in the pattern is architectural: match on structured attributes first and use text similarity only as a fallback, rather than expecting a stronger embedding model to somehow learn jurisdiction or tier compatibility from prose alone.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Semantic Similarity Retrieval Misses Structural Attributes](failures/semantic-similarity-retrieval-misses-structural-attributes.md) | Embedding similarity matches on textual resemblance while structured attributes (category, jurisdiction, tier) that determine true compatibility go unchecked |

**Total: 1 pattern**

## Related Goals

- [Retrieval Quality](../retrieval-quality/) — broader ranking, chunking, and freshness failures beyond structural-attribute mismatch
- [Retrieval](../retrieval/) — the underlying recall/precision and corpus-selection failures that structural mismatch compounds on top of
- [Knowledge Freshness](../knowledge-freshness/) — the scope-assumption patterns there (jurisdiction, version) share the same "wrong scope, right topic" shape as retrieval relevance's structural-attribute mismatch
