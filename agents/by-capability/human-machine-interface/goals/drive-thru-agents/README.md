# Drive-Thru Agents: Goal, Metrics, and Patterns

> **Goal:** Voice ordering gets the order right, shows it, and never pressures or risks someone's health.

## Why this family exists
Drive-thru voice agents take real orders in noise, with a line behind the car and little time to check. This family covers the failures specific to that setting.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Order accuracy at pickup, and orders corrected by a person | Set from baseline | [order mix-ups at the speaker](failures/order-mix-ups-at-the-speaker.md) |

## Patterns
| Pattern | One line |
|---|---|
| Order mix-ups at the speaker | Items are added, dropped, or multiplied with no readback the customer can check |

## Planned (not yet written)
The rest of the family is listed in the [roadmap](../../roadmap/service-and-vertical-patterns.md).

## Related
- [Dialogue management](../dialogue-management/README.md): corrections and clarifying questions
- [Human handoff](../human-handoff/README.md): getting a person
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
