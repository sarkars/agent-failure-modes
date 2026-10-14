# Reasoning and Thought AI Agent Failures by Goal: 23 Patterns, Causes, and Fixes

**Reasoning and Thought failures in AI agents are grouped here into 7 goals, each with a catalog of named failure patterns, the symptoms you will see, the root cause, and mitigations you can copy.** Start from the symptom you are debugging, pick the matching goal below, and open its failure list.

## Key Takeaways

- This capability covers 7 goals and 23 documented failure patterns.
- The largest goal is [Model Behavior and Capabilities](model-behavior-and-capabilities/) with 10 patterns.
- Each goal page explains the failure class, how to tell it apart from its neighbors, and which mitigations apply across its patterns.
- Each failure page covers the symptoms, an example, the root cause, and how to fix it.

## Reasoning and Thought Goals

| Goal | What goes wrong | Patterns |
|---|---|---|
| [Intermediate Token Overflow](intermediate-token-overflow/) | Failures where intermediate reasoning steps exceed context or token limits mid-process (planned, no patterns written yet) | 0 |
| [Model Behavior and Capabilities](model-behavior-and-capabilities/) | A model's behavior degrades without any error being returned because degradation in LLMs is almost always a soft, statistical ceiling rather than a hard limit | 10 |
| [Model Selection and Routing](model-selection-and-routing/) | Model routing layers send requests to the wrong model because routers are typically built to optimize one visible, easy-to-measure axis — cost, latency, or a coarse task-category label | 6 |
| [Model Updates and Versioning](model-updates-and-versioning/) | Model update and versioning failures happen because changing which model version serves an agent never gets the same safety net as a normal code deploy | 7 |
| [Reasoning Latency](reasoning-latency/) | Unpredictable reasoning computation time, SLA breaches, and tail latency issues (planned, no patterns written yet) | 0 |
| [Reasoning Overconfidence](reasoning-overconfidence/) | Reasoning chains that appear sound but lead to incorrect conclusions; confidence in intermediate steps doesn't correlate with correctness (planned, no patterns written yet) | 0 |
| [Search Space Explosion](search-space-explosion/) | Failures where reasoning token generation expands unboundedly, exceeding limits or causing memory exhaustion (planned, no patterns written yet) | 0 |

**Total: 23 patterns**

## Frequently Asked Questions

### Where do I start if my reasoning and thought agent is failing?

Match the symptom to a goal in the table above, then open that goal's page for how to tell its failures apart and where to look first. Each failure page ends in mitigations you can apply directly.

### How are these reasoning and thought failure patterns organized?

By goal: the outcome the agent is supposed to achieve. Under each goal, a `failures` folder holds one page per pattern. For the full picture see the [Reasoning and Thought overview](../).

## Related

- [Reasoning and Thought overview](../)
- [All agent failure patterns](../../../)
