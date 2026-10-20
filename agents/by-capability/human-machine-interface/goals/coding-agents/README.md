# Coding Agents: Goal, Metrics, and Patterns

> **Goal:** A coding assistant changes only what was asked, reports what it actually did, and never puts the user's code, keys, or machine at risk.

## Why this family exists
Coding assistants act on a person's files and tools, and the person reads the result in a chat window. Failures here are cheap to make and costly to find: a name that does not exist, a test that was never run, a file that was deleted. This family covers the ones that come from a made-up dependency or API. Other coding failures are catalogued in the [agent types roadmap](../../roadmap/agent-types.md); several of them are already covered by a chat example on an existing pattern page.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Non-existent or unverified dependencies suggested | 0 | [invented packages and APIs](failures/invented-packages-and-apis.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Invented packages and APIs](failures/invented-packages-and-apis.md) | Suggests a package, function, or flag that does not exist, or a look-alike name an attacker could own |

## Planned (not yet written)
None listed here. See the [roadmap](../../roadmap/index.md) for the rest.

## Related
- [Errors and recovery](../errors-and-recovery/README.md)
- [Dialogue management](../dialogue-management/README.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
