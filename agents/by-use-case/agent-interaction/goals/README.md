# Agent Interaction AI Agent Failures by Goal: 23 Patterns, Causes, and Fixes

**Agent Interaction AI agents fail in 1 distinct ways, grouped by the goal each failure breaks.** Find the goal that matches what you are seeing, open its list, and use the fix on each pattern page.

## Key Takeaways

- 23 documented patterns across 1 goal; the most documented is [Conversation Quality](conversation-quality/) with 23.
- Each pattern page gives the symptoms, an example, the root cause, and mitigations.

## Agent Interaction Goals

| Goal | When it fails | Patterns |
|---|---|---|
| [Conversation Quality](conversation-quality/) | When an agent mismanages the ask-vs-act decision on ambiguous requests, loses track of its own conversational state over many turns, miscalibrates register to context | 23 |

**Total: 23 patterns**

## Frequently Asked Questions

### What causes a conversation to feel "off" even when every individual response seems reasonable?

Most conversation-quality failures are only visible in aggregate: a single clarifying question, tone shift, or satisfied rating looks fine on its own, but [conversation coherence loss](conversation-quality/failures/conversation-coherence-loss.md), [user trust degradation](conversation-quality/failures/user-trust-degradation.md), and [user retention decline](conversation-quality/failures/user-retention-decline.md) all describe damage that compounds silently across turns or sessions precisely because no single instance crosses a per-response quality bar. See [Conversation Quality](conversation-quality/).

## Related

- [Agent Interaction overview](../)
- [All agent failure patterns](../../../)
