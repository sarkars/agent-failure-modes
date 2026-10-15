# Insurance Agents: Business Goals, Failure Patterns, and Fixes

**Insurance Agents fail along 5 goals: Claim Processing, Fraud Detection, Policy Management carry the most documented failures.** This page maps each goal to the failures that threaten it, so you can decide what to protect first and where the fixes are.

## Key Takeaways

- 13 documented failure patterns across 5 goals. What it does: process claims, support underwriting, and flag fraud.
- The most documented goal is [Claim Processing](../by-use-case/insurance/goals/claim-processing/) with 3 patterns.
- Frequencies below are as recorded on each pattern page. They are not measured rates.
- Business-goal definitions (metric, baseline, owner, what counts as a failure) are not written yet for this agent. Define them before choosing which patterns to prioritize.

## Goals this agent must protect

| Goal | When it fails | Patterns |
|---|---|---|
| [Claim Processing](../by-use-case/insurance/goals/claim-processing/) | Claim-processing agents fail in three distinct, recurring ways | 3 |
| [Fraud Detection](../by-use-case/insurance/goals/fraud-detection/) | When agents treat embedding-similarity matches to known fraud ring members as sufficient grounds for escalation without requiring a corroborating structured relational | 3 |
| [Policy Management](../by-use-case/insurance/goals/policy-management/) | When a renewal-pricing RAG step retrieves a similar-looking but territory-mismatched policy precedent | 3 |
| [Underwriting](../by-use-case/insurance/goals/underwriting/) | When an occupation-class retrieval step matches applicants by job-title lexical similarity to a prior case without verifying that the retrieved precedent's actual hazard | 3 |
| [Claims Processing](../by-use-case/insurance/goals/claims-processing/) | When agents assume claims arrive as independent, randomly-distributed events and do not account for catastrophe correlation | 1 |

## Failures most often recorded

| Failure | What goes wrong | Recorded frequency |
|---|---|---|
| [Embedding-Retrieval Wrong Endorsement Version Applied](../by-use-case/insurance/goals/claim-processing/failures/embedding-retrieval-wrong-endorsement-version-applied.md) | A Claims-Adjudication Agent's RAG Retrieval Step Pulls a Lexically Similar but Superseded or Wrong-State Policy Endorsement from the Document Store… | Common |

## Before you build: define each goal

For every goal in the table, write down: the metric and how you measure its baseline today; the person who owns it; what counts as a failure and how severe it is; who is told when it happens; and when a person takes over. Then use the failures above as your test list.

## Human-side failures

Because this agent talks to customers or patients, also check conversation-level failures: tone, handoff to a person, refusals, and choosing the wrong channel. See the [human-machine interface section](../by-capability/human-machine-interface/).

## Security and governance

Every agent also needs the cross-cutting checks in [security](../cross-cutting/security/), [accuracy](../cross-cutting/accuracy/), [governance](../cross-cutting/governance/), and [operations](../cross-cutting/operations/).

## Frequently Asked Questions

### What fails most often in insurance agents?

The most documented goal is Claim Processing (3 patterns). The failures table above lists the ones recorded as most frequent. These are the library's records, not measured rates.

### Where should I start when building insurance agents?

Define your business goals and what counts as failure, then test against the failure patterns for each goal. The section above lists what to write down.

## Related

- [All agents by business goal](./)
