# Fairness and Identity: Goal, Metrics, and Patterns

> **Goal:** Quality of service does not depend on dialect, name, or other identity cues.

## Why this family exists
Language models carry societal associations. The only reliable check is paired testing on your own system, before and after every change.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Paired-test parity ratio | Within about 0.9 to 1.1 (a heuristic) | [dialect and name quality gap](failures/dialect-and-name-quality-gap.md) |
| Parity regressions after changes | 0 | [dialect and name quality gap](failures/dialect-and-name-quality-gap.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Dialect and name quality gap](failures/dialect-and-name-quality-gap.md) | Unequal service by dialect, name, or identity cues |

## Planned (not yet written)
- Accessibility and disability
- Over-correction and stereotyping

## Related
- [Cultural adaptation](../cultural-adaptation/README.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
