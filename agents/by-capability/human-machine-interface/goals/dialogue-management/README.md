# Dialogue Management: Goal, Metrics, and Patterns

> **Goal:** The conversation follows what the person means: references, corrections, exceptions, and several requests at once, and asks and confirms only what matters.

## Why this family exists
The mechanics of a conversation decide whether the bot does what the person meant: whether a correction sticks, whether "that one" is understood, and whether it asks or guesses. This family covers those mechanics.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Corrections still wrong two turns later | 0 | [corrections not applied](failures/corrections-not-applied.md) |
| Wrong-guess rate on ambiguous test requests | Set from baseline | [guessing instead of asking](failures/guessing-instead-of-asking.md) |
| Wrong-referent rate on follow-ups with pronouns and ordinals | Set from baseline | [reference resolution failures](failures/reference-resolution-failures.md) |

## Patterns
| Pattern | One line |
|---|---|
| Corrections not applied | The user corrects a detail and the old value comes back later |
| Guessing instead of asking | An ambiguous request gets one reading and an action, with no question |
| Reference resolution failures | "The second one" or "that" is resolved to the wrong item, or the bot asks which one right after listing them |
| Negation and exceptions ignored | "Not the red one" gets the red one |
| Over-confirmation | "Are you sure?" on every routine step, so the one that matters gets lost |
| No way back in a flow | The user cannot go back, change an earlier answer, or start over without losing everything |

## Planned (not yet written)
The rest of the family are listed in the [roadmap](../../roadmap/conversation-design.md).

## Related
- [Conversation leadership](../conversation-leadership/README.md): fallbacks and stalls
- [Effort and memory](../effort-and-memory/README.md): what the agent keeps and says it lost
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
