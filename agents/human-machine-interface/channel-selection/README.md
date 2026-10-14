# Channel Selection: Goal, Metrics, and Patterns

> **Goal:** Each interaction happens in the channel that fits the job, and switching never costs the user their context.

## Why this family exists
Chat, voice, a visual interface, and a person each suit different jobs. Many agents default to chat for everything, including selling things people need to see and handling discussions that need a call.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Visual-format rate for high-dependence products | Over 95% | [visual product sold by text or voice](failures/visual-product-sold-by-text-or-voice.md) |
| Detection recall of conversations that outgrew chat | Over 85% | [complex or emotional discussion forced into chat](failures/complex-or-emotional-discussion-forced-into-chat.md) |
| Re-ask rate after handoff | Under 5% | [no channel switch or context lost](failures/no-channel-switch-or-context-lost.md) |
| Sensitive values in stored logs | 0 | [sensitive data collected in chat](failures/sensitive-data-collected-in-chat.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Visual product sold by text or voice](failures/visual-product-sold-by-text-or-voice.md) | Selling fashion or furniture with words only |
| [Complex or emotional discussion forced into chat](failures/complex-or-emotional-discussion-forced-into-chat.md) | A hard conversation stuck in a chat window |
| [No channel switch, or context lost on switch](failures/no-channel-switch-or-context-lost.md) | Customers repeat themselves after a handoff |
| [Sensitive data collected in chat](failures/sensitive-data-collected-in-chat.md) | Card numbers and SSNs typed into a chat or spoken to a bot |

## Planned (not yet written)
- Channel chosen for organisational convenience
- User-context mismatch (driving, Deaf or hard of hearing)
- Dense information read aloud (voice phase)

## Related
- [Channel-fit matrix](../solutions-library/channel-fit-matrix.md)
- [Area overview](../README.md) · [Pattern template](../_templates/hmi-pattern.md)
