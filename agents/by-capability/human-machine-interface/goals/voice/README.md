# Voice: Goal, Metrics, and Patterns

> **Goal:** A voice agent listens, speaks, and takes turns the way a competent person would, hears every speaker accurately, never turns noise or silence into words, and never asks for what can't safely be said aloud.

## Why this family exists
Voice has no screen to edit, no scrollback, and little tolerance for delay, so failures that are small in chat are larger when spoken. This family covers the human-side failures of voice agents. Many technical voice failures are already written in the [speech and audio area](../../../speech-and-audio/README.md).

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Correction-success rate | Set from baseline | [repair failure](failures/repair-failure.md) |
| Recovery-success rate after "what?" | Set from baseline | [no repeat or recap controls](failures/no-repeat-or-recap-controls.md) |

## Patterns
| Pattern | One line |
|---|---|
| Repair failure | A spoken correction or "say that again" is not understood or applied |
| [Transcription hallucination](failures/transcription-hallucination.md) | Speech-to-text turns silence, noise, or long pauses into invented phrases that the bot then shows or acts on |
| [Word-error-rate-only evaluation](failures/word-error-rate-only-evaluation.md) | A good average word error rate hides wrong names, numbers, and dropped "not"s; report entity and critical-slot error rates next to it |
| [Dropped negations and small words](failures/dropped-negations-and-small-words.md) | Speech-to-text drops "not" or turns "can't" into "can", and the agent acts on the opposite of what was said |
| [Punctuation and segmentation errors](failures/punctuation-and-segmentation-errors.md) | Wrong sentence breaks or missing commas in a transcript change what an instruction covers |
| [No repeat or recap controls](failures/no-repeat-or-recap-controls.md) | The user missed what the agent said and "what?", "say that again", or "go back" gets a new answer, a vague apology, or nothing |
| [Atypical speech mishandled](failures/atypical-speech-mishandled.md) | Stuttering, dysarthria, or Deaf speech is cut off or misheard and the bot offers only "I didn't catch that" |
| [Fixed speaking rate and volume](failures/fixed-speaking-rate-and-volume.md) | The user asks for slower, shorter, or simpler and the next reply is the same as before |
| [IVR-style menu maze](failures/ivr-style-menu-maze.md) | Forced menus with no typed path, the same menu twice, and no way to a person |
| [Wake-word false activation](failures/wake-word-false-activation.md) | The bot answers and keeps messages that only looked like an invitation |

## Planned (not yet written)
The rest of the family is listed in the [roadmap](../../roadmap/voice.md).

## Related
- [Dialogue management](../dialogue-management/README.md): the chat version of corrections
- [Drive-thru agents](../drive-thru-agents/README.md): voice ordering
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
