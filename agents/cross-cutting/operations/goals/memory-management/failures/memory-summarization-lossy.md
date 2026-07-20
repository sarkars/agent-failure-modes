# Memory Summarization Lossy

## Issue
When long-term memory is compacted to fit a fixed storage or retrieval-token budget — a periodic "condense this user's history into a compact profile" job, rather than the cascading multi-pass summarization that produces summary drift — the single compaction pass must decide what to keep and what to discard under that budget, and it systematically drops details that appear low-value at compaction time but turn out to be exactly what a later query needs. Unlike summary drift, where quality degrades across repeated re-summarization cycles, this is a one-time, budget-driven compression choice: the loss happens once, at the moment of compaction, because the summarizer has no way to know in advance which details a future query will actually require.

**Frequency**: Very Common

**Symptoms**
- A specific, later-needed detail (an exact date, a stated exception, a one-off preference) is missing from the compacted memory even though it was present in the pre-compaction source
- The compacted summary reads as reasonable and complete in isolation, giving no indication anything was dropped
- Retrieval against compacted memory answers general queries fine but fails on queries about specific edge cases or exceptions
- The gap is only discovered when a user references something "you already know" that isn't in the compacted record
- Re-running compaction with a larger budget recovers the missing detail, confirming it was a budget-driven omission, not a source-data gap

## Root Cause
Compaction to a token or storage budget is fundamentally a selection problem under uncertainty: the summarizer has to decide, at the moment of compaction, which facts are worth keeping within a fixed size, but it cannot know which future query will need which specific detail. Summarization prompts and heuristics naturally favor generalizable, frequently-relevant information (stated preferences, recurring patterns) over specific, low-frequency details (a one-time exception, an exact figure mentioned once) because the former looks more "important" by any generic salience heuristic, even though the latter is often precisely what a future targeted query is about. Once the pre-compaction source is deleted or archived beyond easy reach (as is typical, since the whole point of compaction is to reduce what's retained), the omission becomes permanent and unrecoverable through retrieval, even though it was a reasonable-looking compression decision in isolation.

## Example
```
Pre-compaction source: 40 stored interaction records for a client
account, including:
  - 34 routine records: general communication preferences, standard
    scheduling patterns, typical order sizes
  - 1 record from 8 months ago: "Client noted a one-time exception:
    for the annual Q4 order only, ship to the secondary warehouse
    address (1442 Dockside Ave) instead of the default, due to a
    seasonal staffing gap at the primary site."
  - 5 other minor one-off notes

Compaction job runs with a 500-token budget for this account's
profile, prioritizing information judged broadly relevant:

Compacted profile: "Client prefers email communication, typically
orders in Q2 and Q4, standard order size 200-400 units, prefers
morning delivery windows." (the Q4 shipping-address exception,
being a single low-frequency note, does not make the cut)

Six months later, during Q4 order processing, an agent queries the
compacted memory for shipping instructions, finds nothing about a
secondary warehouse, and ships to the default address — resulting
in the exact seasonal misdelivery the original note existed to
prevent, because the fact was compacted away as a
minor detail relative to the 34 more "typical" records.
```

## Statistics
| Finding | Context |
|---------|---------|
| Budget-constrained compaction passes typically retain the majority of high-frequency/generalizable facts but a much smaller share of low-frequency, specific exceptions from the same source | Typical pattern for salience-driven summarization under a fixed budget |
| A meaningful share of "the agent should have known this" incidents in production trace back to a fact that existed pre-compaction but was dropped during a budget-constrained summarization pass | Reported pattern across teams auditing compacted-memory failures |
| Tagging specific categories of fact (exceptions, one-time overrides, safety-relevant notes) as protected from compaction removes the large majority of these incidents in comparative testing | Estimated from before/after adoption of protected-fact tagging |

## Mitigations
1. **Protected fact categories**: Tag categories of information (exceptions, overrides, safety-relevant notes, anything explicitly marked important by a user) as exempt from budget-driven compaction, keeping them in full regardless of frequency-based salience scoring.
2. **Structured fact extraction alongside prose compaction**: Extract discrete, queryable facts (key-value pairs) separately from the compressed narrative summary, so specific details survive even if the prose summary generalizes over them.
3. **Retain raw source for a grace period**: Keep the pre-compaction source retrievable (archived, not deleted) for a defined window after compaction, so a targeted query that misses in the compacted profile can fall back to the raw record before it's truly gone.
4. **Query-aware retention hints**: Where feasible, use observed query patterns to inform what future compaction passes should prioritize retaining, rather than relying solely on a generic salience heuristic blind to actual usage.
5. **Compaction diff review**: For high-value accounts/entities, surface a diff of what was dropped during compaction for lightweight human review before the source is fully discarded, catching high-risk omissions before they become unrecoverable.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| post_compaction_recall_rate | Fraction of pre-compaction facts still answerable from the compacted profile, measured via sampled probe queries | Alert if < 85% |
| protected_fact_drop_count | Count of facts tagged as protected that were nonetheless dropped during a compaction pass | Alert if > 0 |
| exception_note_survival_rate | Fraction of tagged one-time-exception notes retained through compaction | Alert if < 100% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Protected fact dropped during compaction | A fact tagged as protected is missing from the post-compaction profile | High | Restore from pre-compaction source, review compaction logic for the protected-tag handling gap |
| Recall regression after compaction | post_compaction_recall_rate for an account drops below threshold after a compaction run | Medium | Review compaction budget/prompt, consider raising budget for the affected account |

## Related Patterns
- [Summary Drift](./summary-drift.md) - the cascading, multi-cycle version of information loss, versus this pattern's single budget-driven compaction pass
- [Compaction Information Loss](./compaction-information-loss.md) - a closely related pattern focused on age/frequency-based deletion policies rather than summarization-driven compression choices
- [Memory Fragmentation](./memory-fragmentation.md) - the opposite failure mode in the same lifecycle stage: too little consolidation causing bloat, versus too much consolidation causing information loss
