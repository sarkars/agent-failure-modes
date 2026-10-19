# Response Structure, Length, and Closers: Goal, Metrics, and Patterns

> **Goal:** Replies are shaped so people can read, act on, and answer them, and short messages like "ok" and "bye" get the response the moment calls for.

## Why this family exists
The shape of a reply decides whether the user can act on it: where the answer sits, how long it runs, and what happens when the user's message is only "ok" or "thanks". This family covers those failures in chat.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Handling correctness on labelled acknowledgment and closer turns | Over 95% | [no reply to acknowledgments and closers](failures/no-reply-to-acknowledgments-and-closers.md) |

## Patterns
| Pattern | One line |
|---|---|
| No reply to acknowledgments and closers | The user says "ok", "thanks", or "bye" and the bot stays silent, restarts, or repeats its last question |

## Planned (not yet written)
Answer buried, wall of text, over-long replies, and the rest of the family are listed in the [roadmap](../../roadmap/response-structure-and-length.md).

## Related
- [Conversation leadership](../conversation-leadership/README.md): the bot's own turn endings and fallbacks
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
