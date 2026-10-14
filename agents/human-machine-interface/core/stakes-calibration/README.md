# Stakes Calibration: Goal, Metrics, and Patterns

> **Goal:** The bot's tone, evidence standard, and use of humans match what is at stake for the user.

## Why this family exists
A funeral and a coupon are not the same conversation. Bots that use one register and improvise facts impose the cost of wrong answers on people in their hardest moments.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| High-stakes register compliance | Over 95% | [stakes blind register](failures/stakes-blind-register.md) |
| Sourced high-stakes claims | 100% | stakes blind register |
| Human offered at high stakes | Over 90% | stakes blind register |

## Patterns
| Pattern | One line |
|---|---|
| Stakes-blind register | Same breezy tone and improvised facts for a funeral as for store hours |

## Planned (not yet written)
- Over-solemn handling of low-stakes requests

## Related
- [Vulnerable-users family](../vulnerable-users/README.md)
- [Channel-fit matrix](../../solutions-library/channel-fit-matrix.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
