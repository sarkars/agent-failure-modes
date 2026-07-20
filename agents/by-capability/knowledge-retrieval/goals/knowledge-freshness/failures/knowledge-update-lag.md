# Knowledge Update Lag

## Issue
The system of record that an agent's knowledge base is supposed to reflect has been updated — a policy changed, a price changed, a product was discontinued — but the agent's indexed or cached copy has not caught up, because the ingestion/re-indexing pipeline runs on a cadence (scheduled batch job, manual trigger, event-driven pipeline with a backlog) that lags behind the actual rate of change at the source. The agent isn't wrong about what its knowledge base says; its knowledge base itself is behind reality.

**Frequency**: Very Common

**Symptoms**
- Agent confidently states information that was accurate at last index time but has since changed at the source system
- The source-of-truth system shows a more recent update timestamp than the knowledge base's last successful sync
- Errors spike shortly after known high-change-frequency events (pricing updates, policy revisions, product launches) and taper as re-indexing catches up
- No visible warning to users that the knowledge base may be behind the live source

## Root Cause
Ingestion and indexing pipelines are typically built around a fixed cadence (nightly batch, weekly crawl) or an event-driven trigger that can itself queue up and lag under load, and there is usually no mechanism comparing the knowledge base's freshness against the actual rate of change at the source to detect when the pipeline has fallen behind. The gap is invisible from inside the system: the retrieval and generation layers have no way to know their indexed copy is stale, since staleness is a property of the relationship between the index and an external system, not something detectable by examining the index alone. Lag compounds when source systems change faster than expected (a policy revised twice in one month against a monthly re-index schedule) or when the ingestion pipeline itself develops a backlog that isn't actively monitored.

## Example
```
A company's support-agent knowledge base is re-indexed from the product
documentation system every 24 hours via a scheduled batch job. The
product team ships an urgent fix that also changes a previously-
documented workaround, updating the live documentation at 9am.

A customer contacts support at 2pm the same day and the support agent,
whose knowledge base won't re-index until the next overnight batch run,
retrieves and confidently recommends the now-outdated workaround that
was removed from the live documentation five hours earlier.

The customer follows the outdated advice, it doesn't resolve their
issue (since the underlying behavior changed with the fix), and they
escalate, at which point a human agent checking the live documentation
directly identifies the discrepancy between what the bot said and what
the current documentation actually states.
```

## Statistics
| Finding | Context |
|---------|---------|
| Knowledge bases on a 24-hour batch re-index cadence serve at least one materially outdated fact per high-change-frequency source in an estimated 5-10% of query-days | Estimated from freshness-lag audits of scheduled-batch RAG pipelines |
| Event-driven ingestion pipelines reduce average update lag substantially versus fixed-cadence batch jobs, but remain vulnerable to backlog buildup under load without active monitoring | Typical pattern observed in comparative ingestion-architecture evaluation |
| Adding explicit lag monitoring (comparing source-system last-modified timestamps against index last-sync timestamps) catches the large majority of significant lag incidents before they reach a meaningful number of user queries | Reported range across teams that added freshness-lag monitoring |

## Mitigations
1. **Freshness-lag monitoring**: Track the gap between each source system's last-modified timestamp and the knowledge base's last successful sync timestamp per document/source, and alert when the gap exceeds a domain-appropriate threshold.
2. **Change-frequency-aware re-index cadence**: Set re-indexing frequency per source based on its measured rate of change (near-real-time for pricing/inventory, daily for general documentation, weekly for stable reference material) rather than one fixed cadence for the whole knowledge base.
3. **Event-driven ingestion for high-volatility sources**: For sources known to change frequently or urgently (pricing, active incidents, safety-critical documentation), trigger re-indexing on source-system change events rather than waiting for the next scheduled batch.
4. **Backlog monitoring on ingestion pipelines**: Explicitly monitor the ingestion pipeline's queue depth and processing lag, not just whether it's "running," since a healthy-looking pipeline can still be silently falling behind under load.
5. **Staleness disclosure in responses**: Surface the knowledge base's last-sync timestamp for the relevant source alongside time-sensitive answers, so users and downstream systems can judge whether to independently verify.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| source_to_index_lag | Time gap between a source document's last-modified timestamp and its last successful re-index | Alert if > domain-specific threshold (e.g. 1 hour for pricing, 24 hours for general docs) |
| ingestion_backlog_depth | Number of pending updates queued but not yet processed by the ingestion pipeline | Alert if trending upward or exceeding a fixed depth threshold |
| stale_answer_correction_rate | Rate of expert/user corrections tracing an error to the knowledge base lagging a known source update | Track trend; alert on sustained increase |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| High-volatility source lag exceeded | source_to_index_lag for a tagged high-volatility source (pricing, active incident) exceeds its threshold | High | Trigger manual re-index, investigate ingestion pipeline health |
| Ingestion backlog growing | ingestion_backlog_depth increases over a sustained window without processing catching up | Medium | Scale ingestion pipeline capacity, investigate root cause of backlog |

## Related Patterns
- [Knowledge Expiration Not Enforced](./knowledge-expiration-not-enforced.md) - a related but distinct systemic gap: this pattern is the index lagging an actively-changing source, that one is the absence of any decay mechanism at all
- [Fact Timestamp Error](./fact-timestamp-error.md) - the per-fact symptom that update lag produces when a stale indexed fact is applied as though current
- [Knowledge Version Mismatch](./knowledge-version-mismatch.md) - update lag is a common direct cause of version mismatch, when the agent's cached version falls behind the source's current version
