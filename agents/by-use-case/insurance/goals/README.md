# Insurance AI Agent Failures by Goal: 13 Patterns, Causes, and Fixes

**Insurance AI agents fail in 5 distinct ways, grouped by the goal each failure breaks.** Find the goal that matches what you are seeing, open its list, and use the fix on each pattern page.

## Key Takeaways

- 13 documented patterns across 5 goals; the most documented is [Claim Processing](claim-processing/) with 3.
- Each pattern page gives the symptoms, an example, the root cause, and mitigations.

## Insurance Goals

| Goal | When it fails | Patterns |
|---|---|---|
| Claim Processing | Claim-processing agents fail in three distinct, recurring ways: a retrieval step pulls a superseded or wrong-jurisdiction policy document that looks textually similar to the correct one | 3 |
| [Claims Processing](claims-processing/) | When they assume claims arrive as independent, randomly-distributed events and do not account for catastrophe correlation — a single hurricane hits and creates 10,000 simultaneous claims | 1 |
| [Fraud Detection](fraud-detection/) | When they treat embedding-similarity matches to known fraud ring members as sufficient grounds for escalation without requiring a corroborating structured relational signal | 3 |
| [Policy Management](policy-management/) | When a renewal-pricing RAG step retrieves a similar-looking but territory-mismatched policy precedent, when a multi-agent handoff loses a mid-term endorsement that changed the risk profile | 3 |
| [Underwriting](underwriting/) | When an occupation-class retrieval step matches applicants by job-title lexical similarity to a prior case without verifying that the retrieved precedent's actual hazard profile matches… | 3 |

**Total: 13 patterns**

## Frequently Asked Questions

### What causes a claims-adjudication agent to apply the wrong coverage terms?

Most commonly, a retrieval step selects a policy endorsement or clause by embedding similarity rather than by a deterministic match on form number and effective date, so a superseded or wrong-jurisdiction version with near-identical boilerplate gets applied instead of the version actually attached to the policy. See Claim Processing.

### Can an agent detect a fraud-ring member purely from name and address similarity?

No. See Fraud Detection.

### How does a renewal-pricing precedent lookup retrieve the wrong rating territory?

Renewal-pricing retrieval matches the query policy against a corpus of prior renewals by embedding similarity over shared attributes (construction type, coverage limits, property age), which look similar across all territories. See Policy Management.

## Related

- [Insurance overview](../)
- [All agent failure patterns](../../../)
