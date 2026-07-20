# User Feedback Bias

## Issue
The mechanism used to collect quality signal — thumbs-up/down buttons, post-chat surveys, star ratings — is only used by a non-representative subset of users, typically those with strongly positive or strongly negative experiences, while the much larger group with a mediocre-but-tolerable experience stays silent. Teams then treat the collected feedback as representative of overall quality, when it's actually a bimodal sample that systematically misses the median experience, leading to miscalibrated confidence in how the agent is actually performing.

**Frequency**: Common

**Symptoms**
- Feedback response rate is low (often under 5-10% of sessions) yet is treated as statistically representative of the full user base
- Collected ratings skew bimodal — heavy concentration at the extremes with little in the middle — inconsistent with a smoother underlying quality distribution
- Aggregate satisfaction score stays flat or positive while other signals (usage decline, support volume, churn) suggest a different reality
- Certain user segments (e.g. power users, or users who churn quickly) are structurally underrepresented in feedback because the prompt fires at a point they don't reach
- Rating prompt placement or timing correlates with predictable sentiment states rather than being neutral

## Root Cause
Feedback mechanisms are opt-in by construction, and opt-in participation correlates strongly with the intensity of the experience — people are motivated to click a thumbs-down after real frustration or a thumbs-up after being genuinely delighted, but have little motivation to interrupt their flow to rate an interaction that was simply fine. This selection effect means the feedback stream is not a random sample of session quality; it's a sample conditioned on emotional intensity, and any team that aggregates it as if it were representative will systematically overweight the tails and underweight the (often much larger) mediocre middle, where accumulating dissatisfaction that eventually drives churn tends to live.

## Example
```
A product team tracks a thumbs-up rate of 92% on agent responses and
uses it as the headline quality metric in a quarterly review, citing it
as evidence the agent is performing well.

Actual feedback participation rate is 4% of all sessions. Within that
4%, ratings are heavily bimodal: 70% are 5-star raves from power users
who love the product, and most of the rest are 1-star ratings from
users who had a severely bad experience and were motivated enough to
complain.

The 96% of sessions that received no rating at all — where the
experience was adequate but unremarkable, with minor friction the user
didn't bother reporting — are invisible in this metric. Independent
churn data for that same quarter shows retention declining, a trend the
92% thumbs-up figure gave no early warning of.
```

## Statistics
| Finding | Context |
|---------|---------|
| Feedback mechanisms in conversational agent products typically see participation from a small single-digit percentage of total sessions | Typical range across production deployments |
| Collected ratings in low-participation feedback systems tend to skew bimodal relative to the smoother distribution implied by independent quality audits of unrated sessions | Estimated from comparison of rated vs. randomly-sampled session quality |
| Combining passive/inferred signals (task completion, re-contact rate) with explicit ratings narrows the gap between measured and actual quality substantially | Reported range across teams that added passive signal collection |

## Mitigations
1. **Passive signal supplementation**: Track inferred quality signals that don't require opt-in (task completion rate, session abandonment, re-contact within N days) alongside explicit ratings, and weight aggregate quality assessments toward the passive signals.
2. **Representative sampling audits**: Periodically have reviewers assess a random sample of unrated sessions against a quality rubric, independent of which sessions users chose to rate, to calibrate how representative the rated subset actually is.
3. **Response-rate-aware reporting**: Always report feedback participation rate alongside the satisfaction score itself, and flag low-participation metrics as directional rather than conclusive in decision-making contexts.
4. **Prompt-timing neutrality**: Review when and how rating prompts are triggered to ensure they aren't systematically more likely to appear after specific sentiment states (e.g. only after errors, or only after successful completions).
5. **Segment-level feedback tracking**: Break down feedback participation and results by user segment (new vs. returning, power vs. occasional) to detect and correct for segments that are structurally underrepresented.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| feedback_participation_rate | Share of total sessions that receive any explicit rating | Alert if < 10% when used as a primary quality metric |
| rating_bimodality_index | Degree to which collected ratings cluster at the extremes versus a smoother distribution | Alert if highly bimodal without passive-signal cross-check |
| satisfaction_vs_passive_signal_divergence | Gap between explicit satisfaction trend and passive signals like completion/re-contact rate | Alert if trends diverge |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Satisfaction metric diverges from passive signals | satisfaction_vs_passive_signal_divergence crosses threshold | High | Treat satisfaction score as unreliable, prioritize passive signals, audit random session sample |
| Low participation used as headline metric | feedback_participation_rate is low but score is reported without caveat | Medium | Add participation-rate context to reporting, flag for stakeholder review |

## Related Patterns
- [Satisfaction Metric Gaming](./satisfaction-metric-gaming.md) - a compounding failure where optimization pressure exploits the same biased metric this pattern describes as unreliable
- [User Retention Decline](./user-retention-decline.md) - the passive signal that often reveals quality problems the biased feedback stream missed
- [User Support Bottleneck](./user-support-bottleneck.md) - support ticket volume is one of the passive signals that can surface issues invisible in opt-in feedback
