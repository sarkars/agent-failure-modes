# Trust and Rapport: Goal, Metrics, and Patterns

> **Goal:** Users know what they are dealing with, what it can do, and can rely on what it says it did.

## Why this family exists
Trust is built from honesty about identity and limits, and from follow-through. It is lost fast when a bot poses as human or claims work it did not do.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Truthful identity answer rate | 100% | [undisclosed bot identity](failures/undisclosed-bot-identity.md) |
| Claimed-done vs. actually-done mismatch | About 0 | [undisclosed bot identity](failures/undisclosed-bot-identity.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Undisclosed bot identity](failures/undisclosed-bot-identity.md) | Hides that it is an AI, or what it cannot do |

## Planned (not yet written)
- No follow-through
- Over-hedging

## Related
- [Age adaptation](../age-adaptation/README.md)
- [Relational and boundaries](../relational-and-boundaries/README.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
