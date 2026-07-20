# Retrieval Temporal Ordering Failure

## Issue
Retrieval ranks results primarily or purely by semantic similarity to the query, with no explicit weighting for recency, so when a memory store contains both an older fact and a newer fact that supersedes it, the older one can outrank the newer one simply because it happens to phrase things in a way that scores higher against the query embedding. The agent then surfaces or acts on the stale result ahead of the current one, not because the current one is missing from the store, but because the ranking function that decided what to return never considered which one is actually more recent.

**Frequency**: Common

**Symptoms**
- Agent surfaces an older fact ahead of a newer, superseding fact that is also present in the store
- Query for "current status of X" returns a historical status update rather than the latest one
- Behavior appears inconsistent: sometimes the recent fact is surfaced, sometimes the old one, depending on subtle query phrasing differences that shift similarity scores
- Explicitly filtering or sorting by timestamp after retrieval fixes the issue, confirming the ranking function itself ignores recency
- Problem worsens for entities with a long history of updates, where more old candidates compete for top-k slots against the single current one

## Root Cause
Standard similarity-based retrieval treats every stored record as an independent, timeless candidate to be scored purely on textual/semantic closeness to the query; nothing in a cosine-similarity or dot-product score encodes when the record was written or whether it has since been superseded by another record about the same entity. Two records about the same fact, written months apart, can have similarity scores that differ only slightly, and that slight difference is driven by wording, not recency — an older, more generically-phrased record can easily out-score a newer, more specifically-phrased one. Without an explicit recency term or supersession relationship folded into ranking (or a preprocessing step that resolves conflicts before retrieval), similarity search has no way to know that among several candidate matches, only the most recent one is the "true current" answer.

## Example
```
Memory store, project status updates for "Project Falcon":
  "Project Falcon status: on track, targeting Q3 launch"
    (stored 5 months ago) — similarity to query: 0.83
  "Project Falcon status: delayed to Q1 next year due to
   vendor issue" (stored 2 weeks ago) — similarity to
   query: 0.79

Query: "What's the status of Project Falcon?"

Top-1 retrieval by raw similarity returns the 5-month-old "on
track, Q3" record (0.83 > 0.79), because its phrasing happens to
echo the query's generic "status" framing more closely than the
newer record's more specific delay explanation.

Agent tells a stakeholder preparing a quarterly report: "Project
Falcon is on track for a Q3 launch" — directly contradicting the
actual current status, which was in the memory store the entire
time but ranked second because recency was never part of how
the two candidates were scored against each other.
```

## Statistics
| Finding | Context |
|---------|---------|
| Pure similarity-based ranking without a recency term shows a measurable rate of returning a superseded record ahead of its more current counterpart, for entities with multiple historical updates | Typical pattern observed in retrieval evaluations on time-varying facts |
| Adding an explicit recency-decay or supersession-boost term to ranking measurably reduces stale-result-ranked-first incidents in comparative evaluation | Estimated from before/after adoption of recency-aware ranking |
| The rate of this failure increases with the number of historical updates an entity has accumulated, since more old candidates compete against the single current record | Typical pattern for entities with long update histories |

## Mitigations
1. **Recency-weighted scoring**: Fold a recency term (time-decay function) into the ranking score alongside semantic similarity, so newer records are boosted relative to older ones about the same entity.
2. **Supersession tracking**: Explicitly mark records as superseding a prior record about the same fact/entity, and filter or demote superseded records at query time rather than relying on similarity score alone to sort them out.
3. **Entity-scoped latest-wins retrieval**: For time-varying facts scoped to a specific entity (status, price, assignment), retrieve the single latest record per entity directly rather than doing open-ended similarity search across all historical versions.
4. **Time-aware query understanding**: Detect when a query is asking about "current" or "latest" state (versus historical) and apply stronger recency weighting or filtering specifically for those queries.
5. **Periodic archival of superseded records**: Move fully superseded historical records out of the primary retrieval-facing index into a separate archive, so they can't compete for top-k ranking against current records at all.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| stale_result_ranked_first_rate | Rate at which a superseded record outranks its more current counterpart in top-1 retrieval | Alert if > 5% on sampled time-varying-fact queries |
| recency_score_contribution | Measured contribution of recency to final ranking score, to verify it's non-zero for time-sensitive namespaces | Alert if near-zero for entities with known update history |
| current_status_query_accuracy | Accuracy of "current status" style queries against a benchmark set with known-current answers | Alert if < 90% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Stale record surfaced ahead of current | A query returns a superseded record ranked above its known-current counterpart | High | Apply recency boost or supersession filter, review affected entity's ranking behavior |
| Recency signal absent from ranking | Periodic audit finds recency has no measurable effect on ranking for a time-sensitive namespace | Medium | Add recency weighting to the ranking function for that namespace |

## Related Patterns
- [Retrieval Confidence Miscalibration](./retrieval-confidence-miscalibration.md) - temporal ordering failure is a specific, common instance of the broader problem that similarity score doesn't track actual usefulness
- [Memory Not Updated Stale Retrieval](./memory-not-updated-stale-retrieval.md) - both surface an outdated fact, though this pattern is a ranking-logic gap rather than an indexing-lag gap
- [Context Refresh Stale State](./context-refresh-stale-state.md) - both involve the agent trusting an apparently-current result that is actually outdated relative to a more recent truth
