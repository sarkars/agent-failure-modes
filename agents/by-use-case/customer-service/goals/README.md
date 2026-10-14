# Customer Service AI Agent Failures by Goal: 15 Patterns, Causes, and Fixes

**Customer Service failures in AI agents are grouped here into 3 goals, each with a catalog of named failure patterns, the symptoms you will see, the root cause, and mitigations you can copy.** Start from the symptom you are debugging, pick the matching goal below, and open its failure list.

## Key Takeaways

- This use case covers 3 goals and 15 documented failure patterns.
- The largest goal is [Conversation Resolution](conversation-resolution/) with 12 patterns.
- Each goal page explains the failure class, how to tell it apart from its neighbors, and which mitigations apply across its patterns.
- Each failure page covers the symptoms, an example, the root cause, and how to fix it.

## Customer Service Goals

| Goal | What goes wrong | Patterns |
|---|---|---|
| [Conversation Resolution](conversation-resolution/) | Conversation resolution fails when a support agent selects a canned response matching the customer's topic but wrong for their account state, asks repeated questions the customer already answered | 12 |
| [Proactive Retention Outreach](proactive-retention-outreach/) | Proactive retention outreach fails when a retention agent reaches out to an at-risk customer with a fabricated usage-decline narrative to justify the outreach, because a tool call to fetch actual usage data returned empty or errored | 1 |
| [Refund and Billing Disputes](refund-and-billing-disputes/) | Refund and billing-dispute resolution fails when an agent retrieves a billing-dispute template or policy article that is embedding-similar but legally or contractually distinct from the customer's actual account tier or dispute category | 2 |

**Total: 15 patterns**

## Frequently Asked Questions

### Where do I start if my customer service agent is failing?

Match the symptom to a goal in the table above, then open that goal's page for how to tell its failures apart and where to look first. Each failure page ends in mitigations you can apply directly.

### How are these customer service failure patterns organized?

By goal: the outcome the agent is supposed to achieve. Under each goal, a `failures` folder holds one page per pattern. For the full picture see the [Customer Service overview](../).

## Related

- [Customer Service overview](../)
- [All agent failure patterns](../../../)
