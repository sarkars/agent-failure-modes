# Knowledge Expiration Not Enforced

## Issue
A knowledge base or cache stores facts indefinitely with no time-to-live (TTL) or expiration mechanism, so content that was accurate at ingestion time but has a known or implicit shelf life (prices, policies, personnel, regulatory limits) remains fully retrievable and presented with the same confidence as current content, indefinitely, unless someone manually removes or updates it. This is a systems-level gap rather than a per-fact error: the architecture itself has no concept of "this should stop being trusted after time T."

**Frequency**: Very Common

**Symptoms**
- Facts retrieved and presented as current turn out to be years old with no active flag or downgrade
- No expiration date, TTL, or staleness score exists anywhere in the storage or retrieval layer's schema
- Content removal or correction happens only through manual, ad hoc intervention rather than automatic lifecycle management
- Old and new versions of the same fact coexist in the index indefinitely, both retrievable, with no automatic deprecation of the old one

## Root Cause
Most knowledge base and retrieval-augmented-generation architectures are built around an ingest-and-index model optimized for growing a corpus, not for managing its decay — there's no default expiration concept in the storage layer analogous to a cache TTL, because the system was designed to treat "more indexed content" as an unambiguous improvement. Without an explicit design decision to attach expiration metadata to content at ingestion and enforce it at retrieval time (excluding, downweighting, or flagging expired content), the system has no mechanism to distinguish month-old content from year-old content, and by default treats all indexed content as equally live regardless of how long it has actually been accurate.

## Example
```
A support knowledge base ingests a "current pricing" document when a
product launches. Eighteen months later, pricing has changed twice, and
new pricing documents have been added to the knowledge base alongside
the original — but the original was never marked expired or removed,
because the system has no expiration mechanism at all, only an
ever-growing index.

A support agent, asked about pricing, retrieves whichever pricing
document scores highest on semantic relevance to the specific phrasing
of the query. In this case it happens to be the original, 18-month-old
document, since its wording more closely matches the user's casual
phrasing than the newer documents' more formal language.

The agent quotes the original price to a customer, who is later told
at checkout that the price is significantly higher, and escalates a
complaint that the support agent gave them "official" pricing
information that turned out to be obsolete.
```

## Statistics
| Finding | Context |
|---------|---------|
| Knowledge bases without TTL/expiration enforcement retain an estimated 30-50% of ingested content well past its practical accuracy window (e.g. pricing, personnel, time-bound policy) within 18-24 months of initial launch | Estimated from content-audit studies of long-running production knowledge bases |
| Retrieval of expired-but-unflagged content occurs at a rate roughly proportional to the fraction of the index that has gone stale, since ranking treats it identically to current content | Typical pattern observed in RAG system content audits |
| Adding TTL-based expiration and downweighting reduces stale-content retrieval substantially, with the largest gains coming from content categories with short natural shelf life (pricing, staffing, promotions) | Reported range across teams that added expiration enforcement |

## Mitigations
1. **Category-based default TTLs**: Assign default expiration windows at ingestion based on content category (e.g. 30 days for pricing/promotions, 12 months for general policy, no expiration for stable reference material), rather than treating all content as permanent by default.
2. **Automatic deprecation on new-version ingestion**: When a new version of a document is ingested, automatically mark prior versions as expired/deprecated rather than leaving them indefinitely coexisting and retrievable at equal rank.
3. **Retrieval-time expiration filtering**: Enforce expiration at query time — exclude or heavily downweight expired content from retrieval results by default, surfacing it only when a query is explicitly historical.
4. **Staleness-score decay**: For content without a hard expiration date, apply a continuous staleness score that decays relevance/ranking weight over time since last verification, rather than a binary expired/not-expired flag.
5. **Periodic re-verification workflow**: For content near its TTL, route it to a re-verification workflow (automated check against source-of-truth systems, or human review) that either renews, updates, or formally expires it, rather than letting TTLs lapse silently.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| unexpired_stale_content_share | Share of indexed content past its category's typical accuracy window with no expiration/staleness flag | Alert if > 20% |
| expired_content_retrieval_rate | Rate at which expired or superseded content is still returned in top retrieval results | Alert if > 2% |
| ttl_coverage | Share of indexed content with a defined TTL or staleness-scoring policy applied | Alert if < 90% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Expired content served in high-stakes response | Review confirms a response used content past its TTL for pricing/policy/regulatory information | High | Remove or downweight the expired content, verify deprecation-on-new-version logic fired correctly |
| TTL coverage drop | ttl_coverage falls below threshold after a content-ingestion pipeline change | Medium | Audit ingestion pipeline for missing TTL assignment on newly added content |

## Related Patterns
- [Knowledge Update Lag](./knowledge-update-lag.md) - a related but distinct mechanism: this pattern is the absence of any expiration system, that one is a delay in an existing update pipeline
- [Fact Timestamp Error](./fact-timestamp-error.md) - the per-fact symptom that unenforced expiration at the system level makes systematically likely
- [Knowledge Version Mismatch](./knowledge-version-mismatch.md) - unexpired old-version content is a common direct cause of version-mismatch errors
