# Drive-Thru Agents: Goal, Metrics, and Patterns

> **Goal:** Voice ordering gets the order right, shows it, and never pressures or risks someone's health.

## Why this family exists
Drive-thru voice agents take real orders in noise, with a line behind the car and little time to check. This family covers the failures specific to that setting.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Order accuracy at pickup, and orders corrected by a person | Set from baseline | [order mix-ups at the speaker](failures/order-mix-ups-at-the-speaker.md) |
| Modifier errors per 100 customized orders | Set from baseline | [modifiers and customizations misparsed](failures/modifiers-and-customizations-misparsed.md) |
| Upsell offers repeated after a decline | 0 (starting point) | [upsell pressure at the speaker](failures/upsell-pressure-at-the-speaker.md) |
| Mismatches between display and spoken readback | 0 (starting point) | [screen and spoken order disagree](failures/screen-and-spoken-order-disagree.md) |
| Allergy flags that reach the kitchen | 100% (starting point) | [allergy and dietary requests handled loosely](failures/allergy-and-dietary-requests-handled-loosely.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Order mix-ups at the speaker](failures/order-mix-ups-at-the-speaker.md) | Items are added, dropped, or multiplied with no readback the customer can check |
| [Modifiers and customizations misparsed](failures/modifiers-and-customizations-misparsed.md) | "No pickles, extra sauce" lands on the wrong item or is dropped |
| [Upsell pressure at the speaker](failures/upsell-pressure-at-the-speaker.md) | The bot keeps offering add-ons after a no |
| [Screen and spoken order disagree](failures/screen-and-spoken-order-disagree.md) | The display shows one order and the voice reads back another |
| [Allergy and dietary requests handled loosely](failures/allergy-and-dietary-requests-handled-loosely.md) | A stated allergy is dropped or the bot promises safety (needs expert and legal review) |

## Planned (not yet written)
The rest of the family is listed in the [roadmap](../../roadmap/service-and-vertical-patterns.md).

## Related
- [Dialogue management](../dialogue-management/README.md): corrections and clarifying questions
- [Human handoff](../human-handoff/README.md): getting a person
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
