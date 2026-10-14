# Hr Recruiting AI Agent Failures by Goal: 19 Patterns, Causes, and Fixes

**Hr Recruiting failures in AI agents are grouped here into 4 goals, each with a catalog of named failure patterns, the symptoms you will see, the root cause, and mitigations you can copy.** Start from the symptom you are debugging, pick the matching goal below, and open its failure list.

## Key Takeaways

- This use case covers 4 goals and 19 documented failure patterns.
- The largest goal is [Candidate Screening](candidate-screening/) with 5 patterns.
- Each goal page explains the failure class, how to tell it apart from its neighbors, and which mitigations apply across its patterns.
- Each failure page covers the symptoms, an example, the root cause, and how to fix it.

## Hr Recruiting Goals

| Goal | What goes wrong | Patterns |
|---|---|---|
| [Candidate Screening](candidate-screening/) | Candidate screening agents systematically favor articulate or keyword-optimized candidates over substantively qualified ones, confuse surface-level similarity with actual job relevance | 5 |
| [Offer Generation](offer-generation/) | Offer-generation agents produce compensation figures from stale training-data benchmarks instead of querying live market data, anchor offers to mismatched leveling precedents selected via embedding similarity | 4 |
| [Onboarding](onboarding/) | Onboarding agents lose track of conditional requirements (visa-status-specific tasks, jurisdiction-specific benefits, accommodations) across multi-session workflows | 5 |
| [Retention Prediction](retention-prediction/) | Retention-prediction agents fabricate conversational details in risk-score narratives that are not grounded in any source record, use stale industry-attrition benchmarks instead of querying live cohort-comparison tools | 5 |

**Total: 19 patterns**

## Frequently Asked Questions

### Where do I start if my hr recruiting agent is failing?

Match the symptom to a goal in the table above, then open that goal's page for how to tell its failures apart and where to look first. Each failure page ends in mitigations you can apply directly.

### How are these hr recruiting failure patterns organized?

By goal: the outcome the agent is supposed to achieve. Under each goal, a `failures` folder holds one page per pattern. For the full picture see the [Hr Recruiting overview](../).

## Related

- [Hr Recruiting overview](../)
- [All agent failure patterns](../../../)
