# Browser Agents: Goal, Metrics, and Patterns

> **Goal:** Browsing agents stay within the user's intent and the site's rules, and ask before consequential actions.

## Why this family exists
Some chat assistants drive a browser for the user and report back in the chat. This family covers what goes wrong between the page and the reply: the agent reads the page wrong, acts on it, and tells the user it worked. The guidance is design guidance only. Benchmark figures change fast, so check a current leaderboard. Voice and visual reporting are planned, not written.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data.
| Metric | Target | Defined in |
|---|---|---|
| Recovery rate after a wrong click (step success rate reported alongside) | Start: 100% of detected cases | [misreading the screen](failures/misreading-the-screen.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Misreading the screen](failures/misreading-the-screen.md) | The agent clicks the wrong thing or loops, and the chat reply says "done" |

## Planned (not yet written)
The other rows of the family are tracked in the [emerging surfaces roadmap](../../roadmap/emerging-surfaces.md). Several already have an example added to a pattern elsewhere in the repository.

## Related
- [Silent long-running work](../response-time/failures/silent-long-running-work.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
