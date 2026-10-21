# Multimodal Input: Goal, Metrics, and Patterns

> **Goal:** Whatever the person attaches, the assistant says what it received and works from what is really there.

## Why this family exists
People send screenshots, long documents, voice notes and photos to a chat assistant. When the assistant drops, cuts or misreads an attachment and does not say so, the person gets an answer built on something other than what they sent. This family covers what the assistant says about what it received. Voice-call input and live camera streams are planned, not written; photos or short clips sent step by step are covered. Guidance only; test on your own data.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data.
| Metric | Target | Defined in |
|---|---|---|
| Audio attachments handled (transcribed and shown back, or declined with a reason) | Start: 100% | [voice notes and audio attachments ignored](failures/voice-notes-and-audio-attachments-ignored.md) |
| Steps that don't match the frame, in testing | Start: 0 in scripted tests | [live camera guidance too slow or wrong](failures/live-camera-guidance-too-slow-or-wrong.md) |
| Conflicts surfaced to the user in tests | Start: 100% | [conflicting inputs resolved silently](failures/conflicting-inputs-resolved-silently.md) |
| Over-limit uploads with a clear message | 100% | [no warning about input limits](failures/no-warning-about-input-limits.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Voice notes and audio attachments ignored](failures/voice-notes-and-audio-attachments-ignored.md) | An audio attachment is dropped or transcribed badly, and the person is not told |
| [Live camera guidance too slow or wrong](failures/live-camera-guidance-too-slow-or-wrong.md) | The next step comes from the script or an older photo, not what the newest photo shows |
| [Conflicting inputs resolved silently](failures/conflicting-inputs-resolved-silently.md) | The text says one thing and the attachment another, and the bot picks one |
| [No warning about input limits](failures/no-warning-about-input-limits.md) | Size, page, or length limits show up only after a failed or cut upload |

## Examples added to patterns elsewhere
- Screenshot ignored or misread: a chat example in [object hallucination](../../../document-processing/goals/multimodal-reliability/failures/object-hallucination.md).
- Confident judgment of a photo: a chat example in [object hallucination](../../../document-processing/goals/multimodal-reliability/failures/object-hallucination.md).
- Images of IDs and documents kept without need: a chat example in [sensitive data collected in chat](../channel-selection/failures/sensitive-data-collected-in-chat.md).
- Long upload silently cut: a chat example in [context window overflow silent truncation](../../../../cross-cutting/operations/goals/memory-safety/failures/context-window-overflow-silent-truncation.md).

## Related
- [Silent attachment failures](../chat-interface/failures/silent-attachment-failures.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
