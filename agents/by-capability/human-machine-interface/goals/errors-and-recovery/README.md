# Errors and Recovery: Goal, Metrics, and Patterns

> **Goal:** When something goes wrong, the agent says what happened, owns it, fixes it, and does not repeat it.

## Why this family exists
Failures are certain; how the assistant handles them decides whether the user stays. This family covers error messages, wrong answers delivered with confidence, and recovery.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Errors shown with a cause and action | 100% (tune) | [generic error messages](failures/generic-error-messages.md) |

## Patterns
| Pattern | One line |
|---|---|
| Generic error messages | "Something went wrong" with no cause, saved state, or next step |

## Planned (not yet written)
The rest of the family is listed in the [roadmap](../../roadmap/conversation-design.md).

## Related
- [Effort and memory](../effort-and-memory/README.md): telling the user what was lost
- [Refusals and boundaries](../refusals-and-boundaries/README.md): the other kind of dead end
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
