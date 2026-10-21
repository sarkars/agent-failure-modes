# In-Car and Home Assistants: Goal, Metrics, and Patterns

> **Goal:** In-car and home voice assistants stay safe, act only on authorized commands, and are open about what they hear.

## Why this family exists
These assistants are used while driving or from across a room, with no screen to check. Long or visual replies, and commands that land on the wrong device, are the failures written so far. Written for the text form of each case; voice signals (silence, interruptions, speech-recognition errors) are planned, not written. Both pages need expert or legal review before use.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Spoken reply length and visual-only steps per task in driving mode | 0 visual-only steps; under about 10 seconds (starting points) | [replies too long or visual for a driver](failures/replies-too-long-or-visual-for-a-driver.md) |
| Wrong-target commands per 1,000 commands | Under 5 (starting point) | [commands go to the wrong device or room](failures/smart-home-commands-go-to-the-wrong-device-or.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Replies too long or visual for a driver](failures/replies-too-long-or-visual-for-a-driver.md) | The assistant answers like it would at a desk, to a person who is driving (needs expert and legal review) |
| [Smart-home commands go to the wrong device or room](failures/smart-home-commands-go-to-the-wrong-device-or.md) | "Turn off the light" hits the wrong light, and the assistant never says which |

## Planned (not yet written)
Sensitive commands from anyone, always-listening surprises, purchases by children or the TV. See the [roadmap](../../roadmap/service-and-vertical-patterns.md).

## Related
- [Proactive and ambient agents](../proactive-and-ambient/README.md)
- [Drive-thru agents](../drive-thru-agents/README.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
