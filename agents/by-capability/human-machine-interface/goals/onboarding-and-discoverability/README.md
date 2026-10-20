# Onboarding and Discoverability: Goal, Metrics, and Patterns

> **Goal:** People know what the assistant can do and how to start, without needing to guess or to engineer prompts.

## Why this family exists
Most chat assistants fail before the first answer. The box is empty, the suggested questions lead nowhere, a tour stands in the way, or the widget is hidden or pops up at the wrong moment. Later, people never find the features that would save them time, and they learn that only carefully worded prompts get good answers. None of these shows up in answer-accuracy checks; they show up as sessions that end before the first message and as features nobody uses.

## How we measure it
Each pattern page defines its own primary metric. Targets are starting points to tune on your own data and are proposed, not measured.
| Metric | Defined in |
|---|---|
| Share of first sessions with a first message or tap; abandonment before the first message | [blank box: no hint what to ask](failures/blank-box-no-hint-what-to-ask.md) |
| Suggestion success rate: replies rated resolved (target 100% for shown chips) | [starter suggestions that fail](failures/starter-suggestions-that-fail.md) |
| Share of active users who used a given feature | [hidden commands and features](failures/hidden-commands-and-features.md) |
| Quality gap between terse and detailed prompts for the same task | [users must engineer prompts to get good results](failures/users-must-engineer-prompts-to-get-good-results.md) |
| Drop-off during the first-run flow | [first-run tours that block use](failures/first-run-tours-that-block-use.md) |
| Widget open rate; dismissals within a few seconds | [chat widget hard to find, or intrusive](failures/chat-widget-hard-to-find-or-intrusive.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Blank box: no hint what to ask](failures/blank-box-no-hint-what-to-ask.md) | An empty input with "Ask me anything" leaves people unsure what the assistant does or how to start |
| [Starter suggestions that fail](failures/starter-suggestions-that-fail.md) | A suggested question, tapped, leads to a weak or wrong answer |
| [Hidden commands and features](failures/hidden-commands-and-features.md) | Slash commands, shortcuts and settings that people never find |
| [Users must engineer prompts to get good results](failures/users-must-engineer-prompts-to-get-good-results.md) | A short request gets a vague answer, while the same need written in detail gets a real one |
| [First-run tours that block use](failures/first-run-tours-that-block-use.md) | A tutorial must be finished or dismissed before the first question |
| [Chat widget hard to find, or intrusive](failures/chat-widget-hard-to-find-or-intrusive.md) | The launcher is hidden in a corner, or a pop-up covers the page |

Related page in another family: [doesn't say what it can do](../embedded-copilots/failures/doesn-t-say-what-it-can-do.md) covers the same first-screen problem inside an embedded copilot. Whether it and the blank-box page should merge is a question for a person to decide (Needs review).

## Planned (not yet written)
The rest of this family's catalog rows are listed in the [roadmap](../../roadmap/index.md).

## Related
- [Chat interface](../chat-interface/README.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
