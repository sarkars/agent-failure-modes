# Domain Best-Practice Ignorance

## Issue
An agent retrieves and applies information that was once the accepted best practice in a domain but has since been superseded by an evolved standard, even though the underlying fact is still technically true. The agent's knowledge source (a fine-tuned model, a static knowledge base, or a cached document set) captured the practice at a point in time and was never re-indexed against the field's current consensus, so the agent confidently recommends an approach that a current practitioner would flag as outdated. The advice isn't factually wrong in isolation — it's wrong relative to what the domain now considers correct.

**Frequency**: Common

**Symptoms**
- Agent recommendations get pushback from domain experts as "that's not how we do it anymore"
- Advice matches training-era documentation but contradicts current style guides, protocols, or standards
- No distinction in agent output between "historically valid" and "currently recommended"
- Users following agent guidance run into friction with modern tooling, reviewers, or regulators who expect newer conventions

## Root Cause
Best practices in fast-moving domains (security, medicine, software engineering, compliance) are a moving target that isn't captured by "is this fact true" — it's captured by "is this the currently endorsed approach among the set of true approaches." Static knowledge bases and model pretraining snapshot a distribution of practice at a point in time, and there is no signal in the retrieved text itself indicating that a newer, now-preferred alternative exists. Because the old practice is still internally consistent and not contradicted by any single retrieved passage, standard fact-checking and consistency checks never flag it — the gap is only visible in a diff against the current version of the domain's guidance, which the agent typically has no access to.

## Example
```
A user asks a coding agent for the recommended way to manage Python
dependencies for a new project.

The agent, drawing on documentation indexed 14 months ago, recommends:
"Create a requirements.txt with pinned versions and manage your virtual
environment with venv + pip. This is the standard approach."

This was accurate best practice at indexing time. However, the Python
packaging ecosystem has since consolidated around lockfile-based tools
(e.g. uv, Poetry) for reproducible builds, and requirements.txt-only
workflows are now flagged as legacy in current style guides and CI
templates the user's team has adopted.

The user's PR is rejected in code review: "we moved off requirements.txt
six months ago, use the lockfile workflow like every other service."
The agent's advice was true but stale relative to the domain's current
consensus, and it had no way of knowing its source predated the shift.
```

## Statistics
| Finding | Context |
|---------|---------|
| Best-practice guidance in fast-moving technical domains has an estimated effective half-life of 6-18 months before a meaningful fraction is considered outdated | Estimated from observed drift in software/security guidance corpora |
| 20-35% of "how should I do X" agent responses in actively-evolving domains reference an approach practitioners now consider legacy | Typical range observed in production agent telemetry for technical assistants |
| Adding an explicit "last verified as current practice" freshness check to best-practice retrieval reduces stale recommendations by roughly a third | Reported range across teams that added practice-currency checks |

## Mitigations
1. **Practice-currency tagging**: Tag best-practice content with a "current as of" date and a review cadence, distinct from factual-accuracy metadata, and surface staleness explicitly when the tag exceeds the domain's typical drift window.
2. **Community-consensus cross-check**: For fast-moving domains, cross-reference retrieved advice against a periodically refreshed signal of current consensus (style guides, official docs, changelogs) rather than relying solely on static indexed content.
3. **Explicit "current vs. historically valid" framing**: When the agent cannot confirm currency, have it hedge — presenting the retrieved practice as "one valid approach, verify against your team's current standards" rather than as the definitive recommendation.
4. **Domain refresh cadence tied to volatility**: Set re-indexing frequency for best-practice sources based on measured domain volatility (e.g. monthly for security/tooling, yearly for stable engineering fundamentals) instead of a single fixed schedule for all content.
5. **User-correction feedback loop**: Capture and route "that's outdated" corrections from users back into the knowledge source's staleness scoring so repeatedly-flagged practices get prioritized for re-verification.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| best_practice_content_age_days | Age of indexed best-practice content since last currency verification | Alert if > domain-specific staleness window (e.g. 180 days) |
| outdated_advice_correction_rate | Rate of user corrections flagging agent advice as "no longer current practice" | Alert if > 5% of best-practice responses |
| practice_currency_tag_coverage | Share of best-practice content with a valid, unexpired currency tag | Alert if < 90% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Best-practice content stale | Content exceeds domain-specific staleness window without re-verification | Medium | Queue for re-verification against current sources, add hedge language in the interim |
| Repeated outdated-advice corrections | Same content ID flagged outdated by 3+ distinct users | High | Immediately suppress from confident recommendations, escalate for manual review |

## Related Patterns
- [Knowledge Update Lag](./knowledge-update-lag.md) - the underlying mechanism (indexed copy lags the source) that produces stale best-practice advice as one manifestation
- [Domain Rule Misunderstanding](./domain-rule-misunderstanding.md) - both involve misapplying domain knowledge, but this one is about currency rather than scope
- [Fact Timestamp Error](./fact-timestamp-error.md) - shares the temporal-validity mechanism, applied to individual facts rather than aggregate practice
