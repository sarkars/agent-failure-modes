# Difficult Customers: Goal, Metrics, and Patterns

> **Goal:** Angry users end the conversation calmer, or with a person, not angrier.

## Why this family exists
Anger is predictable, and bots that quote policy or apologise generically make it worse. The fix is a change of tactics at known triggers and a clean handoff.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Correct escalation on trigger cases | Over 95% | [no de escalation strategy](failures/no-de-escalation-strategy.md) |
| Policy-first replies in angry threads | Under 2% | no de escalation strategy |
| Handoff after 3 or more negative turns | Over 90% | no de escalation strategy |
| Boundary-then-escalation compliance rate | Over 95% | [mishandled abuse](failures/mishandled-abuse.md) |

## Patterns
| Pattern | One line |
|---|---|
| No de-escalation strategy | Quotes policy at angry customers and never changes tactics |
| [Mishandled abuse](failures/mishandled-abuse.md) | Ignores, mirrors, or punishes abuse instead of one calm boundary |

## Planned (not yet written)
None listed here. See the [roadmap](../../roadmap/index.md) for the rest.

## Related
- [Emotional intelligence](../emotional-intelligence/README.md)
- [Channel selection](../channel-selection/README.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
