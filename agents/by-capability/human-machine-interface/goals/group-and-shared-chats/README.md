# Group and Shared Chats: Goal, Metrics, and Patterns

> **Goal:** In shared conversations the agent knows who is speaking to it, keeps private information private, and does not take over.

## Why this family exists
A bot in a team channel or group thread talks to many people at once. Written for one user, it answers the wrong member, answers talk that was not meant for it, and can show one person's details to the room. Written for chat; voice is not covered.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Replies addressed to the wrong person per 100 group threads | Under 1 (starting point) | [answers the wrong person in a group](failures/answers-the-wrong-person-in-a-group.md) |
| Unsolicited posts per 100 group messages | Under 2 (starting point) | [the bot talks over people](failures/the-bot-talks-over-people.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Answers the wrong person in a group](failures/answers-the-wrong-person-in-a-group.md) | The bot treats every message as coming from one person, so it answers the wrong member |
| [The bot talks over people](failures/the-bot-talks-over-people.md) | The bot treats every message as a request, so it answers people who were talking to each other |

## Extends existing pages
- Private information shown to the group: chat example added to [memory privilege leak](../../../../cross-cutting/operations/goals/memory-safety/failures/memory-privilege-leak.md)
- Conflicting instructions from different members: chat example added to [conflicting instructions](../../../../cross-cutting/accuracy/goals/context-management/failures/conflicting-instructions.md)

## Related
- [Dialogue management](../dialogue-management/README.md)
- [Privacy and governance](../privacy-and-governance/README.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
