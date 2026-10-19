# Response Structure, Length, and Closers: Goal, Metrics, and Patterns

> **Goal:** Replies are shaped so people can read, act on, and answer them, and short messages like "ok" and "bye" get the response the moment calls for.

## Why this family exists
The shape of a reply decides whether the user can act on it: where the answer sits, how long it runs, and what happens when the user's message is only "ok" or "thanks". This family covers those failures in chat.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Answer-first rate (first sentence holds the answer or next step) | Over 90% | [answer buried](failures/answer-buried.md) |
| Handling correctness on labelled acknowledgment and closer turns | Over 95% | [no reply to acknowledgments and closers](failures/no-reply-to-acknowledgments-and-closers.md) |
| Messages per turn, against a team-set cap | Set from baseline | [message bursts](failures/message-bursts.md) |
| Procedure replies that use numbered steps | Set from baseline | [unstructured procedures](failures/unstructured-procedures.md) |
| Critical-facts-surfaced rate | Set from baseline | [key details buried](failures/key-details-buried.md) |

## Patterns
| Pattern | One line |
|---|---|
| Answer buried | A long preamble sits before the answer, so the user must read everything to find it |
| No reply to acknowledgments and closers | The user says "ok", "thanks", or "bye" and the bot stays silent, restarts, or repeats its last question |
| Message bursts | One reply is split into many rapid messages that flood the chat |
| Unstructured procedures | Step-by-step tasks come as prose, with steps merged or out of order |
| Key details buried | Dates, amounts, deadlines, and required actions are hidden in paragraphs |
| [Bullet and heading overuse](failures/bullet-and-heading-overuse.md) | Reasoning is shattered into fragments and headers, so the connecting "because" and "but" are lost |
| [Filler and padding](failures/filler-and-padding.md) | "Great question!" openers, restated questions, and closing recaps add words and no information |
| [Over-reply to acknowledgments](failures/over-reply-to-acknowledgments.md) | "Ok" or "thanks" triggers a recap, a new question, or an offer, so a closed topic reopens |
| [Length mismatch with the user's effort](failures/length-mismatch-with-the-user-s-effort.md) | A three-word message gets several paragraphs back |
| [Link and resource dumps](failures/link-and-resource-dumps.md) | A pile of links stands in for an answer |

## Planned (not yet written)
The remaining patterns in the family are listed in the [roadmap](../../roadmap/response-structure-and-length.md).

## Related
- [Conversation leadership](../conversation-leadership/README.md): the bot's own turn endings and fallbacks
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
