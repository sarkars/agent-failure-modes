# Knowledge Source Reliability Unknown

## Issue
A retrieval system treats every indexed source as equally trustworthy, with no mechanism to weight or rank content by the reliability of where it came from — an official, reviewed policy document is retrieved and used with exactly the same confidence as an unreviewed wiki page, a stale forum post, or a low-quality scraped page, simply because both matched the query with similar semantic relevance. When sources disagree or vary in quality, the system has no basis for preferring the more trustworthy one.

**Frequency**: Very Common

**Symptoms**
- Low-quality or unofficial sources (forum posts, draft documents, informal notes) are cited with the same confidence as authoritative sources
- No metadata exists in the knowledge base distinguishing reviewed/official content from user-generated or unreviewed content
- When sources disagree, whichever scores marginally higher on semantic relevance wins, regardless of actual reliability
- Errors trace back to a technically-indexed but low-trust source that should have been deprioritized or excluded

## Root Cause
Semantic retrieval ranks by similarity between query and content, a signal that is completely orthogonal to how trustworthy or authoritative that content's origin is — a well-written forum comment can score just as high on relevance as an official policy document, sometimes higher if it uses more query-matching conversational phrasing. Building a trust/reliability signal requires explicit source-metadata modeling (who authored it, was it reviewed, how authoritative is the publishing venue) and a deliberate decision to factor that into ranking or filtering, which most retrieval pipelines don't include by default because it's an additional system to build and maintain on top of the relevance-ranking pipeline that ships out of the box.

## Example
```
A company's internal knowledge base indexes both its official,
legal-reviewed compliance handbook and an internal engineering wiki
where individual employees post informal notes and personal
interpretations of policy, including some outdated or simply incorrect
guesses about how a rule works.

An employee asks a policy agent about export control requirements for
a specific product category. The official handbook's relevant section
uses formal regulatory language that matches the query only loosely;
an engineer's wiki note, written in more casual, directly-matching
phrasing, scores higher on semantic relevance and is retrieved as the
top result. The wiki note contains a simplified and, in this case,
materially incorrect summary of the requirement.

The agent presents the wiki note's incorrect summary with the same
confident tone as it would use for authoritative content, since it has
no way to distinguish "official reviewed compliance guidance" from
"one engineer's informal, unreviewed note" — both are just text that
matched the query.
```

## Statistics
| Finding | Context |
|---------|---------|
| Knowledge bases mixing official and user-generated/informal content retrieve the lower-reliability source as the top result in an estimated 10-20% of queries where both are topically relevant | Estimated from source-reliability audits of mixed-authority enterprise knowledge bases |
| Errors traceable to low-reliability sources occur at a markedly higher rate in domains with active informal documentation cultures (engineering wikis, support forums) than in domains relying solely on centrally-published material | Typical pattern observed in mixed-source retrieval evaluation |
| Adding explicit source-reliability weighting to ranking (boosting official/reviewed content, downweighting unreviewed content) substantially reduces low-reliability-source-driven errors in tested systems | Reported range across teams that added reliability-weighted ranking |

## Mitigations
1. **Source-reliability metadata and weighted ranking**: Tag every indexed source with a reliability tier (official/reviewed, semi-official, user-generated/unreviewed) at ingestion time, and incorporate this tier as an explicit ranking factor alongside semantic relevance rather than relying on relevance alone.
2. **Authoritative-source override**: When an official/reviewed source and a lower-tier source both address the same question, default to the official source's content and either suppress the lower-tier content or present it explicitly as a secondary, less-authoritative note.
3. **Reliability-aware confidence framing**: When only lower-reliability sources are available for a query, have the response explicitly indicate the source's tier and hedge accordingly, rather than presenting all retrieved content with uniform confidence.
4. **Periodic low-reliability-source review**: Route content from unreviewed or user-generated sources through a lightweight review or flagging process before it's eligible for high-confidence retrieval, particularly for compliance-adjacent or safety-relevant topics.
5. **Source-tier-segmented indexes for high-stakes domains**: For domains where reliability matters most (compliance, safety, legal), maintain a separate, exclusively-official index that queries in those domains draw from by default, falling back to the broader mixed-reliability index only when no official source exists.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| reliability_tier_coverage | Share of indexed content with an assigned reliability tier | Alert if < 95% |
| low_tier_top_result_rate | Rate at which a low-reliability-tier source is the top retrieval result for queries where an official-tier source also matched | Alert if > 10% |
| unreliable_source_correction_rate | Rate of expert/user corrections tracing an error back to a low-reliability source that should have been deprioritized | Track trend; alert on sustained increase |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Unreliable source drove high-stakes error | Review confirms a compliance/safety/legal response relied on an unreviewed, low-tier source over an available official source | High | Correct the response, verify reliability-weighted ranking is active for the affected topic |
| Reliability tier coverage drop | reliability_tier_coverage falls below threshold after a new content-ingestion pipeline is added | Medium | Audit new ingestion source for missing reliability tagging |

## Related Patterns
- [Knowledge Contradiction Unresolved](./knowledge-contradiction-unresolved.md) - unknown source reliability is a primary reason contradictions can't be authoritatively resolved
- [Fact Source Confusion](./fact-source-confusion.md) - both stem from insufficient source-provenance handling, one for entity identity and one for trust weighting
- [Domain Best Practice Ignorance](./domain-best-practice-ignorance.md) - stale but formerly-authoritative content can itself become a lower-reliability source over time if currency isn't tracked
