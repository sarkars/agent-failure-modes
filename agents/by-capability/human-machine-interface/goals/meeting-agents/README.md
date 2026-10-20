# Meeting Agents: Goal, Metrics, and Patterns

> **Goal:** Meeting agents record, transcribe, and identify speakers only with notice and consent from the people being captured.

## Why this family exists
AI notetakers now join video calls, record audio, write summaries, and label who said what. This family covers what goes wrong when people in the meeting never learned a recorder was there, or when the tool keeps a voice template of someone who never signed up. The guidance is design guidance only, not legal advice. Have counsel read the pages marked "Read this first" before launch, and check which consent rules apply to you. Voice-channel and web-meeting signals are planned, not written.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data.
| Metric | Target | Defined in |
|---|---|---|
| Meetings with a participant-visible notice and consent | Start: 100% | [recorders that join without everyone's consent](failures/recorders-that-join-without-everyone-s-consent.md) |
| Biometric data stored without consent | Start: 0 | [voiceprints captured without consent](failures/voiceprints-captured-without-consent.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Recorders that join without everyone's consent](failures/recorders-that-join-without-everyone-s-consent.md) | An AI notetaker records people who were never told or asked |
| [Voiceprints captured without consent](failures/voiceprints-captured-without-consent.md) | A meeting assistant keeps a voice template of every speaker, including people who never signed up |

## Planned (not yet written)
The other rows of the family are tracked in the [emerging surfaces roadmap](../../roadmap/emerging-surfaces.md). Some already have an example added to a pattern elsewhere in the repository, such as meeting summaries that misattribute or invent action items.

## Related
- [Privacy and governance](../privacy-and-governance/README.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
