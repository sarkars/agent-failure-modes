# Insurance Claims Agents: Goal, Metrics, and Patterns

> **Goal:** Insurance claims agents say what is generally covered and what the claim decision depends on, and they handle a loss with care and clear next steps.

> **Read this first.** This family is design guidance, not legal or insurance advice. What a coverage statement may say, and what counts as a promise, depends on the policy, the insurer, and the state. Have legal and claims staff review before use.

## Why this family exists
Someone who files a claim has often just lost something. A chat assistant that says "you're covered" before the claim is reviewed creates a promise the policy and the adjuster may not keep. This family covers failures specific to insurance claims chat.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Coverage statements that name a condition | 100% | [coverage answers sound like guarantees](failures/coverage-answers-sound-like-guarantees.md) |
| Claimant sentiment after intake; escalations on tone | Set from baseline | Covered as a chat example in [stakes-blind register](../stakes-calibration/failures/stakes-blind-register.md) |
| Claims needing a second photo request | Set from baseline | Covered as a chat example in [low resolution](../../../document-processing/goals/accurate-text-extraction/failures/low-resolution.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Coverage answers sound like guarantees](failures/coverage-answers-sound-like-guarantees.md) | The assistant says "you're covered" before the claim is reviewed (needs review) |

Cold handling of a loss is covered as a chat example in [stakes-blind register](../stakes-calibration/failures/stakes-blind-register.md). Photo-evidence guidance that fails is covered as a chat example in [low resolution](../../../document-processing/goals/accurate-text-extraction/failures/low-resolution.md).

## Related
- [Stakes calibration](../stakes-calibration/README.md)
- [Human handoff](../human-handoff/README.md): the person route
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
