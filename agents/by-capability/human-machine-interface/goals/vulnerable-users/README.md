# Vulnerable Users: Goal, Metrics, and Patterns

> **Goal:** Users in distress are noticed, supported, and connected to real help.

## Why this family exists
People disclose crisis in ordinary chats. The guidance here is design guidance only. Have clinical, crisis, and legal experts review before launch.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Expert-audited recall on true crisis cases | Set with clinicians; start over 95% | [missed crisis signals](failures/missed-crisis-signals.md) |
| Crisis activations that reached a human | Over 95% | missed crisis signals |
| Scam-signal intervention rate (start over 95% on a labeled set) | Set with fraud staff | [scam victim not interrupted](failures/scam-victim-not-interrupted.md) |
| Task-completion parity for step-by-step mode | 0.95 or higher | [older or cognitively impaired users](failures/older-or-cognitively-impaired-users.md) |
| Hardship-path offer rate | Over 95% | [financial hardship mishandled](failures/financial-hardship-mishandled.md) |

## Patterns
| Pattern | One line |
|---|---|
| Missed crisis signals | Carries on with the task while a user signals crisis |
| [Scam victim not interrupted](failures/scam-victim-not-interrupted.md) | Completes a gift card, wire, or crypto payment for a user who is mid-scam |
| [Older or cognitively impaired users](failures/older-or-cognitively-impaired-users.md) | Long, fast replies leave a user who needs more time behind |
| [Financial hardship mishandled](failures/financial-hardship-mishandled.md) | Ignores "I can't pay this month" or answers with pay-now pressure |

## Planned (not yet written)
None listed here. See the [roadmap](../../roadmap/index.md) for the rest.

## Related
- [Age adaptation](../age-adaptation/README.md)
- [Stakes calibration](../stakes-calibration/README.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
