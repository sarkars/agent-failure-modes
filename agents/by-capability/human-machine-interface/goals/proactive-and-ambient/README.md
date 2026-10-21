# Proactive and Ambient Agents: Goal, Metrics, and Patterns

> **Goal:** Proactive and always-listening agents speak up only when invited or useful, and respect a no.

## Why this family exists
An assistant that messages first has one chance to be welcome. Bad timing, repeated suggestions after a dismissal, digests nobody reads and devices that act on talk not meant for them all teach people to switch the assistant off. Written for chat and in-app assistants; voice and always-listening signals are planned, not written. The ambient pattern needs legal review before use.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Dismissals within 5 seconds | Under 20% (starting point) | [interrupts at a bad moment](failures/interrupts-at-a-bad-moment.md) |
| Digest open rate and action rate | Set from your baseline, then rise | [summaries and digests too long to read](failures/summaries-and-digests-too-long-to-read.md) |
| Activations without invitation | 0 that lead to an action | [ambient assistants act on overheard conversation](failures/ambient-assistants-act-on-overheard-conversation.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Interrupts at a bad moment](failures/interrupts-at-a-bad-moment.md) | A message to the user lands while they type or fill a form, and is closed unread |
| [Dismissed suggestions come back](failures/dismissed-suggestions-come-back.md) | The assistant repeats a suggestion the user already dismissed |
| [Summaries and digests too long to read](failures/summaries-and-digests-too-long-to-read.md) | A daily summary runs longer than the items it covers, so it is skipped |
| [Ambient assistants act on overheard conversation](failures/ambient-assistants-act-on-overheard-conversation.md) | An always-on device replies or acts on talk not meant for it (needs legal review) |

## Planned (not yet written)
See the [agent types catalog](../../roadmap/agent-types.md) for the rest.

## Related
- [Privacy and governance](../privacy-and-governance/README.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
