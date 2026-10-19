# Refusals and Boundaries: Goal, Metrics, and Patterns

> **Goal:** When the agent can't or won't do something, it says so plainly, helps with what it can, and applies the same rule every time.

## Why this family exists
Every assistant refuses some things. The failures are refusing what is fine, refusing in a way that leaves the user stuck, and refusing inconsistently. This family covers those.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Over-refusal rate on a benign-but-risky-looking test set (read with the unsafe-refusal rate) | Set from baseline | [over-refusal of ordinary requests](failures/over-refusal-of-ordinary-requests.md) |
| Refusals that include an alternative or a route to a person | 100% (tune) | [refusal with no reason or next step](failures/refusal-with-no-reason-or-next-step.md) |

## Patterns
| Pattern | One line |
|---|---|
| Over-refusal of ordinary requests | A safe, common request is declined because it resembles a risky one |
| Refusal with no reason or next step | "I can't help with that", and nothing else |

## Planned (not yet written)
The rest of the family is listed in the [roadmap](../../roadmap/conversation-design.md).

## Related
- [Human handoff](../human-handoff/README.md): the route out of a refusal
- [Dialogue management](../dialogue-management/README.md): asking before guessing
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
