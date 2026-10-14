# Learning AI Agent Failures by Goal: 12 Patterns, Causes, and Fixes

**Learning AI agents fail in 3 distinct ways, grouped by the goal each failure breaks.** Find the goal that matches what you are seeing, open its list, and use the fix on each pattern page.

## Key Takeaways

- 12 documented patterns across 3 goals; the most documented is [Safe Learning](safe-learning/) with 12.
- Each pattern page gives the symptoms, an example, the root cause, and mitigations.

## Learning Goals

| Goal | When it fails | Patterns |
|---|---|---|
| [Feedback and Adaptation](feedback-and-adaptation/) | When an agent receives correction signals but cannot respond to correction, misinterprets feedback context, or applies corrective action inconsistently across similar scenarios. | 0 |
| [In Context Learning](in-context-learning/) | When an agent receives examples or few-shot instruction within a request but interprets examples incorrectly, forgets examples mid-conversation | 0 |
| Safe Learning | When an agent ingests feedback or metrics and updates its behavior without adequate validation, catching the degradation only weeks later after shipping degraded behavior to production. | 12 |

**Total: 12 patterns**

## Frequently Asked Questions

### How do you catch metric-only-learning when a metric is by definition the thing you're optimizing for?

Metric-only learning fails when the metric omits constraints (compliance, safety, policy adherence) that matter beyond the metric itself. See Safe Learning.

### How do you distinguish feedback that should apply globally vs. feedback that applies only to the current context?

Structured feedback metadata should tag feedback with its intended scope: "user-specific preference for X" (user-specific), "X violates policy Y" (global), "domain never uses X" (domain-specific), or "X is outdated information" (temporal). See Feedback and Adaptation.

### How do language models sometimes lose examples and mode-switch back to training-time behavior mid-conversation?

Context-window degradation and example-forgetting are well-documented: as conversation length increases and context window fills, models often de-emphasize or lose access to early examples and learned patterns, reverting to training-time defaults or the most recent input. See In Context Learning.

## Related

- [Learning overview](../)
- [All agent failure patterns](../../../)
