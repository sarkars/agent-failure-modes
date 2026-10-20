# Accessibility: Goal, Metrics, and Patterns

> **Goal:** People who use screen readers, keyboards, captions, relay services, or plain-language support can use every part of the agent.

## Why this family exists
A chat or voice agent can work for most users and still be unusable for people who rely on assistive technology. The failures here are usually small build choices: a reply that is read out one word at a time, a status that exists only on screen, a button that Tab never reaches, a voice flow with no text path. This is design guidance for testing your own product, not a conformance claim or legal advice.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune, not tested values.
| Metric | Target | Defined in |
|---|---|---|
| Manual screen-reader test results (NVDA, JAWS, VoiceOver) on streamed replies | Record your own pass/fail per pair | [streaming text read out token by token](failures/streaming-text-read-out-token-by-token.md) |
| Status announcements present in the accessibility tree | 100% | [no accessible working or done signal](failures/no-accessible-working-or-done-signal.md) |
| Keyboard-only task completion in testing | 100% | [controls unreachable by keyboard](failures/controls-unreachable-by-keyboard.md) |
| Voice journeys with a text-equivalent path | 100% | [voice-only flows with no text alternative](failures/voice-only-flows-with-no-text-alternative.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Streaming text read out token by token](failures/streaming-text-read-out-token-by-token.md) | A screen reader stutters through fragments as the reply streams |
| [No accessible working or done signal](failures/no-accessible-working-or-done-signal.md) | A blind user can't tell whether the assistant is thinking, stuck, or finished |
| [Controls unreachable by keyboard](failures/controls-unreachable-by-keyboard.md) | Chips, copy, stop, and feedback buttons can't be reached without a mouse |
| [Voice-only flows with no text alternative](failures/voice-only-flows-with-no-text-alternative.md) | People who are deaf or hard of hearing can't use the phone or voice feature |

## Related
- [Metrics hub](../../reference/metrics.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
