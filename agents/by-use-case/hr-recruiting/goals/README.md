# HR Recruiting AI Agent Failures by Goal: 19 Patterns, Causes, and Fixes

**HR Recruiting AI agents fail in 4 distinct ways, grouped by the goal each failure breaks.** Find the goal that matches what you are seeing, open its list, and use the fix on each pattern page.

## Key Takeaways

- 19 documented patterns across 4 goals; the most documented is [Candidate Screening](candidate-screening/) with 5.
- Each pattern page gives the symptoms, an example, the root cause, and mitigations.

## HR Recruiting Goals

| Goal | When it fails | Patterns |
|---|---|---|
| Candidate Screening | Candidate screening agents systematically favor articulate or keyword-optimized candidates over substantively qualified ones, confuse surface-level similarity with actual job relevance | 5 |
| [Offer Generation](offer-generation/) | Offer-generation agents produce compensation figures from stale training-data benchmarks instead of querying live market data | 4 |
| [Onboarding](onboarding/) | Onboarding agents lose track of conditional requirements (visa-status-specific tasks, jurisdiction-specific benefits, accommodations) across multi-session workflows | 5 |
| [Retention Prediction](retention-prediction/) | Retention-prediction agents fabricate conversational details in risk-score narratives that are not grounded in any source record | 5 |

**Total: 19 patterns**

## Frequently Asked Questions

### How do you distinguish between keyword matching and legitimate skill assessment?

Legitimate skill assessment evaluates underlying capabilities independent of terminology or phrasing; keyword matching rewards resume language that mirrors the job description text. See Candidate Screening.

### How do conditional onboarding tasks get lost across sessions?

Each session operates on the hire's persistent structured record. See Onboarding.

### How do you catch narrative hallucinations in risk-score justifications?

Require every specific factual claim in a risk narrative (quotes, dated events, manager-conversation details) to cite the source document or note ID it came from. See Retention Prediction.

## Related

- [HR Recruiting overview](../)
- [All agent failure patterns](../../../)
