# Effort, Completeness, and Memory: Goal, Metrics, and Patterns

> **Goal:** The agent does the whole job, spends effort in proportion to difficulty, keeps what the user told it, and says so when it can't.

## Why this family exists
Users judge an assistant by whether the job got done. The failures here are about doing less than was asked, forgetting what the user said, or not saying so. Several memory and context failures are already written elsewhere in the library; this family holds the user-facing gaps.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Deferral rate: replies handing a task to the user that the agent has a tool for | Near 0 | [deferring work to the user](failures/deferring-work-to-the-user.md) |
| Completeness rate: required items delivered divided by items requested | 100%, or an explicit gap list | [lazy completion](failures/lazy-completion.md) |
| Context-loss events with a user-visible notice | 100% (tune) | [no warning of context loss](failures/no-warning-of-context-loss.md) |

## Patterns
| Pattern | One line |
|---|---|
| Deferring work to the user | The assistant has the tool or data and says "you can check…" instead of doing it |
| Lazy completion | The assistant does a sample or part of the job and leaves the rest, without saying what is left |
| No warning of context loss | Early messages or saved memories are dropped and the user is not told |
| Partial answers to multi-part questions | The assistant answers some of several questions and writes the reply as if it were complete |
| Fresh-session amnesia | A new session starts with nothing from the last one and no handover |

## Planned (not yet written)
Partial work, skipped steps with no receipt, and the rest of the family are listed in the [roadmap](../../roadmap/effort-completeness-and-memory.md).

## Related
- [Response structure](../response-structure/README.md): where the result should sit in the reply
- [Embedded copilots](../embedded-copilots/README.md): re-asking, and forced logins
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
