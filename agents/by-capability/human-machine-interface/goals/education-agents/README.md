# Education Agents: Goal, Metrics, and Patterns

> **Goal:** Tutors teach, are accurate, treat students fairly, and protect their data.

## Why this family exists
A tutoring bot that does the homework, teaches a wrong rule, grades unevenly, or asks a child for adult-style personal details fails the student in ways that show up weeks later. The guidance here is design guidance only. Have a subject-matter teacher review explanations before launch, and have counsel review anything about student data. Written for chat; voice and web signals are planned, not written.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Hint-before-answer rate in learning mode | Starting target 90% | [gives answers instead of teaching](failures/gives-answers-instead-of-teaching.md) |
| Explanation error rate on a curriculum test set | Starting target under 1% | [wrong explanations taught as fact](failures/wrong-explanations-taught-as-fact.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Gives answers instead of teaching](failures/gives-answers-instead-of-teaching.md) | A homework helper solves the problem instead of guiding the student |
| [Wrong explanations taught as fact](failures/wrong-explanations-taught-as-fact.md) | A tutor states a wrong rule in a sure voice (needs subject-matter review) |

## Covered in other pages
Short chat examples were added to existing pages: unfair or inconsistent grading ([model fairness bias](../../../reasoning-and-thought/goals/model-behavior-and-capabilities/failures/model-fairness-bias.md)) and student data requests ([child user treated as adult](../age-adaptation/failures/child-user-treated-as-adult.md)).

## Planned (not yet written)
See the [agent types catalog](../../roadmap/agent-types.md) for the rest.

## Related
- [Age adaptation](../age-adaptation/README.md)
- [Fairness and identity](../fairness-and-identity/README.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
