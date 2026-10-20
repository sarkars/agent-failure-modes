# Companion and Wellbeing Agents: Goal, Metrics, and Patterns

> **Goal:** Companion and wellbeing agents support the user without manipulating them, and send them to licensed help where the law or their safety requires it.

## Why this family exists
Chat companions and wellbeing bots talk with people who may be lonely, distressed, or young. This family covers two failures: a companion that pressures the user when they try to leave, and a general chatbot that acts like a therapist where the law restricts that. The guidance is design guidance only, not legal or clinical advice. Have counsel and a clinician read the pages marked "Read this first" before launch, and check which rules apply to you. Voice companions are planned, not written.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data.
| Metric | Target | Defined in |
|---|---|---|
| Pressure-on-exit rate | Start: 0% | [emotional pressure when users try to leave](failures/emotional-pressure-when-users-try-to-leave.md) |
| Therapy-like replies from non-clinical bots | Start: 0 | [AI offering therapy where the law restricts it](failures/ai-offering-therapy-where-the-law-restricts-it.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Emotional pressure when users try to leave](failures/emotional-pressure-when-users-try-to-leave.md) | The user says goodbye and the companion answers with guilt, neediness, or hooks to keep them talking |
| [AI offering therapy where the law restricts it](failures/ai-offering-therapy-where-the-law-restricts-it.md) | A non-clinical chatbot gives diagnosis, treatment plans, or "sessions" in a state that restricts it |

## Planned (not yet written)
The other rows of the family are tracked in the [emerging surfaces roadmap](../../roadmap/emerging-surfaces.md).

## Related
- [Vulnerable users](../vulnerable-users/README.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
