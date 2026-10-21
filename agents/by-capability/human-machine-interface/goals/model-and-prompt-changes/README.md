# Model and Prompt Changes: Goal, Metrics, and Patterns

> **Goal:** Changes to the model or prompt never surprise users: they are tested, announced, and reversible.

## Why this family exists
Teams change the model, the system prompt, and the experiment setup behind a chat assistant all the time. Users see only the result: a bot that suddenly answers differently, refuses more, or behaves one way for them and another way for a friend. This family covers how those changes are made, tested, and rolled back. Guidance only; test on your own data.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data.
| Metric | Target | Defined in |
|---|---|---|
| Regressions per prompt change | Start: 0 shipped regressions in topics the change note says must not change | [prompt edits by non-engineers break other behavior](failures/prompt-edits-by-non-engineers-break-other-behavior.md) |
| Cross-arm contamination in tests | 0 | [memory contaminates conversation experiments](failures/memory-contaminates-conversation-experiments.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Prompt edits by non-engineers break other behavior](failures/prompt-edits-by-non-engineers-break-other-behavior.md) | A fix for one conversation changes others nobody retested |
| [Memory contaminates conversation experiments](failures/memory-contaminates-conversation-experiments.md) | Remembered state carries across A/B test arms and mixes the results |

## Examples added to patterns elsewhere
- A model change shifts personality, length, or refusals: a chat example in [silent model update](../../../reasoning-and-thought/goals/model-updates-and-versioning/failures/silent-model-update.md).
- Fallback model gives a visibly different experience: a chat example in [model downgrade silent failure](../../../reasoning-and-thought/goals/model-selection-and-routing/failures/model-downgrade-silent-failure.md).
- Quiet degradation under peak load: a chat example in [queue backpressure](../../../../cross-cutting/operations/goals/real-time-performance/failures/queue-backpressure.md).

## Related
- [Tone changes shipped with no regression test](../measurement-and-feedback/failures/tone-changes-shipped-with-no-regression-test.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
