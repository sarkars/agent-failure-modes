# Voice: Goal, Metrics, and Patterns

> **Goal:** A voice agent listens, speaks, and takes turns the way a competent person would, hears every speaker accurately, never turns noise or silence into words, and never asks for what can't safely be said aloud.

## Why this family exists
Voice has no screen to edit, no scrollback, and little tolerance for delay, so failures that are small in chat are larger when spoken. This family covers the human-side failures of voice agents. Many technical voice failures are already written in the [speech and audio area](../../../speech-and-audio/README.md).

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Correction-success rate | Set from baseline | [repair failure](failures/repair-failure.md) |

## Patterns
| Pattern | One line |
|---|---|
| Repair failure | A spoken correction or "say that again" is not understood or applied |
| [Transcription hallucination](failures/transcription-hallucination.md) | Speech-to-text turns silence, noise, or long pauses into invented phrases that the bot then shows or acts on |

## Planned (not yet written)
The rest of the family is listed in the [roadmap](../../roadmap/voice.md).

## Related
- [Dialogue management](../dialogue-management/README.md): the chat version of corrections
- [Drive-thru agents](../drive-thru-agents/README.md): voice ordering
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
