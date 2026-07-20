# Memory Fragmentation

## Issue
As a memory store accumulates entries over months of operation — many small, partial, or redundant writes rather than clean consolidated records — the store fragments: the same underlying fact ends up spread across dozens of small entries, indexes grow disproportionately to the useful information they contain, and retrieval has to search, rank, and merge far more candidate records than the actual amount of distinct information warrants. Retrieval latency climbs and result quality drops, not because any single record is wrong, but because the signal is scattered across so many fragments that ranking and top-k selection can no longer reliably surface the most complete or relevant one.

**Frequency**: Common

**Symptoms**
- Retrieval latency grows over time for the same store even though query patterns haven't changed
- The same fact appears split across multiple small memory entries, none of which is individually complete
- Top-k retrieval returns several partial/overlapping fragments of one fact instead of one complete record
- Index size grows substantially faster than the count of genuinely distinct facts being stored
- Periodic reindex or compaction jobs produce large size reductions, indicating heavy fragmentation had accumulated

## Root Cause
Agents typically write to memory incrementally — a new observation, a small correction, a follow-up detail — and most memory systems default to appending a new record rather than locating and merging into an existing one, because merge logic (finding the right existing record, deciding how to combine fields, handling conflicts) is significantly harder to implement correctly than an append-only insert. Over time this produces many small, overlapping records referring to the same entity or fact. Vector and inverted indexes are built assuming a reasonably compact set of high-quality records; when the true information content is diluted across far more records than necessary, the index itself bloats (more vectors to search, more postings to scan) and ranking algorithms — which weren't designed to recognize "these five fragments are really one fact" — spread relevance score across the fragments instead of concentrating it, degrading top-k precision.

## Example
```
Over 6 months, an agent writes memory about a single enterprise
account across 47 separate small entries as different conversations
touch on it:
  "Account uses SSO" / "Account SSO provider is Okta" /
  "Confirmed Okta SSO, renewed contract" / "SSO integration verified
  working" / "Okta SSO, contract renewal Q3" / ... (42 more variants)

None of these entries is wrong, but they are all fragments of the
same underlying fact ("Account X uses Okta SSO, contract renewed Q3").

Query: "What's this account's SSO setup?"

Retrieval returns the top 10 by similarity score, all fragments of
the same fact phrased slightly differently, none containing the
combination of details (provider + verification status + renewal)
that a single consolidated record would have held. The agent
picks one fragment, omits the renewal detail entirely because it
scored just below the top-10 cutoff, and gives an incomplete answer
despite the information technically being present in the store.

Separately, index search latency for this account's memory space
has grown from ~40ms to ~310ms over the same period as fragment
count grew from roughly 5 to 47 for what is, in substance, one fact.
```

## Statistics
| Finding | Context |
|---------|---------|
| Memory stores using pure append-on-write without periodic consolidation typically show entry counts growing several times faster than genuinely distinct fact counts over long operational periods | Typical range observed in long-lived, incrementally-updated memory stores |
| Retrieval latency in fragmented indexes commonly increases multiple-fold over months of unconsolidated growth for otherwise stable query volume | Typical range from index-size-driven latency scaling |
| Periodic consolidation/compaction passes on fragmented stores routinely reduce record count by half or more while improving top-k precision | Reported range across teams running scheduled memory consolidation |

## Mitigations
1. **Merge-on-write**: Before appending a new memory entry, check for an existing record about the same entity/fact and merge into it rather than defaulting to a new insert.
2. **Scheduled consolidation passes**: Run a periodic job that clusters near-duplicate or fragment records (by entity, by semantic similarity) and merges them into consolidated records, archiving the fragments.
3. **Entity-keyed storage**: Where the domain allows, key memory records by a stable entity ID rather than by write event, so updates naturally overwrite/append to one record instead of creating a new one.
4. **Fragmentation metrics and budgets**: Track a fragmentation ratio (records per distinct entity) and trigger consolidation automatically when it crosses a threshold, rather than waiting for latency complaints.
5. **Retrieval-time fragment merging**: As a stopgap, have the retrieval layer detect when top-k results are near-duplicate fragments of the same entity and merge/summarize them into one result before returning to the agent.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| fragmentation_ratio | Ratio of stored records to estimated distinct entities/facts | Alert if > 5:1 without recent consolidation |
| retrieval_latency_p95 | 95th percentile retrieval latency for a given memory namespace | Alert if grows > 50% over a rolling 90-day window without query volume change |
| index_size_growth_rate | Rate of index size growth relative to rate of genuinely new information | Alert if index grows > 2x faster than distinct-entity count |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Fragmentation threshold exceeded | fragmentation_ratio crosses configured threshold for a namespace | Medium | Schedule consolidation pass for affected namespace |
| Latency degradation from index bloat | retrieval_latency_p95 trend correlates with unconsolidated index growth | Medium | Trigger consolidation, review merge-on-write coverage |

## Related Patterns
- [Retrieval Deduplication Failure](./retrieval-deduplication-failure.md) - a closely related symptom where near-duplicate entries clutter individual query results, often the visible surface of underlying fragmentation
- [Retrieval Index Corruption](./retrieval-index-corruption.md) - both degrade retrieval quality/performance at the index level, though corruption is structural damage rather than accumulated bloat
- [Memory Summarization Lossy](./memory-summarization-lossy.md) - consolidation to fix fragmentation risks the same information-loss failure mode if merge logic is too aggressive
