# User Retention Decline

## Issue
Users who adopted the agent and used it regularly gradually reduce their usage and eventually stop, not because of one bad session but because the cumulative weight of minor conversation-quality issues — repetition, drift, occasional wrong assumptions, tone mismatches — slowly outweighs the value they get, in a way that's invisible session-by-session but clear in aggregate over weeks or months. This differs from user-adoption-failure, which happens in the first sessions before any habit forms; retention decline happens to users who were already engaged and is driven by slow accumulation rather than an abrupt early impression.

**Frequency**: Common

**Symptoms**
- Usage frequency per active user trends downward over a multi-week or multi-month horizon without any single triggering incident
- Users who eventually churn show a gradual pre-churn increase in corrections, re-asks, or session abandonment rate before the actual churn event
- Exit interviews or churn surveys cite general dissatisfaction ("just stopped feeling worth it") rather than a specific incident
- Task variety per user narrows before churn — users retreat to only the small subset of request types the agent reliably handles well
- Aggregate satisfaction metrics stay stable even as usage declines, because the biased feedback population doesn't capture the users quietly disengaging

## Root Cause
No single conversation-quality failure is usually severe enough to cause an engaged user to quit on the spot; the erosion is cumulative, and gradual cumulative effects are structurally hard for a team to detect through session-level quality metrics, which typically evaluate each session independently rather than tracking a user's trend across many sessions. Because each individual session might look "fine" against a per-session quality bar, the compounding effect only becomes visible when usage data is analyzed longitudinally per-user — and by the time that analysis happens, the affected users have often already left.

## Example
```
A user has been using the agent weekly for three months for research
summarization tasks. Individually, no single session in that period
would fail a per-session quality check: outputs are mostly accurate,
no session contains an outright critical error.

But across those months: several sessions required re-explaining the
same source-citation preference the agent didn't retain; a few outputs
drifted into unrequested tangents that had to be redirected; and the
agent's depth calibration was inconsistent, sometimes over-explaining
simple summaries.

None of these were bad enough individually to complain about. By month
four, usage frequency has dropped from 3x/week to 1x every two weeks;
by month five, the user has switched to a different tool entirely,
citing in an exit survey only "it just always took more back-and-forth
than it should have."
```

## Statistics
| Finding | Context |
|---------|---------|
| A meaningful share of eventual churned users show a detectable rise in session correction/re-ask rate in the weeks preceding churn, even when no single session triggers a complaint | Typical range across longitudinal usage analysis of conversational agent products |
| Task variety per user (the range of distinct request types attempted) tends to narrow measurably before churn, as users retreat to only reliably-handled request types | Estimated from pre-churn usage pattern analysis |
| Longitudinal per-user quality tracking, rather than only per-session tracking, surfaces retention-risk users meaningfully earlier | Reported range across teams that added per-user trend monitoring |

## Mitigations
1. **Per-user longitudinal quality tracking**: Track correction rate, re-ask rate, and task variety trends per user over time, not just per-session quality, to surface slow erosion before churn.
2. **Task-variety-narrowing alerts**: Flag users whose range of attempted request types is shrinking over time as an early retention-risk signal, since it often indicates the user has learned to avoid the agent's weak areas rather than the agent having no weak areas.
3. **Proactive quality outreach**: For users showing early erosion signals, proactively surface improvements or ask for specific feedback rather than waiting for an exit survey after churn has already occurred.
4. **Cumulative friction budget per user**: Define an acceptable cumulative friction threshold across a user's session history, and treat crossing it as a trigger for review, distinct from any single session's quality score.
5. **Cross-session consistency improvements**: Address the underlying conversation-quality failures (repetition, drift, tone mismatch, depth mismatch) directly, since these are individually minor but collectively the primary driver of this pattern.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| usage_frequency_trend_per_user | Change in per-user session frequency over a rolling multi-week window | Alert if declining trend detected pre-churn |
| task_variety_narrowing_rate | Rate of decline in distinct request types attempted per user over time | Alert if narrowing without corresponding satisfaction drop |
| pre_churn_correction_rate_trend | Trend in correction/re-ask rate for users in the weeks before churn | Alert if rising trend detected |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Retention-risk user identified | usage_frequency_trend_per_user shows sustained decline alongside rising correction rate | Medium | Trigger proactive outreach, review recent session quality for that user |
| Cohort-wide retention decline | Aggregate retention metrics decline despite stable per-session quality scores | High | Investigate longitudinal/cumulative quality issues, review conversation-quality metrics across sessions |

## Related Patterns
- [User Adoption Failure](./user-adoption-failure.md) - the analogous pattern for new users, driven by early friction rather than long-horizon accumulation
- [User Feedback Bias](./user-feedback-bias.md) - biased feedback collection often fails to surface the users quietly disengaging, masking retention decline until usage data reveals it
- [Conversation Repetition](./conversation-repetition.md) - one of several individually-minor recurring issues whose accumulation across sessions is a common driver of this pattern
