# Multi Agent Systems AI Agent Failures by Goal: 18 Patterns, Causes, and Fixes

**Multi Agent Systems failures in AI agents are grouped here into 4 goals, each with a catalog of named failure patterns, the symptoms you will see, the root cause, and mitigations you can copy.** Start from the symptom you are debugging, pick the matching goal below, and open its failure list.

## Key Takeaways

- This capability covers 4 goals and 18 documented failure patterns.
- The largest goal is [Coordination](coordination/) with 15 patterns.
- Each goal page explains the failure class, how to tell it apart from its neighbors, and which mitigations apply across its patterns.
- Each failure page covers the symptoms, an example, the root cause, and how to fix it.

## Multi Agent Systems Goals

| Goal | What goes wrong | Patterns |
|---|---|---|
| [Coordination](coordination/) | Multi-agent AI systems fail to coordinate because the system-design layer — who owns which decision, how messages are validated at handoffs, and how disagreement gets resolved | 15 |
| [Error Propagation](error-propagation/) | One agent's error amplifies across a multi-agent pipeline because each downstream agent treats the previous agent's output as ground truth rather than an uncertain input to verify | 1 |
| [Handoff Reliability](handoff-reliability/) | A multi-agent handoff loses the upstream agent's confidence signal because the handoff schema is designed to carry only a final value and a status flag | 1 |
| [Reasoning Quality](reasoning-quality/) | Agreement among multiple AI agents does not guarantee a correct answer because agents built from the same base model, training data, or context inherit the same systematic biases | 1 |

**Total: 18 patterns**

## Frequently Asked Questions

### Where do I start if my multi agent systems agent is failing?

Match the symptom to a goal in the table above, then open that goal's page for how to tell its failures apart and where to look first. Each failure page ends in mitigations you can apply directly.

### How are these multi agent systems failure patterns organized?

By goal: the outcome the agent is supposed to achieve. Under each goal, a `failures` folder holds one page per pattern. For the full picture see the [Multi Agent Systems overview](../).

## Related

- [Multi Agent Systems overview](../)
- [All agent failure patterns](../../../)
