# Measurement and Feedback: Goal, Metrics, and Patterns

> **Goal:** Teams can tell whether conversations really work, and users can tell the team when they don't.

## Why this family exists
A chat product can look healthy on a dashboard while users struggle, and users who see a wrong or harmful reply often have no way to say so. This family covers both halves: how teams measure conversations, and how users report problems so the report reaches a person who can fix the cause.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Reports per 1,000 conversations; time to triage | Set from your own baseline | [no way to report bad behaviour](failures/no-way-to-report-bad-behaviour.md) |
| Survey response rate by outcome | Every outcome group reported; none far below the highest | [survey bias](failures/survey-bias.md) |
| Share of reviewed conversations that are random samples | Starting point: at least 50% | [reviewing only failures](failures/reviewing-only-failures.md) |
| Tone scores before and after each release | Starting point: mean drop of 0.2 or less on a 1-5 scale | [tone changes shipped with no regression test](failures/tone-changes-shipped-with-no-regression-test.md) |
| Performance gap between lab and field inputs | Starting point: under 5 points of task success | [clean-lab testing](failures/clean-lab-testing.md) |

## Patterns
| Pattern | One line |
|---|---|
| [No way to report bad behaviour](failures/no-way-to-report-bad-behaviour.md) | Users cannot flag a wrong or harmful reply, or the report goes nowhere |
| [Survey bias](failures/survey-bias.md) | Satisfaction surveys reach only the angriest and the happiest, or only users who finished |
| [Reviewing only failures](failures/reviewing-only-failures.md) | Quality review reads complaints and misses users who quietly give up |
| [Tone changes shipped with no regression test](failures/tone-changes-shipped-with-no-regression-test.md) | A prompt edit makes the bot curt, and nobody notices |
| [Clean-lab testing](failures/clean-lab-testing.md) | Tests use tidy input, so real typos and fragments fail in the field |

## Related
- [Metrics hub](../../reference/metrics.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
