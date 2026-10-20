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

## Patterns
| Pattern | One line |
|---|---|
| [Auto-scroll fights the reader](failures/auto-scroll-fights-the-reader.md) | While a reply streams, the window keeps jumping to the bottom so the person can't read the top |
| [Lost drafts and failed sends](failures/lost-drafts-and-failed-sends.md) | A message typed on a weak connection disappears, or sending fails with no sign |
| [Silent attachment failures](failures/silent-attachment-failures.md) | A file is too large, unsupported or cut short, and the bot answers as if it read it all |

## Planned (not yet written)
The rest of this family's catalog rows (search in history, editing a sent message, export, quick replies, crossed messages, mobile layout) are listed in the [roadmap](../../roadmap/index.md).

## Related
- [Onboarding and discoverability](../onboarding-and-discoverability/README.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
