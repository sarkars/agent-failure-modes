# Customer Support Agents: Business Goals, Failure Patterns, and Fixes

**Customer Support Agents fail along 9 goals: Conversation Quality, Conversation Resolution, Ticket Routing carry the most documented failures.** This page maps each goal to the failures that threaten it, so you can decide what to protect first and where the fixes are.

## Key Takeaways

- 69 documented failure patterns across 9 goals. What it does: answer questions, resolve issues, and hand off to people for customers.
- The most documented goal is [Conversation Quality](../by-use-case/agent-interaction/goals/conversation-quality/) with 23 patterns.
- Frequencies below are as recorded on each pattern page. They are not measured rates.
- Business-goal definitions (metric, baseline, owner, what counts as a failure) are not written yet for this agent. Define them before choosing which patterns to prioritize.

## Goals this agent must protect

| Goal | When it fails | Patterns |
|---|---|---|
| [Conversation Quality](../by-use-case/agent-interaction/goals/conversation-quality/) | When an agent mismanages the ask-vs-act decision on ambiguous requests | 23 |
| [Conversation Resolution](../by-use-case/customer-service/goals/conversation-resolution/) | When a support agent selects a canned response matching the customer's topic but wrong for their account state | 12 |
| [Ticket Routing](../by-use-case/support-services/goals/ticket-routing/) | When agents classify a ticket's product category by embedding similarity to a taxonomy node without verifying the account actually has that product | 8 |
| [Issue Resolution](../by-use-case/support-services/goals/issue-resolution/) | When agents select a canned response by keyword similarity without verifying situational fit | 7 |
| [Self-Service Deflection](../by-use-case/support-services/goals/self-service-deflection/) | When agents offer the same unhelpful suggestion repeatedly without escalating | 6 |
| [Sentiment Escalation](../by-use-case/support-services/goals/sentiment-escalation/) | When agents select an escalation playbook by textual similarity rather than by confirming the ticket's actual severity tier | 6 |
| [SLA Management](../by-use-case/support-services/goals/sla-management/) | When agents apply an incorrect SLA tier because retrieval selected a boilerplate-heavy but wrong-tier policy document | 4 |
| [Refund and Billing Disputes](../by-use-case/customer-service/goals/refund-and-billing-disputes/) | When an agent retrieves a billing-dispute template or policy article that is embedding-similar but legally or contractually distinct from the customer's actual account | 2 |
| [Proactive Retention Outreach](../by-use-case/customer-service/goals/proactive-retention-outreach/) | When a retention agent reaches out to an at-risk customer with a fabricated usage-decline narrative to justify the outreach | 1 |

## Failures most often recorded

| Failure | What goes wrong | Recorded frequency |
|---|---|---|
| [Assumption Validation Failure](../by-use-case/agent-interaction/goals/conversation-quality/failures/assumption-validation-failure.md) | The agent infers an unstated detail about what the user wants — a default value, a scope boundary, an intended recipient, a file format — and… | Very Common |
| [Canned Response Context Mismatch](../by-use-case/support-services/goals/issue-resolution/failures/canned-response-context-mismatch.md) | Agent Selects a Templated/Canned Response That Matches Surface Keywords but Misses the Customer's Actual Situation | Very Common |
| [Chatbot Loop Without Human Escalation Path](../by-use-case/support-services/goals/self-service-deflection/failures/chatbot-loop-without-human-escalation-path.md) | Self-Service Deflection Agent Keeps Offering the Same or Similar Automated Suggestions Without Recognizing the Customer Needs Human Escalation | Very Common |
| [Conversation Depth Mismatch](../by-use-case/agent-interaction/goals/conversation-quality/failures/conversation-depth-mismatch.md) | The agent calibrates the wrong amount of detail for the question at hand — giving a two-line answer to something that needed a careful multi-step… | Very Common |
| [Conversation Repetition](../by-use-case/agent-interaction/goals/conversation-quality/failures/conversation-repetition.md) | The agent restates information, asks a question, or repeats an instruction that it (or the user) already covered earlier in the same conversation, as… | Very Common |
| [Deflection of Unresolved Issues](../by-use-case/support-services/goals/self-service-deflection/failures/deflection-of-unresolved-issues.md) | Self-Service Agent Marks a Conversation as "Deflected" (Resolved Without Human Agent) Based on the Customer Not Replying, Rather Than the Issue… | Very Common |

## Before you build: define each goal

For every goal in the table, write down: the metric and how you measure its baseline today; the person who owns it; what counts as a failure and how severe it is; who is told when it happens; and when a person takes over. Then use the failures above as your test list.

## Human-side failures

Because this agent talks to customers or patients, also check conversation-level failures: tone, handoff to a person, refusals, and choosing the wrong channel. See the [human-machine interface section](../by-capability/human-machine-interface/).

## Security and governance

Every agent also needs the cross-cutting checks in [security](../cross-cutting/security/), [accuracy](../cross-cutting/accuracy/), [governance](../cross-cutting/governance/), and [operations](../cross-cutting/operations/).

## Frequently Asked Questions

### What fails most often in customer support agents?

The most documented goal is Conversation Quality (23 patterns). The failures table above lists the ones recorded as most frequent. These are the library's records, not measured rates.

### Where should I start when building customer support agents?

Define your business goals and what counts as failure, then test against the failure patterns for each goal. The section above lists what to write down.

## Related

- [All agents by business goal](./)
