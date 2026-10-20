# Measurement and Feedback: Goal, Metrics, and Patterns

> **Goal:** Teams can tell whether conversations really work, and users can tell the team when they don't.

## Why this family exists
A chat product can look healthy on a dashboard while users struggle, and users who see a wrong or harmful reply often have no way to say so. This family covers both halves: how teams measure conversations, and how users report problems so the report reaches a person who can fix the cause.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Reports per 1,000 conversations; time to triage | Set from your own baseline | [no way to report bad behaviour](failures/no-way-to-report-bad-behaviour.md) |

## Patterns
| Pattern | One line |
|---|---|
| [No way to report bad behaviour](failures/no-way-to-report-bad-behaviour.md) | Users cannot flag a wrong or harmful reply, or the report goes nowhere |

## Planned (not yet written)
- Survey bias
- Reviewing only failures
- Tone changes shipped with no regression test
- Clean-lab testing

## Related
- [Metrics hub](../../reference/metrics.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
