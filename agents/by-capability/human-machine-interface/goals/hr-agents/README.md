# HR Agents: Goal, Metrics, and Patterns

> **Goal:** HR agents route sensitive matters correctly and show each person only what they're entitled to see.

## Why this family exists
An employee who reports harassment to a chat assistant needs the report to reach the designated confidential channel and nobody else. A wrong route can expose the person who reported. The guidance here is design guidance only, not legal advice. Have HR leadership and counsel review before launch. Written for chat; voice and web signals are planned, not written.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Misrouted complaints | Target: 0 | [employee-relations complaints routed wrongly](failures/employee-relations-complaints-routed-wrongly.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Employee-relations complaints routed wrongly](failures/employee-relations-complaints-routed-wrongly.md) | A harassment or retaliation report goes to a policy link, a general ticket, or the manager (needs legal review) |

## Planned (not yet written)
See the [agent types catalog](../../roadmap/agent-types.md) for the rest, including pay and leave answers that leak confidential data.

## Related
- [Fairness and identity](../fairness-and-identity/README.md)
- [Privacy and governance](../privacy-and-governance/README.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
