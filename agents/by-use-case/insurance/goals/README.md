# Insurance AI Agent Failures by Goal: 13 Patterns, Causes, and Fixes

**Insurance failures in AI agents are grouped here into 5 goals, each with a catalog of named failure patterns, the symptoms you will see, the root cause, and mitigations you can copy.** Start from the symptom you are debugging, pick the matching goal below, and open its failure list.

## Key Takeaways

- This use case covers 5 goals and 13 documented failure patterns.
- The largest goal is [Claim Processing](claim-processing/) with 3 patterns.
- Each goal page explains the failure class, how to tell it apart from its neighbors, and which mitigations apply across its patterns.
- Each failure page covers the symptoms, an example, the root cause, and how to fix it.

## Insurance Goals

| Goal | What goes wrong | Patterns |
|---|---|---|
| [Claim Processing](claim-processing/) | Claim-processing agents fail in three distinct, recurring ways | 3 |
| [Claims Processing](claims-processing/) | Claims-processing reserve models fail when they assume claims arrive as independent, randomly-distributed events and do not account for catastrophe correlation | 1 |
| [Fraud Detection](fraud-detection/) | Fraud-detection agents fail when they treat embedding-similarity matches to known fraud ring members as sufficient grounds for escalation without requiring a corroborating structured relational signal | 3 |
| [Policy Management](policy-management/) | Policy-management agents fail when a renewal-pricing RAG step retrieves a similar-looking but territory-mismatched policy precedent, when a multi-agent handoff loses a mid-term endorsement that changed the risk profile | 3 |
| [Underwriting](underwriting/) | Underwriting agents fail when an occupation-class retrieval step matches applicants by job-title lexical similarity to a prior case without verifying that the retrieved precedent's actual hazard profile matches the current applicant's | 3 |

**Total: 13 patterns**

## Frequently Asked Questions

### Where do I start if my insurance agent is failing?

Match the symptom to a goal in the table above, then open that goal's page for how to tell its failures apart and where to look first. Each failure page ends in mitigations you can apply directly.

### How are these insurance failure patterns organized?

By goal: the outcome the agent is supposed to achieve. Under each goal, a `failures` folder holds one page per pattern. For the full picture see the [Insurance overview](../).

## Related

- [Insurance overview](../)
- [All agent failure patterns](../../../)
