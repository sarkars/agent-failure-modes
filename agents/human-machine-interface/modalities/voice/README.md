# Voice: Human-Machine Interface Patterns (PLANNED)

> **Status: planned, no patterns written yet.** This page reserves the scope so voice can be added without changing the structure.

## Scope
Phone agents, smart speakers, in-car and in-app voice assistants. Failures in how voice agents listen, speak, take turns, and handle what can't be said aloud.

## Core patterns that will get a voice note or variant
The [core patterns](../../README.md) apply to voice. Each already has a "Modality notes (PLANNED)" line describing what changes. Examples: disclose the AI in the first sentence; ask one question at a time; confirm aloud before consequential actions.

> **Full list:** 24 voice patterns with goals and metrics are in the [voice roadmap](../../roadmap/voice.md). The table below is the original short list.

## Planned voice-specific patterns
| Planned pattern | What it will cover |
|---|---|
| Barge-in and interruption handling | Talking over the user, or ignoring interruptions |
| Dead air and latency | Silence that feels like a dropped call |
| Dense information read aloud | Prices, terms, and lists that can't be held in memory |
| Speech-recognition gaps by accent and dialect | Unequal accuracy before the model sees the request |
| Spoken sensitive data | Card numbers and passwords spoken and transcribed; keypad masking |
| Prosody and tone mismatch | Cheerful voice on bad news |
| Turn-taking and endpointing | Cutting users off, or waiting too long |
| Voice-to-visual handoff | Sending a text or app screen when the topic needs to be seen |

## Related existing material
- [Speech and audio capability patterns](../../../by-capability/speech-and-audio/README.md): technical failures (recognition, synthesis). Voice HMI patterns will cover experience failures and link there.
