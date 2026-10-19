# Chatbot Conversation Guides: What the Bot Should Do Instead of Failing

**A conversation guide tells a chatbot what to do at the moment a known failure usually happens, and gives a check that spots when it didn't.** Each guide covers one failure pattern and shares its Pattern ID. Guides steer the conversation as it happens; they do not only grade it afterwards.

> Status: **specification, no guides published yet.** Guides are written from the patterns' own fixes and detection signals. Every check is proposed, not yet calibrated against human-labeled conversations.

## Guides, not only checks
Output guardrails check whether a reply is safe and well formed. A reply can pass every one of those checks and still bury the answer, ask again for something the user already said, or guess when it should ask. A conversation guide covers that gap. It leads with the behavior to aim for, then gives the check.

## What a guide contains
| Part | What it says |
|---|---|
| Do this | The target behavior in one sentence |
| The moment | The conversation situation where the pattern usually happens |
| Moves | The actions the bot can take, in order of preference |
| When not to use it | The over-correction the guide can cause |
| The check | Proposed signals that the bot missed the guide, each with a counter-signal |
| Guide spec | A fixed-format block, so the guide can later be turned into code without rewriting |

The template is [_templates/conversation-guide.md](../_templates/conversation-guide.md).

## The moves
| Move | Use it when | Avoid it when |
|---|---|---|
| Lead with the answer | The request is clear and answerable | The bot is not sure what was asked |
| Ask one clarifying question | One missing fact changes the answer | The answer is the same either way |
| Offer choices | The request has 2-4 likely meanings | The request is already clear, or the options would trap the user in a menu |
| Admit uncertainty and show how to check | The bot cannot verify its answer | The answer is a known fact the bot can cite |
| Hand off to a person | Stakes are high, or the bot has failed twice | The user asked to stay with the bot |

**Offering choices.** Show 2-4 options, always add "Something else", and keep free text open. A choice set guides the user to a quick answer instead of the bot guessing. A choice set with no way out is its own failure.

## Where a guide runs
| Runs | What it can see | Example |
|---|---|---|
| Before sending | The user's turn and the draft reply | A buried answer can be fixed before the user sees it |
| After the turn | The finished turn and the user's next message | A repeated question shows the user was not understood |
| Across the conversation | Earlier turns and stored context | Asking for information the user already gave needs memory of earlier turns |

## Guides
None published yet. Each guide will be listed here with its Pattern ID and the pattern it guides.

| Guide | Pattern ID | Runs |
|---|---|---|

## Related
- [Human-machine interface overview](../)
- [Conversation event schema](../roadmap/specs/conversation-event-schema-v0.1.md)
- [Failure taxonomy](../roadmap/specs/failure-taxonomy-v1.md)
- [Conversation frameworks you can copy](../solutions-library/)
