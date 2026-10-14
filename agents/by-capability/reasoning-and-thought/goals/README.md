# Reasoning and Thought AI Agent Failures by Goal: 23 Patterns, Causes, and Fixes

**Reasoning and Thought AI agents fail in 7 distinct ways, grouped by the goal each failure breaks.** Find the goal that matches what you are seeing, open its list, and use the fix on each pattern page.

## Key Takeaways

- 23 documented patterns across 7 goals; the most documented is [Model Behavior and Capabilities](model-behavior-and-capabilities/) with 10.
- Each pattern page gives the symptoms, an example, the root cause, and mitigations.

## Reasoning and Thought Goals

| Goal | When it fails | Patterns |
|---|---|---|
| [Intermediate Token Overflow](intermediate-token-overflow/) | Failures where intermediate reasoning steps exceed context or token limits mid-process. | 0 |
| [Model Behavior and Capabilities](model-behavior-and-capabilities/) | A model's behavior degrades without any error being returned because degradation in LLMs is almost always a soft, statistical ceiling rather than a hard limit — the API still returns a fluent | 10 |
| [Model Selection and Routing](model-selection-and-routing/) | Model routing layers send requests to the wrong model because routers are typically built to optimize one visible, easy-to-measure axis — cost, latency, or a coarse task-category label | 6 |
| [Model Updates and Versioning](model-updates-and-versioning/) | Model update and versioning failures happen because changing which model version serves an agent never gets the same safety net as a normal code deploy | 7 |
| [Reasoning Latency](reasoning-latency/) | Unpredictable reasoning computation time, SLA breaches, and tail latency issues. | 0 |
| [Reasoning Overconfidence](reasoning-overconfidence/) | Reasoning chains that appear sound but lead to incorrect conclusions; confidence in intermediate steps doesn't correlate with correctness. | 0 |
| [Search Space Explosion](search-space-explosion/) | Failures where reasoning token generation expands unboundedly, exceeding limits or causing memory exhaustion. | 0 |

**Total: 23 patterns**

## Frequently Asked Questions

### Can the model just say when it's uncertain or when a task is too complex for it?

Per [Model Uncertainty Unawareness](model-behavior-and-capabilities/failures/model-uncertainty-unawareness.md), confident, declarative phrasing is simply a more common surface pattern in training data than hedged phrasing, and RLHF has historically reinforced confident phrasing because human raters tend to prefer complete-sounding answers. See [Model Behavior and Capabilities](model-behavior-and-capabilities/).

### What is the difference between Model Update Accuracy Regression and Model Behavior Change Detection Failure?

[Model Update Accuracy Regression](model-updates-and-versioning/failures/model-update-accuracy-regression.md) describes the regression itself — a retrained model trades away a narrow, task-specific capability as an inherent consequence of multi-objective training, even while its aggregate benchmark scores improve. See [Model Updates and Versioning](model-updates-and-versioning/).

### What's the difference between Model Capability Mismatch and Model Version Incompatibility?

[Model Capability Mismatch](model-selection-and-routing/failures/model-capability-mismatch.md) is the coarse case — a text-only model receiving an image, or a non-tool-calling model receiving a function-calling request. See [Model Selection and Routing](model-selection-and-routing/).

## Related

- [Reasoning and Thought overview](../)
- [All agent failure patterns](../../../)
