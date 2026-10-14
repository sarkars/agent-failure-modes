# Learning AI Agent Failures by Goal: 12 Patterns, Causes, and Fixes

**Learning failures in AI agents are grouped here into 3 goals, each with a catalog of named failure patterns, the symptoms you will see, the root cause, and mitigations you can copy.** Start from the symptom you are debugging, pick the matching goal below, and open its failure list.

## Key Takeaways

- This cross-cutting concern covers 3 goals and 12 documented failure patterns.
- The largest goal is [Safe Learning](safe-learning/) with 12 patterns.
- Each goal page explains the failure class, how to tell it apart from its neighbors, and which mitigations apply across its patterns.
- Each failure page covers the symptoms, an example, the root cause, and how to fix it.

## Learning Goals

| Goal | What goes wrong | Patterns |
|---|---|---|
| [Feedback and Adaptation](feedback-and-adaptation/) | Feedback and adaptation fails when an agent receives correction signals but cannot respond to correction, misinterprets feedback context, or applies corrective action inconsistently across similar scenarios (planned, no patterns written yet) | 0 |
| [In Context Learning](in-context-learning/) | In-context learning fails when an agent receives examples or few-shot instruction within a request but interprets examples incorrectly, forgets examples mid-conversation, or applies learned patterns too rigidly to new scenarios (planned, no patterns written yet) | 0 |
| [Safe Learning](safe-learning/) | Safe self-improvement fails when an agent ingests feedback or metrics and updates its behavior without adequate validation, catching the degradation only weeks later after shipping degraded behavior to production | 12 |

**Total: 12 patterns**

## Frequently Asked Questions

### Where do I start if my learning agent is failing?

Match the symptom to a goal in the table above, then open that goal's page for how to tell its failures apart and where to look first. Each failure page ends in mitigations you can apply directly.

### How are these learning failure patterns organized?

By goal: the outcome the agent is supposed to achieve. Under each goal, a `failures` folder holds one page per pattern. For the full picture see the [Learning overview](../).

## Related

- [Learning overview](../)
- [All agent failure patterns](../../../)
