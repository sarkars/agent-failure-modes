# Multimodal Input: Goal, Metrics, and Patterns

> **Goal:** Whatever the person attaches, the assistant says what it received and works from what is really there.

## Why this family exists
People send screenshots, long documents, voice notes and photos to a chat assistant. When the assistant drops, cuts or misreads an attachment and does not say so, the person gets an answer built on something other than what they sent. This family covers what the assistant says about what it received. Voice-call and live-camera input are planned, not written. Guidance only; test on your own data.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data.
| Metric | Target | Defined in |
|---|---|---|
| Audio attachments handled (transcribed and shown back, or declined with a reason) | Start: 100% | [voice notes and audio attachments ignored](failures/voice-notes-and-audio-attachments-ignored.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Voice notes and audio attachments ignored](failures/voice-notes-and-audio-attachments-ignored.md) | An audio attachment is dropped or transcribed badly, and the person is not told |

## Examples added to patterns elsewhere
- Screenshot ignored or misread: a chat example in [object hallucination](../../../document-processing/goals/multimodal-reliability/failures/object-hallucination.md).
- Long upload silently cut: a chat example in [context window overflow silent truncation](../../../../cross-cutting/operations/goals/memory-safety/failures/context-window-overflow-silent-truncation.md).

## Related
- [Silent attachment failures](../chat-interface/failures/silent-attachment-failures.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
