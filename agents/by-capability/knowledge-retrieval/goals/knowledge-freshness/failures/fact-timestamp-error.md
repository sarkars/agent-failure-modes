# Fact Timestamp Error

## Issue
An agent retrieves a fact that was true during a specific window of time and applies it outside that window, because the fact's temporal validity period was mishandled — the agent misattributes when the fact was true, or fails to notice that the fact is now outside its valid period. Unlike a stale cache issue, this is specifically about misreading or mismanaging the time-scoping of the fact itself: applying a 2019 regulatory limit as though it were still current in 2026, or applying a "current" fact to a past scenario the user is actually asking about.

**Frequency**: Common

**Symptoms**
- Agent states a fact as currently true when its source explicitly ties it to a past (or future) date or period
- Agent applies a fact to the wrong time period when the user's query is about a specific historical or future point in time
- No check exists comparing a fact's documented validity window against the current date or the query's implied time reference
- Errors increase for facts sourced from documents with an effective date, superseded version, or "as of" marker that isn't carried into the response

## Root Cause
Facts about policies, rates, prices, and regulations are frequently valid only within a bounded time window, and that window is usually expressed as metadata (an effective date, a "supersedes" note, a version number) separate from the fact's main textual content. Retrieval systems that index and rank primarily on topical relevance don't necessarily preserve or check this temporal metadata against the current date or the query's implied time frame, so a fact retrieved because it's the best topical match can still be outside its valid window without the system noticing — the topical match and the temporal match are two independent checks, and only the first is commonly enforced.

## Example
```
A knowledge base contains two versions of a tax bracket document: one
effective for tax year 2023 and a newer one effective for tax year
2025, each tagged with its effective period but stored as separate,
similarly-titled documents.

A user in 2026 asks a tax-assistance agent about the current bracket
thresholds. Retrieval matches the 2023 document as the top result
(strong topical similarity to the query, and the document happens to
have accumulated more historical references pointing to it), and the
agent reports the 2023 thresholds as current, with no timestamp check
against the current date or against the newer 2025 document sitting
in the same knowledge base.

The user files based on outdated thresholds and later needs to amend
after discovering that the referenced bracket applied to a tax year
that closed three years earlier.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 10-20% of retrievals for facts with documented effective-date metadata surface a version outside its intended validity window | Estimated from temporal-metadata audits of versioned regulatory/pricing knowledge bases |
| Retrieval systems that rank purely on topical similarity, without a temporal-validity filter, show markedly higher timestamp-error rates than systems that filter or boost by effective-date recency | Typical pattern observed in comparative retrieval-architecture evaluation |
| Adding an explicit current-date-vs-validity-window check at retrieval time eliminates the large majority of these errors in tested systems | Reported range across teams that added temporal-validity filtering |

## Mitigations
1. **Effective-date metadata enforcement**: Require every versioned or time-bound fact to carry explicit effective-start and effective-end metadata, and filter or heavily penalize retrieval results whose validity window doesn't cover the current date (or the query's implied reference date).
2. **Superseded-version deprecation**: When a newer version of a time-bound document is ingested, explicitly mark prior versions as superseded and exclude them from default retrieval, surfacing them only when the query is explicitly historical.
3. **Query-time-reference detection**: Detect when a user's query implies a specific time reference (a past tax year, a future effective date) and match retrieval to that specific period rather than defaulting to "most topically relevant" regardless of time.
4. **Explicit "as of" statement in output**: Require every time-bound fact in a response to state the period it applies to, making a timestamp error immediately visible to the user rather than silently presented as current.
5. **Automated validity-window audit**: Periodically scan the knowledge base for facts whose effective-end date has passed without a corresponding newer version being ingested, flagging gaps for content-team follow-up.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| validity_window_match_rate | Share of retrieved time-bound facts whose effective window covers the current date or query's implied reference date | Alert if < 95% |
| superseded_version_retrieval_rate | Rate at which a superseded document version is retrieved instead of its current replacement | Alert if > 2% |
| timestamp_error_correction_rate | Rate of expert/user corrections identifying a fact applied outside its valid time period | Track trend; alert on sustained increase |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Superseded fact presented as current | Review confirms a response stated an outdated, superseded fact as currently valid | High | Correct the response, verify superseded-version deprecation is applied to the source document |
| Validity window match rate drop | validity_window_match_rate falls below threshold after a re-indexing or retrieval-ranking change | Medium | Review recent ranking changes for loss of temporal-validity filtering |

## Related Patterns
- [Knowledge Update Lag](./knowledge-update-lag.md) - a systemic version of this failure, where the whole knowledge base lags rather than a single fact being time-misapplied
- [Knowledge Temporal Context Lost](./knowledge-temporal-context-lost.md) - closely related; this pattern is the retrieval-time mismatch, that one is the generation-time stripping of "as of" framing
- [Knowledge Version Mismatch](./knowledge-version-mismatch.md) - the product/policy-version analog of the same time-scoping mechanism
