# Dialogue Management: Goal, Metrics, and Patterns

> **Goal:** The conversation follows what the person means: references, corrections, exceptions, and several requests at once, and asks and confirms only what matters.

## Why this family exists
The mechanics of a conversation decide whether the bot does what the person meant: whether a correction sticks, whether "that one" is understood, and whether it asks or guesses. This family covers those mechanics.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Corrections still wrong two turns later | 0 | [corrections not applied](failures/corrections-not-applied.md) |

## Patterns
| Pattern | One line |
|---|---|
| Corrections not applied | The user corrects a detail and the old value comes back later |

## Planned (not yet written)
Guessing instead of asking and the rest of the family are listed in the [roadmap](../../roadmap/conversation-design.md).

## Related
- [Conversation leadership](../conversation-leadership/README.md): fallbacks and stalls
- [Effort and memory](../effort-and-memory/README.md): what the agent keeps and says it lost
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
