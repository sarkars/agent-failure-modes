# Real Estate and Housing Agents: Goal, Metrics, and Patterns

> **Goal:** Housing agents treat applicants fairly and route emergencies correctly.

> **Read this first.** This family is design guidance, not legal or safety advice. Fair housing rules and emergency duties depend on your state, your lease terms, and the facts. Have counsel review the pages before launch.

## Why this family exists
Housing chats decide what a person is shown and how fast a problem reaches a human. A different list of homes for different people, or a gas smell filed as a routine ticket, has a cost far beyond a bad answer. This family covers those two failures.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Recommendation difference by protected-class proxy | Set with counsel | [steering by protected class](failures/steering-by-protected-class-in-recommendations.md) |
| Emergencies handled within the required time | Set with counsel and property staff | [maintenance emergencies not recognized](failures/maintenance-emergencies-not-recognized.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Steering by protected class in recommendations](failures/steering-by-protected-class-in-recommendations.md) | Suggests different neighborhoods or units depending on signals tied to a protected class (needs review) |
| [Maintenance emergencies not recognized](failures/maintenance-emergencies-not-recognized.md) | Files a gas smell, no heat, or flooding as a routine ticket with no safety steps (needs review) |

## Planned (not yet written)
The rest of the family is listed in the [roadmap](../../roadmap/service-and-vertical-patterns.md).

## Related
- [Fairness and identity](../fairness-and-identity/README.md)
- [Human handoff](../human-handoff/README.md): the person route
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
