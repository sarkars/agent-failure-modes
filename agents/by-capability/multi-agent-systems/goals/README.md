# Multi Agent Systems AI Agent Failures by Goal: 18 Patterns, Causes, and Fixes

**Multi Agent Systems AI agents fail in 4 distinct ways, grouped by the goal each failure breaks.** Find the goal that matches what you are seeing, open its list, and use the fix on each pattern page.

## Key Takeaways

- 18 documented patterns across 4 goals; the most documented is [Coordination](coordination/) with 15.
- Each pattern page gives the symptoms, an example, the root cause, and mitigations.

## Multi Agent Systems Goals

| Goal | When it fails | Patterns |
|---|---|---|
| Coordination | Multi-agent AI systems fail to coordinate because the system-design layer — who owns which decision, how messages are validated at handoffs, and how disagreement gets resolved — is left implicit | 15 |
| [Error Propagation](error-propagation/) | One agent's error amplifies across a multi-agent pipeline because each downstream agent treats the previous agent's output as ground truth rather than an uncertain input to verify | 1 |
| [Handoff Reliability](handoff-reliability/) | A multi-agent handoff loses the upstream agent's confidence signal because the handoff schema is designed to carry only a final value and a status flag | 1 |
| [Reasoning Quality](reasoning-quality/) | Agreement among multiple AI agents does not guarantee a correct answer because agents built from the same base model, training data, or context inherit the same systematic biases | 1 |

**Total: 18 patterns**

## Frequently Asked Questions

### What's the difference between coordination failures and error propagation in multi-agent systems?

Coordination failures cover the breadth of ways agents fail to work together — authority, roles, communication, consensus. See Coordination.

### How is error propagation different from cascading error in the Coordination goal?

They describe the same underlying mechanism. See Error Propagation.

### Can the downstream agent just read the upstream agent's full reasoning instead?

In practice, downstream agents are built to consume a structured handoff record for reliability and parseability, not to re-parse another agent's free-text chain of reasoning. See Handoff Reliability.

## Related

- [Multi Agent Systems overview](../)
- [All agent failure patterns](../../../)
