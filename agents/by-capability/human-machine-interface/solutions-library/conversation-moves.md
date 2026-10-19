# Chatbot Conversation Moves: Lead With the Answer, Ask, Offer Choices, or Hand Off

**Five moves cover most of what a chatbot should do at the moment a known failure usually happens: lead with the answer, ask one clarifying question, offer choices, admit uncertainty, or hand off to a person.** Each failure pattern lists the moves that fix it in a "Moves" table in its fix section. This page explains each move once.

> Status: **framework.** The moves are drawn from the patterns' own fixes. Any check attached to a move is proposed, not yet calibrated against human-labeled conversations.

## Guiding, not only checking
Output guardrails check whether a reply is safe and well formed. A reply can pass every one of those checks and still bury the answer, ask again for something the user already said, or guess when it should ask. The moves name what the bot should do instead, so a team can steer the conversation as it happens and not only grade it afterwards.

## The moves
| Move | Use it when | Avoid it when |
|---|---|---|
| Lead with the answer | The request is clear and answerable | The bot is not sure what was asked |
| Ask one clarifying question | One missing fact changes the answer | The answer is the same either way |
| Offer choices | The request has 2-4 likely meanings | The request is already clear, or the options would trap the user in a menu |
| Admit uncertainty and show how to check | The bot cannot verify its answer | The answer is a known fact the bot can cite |
| Hand off to a person | Stakes are high, or the bot has failed twice | The user asked to stay with the bot |

## Offering choices
Show 2-4 options, always add "Something else", and keep free text open. A choice set guides the user to a quick answer instead of the bot guessing. A choice set with no way out is its own failure.

## Where a move is checked
| Runs | What it can see | Example |
|---|---|---|
| Before sending | The user's turn and the draft reply | A buried answer can be fixed before the user sees it |
| After the turn | The finished turn and the user's next message | A repeated question shows the user was not understood |
| Across the conversation | Earlier turns and stored context | Asking for information the user already gave needs memory of earlier turns |

Each pattern's "Guide spec" block, at the end of its metrics section, records which moves apply, where the check runs and what to do on a miss, in a fixed format that can later be turned into code.

## Related
- [Conversation frameworks you can copy](README.md)
- [Answer-and-go conversation](../goals/conversation-leadership/failures/answer-and-go-conversation.md)
- [Human-machine interface overview](../)
