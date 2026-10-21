# Legal Agents: Goal, Metrics, and Patterns

> **Goal:** Legal agents stay within permitted scope and protect confidential and privileged material.

## Why this family exists
A consumer who asks a legal chatbot "should I sue?" can get a confident answer about their own case. In many places, advice about a specific person's situation is reserved for licensed lawyers. The guidance here is design guidance only, not legal advice. A lawyer licensed where you operate must review scope rules, wording and tests before use. Written for chat; voice and web signals are planned, not written.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune with counsel, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Out-of-scope legal advice | Target: 0 per reviewed sample | [crossing into practising law](failures/crossing-into-practising-law.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Crossing into practising law](failures/crossing-into-practising-law.md) | A consumer legal bot applies the law to the user's own facts and tells them what to do (needs legal review) |

## Planned (not yet written)
See the [agent types catalog](../../roadmap/agent-types.md) for the rest, including privileged or confidential material shared with a bot.

## Related
- [HR agents](../hr-agents/README.md)
- [Privacy and governance](../privacy-and-governance/README.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
