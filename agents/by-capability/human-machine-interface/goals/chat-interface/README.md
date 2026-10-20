# Chat Interface: Goal, Metrics, and Patterns

> **Goal:** The chat window itself works: messages arrive, drafts and attachments are kept, history is findable, and nothing is silently lost.

## Why this family exists
Some chatbot failures have nothing to do with the model. The window jumps to the bottom while someone is reading, a message typed on a weak connection disappears, or a file is skipped and the bot answers as if it read it. These are client and pipeline bugs, so a better model does not fix them, and they rarely show up in answer-quality reviews. They show up as lost work, repeated messages and answers that confidently ignore what the person sent.

## How we measure it
Each pattern page defines its own primary metric. Targets are starting points to tune on your own data and are proposed, not measured.
| Metric | Defined in |
|---|---|
| Reports of scroll jumping; scroll-up events during streaming that were overridden | [auto-scroll fights the reader](failures/auto-scroll-fights-the-reader.md) |
| Messages lost per 1,000 sent (design target 0) | [lost drafts and failed sends](failures/lost-drafts-and-failed-sends.md) |
| Attachments dropped without a message (design target 0) | [silent attachment failures](failures/silent-attachment-failures.md) |
| Time to find a past answer in a usability test | [long threads can't be searched](failures/long-threads-can-t-be-searched.md) |
| Share of sessions that restart after a single-message error | [no editing or branching of a sent message](failures/no-editing-or-branching-of-a-sent-message.md) |
| Export fidelity pass rate on a sample of reply types | [copy, share, and export lose content](failures/copy-share-and-export-lose-content.md) |
| Typed replies handled when buttons are shown (design target 100%) | [quick-reply buttons that don't match what was typed](failures/quick-reply-buttons-that-don-t-match-what-was.md) |
| Mismatched replies per 1,000 rapid-fire exchanges | [crossed messages](failures/crossed-messages.md) |
| Layout defects per device in release testing | [mobile keyboard or screen hides the reply](failures/mobile-keyboard-or-screen-hides-the-reply.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Auto-scroll fights the reader](failures/auto-scroll-fights-the-reader.md) | While a reply streams, the window keeps jumping to the bottom so the person can't read the top |
| [Lost drafts and failed sends](failures/lost-drafts-and-failed-sends.md) | A message typed on a weak connection disappears, or sending fails with no sign |
| [Silent attachment failures](failures/silent-attachment-failures.md) | A file is too large, unsupported or cut short, and the bot answers as if it read it all |
| [Long threads can't be searched](failures/long-threads-can-t-be-searched.md) | People can't find last week's answer: no message search, vague titles, no pinning |
| [No editing or branching of a sent message](failures/no-editing-or-branching-of-a-sent-message.md) | A typo in one sent message means starting the chat again |
| [Copy, share, and export lose content](failures/copy-share-and-export-lose-content.md) | Tables, code and links break when a reply is copied, shared or exported |
| [Quick-reply buttons that don't match what was typed](failures/quick-reply-buttons-that-don-t-match-what-was.md) | Typed answers are ignored while quick-reply buttons are showing |
| [Crossed messages](failures/crossed-messages.md) | Two quick messages get replies to the wrong one, out of order, or one is dropped |
| [Mobile keyboard or screen hides the reply](failures/mobile-keyboard-or-screen-hides-the-reply.md) | On a phone the keyboard or a small screen hides the latest answer |

## Planned (not yet written)
Row CM-10 (shared devices show someone else's chat) has no page here. Its example lives in [cross session bleed](../../../../cross-cutting/security/goals/data-loss-prevention/failures/cross-session-bleed.md). The rest of the catalog is in the [roadmap](../../roadmap/index.md).

## Related
- [Onboarding and discoverability](../onboarding-and-discoverability/README.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
