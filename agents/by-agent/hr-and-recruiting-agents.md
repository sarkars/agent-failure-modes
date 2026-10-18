# HR and Recruiting Agents: Business Goals, Failure Patterns, and Fixes

**HR and Recruiting Agents fail along 4 goals: Candidate Screening, Onboarding, Retention Prediction carry the most documented failures.** This page maps each goal to the failures that threaten it, so you can decide what to protect first and where the fixes are.

## Key Takeaways

- 19 documented failure patterns across 4 goals. What it does: screen candidates, generate offers, and support onboarding.
- The most documented goal is [Candidate Screening](../by-use-case/hr-recruiting/goals/candidate-screening/) with 5 patterns.
- Frequencies below are as recorded on each pattern page. They are not measured rates.
- Business-goal definitions (metric, baseline, owner, what counts as a failure) are not written yet for this agent. Define them before choosing which patterns to prioritize.

## Goals this agent must protect

| Goal | When it fails | Patterns |
|---|---|---|
| [Candidate Screening](../by-use-case/hr-recruiting/goals/candidate-screening/) | Candidate screening agents systematically favor articulate or keyword-optimized candidates over substantively qualified ones | 5 |
| [Onboarding](../by-use-case/hr-recruiting/goals/onboarding/) | Onboarding agents lose track of conditional requirements | 5 |
| [Retention Prediction](../by-use-case/hr-recruiting/goals/retention-prediction/) | Retention-prediction agents fabricate conversational details in risk-score narratives that are not grounded in any source record | 5 |
| [Offer Generation](../by-use-case/hr-recruiting/goals/offer-generation/) | Offer-generation agents produce compensation figures from stale training-data benchmarks instead of querying live market data | 4 |

## Failures most often recorded

| Failure | What goes wrong | Recorded frequency |
|---|---|---|
| [Resume Keyword Overfit Bias](../by-use-case/hr-recruiting/goals/candidate-screening/failures/resume-keyword-overfit-bias.md) | Candidate-Screening Agent Over-Weights Surface Keyword Matches Against the Job Description, Systematically Filtering Out Qualified Candidates Who… | Very Common |
| [Embedding Retrieval Pulls Wrong-Jurisdiction Benefits Policy During Onboarding](../by-use-case/hr-recruiting/goals/onboarding/failures/embedding-retrieval-pulls-wrong-jurisdiction-benefits-policy-during-onboarding.md) | An Onboarding Agent's Retrieval Step Surfaces a Benefits-Eligibility Policy Document for a Similarly Named but Different Work Jurisdiction or… | Common |
| [Interview Transcript Sentiment Overweighted vs. Content](../by-use-case/hr-recruiting/goals/candidate-screening/failures/interview-transcript-sentiment-overweighted-vs-content.md) | AI-Assisted Interview-Screening Agent Weights a Candidate's Vocal Confidence, Fluency, and Positive Sentiment in the Interview Transcript More… | Common |
| [Protected Class Proxy Discrimination](../by-use-case/hr-recruiting/goals/candidate-screening/failures/protected-class-proxy-discrimination.md) | Resume screener learns that names, dates, or graduation years correlate with performance; uses these as hidden proxy signals for protected… | Common |
| [Resume Keyword Matching Bias](../by-use-case/hr-recruiting/goals/candidate-screening/failures/resume-keyword-matching-bias.md) | AI resume screener uses exact keyword matching; rejects qualified candidates with industry synonyms or relevant but non-exact terminology (e.g., "web… | Common |
| [Stale Training-Corpus Visa-Sponsorship Rule Overrides Live Immigration-Policy Tool](../by-use-case/hr-recruiting/goals/onboarding/failures/stale-training-corpus-visa-sponsorship-rule-overrides-live-immigration-policy-tool.md) | An Onboarding Agent Answering a New International Hire's Question About Visa-Sponsorship Steps, Timelines, or Document Requirements Answers from… | Common |

## Before you build: define each goal

For every goal in the table, write down: the metric and how you measure its baseline today; the person who owns it; what counts as a failure and how severe it is; who is told when it happens; and when a person takes over. Then use the failures above as your test list.

## Security and governance

Every agent also needs the cross-cutting checks in [security](../cross-cutting/security/), [accuracy](../cross-cutting/accuracy/), [governance](../cross-cutting/governance/), and [operations](../cross-cutting/operations/).

## Frequently Asked Questions

### What fails most often in hr and recruiting agents?

The most documented goal is Candidate Screening (5 patterns). The failures table above lists the ones recorded as most frequent. These are the library's records, not measured rates.

### Where should I start when building hr and recruiting agents?

Define your business goals and what counts as failure, then test against the failure patterns for each goal. The section above lists what to write down.

## Related

- [All agents by business goal](./)
